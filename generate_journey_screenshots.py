"""
Captures screenshots of all key user journey states in FestMatch F&B:
1. Floating Shortlist Dock & Aggregate Bar
2. Side-by-Side Comparison Matrix Modal
3. Fest Detail & Logistics Specs Modal
4. Pitch Booking Form Modal
5. Booking Confirmation State
"""

import subprocess
import time
import threading
import http.server
import socketserver
import os
import json
import urllib.request

PORT = 8095
Handler = http.server.SimpleHTTPRequestHandler

def start_server():
    with socketserver.TCPServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()

t = threading.Thread(target=start_server, daemon=True)
t.start()
time.sleep(1)

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# We can create a lightweight helper HTML or use Chrome DevTools Protocol to trigger JS.
# Even simpler: create a test runner page `preview_states.html` that can mount any state on load!
test_html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=index.html">
</head>
<body></body>
</html>
"""

# Let's write small test triggers into an auxiliary script test_interactions.js that will be loaded if present
test_interactions_js = """
// Auto-triggers for visual verification
window.addEventListener('load', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const mode = urlParams.get('mode');

  if (mode === 'shortlist_dock') {
    window.toggleShortlist('mood_indigo_iitb');
    window.toggleShortlist('malhar_xaviers');
  } else if (mode === 'comparison_matrix') {
    window.toggleShortlist('mood_indigo_iitb');
    window.toggleShortlist('malhar_xaviers');
    window.toggleShortlist('cul_ah_mcc');
    setTimeout(() => {
      window.openComparisonModal();
    }, 200);
  } else if (mode === 'fnb_specs') {
    setTimeout(() => {
      window.openFestDetailModal('mood_indigo_iitb');
    }, 200);
  } else if (mode === 'pitch_form') {
    window.toggleShortlist('mood_indigo_iitb');
    window.toggleShortlist('malhar_xaviers');
    setTimeout(() => {
      window.openPitchCallModal();
    }, 200);
  } else if (mode === 'pitch_confirmed') {
    window.toggleShortlist('mood_indigo_iitb');
    window.toggleShortlist('malhar_xaviers');
    setTimeout(() => {
      window.openPitchCallModal();
      document.getElementById('brandNameInput').value = 'Volt Sparks Energy';
      document.getElementById('contactNameInput').value = 'Rohan Mehra';
      document.getElementById('contactEmailInput').value = 'rohan@voltsparks.in';
      document.getElementById('contactPhoneInput').value = '+91 98200 12345';
      const fakeEvent = { preventDefault: () => {} };
      window.handlePitchFormSubmit(fakeEvent);
    }, 200);
  }
});
"""

with open("test_interactions.js", "w", encoding="utf-8") as f:
    f.write(test_interactions_js)

# Inject script tag into index.html if not already present
with open("index.html", "r", encoding="utf-8") as f:
    index_content = f.read()

if "test_interactions.js" not in index_content:
    index_content = index_content.replace(
        '<script src="app.js"></script>',
        '<script src="app.js"></script>\n  <script src="test_interactions.js"></script>'
    )
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

modes = [
    ("shortlist_dock", "screenshot_shortlist_dock.png", 1280, 1000),
    ("comparison_matrix", "screenshot_comparison_matrix.png", 1280, 950),
    ("fnb_specs", "screenshot_fnb_specs.png", 1280, 950),
    ("pitch_form", "screenshot_pitch_form.png", 1280, 900),
    ("pitch_confirmed", "screenshot_pitch_confirmed.png", 1280, 950),
]

for mode, filename, width, height in modes:
    sc_path = os.path.abspath(filename)
    url = f"http://localhost:{PORT}/index.html?mode={mode}"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=3500",
        f"--window-size={width},{height}",
        f"--screenshot={sc_path}",
        url
    ]
    subprocess.run(cmd, timeout=12)
    print(f"Captured {filename}: {os.path.exists(sc_path)} ({os.path.getsize(sc_path) if os.path.exists(sc_path) else 0} bytes)")

print("All screenshots generated successfully.")
