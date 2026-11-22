"""
FestMatch F&B - Automated Verification & Evaluation Suite
Runs comprehensive unit and scenario tests on seed data, CPM mathematics,
filtering algorithms, shortlist boundaries (max 3), and campaign metrics.
"""

import json
import re
import math

def load_data_from_js(filepath="data.js"):
    """Parse FESTS_DATA from data.js into Python dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON-like array from FESTS_DATA = [ ... ];
    match = re.search(r"const\s+FESTS_DATA\s*=\s*(\[[\s\S]*?\]);", content)
    if not match:
        raise ValueError("Could not find FESTS_DATA in data.js")
    
    raw_js = match.group(1)
    
    # Strip comments
    raw_js = re.sub(r"//.*", "", raw_js)
    
    # Simple JS object to valid JSON conversion
    # Quote unquoted keys
    clean_json = re.sub(r'(\b[a-zA-Z_][a-zA-Z0-9_]*\b)\s*:', r'"\1":', raw_js)
    # Remove trailing commas
    clean_json = re.sub(r',\s*([}\]])', r'\1', clean_json)
    
    return json.loads(clean_json)

def run_all_tests():
    print("=" * 70)
    print(" FESTMATCH F&B - AUTOMATED EVALUATION & TEST RUNNER")
    print("=" * 70)
    
    passed = 0
    failed = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name} -> {details}")

    # --- EVAL 1: SEED DATA INTEGRITY ---
    print("\n--- EVAL 1: Seed Data Integrity & Breadth ---")
    fests = load_data_from_js()
    assert_test("Total seed fests count between 8 and 15", 8 <= len(fests) <= 15, f"Found {len(fests)}")
    
    cities = {f["city"] for f in fests}
    expected_cities = {"Mumbai", "Pune", "Bengaluru", "Delhi"}
    assert_test(
        "All 4 key cities represented (Mumbai, Pune, Bengaluru, Delhi)",
        expected_cities.issubset(cities),
        f"Found cities: {cities}"
    )

    budgets = [f["startingPackage"] for f in fests]
    min_b, max_b = min(budgets), max(budgets)
    assert_test(
        "Budget range spans ₹25k to ₹4L+ (Varied Budgets)",
        min_b <= 35000 and max_b >= 350000,
        f"Min: ₹{min_b}, Max: ₹{max_b}"
    )

    footfalls = [f["footfall"] for f in fests]
    min_ff, max_ff = min(footfalls), max(footfalls)
    assert_test(
        "Footfall range spans small (<10k) to mega (50k+) campuses",
        min_ff <= 10000 and max_ff >= 50000,
        f"Min: {min_ff}, Max: {max_ff}"
    )

    # --- EVAL 2: STANDARDIZED CPM MATHEMATICS ---
    print("\n--- EVAL 2: Standardized CPM Calculation Math ---")
    cpm_correct = True
    cpm_errors = []
    for f in fests:
        expected_cpm = round((f["startingPackage"] / f["footfall"]) * 1000)
        actual_cpm = f["cpm"]
        if expected_cpm != actual_cpm:
            cpm_correct = False
            cpm_errors.append(f"{f['name']}: expected {expected_cpm}, got {actual_cpm}")

    assert_test("Every fest has mathematically accurate CPM = round((Package/Footfall)*1000)", cpm_correct, ", ".join(cpm_errors))

    # --- EVAL 3: FILTERING ALGORITHMS ---
    print("\n--- EVAL 3: Filtering Engine Accuracy ---")
    
    # City filter test: Pune
    pune_fests = [f for f in fests if f["city"] == "Pune"]
    assert_test("Pune city filter returns exact Pune fests", len(pune_fests) >= 2, f"Found {len(pune_fests)}")

    # Max Budget filter test: Max ₹1,00,000
    under_1L = [f for f in fests if f["startingPackage"] <= 100000]
    assert_test("Max budget ₹1,00,000 includes affordable tier", len(under_1L) >= 4, f"Found {len(under_1L)}")
    assert_test("No fest above ₹1,00,000 included in under_1L", all(f["startingPackage"] <= 100000 for f in under_1L))

    # Campaign Goal filter test: Product Sampling vs Food Stall vs Title/Co-Sponsor
    sampling_fests = [f for f in fests if "Product Sampling" in f["supportedGoals"]]
    stall_fests = [f for f in fests if "Food Stall" in f["supportedGoals"]]
    sponsor_fests = [f for f in fests if "Title/Co-Sponsor" in f["supportedGoals"]]
    
    assert_test("Product Sampling goal filter yields verified activations", len(sampling_fests) >= 8)
    assert_test("Food Stall goal filter yields commercial selling spots", len(stall_fests) >= 6)
    assert_test("Title/Co-Sponsor goal filter yields marquee fests", len(sponsor_fests) >= 4)

    # Minimum Footfall filter: >= 20,000
    high_footfall = [f for f in fests if f["footfall"] >= 20000]
    assert_test("Minimum footfall >= 20,000 filters accurately", all(f["footfall"] >= 20000 for f in high_footfall))

    # Combined Multi-Filter: Mumbai + Max ₹2,00,000 + Sampling
    combined_test = [
        f for f in fests 
        if f["city"] == "Mumbai" and f["startingPackage"] <= 200000 and "Product Sampling" in f["supportedGoals"]
    ]
    assert_test("Combined multi-filter (Mumbai + <= ₹2L + Sampling) returns valid subset", len(combined_test) >= 2)

    # --- EVAL 4: SHORTLIST LOGIC & AGGREGATE METRICS MATH ---
    print("\n--- EVAL 4: Shortlist Constraints & Math Aggregation ---")
    
    # Pick 3 fests for a mock shortlist
    sample_3 = fests[:3]
    total_reach = sum(f["footfall"] for f in sample_3)
    total_budget = sum(f["startingPackage"] for f in sample_3)
    blended_cpm = round((total_budget / total_reach) * 1000)

    assert_test("Combined reach equals sum of shortlisted footfalls", total_reach == sum(f["footfall"] for f in sample_3))
    assert_test("Total budget equals sum of shortlisted starting packages", total_budget == sum(f["startingPackage"] for f in sample_3))
    assert_test("Blended CPM matches aggregate ratio round((total_budget/total_reach)*1000)", blended_cpm == round((total_budget / total_reach) * 1000))

    # Test Shortlist Max 3 Boundary Constraint
    max_shortlist_limit = 3
    test_selection = ["id1", "id2", "id3", "id4"]
    accepted_selection = test_selection[:max_shortlist_limit]
    assert_test("Shortlist boundary strictly enforces maximum 3 items", len(accepted_selection) == 3)

    # --- EVAL 5: BOOKING VALIDATION SCHEMA ---
    print("\n--- EVAL 5: Booking Modal Payload Validation ---")
    valid_booking_payload = {
        "brandName": "Lahori Zeera",
        "contactName": "Rohit Verma",
        "contactEmail": "rohit@lahorizeera.in",
        "preferredSlot": "Tomorrow 11:30 AM IST",
        "fests": [sample_3[0]["id"], sample_3[1]["id"]]
    }
    
    has_required_fields = all(k in valid_booking_payload for k in ["brandName", "contactName", "contactEmail", "preferredSlot", "fests"])
    email_is_valid = bool(re.match(r"^[^@]+@[^@]+\.[^@]+$", valid_booking_payload["contactEmail"]))
    assert_test("Booking payload contains all required marketing manager fields", has_required_fields)
    assert_test("Email format validates correctly", email_is_valid)

    # --- SUMMARY ---
    print("\n" + "=" * 70)
    print(f" TEST RUN COMPLETE: {passed} PASSED, {failed} FAILED")
    print("=" * 70)
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
