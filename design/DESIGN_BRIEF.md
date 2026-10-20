# Design Brief: Saudi Tech Jobs

Paste this whole file into Claude Design. It describes the product, pages, components, data and
style. Sample data at the bottom is realistic placeholder data for mockups only.

## The product in one line
A live, AI-powered view of the Saudi tech job market: which skills employers want, how demand is
changing, and a personal coach that tells you what to learn next.

## Audience and tone
Students, fresh grads and engineers in Saudi Arabia. They are tech-savvy, mobile-heavy, and
skeptical of fluff. The site should feel like a **trustworthy data product**: calm, precise,
modern, quietly confident. Think the clarity of Linear or Stripe's docs, the data density of a
good analytics dashboard, with a subtle local identity.

## Brand direction
- **Name / wordmark:** "Saudi Tech Jobs" (working name). Simple wordmark, optionally with a small
  mark inspired by a rising bar chart or a palm frond abstracted into lines.
- **Color:** neutral base (off-white / near-black for dark mode). One primary accent in a deep
  green with a hint of teal (nod to the Saudi flag without copying it), plus a warm sand/gold
  secondary used sparingly for highlights. Chart palette: 5-6 distinguishable, colorblind-safe
  hues built around the accent.
- **Type:** a clean geometric or grotesk sans (e.g. Inter, Geist, or IBM Plex Sans) with
  tabular numerals for stats. Must pair with an Arabic font later (e.g. IBM Plex Sans Arabic).
- **Light and dark mode** both required.
- **RTL-ready:** use logical layout (start/end, not left/right) so an Arabic version can mirror.

## Pages
### 1. Home / Market dashboard (most important)
- Top bar: wordmark, nav (Dashboard, Jobs, Skills, CV Coach), theme toggle, "Updated 2h ago".
- Hero strip with 4 stat cards: Active tech postings, New this week (with +/- vs last week),
  Companies hiring, Remote/hybrid share.
- Filter row: role family chips (All, Software, Data & AI, DevOps & Cloud, Security,
  Product & Design), seniority dropdown, time range (30d / 90d / 1y).
- "Top skills in demand": horizontal bar chart, top 15, each bar shows count and % of postings;
  clicking a bar opens the skill page.
- "Rising and falling": two compact lists with sparklines and % change this month.
- "Skill trends": multi-line chart with a skill picker (max 5 skills).
- "Where the jobs are": cities breakdown (bar or simple map of KSA with bubbles).
- "Who's hiring": company logos grid with open role counts.
- "Salary insights": range bars per role family and seniority, with sample size shown
  ("based on 23 postings"); empty state when data is too thin.
- Footer: data sources note, methodology link, "Built by Abdulaziz" with GitHub/LinkedIn.

### 2. Jobs explorer
- Search bar + filters (role family, skill, city, seniority, work mode, company) as a left
  sidebar on desktop and a bottom sheet on mobile.
- Result cards: company logo, title, company, city, work mode badge, seniority, posted date,
  top extracted skills as tags (required skills solid, nice-to-have outlined),
  "Apply on company site" button.
- Sorting (newest, best match), pagination or infinite scroll, empty state.

### 3. Skill page (e.g. /skills/python)
- Header: skill name, category tag, demand rank, % of postings mentioning it.
- Demand over time line chart.
- "Roles that ask for it" (bar), "Often appears with" (tag cloud or ranked list).
- Latest postings that require it (cards from page 2).

### 4. CV Coach
- Step 1: upload PDF (drag and drop) or paste text, choose target role and seniority.
- Step 2: loading state that shows the agent's steps ("Reading your CV", "Comparing with 812
  Data & AI postings", "Building your plan").
- Step 3 report: match score (radial gauge), your skills that match (green tags), missing skills
  ranked by demand (with % of postings), 3-step learning plan with links, matching open jobs.
- Privacy note: "Your CV is not stored."

### 5. About / Methodology
How data is collected (company job boards), how AI extraction works, accuracy numbers
(skills F1 etc.), update frequency, limitations.

## Components to design
Stat card, filter chip, dropdown, search input, bar chart, line chart with sparkline variant,
skill tag (required / nice-to-have), job card, company logo tile, salary range bar, radial score
gauge, step progress indicator, empty state, loading skeletons, toast, top nav (desktop and
mobile), footer.

## Responsive
Mobile first. Dashboard cards stack to one column on phones; charts stay readable at 360px wide.

## Accessibility
WCAG AA contrast, visible focus states, charts have text equivalents (values on hover and in a
table toggle), no information conveyed by color alone.

## Sample data for mockups (placeholder, not real)
- Overview: 1,248 active postings · 186 new this week (+12%) · 74 companies · 31% remote/hybrid
- Top skills (Data & AI, 30d): Python 68%, SQL 61%, Machine Learning 44%, AWS 32%, Spark 27%,
  Power BI 25%, TensorFlow/PyTorch 22%, LLMs 19%, Docker 18%, Airflow 14%
- Rising: LLMs +38%, Kubernetes +17%, dbt +15% · Falling: jQuery -21%, PHP -9%
- Cities: Riyadh 71%, Jeddah 14%, Dammam/Khobar 9%, Remote 6%
- Example job card: "Junior Data Engineer · Foodics · Riyadh · Hybrid · Posted 2 days ago ·
  Python, SQL, Airflow, GCP"
- Salary example: Software, Junior: 9,000 to 14,000 SAR/month (based on 23 postings)
- CV Coach example: Target "Junior Data Scientist", match 64%, missing: SQL (61% of postings),
  Docker (18%), A/B testing (12%)
