# MasterCopy — every target with an hourly meter has a teardown twin.
.PHONY: install bootstrap-budget deploy-dev destroy-dev seed score event-window walkthrough

install:
	uv sync

bootstrap-budget:
	# The Budgets alarm must exist before anything else deploys, so it is
	# bootstrapped outside the CDK app the pre-deploy hook guards.
	uv run --extra aws python infra/bootstrap_budget.py

deploy-dev:
	python .claude/hooks/pre_deploy.py
	@echo "TODO(m01): cdk deploy --context stage=dev"

destroy-dev:
	@echo "TODO(m01): cdk destroy --context stage=dev"

seed:
	@echo "TODO(m01): upload golden catalog mezzanines to the ingest bucket"

score:
	@echo "TODO(m03): run scored eval suite -> evals/history/"

event-window:
	python .claude/hooks/pre_deploy.py
	@echo "TODO(m07): the ONLY way MediaLive runs — TTL-tagged channel, scheduled teardown"

walkthrough:
	@echo "TODO(m06): replay the demo path"
