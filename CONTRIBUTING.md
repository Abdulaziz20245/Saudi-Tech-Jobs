# Contributing

## Workflow
1. Create a branch from `main`: `feat/<short-name>`, `fix/<short-name>`, or `docs/<short-name>`
2. Make small, focused commits using [Conventional Commits](https://www.conventionalcommits.org/):
   `feat(collector): add Lever adapter`, `fix(api): handle empty skill filter`
3. Open a pull request using the template; CI must be green
4. Squash-merge into `main`

## Standards
- Python: type hints, `ruff` formatting, `mypy` clean, tests for new logic
- TypeScript: strict mode, ESLint clean, no `any` without a comment explaining why
- Keep docs current: a change to behavior updates the relevant file in `docs/` in the same PR
- Any extraction prompt change bumps `PROMPT_VERSION` and logs eval results

## Suggesting a company
Open an issue with the "Add a company" template, including a link to the company's careers page.
