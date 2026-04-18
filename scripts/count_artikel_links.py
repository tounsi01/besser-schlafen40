import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "artikel"
for f in sorted(p.glob("*.html")):
    if f.name.startswith("_"):
        continue
    t = f.read_text(encoding="utf-8")
    n = len(re.findall(r'href="/artikel/[^"]+"', t))
    if n < 10:
        print(f"{n:3d}  {f.name}")
