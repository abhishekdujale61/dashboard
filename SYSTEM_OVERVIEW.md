# GovAI Dashboard — System Overview

**Canada AI Task Force: National AI Strategy Consultation Dashboard**

---

## What This System Is

This dashboard makes Canada's official AI strategy consultation transparent and explorable. The Government of Canada ran a public consultation that collected responses from **11,383 Canadians** (with 3,162 fully submitted) across 68,702 open-text responses. Separately, a **Task Force of 28 AI experts** produced 32 reports with their own strategic recommendations.

The problem: the government's official summary was vague, contained no data weighting, and did not surface where the public and experts actually agreed or disagreed.

This dashboard fixes that. It takes the raw data from open.canada.ca and gives you an interactive, visual way to understand what Canadians said, what the experts said, where they align, and what specific actions are being recommended.

---

## The Core Question This System Answers

> *Across 8 strategic domains, how do the priorities of 11,383 Canadians compare to the priorities of 28 AI experts — and where do they diverge?*

Everything in the dashboard flows from this question.

---

## The 5 Main Sections

The dashboard has five areas, each answering a different question:

| Section | Question It Answers |
|---|---|
| **Overview** | What is this consultation about and what are the headline numbers? |
| **Demographics** | Who responded? Is this sample representative? |
| **Alignment** | Where do public and expert views agree or conflict? |
| **Recommendations** | What concrete actions are being proposed, and by whom? |
| **Pillar Detail** | What did people say specifically about one strategic area? |

---

## The 8 Pillars — What Each One Means

A "pillar" is a strategic domain. Everything in the dashboard is organized around these 8 pillars. Think of them as the 8 chapters of Canada's AI strategy.

### Pillar 1 — Talent & Research
**What it covers:** How Canada attracts, trains, and retains AI researchers and talent. Includes graduate funding, access to computing resources, and bringing global talent to Canada.

**Why it matters:** Without a strong talent base, Canada cannot lead in AI. This pillar tracks whether Canada is investing in the people who build AI systems.

---

### Pillar 2 — Data & Infrastructure
**What it covers:** Canada's ability to own and manage its own data systems. Includes sovereign data infrastructure (not dependent on foreign clouds) and open government datasets.

**Why it matters:** AI is only as good as the data it learns from. This pillar tracks whether Canada is building the data foundations to support AI development domestically.

---

### Pillar 3 — Adoption & Commercialization
**What it covers:** How Canadian businesses and government actually use AI. Includes tax incentives, regulatory sandboxes (safe testing zones), and bridges from academic research to commercial products.

**Why it matters:** Canada invents AI but often loses companies to the US. Only 32.4% of Canadian-founded AI companies remain in Canada as of 2024, down from 74.9% in 2016. This pillar tracks whether Canada can keep and scale its AI companies.

---

### Pillar 4 — Regulation & Governance
**What it covers:** The legal and policy framework for AI in Canada. Includes risk-tiered regulation (stricter rules for high-risk AI), the Artificial Intelligence and Data Act (AIDA), and accountability mechanisms.

**Why it matters:** Without clear rules, AI can cause harm. Without proportionate rules, it stifles innovation. This pillar tracks the balance between enabling and constraining AI.

---

### Pillar 5 — International Collaboration
**What it covers:** Canada's role in shaping global AI governance. Includes leadership in G7, OECD, and bilateral agreements with other countries.

**Why it matters:** AI doesn't respect borders. Canada's ability to influence international norms affects what AI systems look like globally and what standards Canadian companies must meet.

---

### Pillar 6 — Public Trust & Safety
**What it covers:** Whether Canadians can trust AI systems. Includes public AI literacy programs, transparent auditing of AI systems, and mechanisms for people to challenge AI decisions that affect them.

**Why it matters:** 83% of public responses mentioned trust and safety keywords — more than any other topic. This is the issue Canadians care most about.

---

### Pillar 7 — Inclusive AI
**What it covers:** Whether AI works fairly for everyone. Includes Indigenous data sovereignty (First Nations control over their own data), accessibility, and building equity into AI by design.

**Why it matters:** AI systems trained on biased data replicate and amplify bias. This pillar tracks whether Canada is actively designing AI to serve all communities, not just the majority.

---

### Pillar 8 — Sovereignty & Security
**What it covers:** Protecting Canada's critical AI infrastructure from foreign threats. Includes national security review processes for AI systems and protection of strategic AI assets.

**Why it matters:** AI is becoming national infrastructure. This pillar tracks whether Canada is treating AI security with the same seriousness as energy or telecommunications security.

---

## The Key Entities

### Priority Score (0–10)
Every pillar has two scores:
- **Public Priority Score** — derived from how frequently and strongly Canadians engaged with that pillar's topics in their open-text responses. Calculated by keyword frequency analysis and normalized to a 0–10 scale.
- **Expert Priority Score** — derived from how prominently Task Force experts emphasized that pillar across their 32 reports. Same normalization method.

A score of 10 means this pillar dominated the conversation. A score of 5 means it was mentioned but not heavily weighted.

---

### Alignment Status
When you compare the public score to the expert score for a pillar, you get a gap (delta). The system classifies this gap:

- **Aligned** (gap < 1.0) — Public and experts are roughly in agreement on how important this pillar is.
- **In Tension** (gap 1.0–1.5) — There is a meaningful difference. One group rates it notably higher than the other.
- **Diverges** (gap > 1.5) — A significant difference exists, indicating either a values difference or an awareness gap.

Important nuance: a tension doesn't always mean conflict. The "Adoption & Commercialization" pillar shows a small gap where the public rates it *higher* than experts — but the real tension is about *pace vs. safety*, not whether to commercialize AI at all.

---

### Recommendation
A specific, actionable proposal made by one of the 28 Task Force experts. Each recommendation:
- Belongs to a pillar
- Has a priority level (High / Medium / Low)
- Has an estimated public support score (how much survey data suggests Canadians would support it)
- May be "Expert Only" (not surfaced in the public-facing summary)

Example: *"Establish a National AI Research Fund of $500M over 5 years, prioritizing compute access grants for university labs outside major centres"* — Dr. Yoshua Bengio, High priority, 8.4/10 public support.

---

### Expert Report
A detailed analytical document produced by a Task Force working group. Each report:
- Covers one pillar
- Has an urgency level (Critical / High / Medium)
- Contains specific findings, strategic recommendations, and an assessment of the current policy gap

Example urgency: The Adoption & Commercialization report is rated **Critical**, with the finding that Canada has lost 42 percentage points of AI company retention over 8 years.

---

### Expert Reports Toggle
A global on/off switch in the navigation bar. When turned **on**, the dashboard shows:
- Expert priority scores alongside public scores
- Expert-only recommendations
- Full expert report content on each pillar's detail page

When turned **off**, the dashboard shows only what was visible in the public-facing consultation — useful for understanding what the public actually saw vs. what the experts added.

---

## The 6 Visualizations — What Each One Shows

### 1. Radar Chart (Overview page)
**What it shows:** All 8 pillars at once, comparing public vs. expert priority as an 8-sided spider web.

**How to read it:** Each axis radiates outward from the center. The further out a point sits, the higher the priority score. There are two lines drawn — one for public scores (solid), one for expert scores (dashed). Where the lines overlap, there is alignment. Where one line extends further than the other, there is a gap.

**What to look for:** Areas where the two shapes diverge reveal the most important strategic tensions in the consultation.

---

### 2. Pillar Bar Chart (Overview page)
**What it shows:** How many recommendations exist for each pillar.

**How to read it:** Taller bars = more recommendations mapped to that pillar. Each bar is colored to match its pillar.

**What to look for:** Regulation & Governance has the most recommendations (16), suggesting it is the most actively debated domain. International Collaboration has the fewest (8).

**Interaction:** Clicking any bar navigates to that pillar's detail page.

---

### 3. Respondent Donut Chart (Overview / Demographics)
**What it shows:** The split between individual Canadians and organizations in the consultation.

**How to read it:** The donut segments show the proportion. The center label shows the total. Hover for exact numbers.

**What to look for:** The consultation was 84.7% individuals and 15.3% organizations — meaning the voice is largely that of engaged citizens, not just industry lobby groups.

---

### 4. Geography Bar Chart (Demographics page)
**What it shows:** Which provinces and territories contributed the most responses.

**How to read it:** Horizontal bars, sorted by volume. The length of the bar represents the percentage of total responses from that region.

**What to look for:** Ontario (38.9%) and British Columbia (20.7%) together account for nearly 60% of responses. This is a geographic concentration risk — the survey may underrepresent voices from the Prairies, the North, and Atlantic Canada.

---

### 5. Alignment Scatter Plot (Alignment page)
**What it shows:** All 8 pillars plotted against each other based on public score (horizontal axis) vs. expert score (vertical axis).

**How to read it:**
- The diagonal line running from bottom-left to top-right represents perfect alignment (public score = expert score).
- Points **above** the line: experts rate this pillar higher than the public.
- Points **below** the line: the public rates this pillar higher than experts.
- Point **color**: Green = aligned, Amber = in tension, Red = diverges.
- Point **label**: Single-letter abbreviation for each pillar.

**What to look for:** Points that sit furthest from the diagonal line are the most important areas of divergence. The Inclusive AI point sits well above the diagonal — experts care more about it than the public's responses suggest they do.

**Interaction:** Hover any point to see the pillar name, both scores, the gap, and a written explanation of what the tension actually means.

---

### 6. Response Volume by Pillar (Demographics page)
**What it shows:** How many open-text responses were submitted for each pillar.

**How to read it:** Horizontal bars sorted descending. Longer = more responses.

**What to look for:** Adoption & Commercialization has 23,303 responses — far more than others. This is because it covered 10 survey questions, while other pillars had fewer. This means raw response volume alone cannot be used to compare how much Canadians care about each pillar without normalizing for question count.

---

## How the System Works Logically

**Step 1 — Data enters the system.**
Raw consultation data from open.canada.ca is processed into structured records: pillar scores, demographic breakdowns, individual recommendations, and expert reports.

**Step 2 — The user lands on Overview.**
They see the headline numbers (11,383 respondents, 68,702 responses, 28 experts, 32 reports) and the radar chart showing the full strategic landscape at a glance.

**Step 3 — The user explores Demographics.**
They can assess whether the consultation sample is representative — checking geographic spread, age distribution, gender breakdown, sector representation, and response volume by pillar.

**Step 4 — The user examines Alignment.**
The scatter plot and alignment table reveal exactly where public and expert views converge and where they diverge. Each divergence includes a plain-language explanation of what the tension actually means.

**Step 5 — The user reviews Recommendations.**
Concrete action proposals are searchable and filterable by pillar, priority level, and keyword. Each recommendation shows who proposed it, which pillar it belongs to, and how much public support the data suggests it has.

**Step 6 — The user drills into a Pillar.**
Clicking any pillar anywhere in the dashboard goes to a full detail page: the strategic summary, alignment scores, the full expert report (if the toggle is on), policy gaps, key findings, and all recommendations for that pillar.

**Step 7 — Expert Reports toggle changes the lens.**
With Expert Reports off, the user sees the public-facing picture. With it on, they see the fuller expert analysis layered on top — urgency ratings, specific findings, policy gap assessments, and expert-only recommendations.

---

## Key Insights the Dashboard Surfaces

**1. Adoption & Commercialization is not a conflict — it is a timing debate.**
Both the public (9.1) and experts (8.5) rate this pillar highly. The tension is not whether Canada should commercialize AI — everyone agrees it should. The debate is about whether to move fast now or ensure safety guardrails are in place first.

**2. Inclusive AI has an awareness gap, not a values gap.**
Experts rate Inclusive AI at 7.5; the public rates it at 6.2. This is the largest divergence in the consultation. But it does not mean the public opposes inclusive AI — only 25% of respondents mentioned inclusion-related keywords, versus 83% who mentioned trust and safety. The public may simply not have been prompted to think about inclusion in the same depth.

**3. Public Trust & Safety is the dominant public concern.**
83% of public responses included trust and safety keywords. No other topic came close. This tells policymakers that any AI strategy must lead with trust mechanisms, not treat them as an afterthought.

**4. Geographic concentration is a risk.**
Ontario and BC dominate the response sample. Voices from northern Canada, rural communities, and smaller provinces are underrepresented. Any policy derived from this consultation carries that geographic bias.

**5. Canada is losing its AI companies.**
The expert reports flag a critical statistic: only 32.4% of Canadian-founded AI companies remain in Canada, down from 74.9% in 2016. This informs the urgency rating on the Adoption & Commercialization expert report.

---

## Who the Entities Are

### The 11,383 Respondents
Canadians who participated in the online consultation. Broken down as:
- 84.7% individuals, 15.3% organizations
- Primarily from IT/tech (20.7%) and professional/scientific (14%) sectors
- Disproportionately from Ontario (38.9%) and BC (20.7%)
- Mostly aged 35–54
- 46.2% identified as men, 34.5% as women

### The 28 Task Force Experts
Members of the Government of Canada's AI Task Force, drawn from academia, industry, and civil society. They produced 32 reports covering all 8 pillars. Their recommendations and findings are the "expert" side of the public vs. expert comparison.

Notable members include researchers like Dr. Yoshua Bengio (Turing Award winner, Mila) and industry figures like Patrick Pichette (former Google CFO, now investor). Each recommendation in the system is attributed to a specific member with their role.

### The Survey Questions
26 questions across the 8 pillars. Not evenly distributed — some pillars had more questions than others, which directly affects response volume comparisons.

---

## What the Dashboard Does NOT Do

- It does not tell you what Canada's AI policy should be. It shows what the data says.
- It does not weight responses by expertise or credibility. An AI researcher and a curious student count equally in the public scores.
- It does not resolve the tensions it surfaces. Tensions are named and explained, but the policy choices remain with decision-makers.
- It does not represent all Canadians equally. The sample is self-selected and geographically concentrated.

These limitations are intentional and transparent — the dashboard aims to be honest about what the data can and cannot say.
