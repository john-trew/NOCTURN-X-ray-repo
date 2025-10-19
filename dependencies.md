# Workflow Dependencies

This document shows the relationships between GitHub Actions workflows and their associated Python scripts.

## Scheduled Workflows

### Parse MorphoSource API (total_count + latest record) (`parse-morphosource-api.yml`)

**Schedule:** Every 5 minutes

**Required Scripts:**
- `.github/scripts/parse_morphosource_api.py`


---

### GitHub Pages Content Generation (`github-pages.yml`)

**Schedule:** Cron: 0 * * * *


---

### Daily MorphoSource Check (`daily.yml`)

**Schedule:** Daily at midnight

**Required Scripts:**
- `.github/scripts/daily.py`


---

### Release Reactions Collector (`release-reactions.yml`)

**Schedule:** Daily at midnight

**Required Scripts:**
- `.github/scripts/collect_reactions.py`


---

### Monthly MorphoSource Collection (`monthly.yml`)

**Schedule:** Monthly on day 1 at 0:0

**Required Scripts:**
- `.github/scripts/monthly.py`


---

### Cleanup CT Error Releases (`cleanup_ct_error_releases.yml`)

**Schedule:** Cron: 0 */6 * * *


---

### MorphoSource Blockchain Snapshot (`morphosource_blockchain.yml`)

**Schedule:** Cron: 30 2 * * *

**Required Scripts:**
- `.github/scripts/morphosource_blockchain.py`


---

### Fine-tune Model from Reactions (`finetune-model.yml`)

**Schedule:** Weekly on Sunday at midnight

**Required Scripts:**
- `.github/scripts/finetune_model.py`
- `.github/scripts/prepare_finetune_data.py`


---

### Wiki Generation (`wiki-generation.yml`)

**Schedule:** Weekly on Sunday at midnight

**Required Scripts:**
- `.github/scripts/release_analysis.py`


---

## Other Workflows

### Auto Code Generation with Claude on Issue (`Claude_issue_automation.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/generate_code.py`

### OpenAI Release Analysis (`OpenAI-release-analysis.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/OpenAI-release-analysis.py`

### Analyze Workflow Dependencies (`analyze_dependencies.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/analyze_dependencies.py`

### Audit CT Text Releases (`audit_ct_releases.yml`)
**Manual trigger available**

### Code Review and Analysis (`code_review_workflow.yml`)
**Triggered by:**
- `Auto Code Generation with Claude on Issue`
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/analyze_code.py`

### MorphoSource CT API Pipeline (`combined_ct_images_to_text.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/process_morphosource_records.py`

### Compress Data Directory (`compress-data.yml`)
**Manual trigger available**

### CT to Text Analysis (`ct_to_text.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/ct_to_text.py`

### Deploy GitHub Pages (`deploy-pages.yml`)

### 2D or 3D Selenium Fullscreen Test (`dimension_test.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/dimension_media_fetcher.py`
- `.github/scripts/selenium_fullscreen_test2D.py`
- `.github/scripts/selenium_fullscreen_test3D.py`

### Issue Workflow Dependency Check (`issue-dependency-check.yml`)

### Metadata Record Extractor (`metadata_record_extract.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/metadata_record_extract.py`

### Check Modified MorphoSource Records (`modified_morphosource.yml`)
**Triggered by:**
- `Parse MorphoSource Data`
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/check_modified_morphosource.py`

### Parquet Data Grapher (`parquet_grapher.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/parquet_grapher.py`

### Parquet Data Processor (`parquet_processor.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/parquet_processor.py`

### Parse MorphoSource Data (`parse_morphosource.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/scrape_morphosource.py`

### Release Analysis and Wiki Generation (`release_analysis.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/release_analysis.py`
- `.github/scripts/release_analyzer.py`

### Save User Ratings (`save-ratings.yml`)

### Test Attestation Generation (`test-attestation.yml`)
**Manual trigger available**

### Test URL Processing Workflow (`test-run-run.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/2D3D_check.py`
- `.github/scripts/ct_image_to_text.py`
- `.github/scripts/ct_slices_to_text.py`
- `.github/scripts/url_screenshot_check.py`

### 3D Screenshot Tests (`test_3d_screenshot.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/test_3D_screenshot.py`

### Test 3D Screenshot with Prompt (`test_3d_screenshot_prompt.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/analyze_ct_images.py`
- `.github/scripts/test_3D_screenshot.py`

### Test MorphoSource Screenshots Analysis (`test_3d_screenshots_prompt.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/ct_image_to_text.py`

### Test Workflow (`test_commit_workflow.yml`)
**Manual trigger available**

### Test Daily Check (`test_daily.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/daily.py`
- `.github/scripts/test_daily.py`

### Test Monthly Collection (`test_monthly.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/test_monthly.py`

### Test Parquet Results Aggregator (`test_parquet_aggregator.yml`)
**Manual trigger available**

### Test Parquet Processing Coordinator (`test_parquet_coordinator.yml`)
**Manual trigger available**

### Test Parquet Data Processor (`test_parquet_processor.yml`)
**Manual trigger available**
**Required Scripts:**
- `.github/scripts/test_parquet_processor.py`

### Update README (`update_readme.yml`)
**Triggered by:**
- `Parse MorphoSource Data`
**Manual trigger available**

### Workflow Monitor (`workflow-monitor.yml`)
**Triggered by:**
- `*`

## Scripts and Their Workflows

This section shows which workflows use each script:

### 2D3D_check.py
**Used in Workflows:**
- `test-run-run.yml`

### OpenAI-release-analysis.py
**Used in Workflows:**
- `OpenAI-release-analysis.yml`

### analyze_code.py
**Used in Workflows:**
- `code_review_workflow.yml`

### analyze_ct_images.py
**Used in Workflows:**
- `test_3d_screenshot_prompt.yml`

### analyze_dependencies.py
**Used in Workflows:**
- `analyze_dependencies.yml`

### check_modified_morphosource.py
**Used in Workflows:**
- `modified_morphosource.yml`

### collect_reactions.py
**Used in Workflows:**
- `release-reactions.yml`

### ct_image_to_text.py
**Used in Workflows:**
- `test-run-run.yml`
- `test_3d_screenshots_prompt.yml`

### ct_slices_to_text.py
**Used in Workflows:**
- `test-run-run.yml`

### ct_to_text.py
**Used in Workflows:**
- `ct_to_text.yml`

### daily.py
**Used in Workflows:**
- `daily.yml`
- `test_daily.yml`

### dimension_media_fetcher.py
**Used in Workflows:**
- `dimension_test.yml`

### finetune_model.py
**Used in Workflows:**
- `finetune-model.yml`

### generate_code.py
**Used in Workflows:**
- `Claude_issue_automation.yml`

### metadata_record_extract.py
**Used in Workflows:**
- `metadata_record_extract.yml`

### monthly.py
**Used in Workflows:**
- `monthly.yml`

### morphosource_blockchain.py
**Used in Workflows:**
- `morphosource_blockchain.yml`

### parquet_grapher.py
**Used in Workflows:**
- `parquet_grapher.yml`

### parquet_processor.py
**Used in Workflows:**
- `parquet_processor.yml`

### parse_morphosource_api.py
**Used in Workflows:**
- `parse-morphosource-api.yml`

### prepare_finetune_data.py
**Used in Workflows:**
- `finetune-model.yml`

### process_morphosource_records.py
**Used in Workflows:**
- `combined_ct_images_to_text.yml`

### release_analysis.py
**Used in Workflows:**
- `release_analysis.yml`
- `wiki-generation.yml`

### release_analyzer.py
**Used in Workflows:**
- `release_analysis.yml`

### scrape_morphosource.py
**Used in Workflows:**
- `parse_morphosource.yml`

### selenium_fullscreen_test2D.py
**Used in Workflows:**
- `dimension_test.yml`

### selenium_fullscreen_test3D.py
**Used in Workflows:**
- `dimension_test.yml`

### test_3D_screenshot.py
**Used in Workflows:**
- `test_3d_screenshot.yml`
- `test_3d_screenshot_prompt.yml`

### test_daily.py
**Used in Workflows:**
- `test_daily.yml`

### test_monthly.py
**Used in Workflows:**
- `test_monthly.yml`

### test_parquet_processor.py
**Used in Workflows:**
- `test_parquet_processor.yml`

### url_screenshot_check.py
**Used in Workflows:**
- `test-run-run.yml`
