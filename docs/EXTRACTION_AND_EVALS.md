# LLM Extraction and Evals

## What we extract (per posting)
```json
{
  "is_tech": true,
  "role_family": "data_ai | software | devops_cloud | security | product_design | it_support | other",
  "seniority": "intern | junior | mid | senior | lead | manager | unknown",
  "city": "Riyadh | Jeddah | Dammam/Khobar | ... | remote | unknown",
  "work_mode": "onsite | hybrid | remote | unknown",
  "employment_type": "full_time | part_time | contract | internship | unknown",
  "years_experience_min": 3,
  "salary": {"min": null, "max": null, "currency": "SAR", "period": "month"},
  "skills": [{"name": "Python", "requirement": "required"},
             {"name": "Airflow", "requirement": "nice_to_have"}]
}
```
Rules for the model: only extract what the text states (null/unknown otherwise), output canonical
English skill names, handle Arabic and mixed-language text, never guess salary.

Implementation: Anthropic SDK with structured output (tool use / JSON schema), validated by
Pydantic. Store `prompt_version`, `model`, and token counts with each result.

## Evaluation
- **Dataset:** ~200 postings, stratified by role family and language (include at least 40 Arabic
  or mixed). Hand-label them in `backend/evals/labeled.jsonl` using the same schema.
- **Metrics:**
  - Skills: precision, recall, F1 (exact match after normalization)
  - Categorical fields (role_family, seniority, work_mode, city): accuracy
  - is_tech: precision/recall (false positives pollute the dashboard)
  - Salary: exact-match rate on postings that state one
- **Process:** every prompt/schema/model change bumps `PROMPT_VERSION`, runs
  `python -m evals.score`, and appends a row below. Keep a split of 50 postings never used while
  tuning, as a final held-out check.

## Results log
| Date | Prompt version | Model | Skills F1 | Role acc. | Seniority acc. | Cost / 1k postings | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | baseline |
