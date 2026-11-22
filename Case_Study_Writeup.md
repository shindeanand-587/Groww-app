# Product Case Study: FestMatch F&B
**Campus Fest Discovery & ROI Engine for Emerging Indian F&B Brands**  
*Author: Product Candidate*

---

### 1. My Take on the Problem Statement
Every year between November and March, over 1,500 college festivals take place across India. For emerging consumer packaged goods (CPG) and food & beverage (F&B) brands—particularly ready-to-drink (RTD) beverages, craft sodas, clean-label protein bars, and quick-service restaurant (QSR) kiosks—college campuses represent the single most concentrated demographic of Gen-Z early adopters. Getting *"liquid-to-lips"* or immediate taste-testing at an IIT Bombay (Mood Indigo) or St. Xavier's (Malhar) can trigger viral campus word-of-mouth and rapid repeat orders on quick-commerce apps (Zepto, Blinkit, Instamart).

However, the sponsorship discovery process today is broken, opaque, and inefficient:
- **Asymmetric Information & Arbitrary Pricing:** Student sponsorship committees quote ad-hoc numbers (e.g., ₹2.5 Lakhs to one brand and ₹60k to another for identical stall dimensions).
- **Inflated, Unaudited Footfall:** Festivals routinely claim 80,000 visitors when actual daily unique attendance is under 15,000.
- **No Standardized ROI Metric:** Marketers cannot calculate an apples-to-apples Cost per 1,000 Students reached (CPM) to defend their budget allocation to founders or CFOs.
- **Logistical Blindspots:** Marketers spend weeks in WhatsApp groups just to discover whether a fest permits continuous 15A power lines for deep chillers, or allows direct commercial cash/UPI sales versus free product sampling only.

**What I Verified vs. What I Guessed:**
- *Verified (via conversations with 2 D2C beverage brand marketers & 1 college fest corporate POC):* Emerging brands have quarterly experimental budgets of ₹50k to ₹2.5 Lakhs; their #1 bottleneck is getting ghosted by student POCs or discovering power/chiller restrictions after signing.
- *Guessed / Assumed:* A standardized Cost-per-1,000 (CPM) metric and a 3-fest side-by-side shortlist comparison reduces festival discovery-to-pitch cycle time from 18 days to under 48 hours.

---

### 2. What is In Scope
1. **Curated & Verified Multi-City Directory:** 12 pre-seeded realistic Indian college fests across the top 4 consumer hubs (Mumbai, Pune, Bengaluru, Delhi NCR) covering small trial setups (₹28k, 6k footfall) to national marquee fests (₹3.8L, 52k footfall).
2. **Instant Multi-Parameter Filter Engine:**
   - City Hub (All, Mumbai, Pune, Bengaluru, Delhi NCR)
   - Max Budget Slider (₹25k to ₹5.0L)
   - Campaign Activation Goal (Product Sampling, Commercial Food Stall, Title/Co-Sponsorship)
   - Minimum Footfall Threshold (3,000 to 50,000+ students)
   - Real-time text search and sorting by Lowest CPM, Highest Footfall, and Budget.
3. **Fest Discovery Cards with Standardized Decision Metrics:**
   - College & Fest Name, Verified Footfall badge, Dates, Starting Package.
   - **Auto-Calculated CPM (Cost per 1,000 Students):** `(Starting Package / Verified Footfall) * 1,000`.
   - Campus crowd vibe tags and activation chips.
   - Dedicated "F&B Logistics Specs" drawer (chiller power, peak consumption rush, past F&B sponsors).
4. **Interactive Shortlist & Compare Dock:**
   - Constraint-enforced shortlisting (up to 3 festivals max).
   - Real-time aggregation of **Combined Reach**, **Total Budget**, and **Blended CPM**.
   - Full side-by-side matrix comparing dimensions, power backup, sampling policies, and brand fit verdicts.
5. **Pitch Call Request & Confirmation State:**
   - Streamlined booking modal capturing brand name, F&B category, work email, and preferred slot.
   - Instant confirmation state with unique reference ID (`#FEST-PITCH-XXXX`), email confirmation recap, and downloadable campaign brief.

---

### 3. What is Out of Scope
- **No Auth / Login Barriers:** Frictionless zero-login experience for fast testing by evaluators and marketing managers.
- **No Fest-Side Admin Portal:** Student committees do not log in to edit listings; data is standardized and curated.
- **No In-App Payment Gateway:** Actual sponsorship agreements involve legal contracts and tax invoices; the app solves *discovery, shortlisting, and initial pitch booking*, not final payment escrow.

---

### 4. What is the Solution and Why
The solution is **FestMatch F&B**—a lightweight, responsive discovery and decision-engine built specifically for the trade marketing workflow of Indian F&B brands.

**Why this solution works:**
1. **Translates Opaque Sponsorships into Performance Marketing:** By introducing auto-calculated CPM, brands can evaluate a ₹35k stall at Fergusson College (₹4,118 CPM) against a ₹1.4L stall at St. Xavier's (₹5,000 CPM) using clear quantitative metrics.
2. **Max 3 Shortlist Constraint Prevents Decision Fatigue:** Rather than browsing dozens of vague PDF brochures, managers shortlist up to 3 complementary festivals (e.g., 1 high-reach Mumbai fest + 1 targeted Bengaluru fest + 1 low-cost Pune testing kiosk) and review total campaign reach instantly.
3. **F&B-Specific Feasibility Data:** Unlike generic event directories, every listing highlights chiller wattage, peak hunger/thirst hours, and commercial selling rules—eliminating costly logistical surprises.
