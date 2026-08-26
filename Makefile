# MasterCopy — every target with an hourly meter has a teardown twin.
.PHONY: install deploy-dev destroy-dev seed score event-window walkthrough

install:
	@echo "TODO(m00a): uv sync"

deploy-dev:
	@echo "TODO(m01): cdk deploy --context stage=dev  (hook: requires Budgets alarm)"

destroy-dev:
	@echo "TODO(m01): cdk destroy --context stage=dev"

seed:
	@echo "TODO(m01): upload golden catalog mezzanines to the ingest bucket"

score:
	@echo "TODO(m03): run scored eval suite -> evals/history/"

event-window:
	@echo "TODO(m07): the ONLY way MediaLive runs — TTL-tagged channel, scheduled teardown"

walkthrough:
	@echo "TODO(m06): replay the demo path"
