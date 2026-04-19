"""
fix_theme.py — Run from your IT-Projects-Portfolio repo root.
Replaces the inline <style> block in each project page with a
link to the shared styles.css, keeping everything else intact.
"""

import re
from pathlib import Path

PROJECT_PAGES = [
    "m365-tenant.html",
    "vlan-design.html",
    "virtual-ad-vpn.html",
    "dns-portfolio.html",
]

SHARED_CSS_LINK = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">\n'
    '  <link rel="stylesheet" href="styles.css">'
)

def patch_file(path: Path):
    html = path.read_text(encoding="utf-8")

    # Remove existing Google Fonts preconnect + link tags
    html = re.sub(
        r'\s*<link rel="preconnect"[^>]+>\s*',
        '\n',
        html
    )
    html = re.sub(
        r'\s*<link[^>]+fonts\.googleapis\.com[^>]+>\s*',
        '\n',
        html
    )

    # Replace inline <style>...</style> block with shared stylesheet link
    new_html, count = re.subn(
        r'\s*<style>.*?</style>',
        '\n' + SHARED_CSS_LINK,
        html,
        flags=re.DOTALL
    )

    if count == 0:
        print(f"  ⚠️  No <style> block found in {path.name} — skipping.")
        return

    path.write_text(new_html, encoding="utf-8")
    print(f"  ✅  Patched: {path.name}")

if __name__ == "__main__":
    repo = Path(__file__).parent
    print(f"Running in: {repo}\n")

    for filename in PROJECT_PAGES:
        p = repo / filename
        if not p.exists():
            print(f"  ❌  Not found: {filename}")
            continue
        patch_file(p)

    print("\nDone. Commit styles.css + all patched HTML files and push.")
