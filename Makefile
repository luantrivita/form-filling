PYTHON ?= python3

.PHONY: repo-init setup test validate check smoke-local data public-baselines benchmark-smoke benchmark-dev benchmark-summary ai-setup ai-refresh ai-status graphify-watch upstream-init upstream-check clean

repo-init:
	bash scripts/devtools/bootstrap_repo.sh

setup:
	$(PYTHON) -m pip install -e '.[test,retrieval]'

validate:
	$(PYTHON) scripts/validate_contracts.py

test:
	$(PYTHON) -m pytest -q

check: validate test

smoke-local:
	$(PYTHON) -m pytest -q tests/test_step4_llm_harness.py tests/test_split_guard.py

data:
	$(PYTHON) scripts/data/download_public_datasets.py
	$(PYTHON) scripts/build_public_manifest.py

public-baselines:
	$(PYTHON) scripts/run_synur_retrieval_baseline.py
	$(PYTHON) scripts/run_mts_section_baseline.py

benchmark-smoke:
	$(PYTHON) scripts/wait_for_teacher_endpoints.py
	LIMIT=5 bash scripts/run_teacher_dev_matrix.sh

benchmark-dev:
	$(PYTHON) scripts/wait_for_teacher_endpoints.py
	LIMIT=0 bash scripts/run_teacher_dev_matrix.sh

benchmark-summary:
	$(PYTHON) scripts/summarize_teacher_benchmarks.py --dir experiments/llm_baselines

ai-setup:
	bash scripts/devtools/setup_ai_context.sh

ai-refresh:
	bash scripts/devtools/refresh_ai_context.sh

ai-status:
	bash scripts/devtools/ai_status.sh

graphify-watch:
	bash scripts/devtools/graphify_watch.sh

upstream-init:
	bash scripts/devtools/init_upstreams.sh

upstream-check:
	bash scripts/devtools/update_upstreams.sh

clean:
	rm -rf .pytest_cache **/__pycache__
