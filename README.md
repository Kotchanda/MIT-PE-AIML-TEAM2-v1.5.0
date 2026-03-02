# Irish Health Insurance Chooser — lindy.ai Package v1.2.0

Generated: 2026-02-01T20:13:50Z

## Coverage
- This version expands plan coverage significantly by adding:
  - All **Laya scheme names** listed on their public schemes page.
  - A broad set of **VHI plan names** listed on VHI’s public downloads page.
- Many new entries are **stubs** (features NULL) but include real `source_url` pages where the plan documents are available.

## New capabilities
- Post-session stats panel (question order movements, drop-off, info-gain)
- Optimization cycle to re-rank questions using anonymous telemetry
- Concise consent gate for the no-storage privacy model

## Files added
- compliance_statement.md
- post_session_stats_panel.md

## Next step
Run enrichment in waves:
1) Fill plan-specific PDFs/URLs for the most-used stubs first
2) Populate key benefit fields
3) Recompute completeness_score after each batch

## v1.3.0 additions
- Added new plans from HIA insurer updates (Jan–Feb 2026)
- Added broker_mode_runbook.md, policy_refresh_runbook.md, policy_registry_sources.md
- Added analytics_dashboard.html + analytics_summary.sample.json


## Added in v1.4.0
- ilh_toc_ingest.py / ilh_toc_ingest.md
- gov_health_dashboard.html + gov_health_summary.sample.json


## New in v1.4.1
- lindy_block_manifest.md
- gov_dashboard_kpi_catalog.md
- analytics_summary_contract.md
- acceptance_tests.md


## Backend (FastAPI)
A ready-to-run minimal backend is included in `backend_fastapi/`.
See `backend_fastapi/README.md`.


## v1.5.1 Broker-mode upgrade
- question_bank.json includes broker_openers/soft_probes and is not meant to be shown verbatim.
- Added broker_conversation_playbook.md
- Added Lindy_Block_Config_Guide_v1_5_1.md


## v1.5.2 Data sanitation update
- plans.json is now valid JSON (no NaN); blanks are explicit null.
- plans.csv refreshed; null_key_count and completeness_score recomputed.
- public_open_url populated (defaults to source_url).


## v1.6.0 Full benefit-level ingestion
- Added benefits[] per plan and ingestion framework under /ingestion
- Added /plan/{plan_id} and /plan/{plan_id}/benefits endpoints in backend
- Added UI-only ingestion runbook
