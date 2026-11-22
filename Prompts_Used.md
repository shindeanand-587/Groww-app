# Prompts Used to Create the FestMatch F&B Tool
**Artifact 2: Prompt Engineering Log & Architecture Prompts**

This document records the structured prompts and design instructions used to build the FestMatch F&B web application.

---

### Prompt 1: Domain Modeling & Seed Dataset Architecture
```text
Act as a Principal Product Architect and Domain Expert in Indian D2C / F&B Trade Marketing.
We are designing a digital platform called 'FestMatch F&B' for emerging beverage, snack, and QSR brands 
to discover and sponsor Indian college festivals.

Create a curated JavaScript seed dataset of 10 to 12 realistic Indian college festivals across 
Mumbai, Pune, Bengaluru, and Delhi NCR.

Requirements for each fest object:
1. Realistic fest and college name (e.g. Mood Indigo - IIT Bombay, Malhar - St. Xavier's, Crossroads - SRCC, 
   Sympulse - Symbiosis, Cul-Ah! - Mount Carmel, 8th Mile - RVCE, MindSpark - COEP, etc.).
2. Varied budgets spanning ₹25,000 to ₹4,00,000 and verified student footfalls from 6,000 to 52,000+.
3. Supported Campaign Goals: "Product Sampling", "Food Stall", "Title/Co-Sponsor".
4. Standardized decision metric: CPM (Cost per 1,000 students) = round((startingPackage / footfall) * 1000).
5. Granular F&B logistical specs:
   - Chiller/Freezer electrical power (15A socket availability)
   - Stall dimensions
   - Sampling permissions (canopy roaming vs fixed spot)
   - Commercial selling rights (cash/UPI permissions)
   - Peak consumption hours (lunch rush vs evening pro-nites)
   - Student demographic split (hostellers % vs day scholars)
   - Past F&B brands that activated.
```

---

### Prompt 2: Core User Interface, Theme, and Responsive Layout
```text
Build a crisp, responsive Single-Page Web App using Tailwind CSS and Lucide icons for the FestMatch tool.
Theme: Clean, modern, high-contrast B2B SaaS palette. Use Slate neutrals with vibrant Rose/Crimson accents 
to evoke food & beverage energy, paired with Emerald for high-ROI metrics.

Sections to build:
1. Header: Brand badge ("FestMatch F&B - India Edition"), tagline, live shortlist badge counter, and 
   "How CPM is Calculated" trigger modal.
2. Hero Banner: Tailored for D2C beverage & snack brand marketing managers looking for verified student footfall.
3. Quick Preset Filter Chips: "All Fests", "Starter Budget (< ₹1 Lakh)", "Mega Footfall (25k+)", "Best ROI (< ₹5k CPM)", 
   "Sampling Ready".
4. Filter Bar:
   - City Tabs: All Cities, Mumbai, Pune, Bengaluru, Delhi NCR
   - Search input: Live fuzzy matching for college/fest name
   - Sort dropdown: Lowest CPM (Best ROI), Highest Footfall, Budget Low-to-High, Budget High-to-Low
   - Max Budget Slider: ₹25,000 to ₹5,00,000 with Indian currency formatting (₹ Lakhs)
   - Campaign Goal Dropdown: Product Sampling, Food Stall, Title/Co-Sponsor
   - Min Footfall Slider: 3,000 to 50,000+
5. Responsive Card Grid (1 col mobile, 2 col tablet, 3 col desktop) with empty state fallback when no results match.
```

---

### Prompt 3: Discovery Cards & Standardized Decision Metrics
```text
Render each fest card as a decision cockpit for a marketing manager.
Key elements on each card:
1. Gradient header with fest cover tag, edition, city/campus location, and verified footfall badge.
2. College name, fest title, dates, and days count.
3. Audience & Campus vibe tag (e.g. "Asia's Largest Fest • Massive Night Concerts").
4. Standardized Decision Metrics Grid:
   - Verified Footfall (e.g. 28,000 Students)
   - Starting Package formatted in INR (e.g. ₹1.4 Lakhs / ₹1,40,000)
   - Cost per 1,000 Students (CPM) auto-calculated in real time (e.g. ₹5,000 / 1k)
5. Activation tags: 🥤 Product Sampling, 🍔 Food Stall, ⭐ Title/Co-Sponsor
6. Actions:
   - "F&B Specs": Opens an in-depth modal showing power backup, stall dimensions, and peak consumption hours.
   - "+ Shortlist" / "✓ Shortlisted": Toggles selection with visual feedback and state management.
```

---

### Prompt 4: Shortlist Constraints, Floating Dock & Comparison Matrix
```text
Implement an interactive shortlist engine with the following business constraints:
1. Maximum 3 Fests: If the user attempts to add a 4th fest, prevent addition and display an intuitive toast:
   "Shortlist limit reached! You can shortlist up to 3 fests at a time."
2. Floating Bottom Dock:
   - Displays whenever 1 to 3 fests are shortlisted.
   - Shows festival thumbnail pills with individual 'x' remove buttons.
   - Real-time aggregate metrics:
     * Combined Reach = sum of footfalls
     * Total Budget = sum of starting packages
     * Blended CPM = round((total budget / total reach) * 1000)
3. Side-by-Side Comparison Modal:
   - Renders a multi-column comparison table comparing all 3 shortlisted fests across Footfall, Package, CPM, 
     Dates, Vibe, Chiller Power, Sampling Permissions, Peak Hours, and Brand Fit Verdict.
   - Shows empty slot indicators if fewer than 3 fests are selected.
4. "Request Pitch Call" Workflow:
   - Booking modal collecting Brand Name, F&B Category, Marketing Contact, Work Email, Preferred 15-min Slot, 
     and Special Logistics Notes.
   - Form submission smoothly transitions to a confirmation state with a generated reference code (#FEST-PITCH-XXXX), 
     email recap, 3-step timeline ("What happens next"), and a 1-click "Download Campaign Brief" button.
```

---

### Prompt 5: Automated Testing & Verification Suite
```text
Write a standalone Python evaluation test suite `test_suite.py` that verifies:
1. Seed data coverage (all 4 cities, budget spread ₹25k to ₹4L+, footfalls 6k to 50k+).
2. Exact mathematical correctness of CPM = round((Package / Footfall) * 1000) for every item.
3. Multi-parameter filtering algorithms (city, budget ceiling, footfall threshold, campaign goals).
4. Shortlist boundary constraints (strict 3-item ceiling).
5. Aggregate math (combined reach, total budget, blended CPM).
6. Booking payload schema and email format validation.
```
