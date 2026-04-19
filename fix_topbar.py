"""
fix_topbar.py — Run from your IT-Projects-Portfolio repo root.
Injects the matching homepage topbar into all project pages
and adds the required CSS for it.
"""

import re
from pathlib import Path

PROJECT_PAGES = {
    "m365-tenant.html":   {"num": "Project 01", "label": "Cloud & Identity"},
    "vlan-design.html":   {"num": "Project 02", "label": "Network Design"},
    "virtual-ad-vpn.html":{"num": "Project 03", "label": "Azure & Active Directory"},
    "dns-portfolio.html": {"num": "Project 04", "label": "DNS & Web Infrastructure"},
}

# ── Topbar CSS to inject (matches index.html exactly) ─────────────────────────
TOPBAR_CSS = """
  /* ── Injected shared topbar styles ── */
  .topbar {
    background: #111620;
    border-bottom: 1px solid #1e2a3a;
    padding: 0 2rem;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 50;
  }
  .topbar-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #7a8fa8;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .topbar-brand .prompt { color: #00e676; }
  .tb-cursor {
    display: inline-block;
    width: 7px; height: 14px;
    background: #00e676;
    animation: tblink 1.1s step-end infinite;
    vertical-align: middle;
    margin-left: 1px;
  }
  @keyframes tblink { 50% { opacity: 0; } }
  .topbar-nav { display: flex; gap: 20px; align-items: center; }
  .topbar-nav a {
    font-size: 13px;
    color: #7a8fa8;
    font-family: 'JetBrains Mono', monospace;
    text-decoration: none;
    transition: color .15s;
  }
  .topbar-nav a:hover { color: #00e676; }
"""

# ── Topbar HTML template ───────────────────────────────────────────────────────
def make_topbar(num):
    return f"""
<header class="topbar">
  <div class="topbar-brand">
    <span class="prompt">$</span>
    <span>aayush-acharya</span>
    <span class="tb-cursor"></span>
  </div>
  <nav class="topbar-nav">
    <a href="index.html">&#8592; Home</a>
    <a href="index.html#projects">Projects</a>
    <a href="index.html#skills">Skills</a>
    <a href="https://aayushacharya.com.au" target="_blank">Portfolio &#8599;</a>
    <a href="mailto:aayush@aayush.com.au">Contact</a>
  </nav>
</header>"""

def patch_file(path: Path, meta: dict):
    html = path.read_text(encoding="utf-8")

    # 1. Inject topbar CSS into the existing <style> block
    if TOPBAR_CSS.strip() not in html:
        html = re.sub(
            r'(<style>)',
            r'\1' + TOPBAR_CSS,
            html,
            count=1
        )
        print(f"  ✅  CSS injected: {path.name}")
    else:
        print(f"  ⏭️   CSS already present: {path.name}")

    # 2. Remove the old bare back-link / breadcrumb header if present
    #    (Targets common patterns from the original build)
    html = re.sub(
        r'<div[^>]*class="[^"]*page-header[^"]*"[^>]*>.*?</div>\s*',
        '',
        html,
        flags=re.DOTALL
    )
    # Also remove standalone back/breadcrumb bars (the simple flex header)
    html = re.sub(
        r'<div[^>]*style="[^"]*display:\s*flex[^"]*justify-content:\s*space-between[^"]*"[^>]*>\s*<a[^>]*>.*?Back.*?</a>.*?</div>\s*',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 3. Inject topbar right after <body>
    topbar_html = make_topbar(meta["num"])
    if 'class="topbar"' not in html:
        html = re.sub(
            r'(<body[^>]*>)',
            r'\1' + topbar_html,
            html,
            count=1
        )
        print(f"  ✅  Topbar injected: {path.name}")
    else:
        print(f"  ⏭️   Topbar already present: {path.name}")

    path.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    repo = Path(__file__).parent
    print(f"Running in: {repo}\n")

    for filename, meta in PROJECT_PAGES.items():
        p = repo / filename
        if not p.exists():
            print(f"  ❌  Not found: {filename}")
            continue
        print(f"\n→ {filename}")
        patch_file(p, meta)

    print("\n✅ Done. Review in browser, then: git add . && git commit -m 'Add matching topbar to project pages' && git push")
