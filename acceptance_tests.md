# Acceptance Tests — v1.4.1

Generated: 2026-02-28T18:34:09Z

## Privacy / No‑storage
- [ ] No conversation payload stored server-side
- [ ] Telemetry contains only schema-approved fields (no free text, no PHI)
- [ ] Consent gate blocks the questionnaire until accepted

## Recommendation correctness
- [ ] NULL never treated as false
- [ ] “Verification needed” shown when must-have field is NULL
- [ ] Each recommended plan has clickable public_open_url

## Optimization loop
- [ ] Post-session stats panel renders from aggregated metrics
- [ ] Rank changes computed week-over-week

## Gov dashboard
- [ ] Widgets render with missing-data placeholders
- [ ] Charts readable in 10 minutes