# FestMatch F&B — College Fest Sponsorship & Sampling Engine

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=shindeanand-587/Groww-app&branch=main&mainModule=streamlit_app.py)

> A clean, responsive web application for emerging Indian Food & Beverage (F&B) brands to discover, compare, and shortlist college festivals for product sampling, food stalls, and sponsorships.

---

## 🎯 Target Persona & Problem Context
- **Core User:** Trade Marketing Manager / Growth Lead at an emerging Indian F&B brand (e.g., ready-to-drink beverages, cold brew, healthy snacks, craft chips, or QSR pop-up brands).
- **Core Problem:** College fest sponsorships in India are plagued by opaque pricing, unaudited footfall claims, fragmented WhatsApp communications, and a lack of standardized ROI metrics. Emerging brands waste weeks trying to evaluate whether a college fest offers viable trial density and chiller logistics.
- **The Solution:** **FestMatch F&B** standardizes fest discovery through verified student footfalls, transparent package rates, auto-calculated **Cost per 1,000 Students (CPM)**, a 3-fest comparison matrix, and a direct pitch call request workflow.

---

## 🚀 Key Features Built (In Scope)

### 1. Interactive Multi-Parameter Filter Bar
- **City Hubs:** Quick tabs for **All Cities (12)**, **Mumbai**, **Pune**, **Bengaluru**, and **Delhi NCR**.
- **Max Budget (in ₹):** Dual interactive slider & display spanning ₹25,000 to ₹5,00,000 with Indian currency formatting.
- **Campaign Goals:** Multi-activation filter for **Product Sampling (Kiosks/Chillers)**, **Food Stall (Commercial Selling)**, and **Title/Co-Sponsorship**.
- **Minimum Footfall:** Slider ranging from 3,000 to 50,000+ verified students.
- **Sorting Options:** Lowest CPM (Best ROI), Highest Footfall, Budget (Low to High), and Budget (High to Low).
- **Live Search & Quick Presets:** Search by fest or college name; 1-click presets for Starter Budget (< ₹1L), Mega Footfall (25k+), and Best ROI (< ₹5k CPM).

### 2. Fest Discovery Cards with Standardized Decision Metrics
Each festival card acts as an executive decision cockpit:
- **College & Fest Name:** e.g., *Mood Indigo (IIT Bombay)*, *Malhar (St. Xavier's)*, *Crossroads (SRCC)*.
- **Location & Edition:** City, campus area, and festival edition.
- **Dates & Days:** Event calendar duration.
- **Verified Footfall:** Audited attendance with verification badge.
- **Starting Package (₹):** Transparent entry package cost.
- **Cost per 1,000 Students (CPM):** Auto-calculated in real time using:
  $$\text{CPM} = \left(\frac{\text{Starting Package (₹)}}{\text{Verified Footfall}}\right) \times 1,000$$
- **Crowd & Campus Vibe Tag:** Contextual audience insights (e.g., *"Asia's Largest Fest • Massive Night Concerts"*).
- **Activation Chips:** Supported activations (🥤 Product Sampling, 🍔 Food Stall, ⭐ Title/Co-Sponsor).
- **F&B Logistics Specs Modal:** Detailed breakdown of continuous 15A chiller power sockets, stall canopy dimensions, peak consumption hours, hosteller demographics, and past F&B sponsors.

### 3. Shortlist & Compare Drawer (Max 3 Fests)
- **Hard Limit of 3 Fests:** Prevents cognitive overload; attempts to add a 4th festival trigger a clear warning toast.
- **Floating Bottom Dock:** Appears smoothly when 1–3 fests are shortlisted, featuring:
  - Selected festival chips with 1-click removal.
  - **Combined Estimated Reach:** Sum of verified student footfalls.
  - **Total Starting Budget:** Sum of package costs in ₹.
  - **Blended CPM:** Combined cost per 1,000 students across the selected portfolio.
- **Side-by-Side Comparison Matrix:** Full modal comparing shortlisted fests across footfall, package, CPM, power availability, sampling permissions, peak hours, and brand fit verdicts.

### 4. "Request Pitch Call" Booking Modal & Confirmation State
- **Streamlined Booking Modal:** Captures Brand Name, F&B Category, Marketing Contact Name, Work Email, Phone Number, Preferred 15-min Slot, and Special Logistics Notes.
- **Confirmation State:**
  - Unique booking reference code (e.g., `#FEST-PITCH-2026-9531`).
  - Summary of shortlisted fests and combined audience reach.
  - 3-step *"What happens next"* timeline.
  - **Download Campaign Brief:** 1-click `.txt` export of the complete shortlist summary.

### 5. Curated Seed Dataset (12 Realistic Indian College Fests)
Pre-populated with 12 iconic fests across Mumbai, Pune, Bengaluru, and Delhi NCR:
- Budgets range from **₹28,000** (*Taarangana, IGDTUW*) to **₹3,80,000** (*Rendezvous, IIT Delhi*).
- Footfalls range from **6,000** to **52,000+** students.
- All fests include comprehensive F&B specs and verified historical data.

---

## 🚫 Out of Scope (By Design)
- **No Login / Authentication Walls:** Instant zero-login access for fast product evaluation.
- **No Fest-Side Admin Portal:** Student committees do not submit listings; data is pre-verified.
- **No Payment Gateways:** Sponsorship deals involve legal and tax compliance; the app focuses on discovery, comparison, and pitch scheduling.

---

## 💻 How to Run the Web App Locally

### Option 1: Python Local Server (Recommended)
Open a terminal in the project directory and run:
```bash
python -m http.server 8000
```
Then open your browser and navigate to:
```
http://localhost:8000
```

### Option 2: Direct File Open
You can directly open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari). All styles and scripts run natively with zero compilation steps.

---

## 🧪 Automated Test Suite & Evals
The project includes a standalone automated Python evaluation runner `test_suite.py`:
```bash
python test_suite.py
```
**Test Results:** 19 Passed, 0 Failed (100% test pass rate).
Verifies:
- Seed data coverage across all 4 cities and budget/footfall ranges.
- Mathematical accuracy of CPM for every festival.
- Multi-parameter filtering algorithms and edge cases.
- Shortlist hard ceiling (max 3 items).
- Aggregate math (combined reach, total budget, blended CPM).
- Booking payload validation schema.

---

## 📁 Repository Structure & Submission Artifacts

```
c:\Groww Assignment\
├── index.html                    # Semantic, accessible SPA layout with Tailwind CSS & Lucide icons
├── styles.css                    # Glassmorphism, animations, custom scrollbars, print stylesheets
├── data.js                       # 12 curated Indian college fests with granular F&B specs
├── app.js                        # State machine, CPM math, filter engine, shortlist & modal controllers
├── test_suite.py                 # Automated verification suite (19 unit/eval tests)
├── generate_journey_screenshots.py # Headless browser screenshot generator
│
├── Case_Study_Writeup.md         # Artifact 1: 1-Page (~550 words) Product Case Study writeup
├── Prompts_Used.md               # Artifact 2: Prompt engineering and architectural prompt log
├── Evaluation_and_Test_Plan.md   # Artifact 3: Systematic evaluation report and edge-case matrix
├── README.md                     # Project overview and execution documentation
│
└── screenshots/                  # High-resolution screenshots of all user journey states
    ├── screenshot_desktop.png            # Main discovery dashboard with active filters
    ├── screenshot_full_cards.png         # Cards grid with decision metrics & activation chips
    ├── screenshot_shortlist_dock.png     # Floating shortlist dock with aggregate reach & budget
    ├── screenshot_comparison_matrix.png  # Side-by-side 3-fest comparison matrix
    ├── screenshot_fnb_specs.png          # Fest detail modal with F&B logistics specs
    ├── screenshot_pitch_form.png         # Pitch call booking modal
    └── screenshot_pitch_confirmed.png    # Booking confirmation state with reference code
```
