.PHONY: help run lint lint_fix clean preview \
	fetch bronz silver gold1 gold2

help:  ## Show available commands
	@echo "🛠️  Available commands:"
	@awk -F':.*?## ' '/^[a-zA-Z0-9_.-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run:  ## Run the main application
	cd src && python -m main

lint:  ## Lint code with ruff
	ruff src

lint_fix:  ## Automatically fix lint issues
	ruff src --fix

clean:  ## Remove all .parquet, .csv, .json, .log files
	find data/raw -name '*.json' -delete
	rm -rf data/bronze/*.parquet
	rm -rf data/silver/*.parquet
	rm -rf data/gold/*.parquet
	find logs -name '*.log' -delete

clean_preview:  ## Remove preview files
	find data/preview -name '*.csv' -delete

preview:  ## Run preview generator script
	cd src && python -m preview_generator

fetch:  ## Run fetch_seasons step
	cd src && python -m data_pipeline.fetch_seasons

bronz:  ## Run seasons_to_bronze step
	cd src && python -m data_pipeline.seasons_to_bronze

silver:  ## Run clean_bronze step
	cd src && python -m data_pipeline.clean_bronze

gold1:  ## Run gold match team stats step
	cd src && python -m data_pipeline.gold.generate_match_team_stats

gold2:  ## Run gold team season summary step
	cd src && python -m data_pipeline.gold.generate_team_season_summary
