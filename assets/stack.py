"""Painel animado do stack: cada área é uma constelação, cada ferramenta uma estrela.

SVG escrito à mão (não matplotlib) para poder animar com CSS dentro do <img> do GitHub:
estrelas cintilam e as linhas das constelações se traçam. Texto em STIX convertido em
curvas com matplotlib.textpath, para ficar igual ao header. Mesma paleta do header
(bico de pena em negativo, esteves-layout). Respeita prefers-reduced-motion.

    python stack.py            -> assets/stack.svg
"""
import pathlib

import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from matplotlib.textpath import TextPath

OUT = pathlib.Path(__file__).resolve().parent / "stack.svg"
FUNDO, TINTA, TINTA2 = "#0D1117", "#D9DEE3", "#9AA5B1"
CEU, AREIA, ROSA = "#56BDF0", "#DEC545", "#E0607A"

# unidades: 1 mm = 10 u (mesma largura de 170 mm do header)
W, H = 1700, 1000
SERIF = FontProperties(family="STIXGeneral")
SERIF_I = FontProperties(family="STIXGeneral", style="italic")
PT = 10 * 25.4 / 72          # 1 pt em unidades

# Levantado dos projetos (requirements, package.json, ambientes conda/venv, imports):
# PRISMA, DESTEV, VVV_EXCESS_CATALOG, HMXB_IR_VAR, SOAR_2027A_DIPPERS, GAIA_BINARY,
# DEBRIS-KMOS, PHOEBE/HW Vir, Planetário 2026 (apresenta-es), vídeo da SIC.
# O primeiro item de cada grupo é a estrela principal (4 pontas).
GRUPOS = [
    ("Astronomy", "surveys, photometry, inference", CEU, [
        "Astropy", "Astroquery · PyVO", "Photutils", "Lightkurve", "PHOEBE",
        "emcee · dynesty", "healpy", "ESO EDPS", "dust_extinction"]),
    ("Data & ML", "catalogues at scale", AREIA, [
        "NumPy · SciPy", "pandas", "Polars · PyArrow", "Dask", "Numba",
        "scikit-learn", "XGBoost", "Matplotlib", "Jupyter"]),
    ("Web & apps", "full-stack products", ROSA, [
        "FastAPI", "SQLAlchemy · Alembic", "PostgreSQL", "Next.js · React", "TypeScript",
        "Vite", "D3 · GSAP", "Remotion", "pywebview"]),
    ("Dev tools", "tests, delivery, writing", TINTA, [
        "Docker Compose", "pytest", "Playwright", "Selenium", "PyInstaller",
        "Git · GitHub", "WSL · conda", "PowerShell", "LaTeX"]),
]


def texto(s, x, y, size_pt, cor, ha="left", prop=SERIF, extra=""):
    """Texto -> <path> (y para baixo; baseline em y)."""
    tp = TextPath((0, 0), s, size=size_pt * PT, prop=prop)
    ext = tp.get_extents(); w = ext.x1
    dx = {"left": 0, "center": -w / 2, "right": -w}[ha]
    CAIXAS.append((x + dx - 10, y - ext.y1 - 10, x + dx + w + 10, y - ext.y0 + 10))
    d, i = [], 0
    for verts, code in tp.iter_segments(curves=True, simplify=False):
        pts = verts.reshape(-1, 2)
        pts = [(x + dx + px, y - py) for px, py in pts]
        cmd = {Path.MOVETO: "M", Path.LINETO: "L", Path.CURVE3: "Q", Path.CURVE4: "C",
               Path.CLOSEPOLY: "Z"}[code]
        d.append(cmd if cmd == "Z" else cmd + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts))
    return f'<path d="{"".join(d)}" fill="{cor}"{extra}/>'


CAIXAS = []      # áreas de texto e marcadores: o céu de fundo não entra nelas


def estrela4(x, y, R, cor, k=0.26):
    t = np.arange(8) * np.pi / 4 - np.pi / 2
    r = np.where(np.arange(8) % 2 == 0, R, k * R)
    return " ".join(f"{x + a:.1f},{y + b:.1f}" for a, b in zip(r * np.cos(t), r * np.sin(t)))


rng = np.random.default_rng(2026)
el = []

# moldura
el.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="8" fill="{FUNDO}" '
          f'stroke="{TINTA2}" stroke-width="1.8"/>')

# título do painel
el.append(texto("Toolkit", 60, 95, 13, TINTA))
el.append(texto("tools I use across research and software projects, drawn as constellations",
                60, 140, 7.0, TINTA2, prop=SERIF_I))

# constelações
CW = (W - 120) / 4
dy = 74
for g, (nome, sub, cor, itens) in enumerate(GRUPOS):
    x0 = 60 + g * CW
    el.append(texto(nome, x0 + 10, 215, 8.5, cor))
    el.append(texto(sub, x0 + 10, 250, 6.3, TINTA2, prop=SERIF_I))
    # posições: corrente em zigue-zague, deslocamentos suaves
    xs = x0 + 34 + 26 * np.sin(np.arange(len(itens)) * 1.7 + g) + rng.uniform(-6, 6, len(itens))
    ys = 300 + dy * np.arange(len(itens)) + rng.uniform(-8, 8, len(itens))
    # linhas da constelação (traçadas pela animação)
    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in zip(xs, ys))
    comp = float(np.sum(np.hypot(np.diff(xs), np.diff(ys)))) + 10
    el.append(f'<polyline points="{pts}" fill="none" stroke="{cor}" stroke-opacity="0.55" '
              f'stroke-width="1.6" stroke-linecap="round" class="draw" '
              f'style="stroke-dasharray:{comp:.0f};stroke-dashoffset:{comp:.0f};'
              f'animation-delay:{0.3 + 0.5*g:.1f}s"/>')
    for i, (x, y, s) in enumerate(zip(xs, ys, itens)):
        atraso = f"animation-delay:{(i * 0.7 + g * 1.3) % 5:.1f}s"
        if i == 0:
            el.append(f'<polygon points="{estrela4(x, y, 15, cor)}" fill="{cor}" '
                      f'fill-opacity="0.85" class="tw" style="{atraso}"/>')
        else:
            el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{cor}" fill-opacity="0.85" '
                      f'class="tw" style="{atraso}"/>')
        el.append(texto(s, x + 22, y + 8, 8.0 if i == 0 else 7.6, TINTA))
        CAIXAS.append((x - 22, y - 22, x + 22, y + 22))

# céu de fundo: estrelas finas fora dos textos e marcadores, algumas cintilando
fundo, k = [], 0
while len(fundo) < 230:
    x, y = rng.uniform(20, W - 20), rng.uniform(20, H - 20)
    k += 1
    if any(a < x < c and b < y < d for a, b, c, d in CAIXAS):
        continue
    r = np.clip(rng.exponential(1.1), 0.5, 3.0)
    cls = f' class="tw t{k % 6}"' if len(fundo) % 4 == 0 else ""
    fundo.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{TINTA}" '
                 f'opacity="{0.25 + 0.12*r:.2f}"{cls}/>')
el[1:1] = fundo

# rodapé: linguagens
el.append(texto("Python  ·  TypeScript  ·  SQL  ·  LaTeX  ·  Shell / PowerShell",
                W / 2, H - 38, 7.2, TINTA2, ha="center"))

css = """
.tw{animation:tw 4.5s ease-in-out infinite}
.t0{animation-delay:0s}.t1{animation-delay:.8s}.t2{animation-delay:1.6s}
.t3{animation-delay:2.4s}.t4{animation-delay:3.2s}.t5{animation-delay:4s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.25}}
.draw{animation:draw 2.4s ease-out forwards}
@keyframes draw{to{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){.tw{animation:none}.draw{animation:none;stroke-dashoffset:0!important}}
"""
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'role="img" aria-labelledby="t d"><title id="t">Toolkit</title>'
       f'<desc id="d">Tools grouped as four constellations: astronomy, data and ML, web and apps, '
       f'dev tools.</desc><style>{css}</style>' + "".join(el) + "</svg>")
OUT.write_text(svg, encoding="utf-8")
print("ok", OUT.stat().st_size // 1024, "KB")
