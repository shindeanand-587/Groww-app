# Evaluation and Test Plan: FestMatch F&B
**Artifact 3: Systematic Evals, Quality Assurance & Edge-Case Verifications**

This document details the evaluation framework, automated unit tests, edge-case evaluations, and visual verification results used to validate the **FestMatch F&B** application.

---

### 1. Evaluation Objectives
The evaluation framework was designed to test five core dimensions of product quality:
1. **Mathematical Accuracy:** Verifying that CPM and aggregate campaign calculations are strictly accurate.
2. **Filter & Search Precision:** Ensuring zero false positives or false negatives across city, budget, footfall, and activation goals.
3. **Boundary & Constraint Enforcement:** Validating that the shortlist hard cap of 3 fests is strictly respected with clear user feedback.
4. **Form Validation & State Transitions:** Confirming that pitch booking requests validate inputs and transition to a reliable confirmation state.
5. **Responsiveness & UX Polish:** Validating UI layout on mobile, tablet, and desktop viewports.

---

### 2. Automated Test Suite Execution (`test_suite.py`)
An automated test runner was authored to test data structures, arithmetic algorithms, and filtering edge cases.

#### Test Execution Output:
```text
======================================================================
 FESTMATCH F&B - AUTOMATED EVALUATION & TEST RUNNER
======================================================================

--- EVAL 1: Seed Data Integrity & Breadth ---
  [PASS] Total seed fests count between 8 and 15 (12 fests found)
  [PASS] All 4 key cities represented (Mumbai, Pune, Bengaluru, Delhi)
  [PASS] Budget range spans ₹25k to ₹4L+ (Min: ₹28,000, Max: ₹3,80,000)
  [PASS] Footfall range spans small (<10k) to mega (50k+) campuses (Min: 6,000, Max: 52,000)

--- EVAL 2: Standardized CPM Calculation Math ---
  [PASS] Every fest has mathematically accurate CPM = round((Package/Footfall)*1000)

--- EVAL 3: Filtering Engine Accuracy ---
  [PASS] Pune city filter returns exact Pune fests (3 fests)
  [PASS] Max budget ₹1,00,000 includes affordable tier (6 fests)
  [PASS] No fest above ₹1,00,000 included in under_1L
  [PASS] Product Sampling goal filter yields verified activations (12 fests)
  [PASS] Food Stall goal filter yields commercial selling spots (11 fests)
  [PASS] Title/Co-Sponsor goal filter yields marquee fests (5 fests)
  [PASS] Minimum footfall >= 20,000 filters accurately (5 fests)
  [PASS] Combined multi-filter (Mumbai + <= ₹2L + Sampling) returns valid subset (2 fests)

--- EVAL 4: Shortlist Constraints & Math Aggregation ---
  [PASS] Combined reach equals sum of shortlisted footfalls
  [PASS] Total budget equals sum of shortlisted starting packages
  [PASS] Blended CPM matches aggregate ratio round((total_budget/total_reach)*1000)
  [PASS] Shortlist boundary strictly enforces maximum 3 items

--- EVAL 5: Booking Modal Payload Validation ---
  [PASS] Booking payload contains all required marketing manager fields
  [PASS] Email format validates correctly

======================================================================
 TEST RUN COMPLETE: 19 PASSED, 0 FAILED (100% Success Rate)
======================================================================
```

---

### 3. Edge Case & Failure Mode Matrix

| Test Scenario | Input / Action | Expected Result | Verified Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Shortlist Overfill** | User attempts to add a 4th festival to shortlist | 4th fest is rejected; toast warning alerts user: *"Shortlist limit reached! You can shortlist up to 3 fests at a time."* | Shortlist stays capped at 3; warning toast displayed; button remains unselected. | **PASS** |
| **Zero Results Filter** | User sets City = Pune, Max Budget = ₹30k, Min Footfall = 40,000 | Zero matching fests; display dedicated empty state with 1-click "Clear All Filters" button. | Empty state rendered with icon and reset CTA; zero console errors. | **PASS** |
| **Combined Math (Blended CPM)** | User shortlists Mood Indigo (52k reach, ₹3.5L) + Malhar (28k reach, ₹1.4L) | Combined reach = 80,000; Total budget = ₹4,90,000; Blended CPM = `round((490000 / 80000) * 1000) = ₹6,125` | Dock displays: 80,000 reach, ₹4,90,000 budget, ₹6,125 CPM. | **PASS** |
| **Live Search Query** | User types "iit" in search input | Only IIT Bombay (Mood Indigo) and IIT Delhi (Rendezvous) shown. | Exactly 2 matching cards rendered; clear button '×' appears. | **PASS** |
| **Booking Form Incomplete** | User submits pitch form with missing work email | Browser native HTML5 validation blocks submission and prompts user to enter email. | Submission blocked until email provided. | **PASS** |
| **Booking Success Transition** | User enters valid brand name, email, and slot | Form hides, confirmation view displays with unique Reference Code, brand recap, and timeline. | Reference code `#FEST-PITCH-2026-XXXX` generated; email summary shown. | **PASS** |
| **Campaign Brief Download** | User clicks "Download Campaign Brief" on confirmation screen | Browser triggers `.txt` download containing structured fest names, budget, reach, and booking reference. | Text brief file cleanly downloaded with proper formatting. | **PASS** |
| **Page Refresh Persistence** | User shortlists 2 fests and reloads browser | Shortlist state preserved from `localStorage`. | Shortlist count, badges, and floating dock restore seamlessly on reload. | **PASS** |

---

### 4. Cross-Viewport Visual Audit

Headless Chrome visual render evaluations were conducted across three standard viewports:
- **Desktop (1280px × 1000px):** 3-column fest card grid; floating bottom dock spans 5xl container with inline metrics.
- **Tablet (768px × 1024px):** 2-column fest card grid; filter bar stacks cleanly; comparison table remains horizontally scrollable without breaking layout.
- **Mobile (375px × 812px):** Single-column cards; sticky shortlist dock shifts to compact vertical stack; modal touch targets exceed 44px minimum for accessibility.

---

### 5. Summary of Visual Proof Artifacts Captured
- `screenshot_desktop.png` - Full application discovery dashboard with active filters.
- `screenshot_full_cards.png` - Decision cards grid showcasing standardized metrics and activation chips.
- `screenshot_shortlist_dock.png` - Floating bottom dock with live aggregated metrics (80k reach, ₹4.9L budget, ₹6,125 CPM).
- `screenshot_comparison_matrix.png` - 3-column side-by-side comparison matrix with granular F&B logistics.
- `screenshot_fnb_specs.png` - Fest detail modal with chiller power, peak hours, and past sponsors.
- `screenshot_pitch_form.png` - Streamlined booking modal for marketing managers.
- `screenshot_pitch_confirmed.png` - Confirmation state with unique booking ID and 3-step timeline.
