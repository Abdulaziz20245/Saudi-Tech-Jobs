# Product Requirements

## Problem
People looking for tech jobs in Saudi Arabia (students, fresh grads, career switchers, and
working engineers) have no clear, data-backed view of the market. Which skills are employers
actually asking for? Which roles are growing? What does a junior data role pay in Riyadh?
Today the answers come from anecdotes and scattered job sites.

## Users
1. **Students and fresh grads** (primary at launch): deciding what to learn and where to apply.
2. **Working engineers**: checking demand and salary for their skills, planning a move.
3. **Bootcamps, university clubs, career advisors**: want trend data to guide others.

## Value proposition
"See what the Saudi tech market is really asking for, updated every day, and get a personal
plan to close your gap."

## MVP features (in priority order)
1. **Market dashboard**
   - Headline stats: active tech postings, new this week, companies hiring, % remote/hybrid
   - Top skills (bar chart), filterable by role family (software, data/AI, DevOps/cloud,
     security, product/design) and seniority
   - Skill trends over time (line chart), rising and falling skills this month
   - Postings by city and by company
   - Salary ranges where available, clearly labeled with sample size
2. **Job explorer**
   - Search and filter postings (role, skill, city, seniority, work mode, company)
   - Each posting shows extracted skills as tags and links to the original application page
3. **Skill pages**
   - One page per skill (e.g. "Python"): demand over time, roles that ask for it, skills that
     usually appear with it, sample postings
4. **CV coach agent** (after launch)
   - Upload a CV (PDF) or paste text, pick a target role
   - Agent extracts your skills, compares against current postings for that role, and returns
     a match score, missing skills ranked by demand, matching open postings, and a short
     learning plan
   - CVs are processed and not stored unless the user opts in

## Out of scope for MVP
User accounts, job applications inside the site, non-tech jobs, other countries, mobile app.

## Success metrics (these go on the resume)
- Postings collected (total and daily), number of companies covered
- Extraction quality: precision / recall / F1 on the labeled eval set
- Unique visitors and returning visitors per week (privacy-friendly analytics)
- CV coach sessions completed
- Reach of launch posts (LinkedIn impressions)

## Principles
- Honest data: always show sample size and "last updated"; never invent salaries.
- Fast and clean: dashboard loads in under 2 seconds; works well on mobile.
- Bilingual-ready: English UI first, layout ready for Arabic (RTL) later.
