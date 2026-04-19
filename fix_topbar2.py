"""
fix_topbar2.py — Run from your IT-Projects-Portfolio repo root.
Replaces the old simple back-button topbar with the branded homepage topbar.
"""

import re
from pathlib import Path

PROJECT_PAGES = [
    "m365-tenant.html",
    "vlan-design.html",
    "virtual-ad-vpn.html",
    "dns-portfolio.html",
]

NEW_TOPBAR = """<header class="topbar">
  <div class="topbar-brand">
    <span class="prompt">$</span>
    <span>aayush-acharya</span>
    <span class="cursor"></span>
  </div>
  <nav class="topbar-nav">
    <a href="index.html">&#8592; Home</a>
    <a href="index.html#projects">Projects</a>
    <a href="index.html#skills">Skills</a>
    <a href="https://aayushacharya.com.au" target="_blank">Portfolio &#8599;</a>
    <a href="mailto:aayush@aayush.com.au">Contact</a>
  </nav>
</header>"""

def patch(path: Path):
    html = path.read_text(encoding="utf-8")

    # Match the old simple topbar div (any breadcrumb text)
    new_html, n = re.subn(
        r'<div class="topbar">.*?</div>',
        NEW_TOPBAR,
        html,
        count=1,
        flags=re.DOTALL
    )

    if n == 0:
        print(f"  ⚠️  Pattern not found in {path.name} — skipping.")
        return

    path.write_text(new_html, encoding="utf-8")
    print(f"  ✅  Fixed: {path.name}")

if __name__ == "__main__":
    repo = Path(__file__).parent
    print(f"Running in: {repo}\n")
    for f in PROJECT_PAGES:
        p = repo / f
        if p.exists():
            patch(p)
        else:
            print(f"  ❌  Not found: {f}")

    print("\nDone. Run: git add . && git commit -m 'Fix topbar on project pages' && git push")
