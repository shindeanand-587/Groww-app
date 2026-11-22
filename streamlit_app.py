import streamlit as st
import pandas as pd
import json
import random
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FestMatch F&B | College Fest Discovery & Sampling Engine",
    page_icon="🥤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }
    
    .fest-header-card {
        border-radius: 14px;
        padding: 16px 18px;
        color: white;
        margin-bottom: 12px;
    }
    
    .badge-roi {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }

    .badge-tag {
        background-color: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- SEED DATA (12 REALISTIC INDIAN COLLEGE FESTS) ---
FESTS_DATA = [
    {
        "id": "mood_indigo_iitb",
        "name": "Mood Indigo",
        "edition": "55th Edition",
        "college": "IIT Bombay",
        "city": "Mumbai",
        "campusArea": "Powai, Mumbai",
        "dates": "Dec 18 - 21, 2026",
        "daysCount": 4,
        "footfall": 52000,
        "verified": True,
        "startingPackage": 350000,
        "vibeTag": "Asia's Largest Fest • Massive Night Concerts",
        "supportedGoals": ["Product Sampling", "Food Stall", "Title/Co-Sponsor"],
        "gradient": "linear-gradient(135deg, #1e40af 0%, #1e1b4b 100%)",
        "description": "The crown jewel of Indian college fests. Draws massive student crowds from across India with world-class pro-nites and international acts. Unrivalled volume for high-velocity beverage sampling.",
        "specs": {
            "stallDimensions": "15 x 12 ft Premium Canopy",
            "chillerPower": "2x 15A Power Backup (Ideal for Deep Freezers)",
            "samplingPermissions": "Full campus roaming + Main Stage chillers",
            "commercialSales": "Allowed (No revenue cut)",
            "peakHours": "1:30 PM - 4:00 PM & 7:00 PM - 11:30 PM (Concerts)",
            "demographics": "68% Hostellers, 32% Visiting Colleges • Avg age 19-23",
            "pastBrands": "Red Bull, Paper Boat, Chaayos, Epigamia, Bira 91 0.0",
            "verdict": "High-volume RTD beverages, cold brew, grab-and-go snack packs"
        }
    },
    {
        "id": "malhar_xaviers",
        "name": "Malhar",
        "edition": "48th Edition",
        "college": "St. Xavier's College",
        "city": "Mumbai",
        "campusArea": "Fort, South Mumbai",
        "dates": "Aug 14 - 16, 2026",
        "daysCount": 3,
        "footfall": 28000,
        "verified": True,
        "startingPackage": 140000,
        "vibeTag": "South Mumbai Arts & Media • Trendsetting Gen-Z",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #d97706 0%, #9f1239 100%)",
        "description": "The most iconic cultural festival in South Mumbai. Known for high aesthetic standards, design, media, and liberal arts students with strong disposable income and high organic social sharing.",
        "specs": {
            "stallDimensions": "10 x 10 ft Quadrangle Stall",
            "chillerPower": "1x 15A Power Socket (Single chiller allowed)",
            "samplingPermissions": "Main Quadrangle + Foyer zone",
            "commercialSales": "Allowed (Packaged snacks & gourmet foods)",
            "peakHours": "12:00 PM - 3:30 PM & 5:00 PM - 8:30 PM",
            "demographics": "58% Female, 42% Male • High D2C & specialty coffee affinity",
            "pastBrands": "Sleepy Owl, Raw Pressery, 4700BC Popcorn, Keventers",
            "verdict": "Artisanal kombucha, matcha, specialty cold coffee, healthy snack bites"
        }
    },
    {
        "id": "crossroads_srcc",
        "name": "Crossroads",
        "edition": "44th Edition",
        "college": "SRCC (Delhi University)",
        "city": "Delhi",
        "campusArea": "North Campus, Delhi",
        "dates": "Mar 05 - 08, 2027",
        "daysCount": 4,
        "footfall": 32000,
        "verified": True,
        "startingPackage": 220000,
        "vibeTag": "Premier Commerce Fest • High Spend & Brand Affinity",
        "supportedGoals": ["Product Sampling", "Food Stall", "Title/Co-Sponsor"],
        "gradient": "linear-gradient(135deg, #059669 0%, #134e4a 100%)",
        "description": "Delhi University North Campus's flagship cultural festival. Draws commerce and economics elite from across DU with high daily repeat spending and intense music concert hype.",
        "specs": {
            "stallDimensions": "12 x 10 ft Sports Ground Kiosk",
            "chillerPower": "2x 15A Power Connection",
            "samplingPermissions": "North Gate Entrance + Central Arena",
            "commercialSales": "Allowed (Food courts operate until 9 PM)",
            "peakHours": "1:00 PM - 4:30 PM & 6:00 PM - 9:30 PM",
            "demographics": "52% Female, 48% Male • Urban metro Gen-Z with high food delivery frequency",
            "pastBrands": "Lahori Zeera, Burger King, Wingreens, Beyond Snack",
            "verdict": "Spicy crunch snacks, sparkling fruit sodas, trendy quick-service rolls"
        }
    },
    {
        "id": "rendezvous_iitd",
        "name": "Rendezvous",
        "edition": "49th Edition",
        "college": "IIT Delhi",
        "city": "Delhi",
        "campusArea": "Hauz Khas, New Delhi",
        "dates": "Oct 16 - 19, 2026",
        "daysCount": 4,
        "footfall": 45000,
        "verified": True,
        "startingPackage": 380000,
        "vibeTag": "North India's Largest • High Energy & Hostel Footfall",
        "supportedGoals": ["Product Sampling", "Food Stall", "Title/Co-Sponsor"],
        "gradient": "linear-gradient(135deg, #7c3aed 0%, #312e81 100%)",
        "description": "North India's biggest university cultural event. Over 45k engineering & management students, intense late-night pro-nights, and bustling open-air midnight food courts.",
        "specs": {
            "stallDimensions": "15 x 15 ft Food Court Space",
            "chillerPower": "3x 15A Dedicated Lines",
            "samplingPermissions": "SAC Lawns & OAT Amphitheatre",
            "commercialSales": "Allowed (Midnight sales permitted until 1:00 AM)",
            "peakHours": "2:00 PM - 5:00 PM & 7:30 PM - 12:30 AM (Midnight rush)",
            "demographics": "72% Engineering hostellers • Heavy night snack & caffeine demand",
            "pastBrands": "Monster Energy, Domino's, Wow! Momo, Tata Gluco+",
            "verdict": "Midnight snack combos, energy drinks, instant noodles, electrolyte refreshers"
        }
    },
    {
        "id": "sympulse_scms",
        "name": "Sympulse",
        "edition": "16th Edition",
        "college": "Symbiosis (SCMS)",
        "city": "Pune",
        "campusArea": "Viman Nagar, Pune",
        "dates": "Jan 22 - 25, 2027",
        "daysCount": 4,
        "footfall": 22000,
        "verified": True,
        "startingPackage": 115000,
        "vibeTag": "Cosmopolitan BBA Crowd • Premium Food Early Adopters",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #c026d3 0%, #701a75 100%)",
        "description": "The epicenter of Pune's international and cosmopolitan undergraduate crowd. High willingness to test exotic D2C flavours, modern beverages, and aesthetic packaging.",
        "specs": {
            "stallDimensions": "10 x 10 ft Courtyard Stall",
            "chillerPower": "1x 15A Power Point",
            "samplingPermissions": "Campus promenade + Registration zone",
            "commercialSales": "Allowed (High average order value >₹180)",
            "peakHours": "12:30 PM - 4:00 PM & 5:30 PM - 9:00 PM",
            "demographics": "55% Outstation students, 45% Pune residents • High D2C brand loyalty",
            "pastBrands": "Svami Drinks, The Whole Truth, Subway, Baskin Robbins",
            "verdict": "Gourmet iced teas, clean-label protein bars, bubble teas, Mexican bites"
        }
    },
    {
        "id": "mindspark_coep",
        "name": "MindSpark",
        "edition": "18th Edition",
        "college": "COEP Tech University",
        "city": "Pune",
        "campusArea": "Shivajinagar, Pune",
        "dates": "Nov 12 - 14, 2026",
        "daysCount": 3,
        "footfall": 14000,
        "verified": True,
        "startingPackage": 60000,
        "vibeTag": "Engineering Minds • Long Day Sessions & Quick Bites",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #0891b2 0%, #1e3a8a 100%)",
        "description": "Maharashtra's leading technical festival. Thousands of participants from 100+ colleges competing in hackathons, robotics, and tech paper presentations. Exceptional value CPM under ₹4,500.",
        "specs": {
            "stallDimensions": "10 x 8 ft Covered Canopy",
            "chillerPower": "1x 15A Socket provided",
            "samplingPermissions": "Main Quadrangle & Hackathon Hall",
            "commercialSales": "Allowed (High tea/coffee & finger snacks volume)",
            "peakHours": "11:00 AM - 3:00 PM & 5:00 PM - 8:00 PM",
            "demographics": "65% Male, 35% Female • Heavy sustained screen-time sessions",
            "pastBrands": "Bru Coffee, Parle Agro, Balaji Wafers, Hell Energy",
            "verdict": "Quick energy boosters, affordable crunch snacks, iced teas"
        }
    },
    {
        "id": "cul_ah_mcc",
        "name": "Cul-Ah!",
        "edition": "38th Edition",
        "college": "Mount Carmel College",
        "city": "Bengaluru",
        "campusArea": "Vasanth Nagar, Bengaluru",
        "dates": "Dec 04 - 06, 2026",
        "daysCount": 3,
        "footfall": 18000,
        "verified": True,
        "startingPackage": 95000,
        "vibeTag": "Fashion & Lifestyle Hub • Viral Social Media Reach",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #f43f5e 0%, #881337 100%)",
        "description": "One of Bengaluru's most vibrant and culturally influential college festivals. Renowned for supreme social media engagement, fashion events, and female student creator networks.",
        "specs": {
            "stallDimensions": "10 x 10 ft Lawn Stall",
            "chillerPower": "1x 15A Clean Power Outlet",
            "samplingPermissions": "Central Walkway & Food Pavilion",
            "commercialSales": "Allowed (High dessert & cold beverage velocity)",
            "peakHours": "11:30 AM - 3:30 PM & 4:30 PM - 7:30 PM",
            "demographics": "90% Female student body + Co-ed intercollege fest passes",
            "pastBrands": "Smoor Chocolates, Epigamia Greek Yogurt, Chaayos, Paper Boat",
            "verdict": "Flavoured yogurts, prebiotic sodas, artisanal chocolates, aesthetic treats"
        }
    },
    {
        "id": "eighth_mile_rvce",
        "name": "8th Mile",
        "edition": "22nd Edition",
        "college": "RV College of Engineering",
        "city": "Bengaluru",
        "campusArea": "Mysore Road, Bengaluru",
        "dates": "Feb 18 - 20, 2027",
        "daysCount": 3,
        "footfall": 24000,
        "verified": True,
        "startingPackage": 125000,
        "vibeTag": "Bengaluru Tech & Rock Crowd • Massive Night Concerts",
        "supportedGoals": ["Product Sampling", "Food Stall", "Title/Co-Sponsor"],
        "gradient": "linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%)",
        "description": "RVCE's premier national cultural fest attracting engineering and tech crowds from across Karnataka. Features legendary rock nights, battle of bands, and packed evening crowds.",
        "specs": {
            "stallDimensions": "12 x 10 ft Stall with LED spotlights",
            "chillerPower": "2x 15A Power line",
            "samplingPermissions": "Main Stadium Ground & Tech Block",
            "commercialSales": "Allowed (Fast food, fries, rolls & drinks)",
            "peakHours": "1:00 PM - 4:00 PM & 6:30 PM - 10:30 PM (Rock Nite)",
            "demographics": "70% Hostellers & South Bengaluru college networks",
            "pastBrands": "Red Bull, Keventers, Taco Bell, Sunfeast Dark Fantasy",
            "verdict": "High-energy drinks, loaded nachos/fries, burger popups, instant refreshers"
        }
    },
    {
        "id": "kshitij_mithibai",
        "name": "Kshitij",
        "edition": "19th Edition",
        "college": "Mithibai College",
        "city": "Mumbai",
        "campusArea": "Vile Parle West, Mumbai",
        "dates": "Jan 14 - 17, 2027",
        "daysCount": 4,
        "footfall": 35000,
        "verified": True,
        "startingPackage": 180000,
        "vibeTag": "Bollywood & Media Epicenter • Heavy Suburban Footfall",
        "supportedGoals": ["Product Sampling", "Food Stall", "Title/Co-Sponsor"],
        "gradient": "linear-gradient(135deg, #f97316 0%, #7c2d12 100%)",
        "description": "One of suburban Mumbai's most massive college festivals. Frequent celebrity visits, film promotional crews, high fashion shows, and constant food lane congestion in Vile Parle.",
        "specs": {
            "stallDimensions": "12 x 10 ft Canopy in Prime Lane",
            "chillerPower": "2x 15A Plugs",
            "samplingPermissions": "Main Stage Enclosure & Street Promenade",
            "commercialSales": "Allowed (High turnover street food & beverage stalls)",
            "peakHours": "12:00 PM - 4:00 PM & 6:00 PM - 9:30 PM",
            "demographics": "Commerce, Arts & Mass Media students with active social followings",
            "pastBrands": "Frooti, Mad Over Donuts, Haldiram's, Storia Shakes",
            "verdict": "Dairy shakes, gourmet wafers, cookies, fizzy lemonades, popcorn"
        }
    },
    {
        "id": "spandan_fergusson",
        "name": "Spandan",
        "edition": "31st Edition",
        "college": "Fergusson College",
        "city": "Pune",
        "campusArea": "FC Road, Pune",
        "dates": "Dec 11 - 12, 2026",
        "daysCount": 2,
        "footfall": 8500,
        "verified": True,
        "startingPackage": 35000,
        "vibeTag": "Historic FC Road Hub • High Density & Rapid Turnaround",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #0d9488 0%, #064e3b 100%)",
        "description": "Located right on Pune's iconic FC Road youth corridor. Spandan allows emerging brands to set up high-impact sampling kiosks at an ultra-accessible ₹35,000 entry price point.",
        "specs": {
            "stallDimensions": "8 x 8 ft Compact Sampling Kiosk",
            "chillerPower": "1x 5A/15A socket",
            "samplingPermissions": "FC Amphitheatre Gate",
            "commercialSales": "Allowed (Snacks and packaged refreshments)",
            "peakHours": "11:00 AM - 2:30 PM & 4:30 PM - 7:30 PM",
            "demographics": "Undergraduate Arts, Science & Pune University students",
            "pastBrands": "Wagh Bakri Iced Tea, MTR Minute Meals, Yoga Bar",
            "verdict": "Superb for first-time sampling experiments, low-risk brand launches"
        }
    },
    {
        "id": "inbloom_christ",
        "name": "In-Bloom",
        "edition": "27th Edition",
        "college": "Christ University",
        "city": "Bengaluru",
        "campusArea": "Hosur Road, Bengaluru",
        "dates": "Feb 26 - 28, 2027",
        "daysCount": 3,
        "footfall": 16500,
        "verified": True,
        "startingPackage": 80000,
        "vibeTag": "Pan-India Student Body • High Hygiene & Brand Affinity",
        "supportedGoals": ["Product Sampling", "Food Stall"],
        "gradient": "linear-gradient(135deg, #0284c7 0%, #082f49 100%)",
        "description": "Christ University's flagship national festival. Known for disciplined campus culture, pristine cleanliness standards, and a pan-Indian student demographic with high affinity for premium packaged snacks.",
        "specs": {
            "stallDimensions": "10 x 10 ft Audi Block Kiosk",
            "chillerPower": "1x 15A Clean Line (Eco-packaging mandatory)",
            "samplingPermissions": "Main Birds Park Lawn & Audi foyer",
            "commercialSales": "Allowed (Packaged & ready-to-eat items only; no live cooking)",
            "peakHours": "12:00 PM - 3:00 PM & 4:30 PM - 7:00 PM",
            "demographics": "Pan-Indian multi-faculty students, 54% Female, 46% Male",
            "pastBrands": "Raw Pressery, Yoga Bar, Dorset Snacks, Paper Boat",
            "verdict": "Clean-label nutrition bars, functional waters, cold-pressed juices, muesli cups"
        }
    },
    {
        "id": "taarangana_igdtuw",
        "name": "Taarangana",
        "edition": "12th Edition",
        "college": "IGDTUW Delhi",
        "city": "Delhi",
        "campusArea": "Kashmere Gate, Delhi",
        "dates": "Jan 29 - 30, 2027",
        "daysCount": 2,
        "footfall": 6000,
        "verified": True,
        "startingPackage": 28000,
        "vibeTag": "All-Women Tech Campus • High Engagement & Sampling Trial",
        "supportedGoals": ["Product Sampling"],
        "gradient": "linear-gradient(135deg, #db2777 0%, #581c87 100%)",
        "description": "Delhi's leading women's engineering festival. An intimate, high-engagement environment where brands get 1-on-1 sampling interactions, direct user feedback, and stellar survey completion rates.",
        "specs": {
            "stallDimensions": "8 x 8 ft Sampling Counter",
            "chillerPower": "1x 5A Socket",
            "samplingPermissions": "Auditorium Walkway",
            "commercialSales": "Sampling only (Brand awareness & QR code downloads)",
            "peakHours": "11:30 AM - 2:30 PM & 4:00 PM - 6:30 PM",
            "demographics": "100% Female Engineering & Tech Undergraduates",
            "pastBrands": "Epigamia, Open Secret, Dabur Real, Lotte Choco Pie",
            "verdict": "Health snacks, protein cookies, sparkling waters, guilt-free treats"
        }
    }
]

# Calculate CPM for each fest: (package / footfall) * 1000
for f in FESTS_DATA:
    f["cpm"] = round((f["startingPackage"] / f["footfall"]) * 1000)

# --- SESSION STATE INITIALIZATION ---
if "shortlist" not in st.session_state:
    st.session_state.shortlist = []

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = None

# --- HEADER SECTION ---
col_logo, col_desc = st.columns([1, 4])
with col_logo:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #e11d48, #f59e0b); padding: 18px; border-radius: 16px; text-align: center; color: white;">
            <span style="font-size: 38px;">🥤</span>
        </div>
    """, unsafe_allow_html=True)
with col_desc:
    st.markdown("""
        <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #0f172a;">
            FestMatch <span style="color: #e11d48;">F&B</span>
            <span style="font-size: 13px; font-weight: 700; background: #ffe4e6; color: #be123c; padding: 4px 10px; border-radius: 999px; margin-left: 8px; vertical-align: middle;">
                India Edition
            </span>
        </h1>
        <p style="margin: 4px 0 0 0; font-size: 14px; color: #475569; font-weight: 500;">
            Discover & shortlist high-ROI Indian college fests for product sampling, food stalls, and sponsorships.
        </p>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("### 🎯 Filter College Fests")

# City Hub Filter
city_choice = st.sidebar.selectbox(
    "Target City Hub",
    ["All Cities", "Mumbai", "Pune", "Bengaluru", "Delhi"],
    index=0
)

# Max Budget Slider
max_budget = st.sidebar.slider(
    "Max Budget (in ₹)",
    min_value=25000,
    max_value=500000,
    value=500000,
    step=10000,
    format="₹%d"
)

# Campaign Goal Filter
goal_choice = st.sidebar.selectbox(
    "Campaign Goal",
    ["All Goals", "Product Sampling", "Food Stall", "Title/Co-Sponsor"],
    index=0
)

# Minimum Footfall Slider
min_footfall = st.sidebar.slider(
    "Minimum Verified Footfall",
    min_value=3000,
    max_value=50000,
    value=3000,
    step=1000,
    format="%d Students"
)

# Search Input
search_query = st.sidebar.text_input("🔍 Search College or Fest", "").strip().lower()

# Sort Selector
sort_choice = st.sidebar.selectbox(
    "Sort By",
    ["Lowest CPM (Best Value)", "Highest Footfall (Max Reach)", "Budget: Low to High", "Budget: High to Low"]
)

# Reset Button
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# --- FILTERING LOGIC ---
filtered = []
for f in FESTS_DATA:
    if city_choice != "All Cities" and f["city"].lower() != city_choice.lower():
        continue
    if f["startingPackage"] > max_budget:
        continue
    if f["footfall"] < min_footfall:
        continue
    if goal_choice != "All Goals" and goal_choice not in f["supportedGoals"]:
        continue
    if search_query:
        query_match = (
            search_query in f["name"].lower() or 
            search_query in f["college"].lower() or 
            search_query in f["city"].lower() or
            search_query in f["vibeTag"].lower()
        )
        if not query_match:
            continue
    filtered.append(f)

# Sort logic
if sort_choice == "Lowest CPM (Best Value)":
    filtered.sort(key=lambda x: x["cpm"])
elif sort_choice == "Highest Footfall (Max Reach)":
    filtered.sort(key=lambda x: x["footfall"], reverse=True)
elif sort_choice == "Budget: Low to High":
    filtered.sort(key=lambda x: x["startingPackage"])
elif sort_choice == "Budget: High to Low":
    filtered.sort(key=lambda x: x["startingPackage"], reverse=True)

# --- SHORTLIST FLOATING TRAY / AGGREGATE STATS ---
shortlisted_fests = [f for f in FESTS_DATA if f["id"] in st.session_state.shortlist]
shortlist_count = len(shortlisted_fests)

if shortlist_count > 0:
    total_reach = sum(f["footfall"] for f in shortlisted_fests)
    total_budget = sum(f["startingPackage"] for f in shortlisted_fests)
    blended_cpm = round((total_budget / total_reach) * 1000) if total_reach > 0 else 0
    
    st.markdown(f"""
        <div style="background: #0f172a; color: white; border-radius: 14px; padding: 14px 20px; margin-bottom: 24px; border: 1px solid #334155; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="background: #e11d48; color: white; padding: 4px 10px; border-radius: 8px; font-weight: 800; font-size: 13px;">
                    {shortlist_count}/3 SHORTLISTED
                </span>
                <span style="font-size: 13px; color: #cbd5e1; font-weight: 600;">
                    {' • '.join([f['name'] for f in shortlisted_fests])}
                </span>
            </div>
            <div style="display: flex; gap: 24px; font-size: 12px;">
                <div>Combined Reach: <strong style="color: white; font-family: monospace; font-size: 14px;">{total_reach:,}</strong></div>
                <div>Total Budget: <strong style="color: #fb7185; font-family: monospace; font-size: 14px;">₹{total_budget:,}</strong></div>
                <div>Blended CPM: <strong style="color: #34d399; font-family: monospace; font-size: 14px;">₹{blended_cpm:,}</strong></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- TABS FOR DISCOVERY, COMPARISON, AND PITCH BOOKING ---
tab_discover, tab_compare, tab_pitch = st.tabs([
    f"🎪 Discover Fests ({len(filtered)})",
    f"📊 Compare Shortlist ({shortlist_count}/3)",
    "📞 Request Pitch Call"
])

# ================= TAB 1: DISCOVER =================
with tab_discover:
    st.markdown(f"Showing **{len(filtered)}** verified college festivals:")
    
    if len(filtered) == 0:
        st.info("No college fests match these filters. Try expanding your budget or minimum footfall in the sidebar.")
    
    # 2-Column Responsive Card Grid
    cols = st.columns(2)
    for idx, fest in enumerate(filtered):
        col = cols[idx % 2]
        with col:
            is_in_shortlist = fest["id"] in st.session_state.shortlist
            
            # Card Container
            with st.container(border=True):
                # Gradient Header
                st.markdown(f"""
                    <div style="background: {fest['gradient']}; border-radius: 10px; padding: 14px 16px; color: white; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 600; opacity: 0.9;">
                            <span>{fest['edition']}</span>
                            <span>📍 {fest['campusArea']}</span>
                        </div>
                        <h3 style="margin: 6px 0 2px 0; font-size: 20px; font-weight: 800; color: white;">{fest['name']}</h3>
                        <div style="font-size: 12px; opacity: 0.95;">{fest['college']}</div>
                        <div style="margin-top: 8px; font-size: 11px; opacity: 0.85;">📅 {fest['dates']} ({fest['daysCount']} Days)</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Crowd & Campus Vibe Tag
                st.markdown(f"✨ **Vibe:** *{fest['vibeTag']}*")
                
                # Standardized Decision Metrics Grid
                m1, m2, m3 = st.columns(3)
                m1.metric("Verified Reach", f"{fest['footfall']:,}")
                m2.metric("Starting Package", f"₹{fest['startingPackage']:,}")
                m3.metric("CPM (Cost/1k)", f"₹{fest['cpm']:,}")
                
                # Supported Activations Chips
                goals_html = " ".join([f"<span class='badge-tag'>{g}</span>" for g in fest['supportedGoals']])
                st.markdown(f"<div style='margin-bottom: 10px;'>{goals_html}</div>", unsafe_allow_html=True)
                
                # F&B Specs Expander
                with st.expander("🔍 View F&B Logistics & Power Specs"):
                    st.write(f"**Campus Profile:** {fest['description']}")
                    st.write(f"⚡ **Chiller/Freezer Power:** {fest['specs']['chillerPower']}")
                    st.write(f"⛺ **Stall Dimensions:** {fest['specs']['stallDimensions']}")
                    st.write(f"🥤 **Sampling Permissions:** {fest['specs']['samplingPermissions']}")
                    st.write(f"⏰ **Peak Consumption Rush:** {fest['specs']['peakHours']}")
                    st.write(f"👥 **Demographics:** {fest['specs']['demographics']}")
                    st.write(f"🏷️ **Past F&B Brands:** {fest['specs']['pastBrands']}")
                    st.info(f"💡 **Brand Fit Verdict:** {fest['specs']['verdict']}")
                
                # Shortlist Button Action
                btn_label = "✅ Shortlisted (Click to Remove)" if is_in_shortlist else "➕ Add to Shortlist"
                btn_type = "secondary" if is_in_shortlist else "primary"
                
                if st.button(btn_label, key=f"btn_{fest['id']}", type=btn_type, use_container_width=True):
                    if is_in_shortlist:
                        st.session_state.shortlist.remove(fest["id"])
                        st.toast(f"Removed {fest['name']} from shortlist", icon="ℹ️")
                        st.rerun()
                    else:
                        if len(st.session_state.shortlist) >= 3:
                            st.toast("Shortlist limit reached! You can shortlist up to 3 festivals.", icon="⚠️")
                        else:
                            st.session_state.shortlist.append(fest["id"])
                            st.toast(f"Added {fest['name']} to shortlist ({len(st.session_state.shortlist)}/3)", icon="✅")
                            st.rerun()

# ================= TAB 2: COMPARE =================
with tab_compare:
    if shortlist_count == 0:
        st.info("Your shortlist is currently empty. Go to the 'Discover Fests' tab and click '+ Add to Shortlist' on up to 3 festivals.")
    else:
        st.markdown(f"### Side-by-Side Comparison ({shortlist_count} of 3 Selected)")
        
        # Build Comparison DataFrame
        compare_data = {
            "Decision Metric": [
                "College & City",
                "Verified Student Reach",
                "Starting Package (₹)",
                "Cost per 1,000 Students (CPM)",
                "Dates & Days",
                "Campus Vibe",
                "Chiller & Freezer Power",
                "Sampling Permissions",
                "Peak Consumption Hours",
                "Student Demographics",
                "Past F&B Brands",
                "Best Brand Fit Verdict"
            ]
        }
        
        for f in shortlisted_fests:
            compare_data[f["name"]] = [
                f"{f['college']} ({f['city']})",
                f"{f['footfall']:,} Students",
                f"₹{f['startingPackage']:,}",
                f"₹{f['cpm']:,} / 1k students",
                f"{f['dates']} ({f['daysCount']} Days)",
                f["vibeTag"],
                f["specs"]["chillerPower"],
                f["specs"]["samplingPermissions"],
                f["specs"]["peakHours"],
                f["specs"]["demographics"],
                f["specs"]["pastBrands"],
                f["specs"]["verdict"]
            ]
        
        df_compare = pd.DataFrame(compare_data)
        st.dataframe(df_compare, use_container_width=True, hide_index=True)
        
        # Quick remove buttons
        st.markdown("##### Manage Shortlist:")
        rm_cols = st.columns(3)
        for i, f in enumerate(shortlisted_fests):
            with rm_cols[i]:
                if st.button(f"🗑️ Remove {f['name']}", key=f"rm_cmp_{f['id']}", use_container_width=True):
                    st.session_state.shortlist.remove(f["id"])
                    st.rerun()

# ================= TAB 3: PITCH BOOKING =================
with tab_pitch:
    if shortlist_count == 0:
        st.warning("Please shortlist at least 1 festival first to schedule a pitch call.")
    else:
        st.markdown("### 📞 Schedule Sponsorship Pitch Call")
        st.write(f"Connecting with student sponsorship heads for: **{' + '.join([f['name'] for f in shortlisted_fests])}**")
        st.info(f"Combined Audience Reach: **{sum(f['footfall'] for f in shortlisted_fests):,} Students** | Total Starting Budget: **₹{sum(f['startingPackage'] for f in shortlisted_fests):,}**")
        
        with st.form("pitch_booking_form"):
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                brand_name = st.text_input("Brand Name *", placeholder="e.g. Svami / Lahori Zeera / CoolBite")
                contact_name = st.text_input("Marketing Contact Name *", placeholder="e.g. Ananya Sharma")
                contact_email = st.text_input("Work Email *", placeholder="ananya@brand.in")
            with col_b2:
                brand_category = st.selectbox(
                    "F&B Product Category *",
                    [
                        "Cold RTD Beverage / Energy Drinks",
                        "Healthy Chips / Gourmet Snacks",
                        "Quick Service Food (QSR) / Rolls / Burgers",
                        "Artisanal Coffee & Tea",
                        "Desserts / Bakery / Confectionery",
                        "Nutrition / Protein Bars"
                    ]
                )
                preferred_slot = st.selectbox(
                    "Preferred 15-Minute Pitch Slot *",
                    [
                        "Tomorrow 11:30 AM IST",
                        "Tomorrow 3:00 PM IST",
                        "Tomorrow 5:30 PM IST",
                        "Day After Tomorrow 11:00 AM IST",
                        "Day After Tomorrow 4:00 PM IST",
                        "Immediate Call (Next 2 Hours)"
                    ]
                )
                contact_phone = st.text_input("Phone / WhatsApp (Optional)", placeholder="+91 98765 43210")
            
            special_notes = st.text_area(
                "F&B Logistics Requirements / Special Notes",
                placeholder="e.g. Need 15A power socket for deep freeze chillers + 4 student sampling promoter passes..."
            )
            
            submitted = st.form_submit_button("🚀 Submit Pitch Call Request", type="primary", use_container_width=True)
            
            if submitted:
                if not brand_name or not contact_name or not contact_email:
                    st.error("Please fill in Brand Name, Contact Name, and Work Email.")
                elif "@" not in contact_email or "." not in contact_email:
                    st.error("Please enter a valid work email address.")
                else:
                    ref_code = f"#FEST-PITCH-2026-{random.randint(1000, 9999)}"
                    st.session_state.booking_confirmed = {
                        "ref_code": ref_code,
                        "brand_name": brand_name,
                        "brand_category": brand_category,
                        "contact_name": contact_name,
                        "contact_email": contact_email,
                        "preferred_slot": preferred_slot,
                        "fests": [f["name"] for f in shortlisted_fests],
                        "total_reach": sum(f["footfall"] for f in shortlisted_fests),
                        "total_budget": sum(f["startingPackage"] for f in shortlisted_fests),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.rerun()

    # --- CONFIRMATION STATE VIEW ---
    if st.session_state.booking_confirmed:
        b = st.session_state.booking_confirmed
        st.success(f"🎉 Pitch Call Confirmed! Booking Reference: **{b['ref_code']}**")
        
        with st.container(border=True):
            st.markdown(f"""
                ### 📋 Booking Summary
                - **Booking Reference:** `{b['ref_code']}`
                - **Brand:** **{b['brand_name']}** ({b['brand_category']})
                - **Contact:** **{b['contact_name']}** ({b['contact_email']})
                - **Scheduled Pitch Slot:** **{b['preferred_slot']}**
                - **Shortlisted Festivals:** **{' • '.join(b['fests'])}**
                - **Estimated Reach:** **{b['total_reach']:,} Students**
                - **Total Starting Budget:** **₹{b['total_budget']:,}**
            """)
            
            st.markdown("""
                ##### What happens next:
                1. 📄 Official festival deck & stall layouts dispatched to your email.
                2. 🤝 Fest corporate relations POC connects within 4 hours with Google Meet invite.
                3. ⚡ Finalize chiller electricity load, sampling perimeter, and student promoter passes.
            """)
            
            # Download Campaign Brief
            brief_text = f"""=================================================================
FESTMATCH F&B - CAMPUS SPONSORSHIP CAMPAIGN BRIEF
=================================================================
Reference ID:    {b['ref_code']}
Brand Name:      {b['brand_name']}
Contact Person:  {b['contact_name']} ({b['contact_email']})
Scheduled Slot:  {b['preferred_slot']}
Created At:      {b['timestamp']}

Total Reach:     {b['total_reach']:,} Verified Students
Total Budget:    ₹{b['total_budget']:,}
Shortlisted:     {' • '.join(b['fests'])}
=================================================================
Generated via FestMatch F&B Engine
"""
            st.download_button(
                label="📥 Download Campaign Brief (.txt)",
                data=brief_text,
                file_name=f"FestMatch_Brief_{b['ref_code'].replace('#', '')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            if st.button("Explore More Festivals", use_container_width=True):
                st.session_state.booking_confirmed = None
                st.rerun()
