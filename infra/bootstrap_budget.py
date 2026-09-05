#!/usr/bin/env python3
"""Create the MasterCopy Budgets alarm and its SNS topic. Idempotent.

The Budgets alarm has to exist before anything else deploys, which is why it
is bootstrapped here instead of inside the CDK app -- the pre-deploy hook
blocks the very deploy that would otherwise create it.

    make bootstrap-budget                       # uses MASTERCOPY_ALERT_EMAIL
    uv run --extra aws python infra/bootstrap_budget.py --dry-run
    uv run --extra aws python infra/bootstrap_budget.py --email you@example.com

Scope: a monthly cost budget filtered to the `project=mastercopy` cost
allocation tag, alerting at 80% actual and 100% forecasted (PROJECT.md 7).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:  # pragma: no cover - exercised by humans, not CI
    sys.exit(
        "boto3 is not installed. Run `make bootstrap-budget`, or "
        "`uv run --extra aws python infra/bootstrap_budget.py`."
    )


DEFAULT_BUDGET_NAME = "mastercopy-monthly"
DEFAULT_LIMIT_USD = "50"
TOPIC_NAME = "mastercopy-budget-alerts"
COST_TAG = "user:project$mastercopy"


def topic_access_policy(topic_arn: str, account_id: str) -> str:
    """Budgets can only notify a topic that lets it publish."""
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowOwnerFullAccess",
                    "Effect": "Allow",
                    "Principal": {"AWS": account_id},
                    "Action": "SNS:Publish",
                    "Resource": topic_arn,
                },
                {
                    "Sid": "AllowBudgetsPublish",
                    "Effect": "Allow",
                    "Principal": {"Service": "budgets.amazonaws.com"},
                    "Action": "SNS:Publish",
                    "Resource": topic_arn,
                },
            ],
        }
    )


def ensure_topic(sns, account_id: str, email: str | None, dry_run: bool) -> str:
    if dry_run:
        print(f"[dry-run] would create SNS topic {TOPIC_NAME}")
        if email:
            print(f"[dry-run] would subscribe {email}")
        return f"arn:aws:sns:*:{account_id}:{TOPIC_NAME}"

    topic_arn = sns.create_topic(
        Name=TOPIC_NAME, Tags=[{"Key": "project", "Value": "mastercopy"}]
    )["TopicArn"]
    sns.set_topic_attributes(
        TopicArn=topic_arn,
        AttributeName="Policy",
        AttributeValue=topic_access_policy(topic_arn, account_id),
    )
    print(f"SNS topic: {topic_arn}")

    if email:
        existing = {
            subscription["Endpoint"]
            for subscription in sns.list_subscriptions_by_topic(TopicArn=topic_arn)[
                "Subscriptions"
            ]
        }
        if email in existing:
            print(f"Subscription for {email} already exists.")
        else:
            sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
            print(f"Subscribed {email} -- confirm the email to receive alerts.")
    return topic_arn


def budget_definition(name: str, limit_usd: str) -> dict:
    return {
        "BudgetName": name,
        "BudgetLimit": {"Amount": limit_usd, "Unit": "USD"},
        "CostFilters": {"TagKeyValue": [COST_TAG]},
        "CostTypes": {
            "IncludeTax": True,
            "IncludeSubscription": True,
            "UseBlended": False,
        },
        "TimeUnit": "MONTHLY",
        "BudgetType": "COST",
    }


def notifications(topic_arn: str) -> list[dict]:
    subscribers = [{"SubscriptionType": "SNS", "Address": topic_arn}]
    return [
        {
            "Notification": {
                "NotificationType": "ACTUAL",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 80.0,
                "ThresholdType": "PERCENTAGE",
            },
            "Subscribers": subscribers,
        },
        {
            "Notification": {
                "NotificationType": "FORECASTED",
                "ComparisonOperator": "GREATER_THAN",
                "Threshold": 100.0,
                "ThresholdType": "PERCENTAGE",
            },
            "Subscribers": subscribers,
        },
    ]


def ensure_budget(
    budgets, account_id: str, name: str, limit_usd: str, topic_arn: str, dry_run: bool
) -> None:
    definition = budget_definition(name, limit_usd)
    if dry_run:
        print(f"[dry-run] would create budget {name} at ${limit_usd}/month")
        print(f"[dry-run]   cost filter: {COST_TAG}")
        print("[dry-run]   alerts: 80% actual, 100% forecasted")
        return

    try:
        budgets.create_budget(
            AccountId=account_id,
            Budget=definition,
            NotificationsWithSubscribers=notifications(topic_arn),
        )
        print(f"Created budget {name} at ${limit_usd}/month.")
    except ClientError as error:
        if error.response["Error"]["Code"] != "DuplicateRecordException":
            raise
        budgets.update_budget(AccountId=account_id, NewBudget=definition)
        print(f"Budget {name} already existed; limit and filter updated.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default=DEFAULT_BUDGET_NAME)
    parser.add_argument("--limit", default=DEFAULT_LIMIT_USD, help="USD per month")
    parser.add_argument("--email", default=os.environ.get("MASTERCOPY_ALERT_EMAIL"))
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()

    account_id = boto3.client("sts").get_caller_identity()["Account"]
    print(f"Account: {account_id}")
    if not arguments.email:
        print(
            "No --email and no MASTERCOPY_ALERT_EMAIL: the topic will be created "
            "without a subscriber, so alerts will fire into the void."
        )

    topic_arn = ensure_topic(
        boto3.client("sns"), account_id, arguments.email, arguments.dry_run
    )
    ensure_budget(
        boto3.client("budgets"),
        account_id,
        arguments.name,
        arguments.limit,
        topic_arn,
        arguments.dry_run,
    )

    print(
        "\nNext: activate the `project` cost allocation tag in Billing > Cost "
        "allocation tags. Until it is active the filter matches nothing, and "
        "usd_actual in SPEC-00 verdicts cannot be sourced (SPEC-00 rule 1)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
