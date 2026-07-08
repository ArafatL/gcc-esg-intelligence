# I scored 21 GCC companies on ESG disclosure quality. Not one reached the top band.

*(Post after human verification is complete. Attach: dashboard screenshot +
Figure 1 ranking chart. First comment: GitHub repo + live dashboard links.)*

Over the past week I built something that, as far as I can tell, didn't
exist: an open dataset measuring how well GCC-listed companies actually
disclose their sustainability data.

Not how "green" they are — how *transparent* they are. Those are different
questions, and conflating them is why commercial ESG ratings famously
disagree with each other.

**What I did.** I took the FY2024 sustainability reports of 21 major listed
companies across the DFM, ADX, Tadawul, QSE and Boursa Kuwait — banks,
telecoms, energy, utilities, real estate — and ran them through an
open-source pipeline I built: automated extraction of 9 core metrics
(Scope 1/2/3 emissions, energy, water, diversity, governance) where every
number is traceable to the exact sentence in the source PDF, followed by
human verification against every report.

Then I scored each company 0–100 on a fully transparent Disclosure Quality
Score: Coverage (45) + Framework alignment (30) + Rigor: assurance,
net-zero targets, Scope 3 (25). Every weight is public. If you disagree
with them, the code lets you re-score the market with your own.

**What I found:**
- Market average: **43.9 / 100**
- **No company reached the Leader band (75+).** The best scores in the
  region were 70.0 — Advanced, not Leader
- The spread is huge: from 70.0 down to 10.0 across major index names
- The gaps are consistent: Scope 3 emissions and independent assurance are
  where GCC disclosure goes quiet
- The bright spot: framework adoption (GRI, TCFD, emerging ISSB) is real —
  the region is mid-transition, past boilerplate but short of the frontier

One example of what verified disclosure looks like: Emirates NBD publishes
a KPMG-assured data pack down to eight Scope 3 categories. That's the
frontier the rest of the market hasn't reached.

**Why it matters now.** ISSB-aligned requirements and the UAE's climate law
are arriving. Regulators will need baselines to measure whether mandates
work. Investors will need to know who they can actually analyse. This
dataset is that baseline — FY2024, pre-mandate, open, and auditable.

Everything is public: dataset, code, methodology, live dashboard, and a
preprint is on the way. Links in the first comment.

If you work in sustainability, ESG analysis, or capital markets in the
region — I'd genuinely love to hear what you'd want measured next.
Scope 3 by sector? Arabic-language reports? Multi-year trends (2020–2025
is in progress)?

#ESG #Sustainability #GCC #UAE #DataScience #SustainableFinance #ISSB
