"""Header do perfil GitHub: prancha celeste em bico de pena, em negativo.

Gravura em traço claro sobre o fundo escuro do GitHub, paleta esteves-layout. Como o traço é
claro, a lógica de tom do bico de pena se inverte: a marca se adensa no lado ILUMINADO (alto à
esquerda) e a sombra fica vazia. Cor só como mancha chapada por baixo do traço.
Objetos: Lua gibosa com luz cinérea, planeta com anéis, cometa, galáxia espiral e aglomerado
aberto, sobre uma gratícula de carta celeste. Texto em STIX convertido em curvas.

    python header.py                      -> assets/header.svg
    PREVIEW=caminho.png python header.py  -> também um PNG de prévia (fora do repositório)
"""
import os
import pathlib
import sys

import numpy as np
import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon

sys.path.insert(0, r"C:/Users/estev/.claude/skills/esteves-bico-de-pena/assets")
import bico_de_pena as bp

FUNDO = "#0D1117"          # fundo escuro do GitHub
TINTA = "#D9DEE3"          # cinza claro do esteves-layout faz o papel da tinta
TINTA2 = "#9AA5B1"         # cinza: linhas de construção, texto secundário
CEU = "#56BDF0"; AREIA = "#DEC545"; ROSA = "#E0607A"

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIX Two Text", "STIXGeneral", "Times New Roman"],
    "mathtext.fontset": "stix",
    "svg.fonttype": "path",
    "svg.hashsalt": "pedroestevs",
})

OUT = pathlib.Path(__file__).resolve().parent
W, H = 170.0, 50.0
fig = plt.figure(figsize=(W / 25.4, H / 25.4), facecolor=FUNDO)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.set_aspect("equal"); ax.axis("off")

# em negativo, o ponto de concentração das marcas vai para o lado iluminado
bp.LIGHT = -bp.LIGHT


def T(x, y, s, size, ha="left", va="baseline", color=TINTA, **kw):
    ax.text(x, y, s, fontsize=size, ha=ha, va=va, color=color, zorder=30, **kw)


def arco(cx, cy, a, b, ang, t0, t1, n=200):
    t = np.linspace(t0, t1, n); c, s = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    x, y = a*np.cos(t), b*np.sin(t)
    return np.c_[cx + c*x - s*y, cy + s*x + c*y]


def linhas(segs, lw, alphas, cor=TINTA, z=6):
    cols = [to_rgba(cor, a) for a in alphas]
    ax.add_collection(LineCollection(segs, colors=cols, linewidths=lw, capstyle="round", zorder=z))


# ---------------------------------------------------------------- moldura e gratícula
ax.add_patch(FancyBboxPatch((0.6, 0.6), W - 1.2, H - 1.2,
                            boxstyle="round,pad=0,rounding_size=0.8",
                            facecolor=FUNDO, edgecolor=TINTA2, lw=0.5, zorder=0))
X0 = 70.0                                   # início da área celeste
gx0, gy0 = 118.0, 150.0                     # polo da gratícula, fora da prancha
for R in np.arange(112, 160, 12):
    p = arco(gx0, gy0, R, R, 0, np.deg2rad(-150), np.deg2rad(-30))
    m = (p[:, 0] > X0) & (p[:, 0] < W - 2) & (p[:, 1] > 2)
    ax.plot(p[m, 0], p[m, 1], color=TINTA2, lw=0.35, ls=(0, (0.5, 1.5)), alpha=0.45, zorder=1)
for ang in np.arange(-130, -45, 12):
    a = np.deg2rad(ang)
    r = np.linspace(110, 165, 50); p = np.c_[gx0 + r*np.cos(a), gy0 + r*np.sin(a)]
    m = (p[:, 0] > X0) & (p[:, 0] < W - 2) & (p[:, 1] > 2) & (p[:, 1] < H - 2)
    ax.plot(p[m, 0], p[m, 1], color=TINTA2, lw=0.35, ls=(0, (0.5, 1.5)), alpha=0.45, zorder=1)

# zonas ocupadas pelos objetos (estrelas de fundo não entram nelas)
OBJ = [(86, 24, 10.5), (120, 32, 12.0), (119, 9, 9.0), (153, 20, 10.5), (146, 41, 5.0)]


def livre(x, y, folga=0.6):
    return all(np.hypot(x - cx, y - cy) > rr + folga for cx, cy, rr in OBJ)


# ---------------------------------------------------------------- céu de fundo
rng = np.random.default_rng(42)
xs, ys = rng.uniform(X0, W - 3, 420), rng.uniform(2.5, H - 3, 420)
mag = rng.exponential(1.0, xs.size)
ok = np.array([livre(x, y) for x, y in zip(xs, ys)])
xs, ys, mag = xs[ok], ys[ok], mag[ok]
ax.scatter(xs, ys, s=np.clip(0.75 - 0.3*mag, 0.04, 0.75)**2 * 1.3, c=TINTA, linewidths=0,
           alpha=0.85, zorder=2)
# poucas estrelas brilhantes: disco com mancha areia + contorno fino
for (x, y, r) in [(74.5, 7.0, 0.8), (103.0, 6.0, 0.6), (101.5, 42.0, 0.75), (138.5, 23.5, 0.6),
                  (165.0, 36.0, 0.7), (79.0, 42.5, 0.55)]:
    ax.add_patch(Circle((x, y), r, facecolor=AREIA, alpha=0.5, edgecolor="none", zorder=3))
    ax.add_patch(Circle((x, y), r, facecolor="none", edgecolor=TINTA, lw=0.45, zorder=3))

# ---------------------------------------------------------------- Lua gibosa
mx, my, mr = 86.0, 24.0, 9.2
bp.esfera(ax, mx, my, mr, tinta=TINTA, cor=TINTA2, alpha=0.16, seed=5, z=5, detalhe=1.2)
# região na sombra (baixo-direita): apaga o traço e deixa só luz cinérea
t = np.linspace(-np.pi/2, np.pi/2, 160)
term = np.c_[np.cos(t)*0.35*mr, np.sin(t)*mr]           # terminador (elipse) visto de lado
limbo = np.c_[np.cos(t[::-1])*mr, np.sin(t[::-1])*mr]
ang = np.deg2rad(45)                                     # eixo luz -> sombra (y para baixo)
c, s = np.cos(ang), np.sin(ang)
rot = lambda P: np.c_[mx + c*P[:, 0] - s*P[:, 1], my + s*P[:, 0] + c*P[:, 1]]
sombra = rot(np.r_[term, limbo])
ax.add_patch(Polygon(sombra, closed=True, facecolor=FUNDO, edgecolor="none", zorder=7))
bp.pontilhado(ax, sombra, lambda x, y: np.full_like(x, 0.10), 900, np.random.default_rng(9),
              cor=TINTA2, tam=0.12, z=8)
# mares: manchas de pontilhado no lado iluminado
for (dx, dy, a, b, sd) in [(-2.5, -1.0, 2.6, 1.8, 1), (1.0, -4.2, 1.7, 1.2, 2), (-4.6, 3.2, 1.6, 1.1, 3)]:
    e = arco(mx + dx, my + dy, a, b, 25, 0, 2*np.pi, 60)
    bp.pontilhado(ax, e, lambda x, y: np.full_like(x, 0.55), 260, np.random.default_rng(sd),
                  cor=FUNDO, tam=0.3, z=8)
# crateras: parede iluminada é a do lado oposto à luz (baixo-direita)
for (dx, dy, rr) in [(-3.6, -4.6, 0.9), (-6.2, -0.4, 0.6), (-2.6, 1.6, 0.55), (-5.4, 3.4, 0.7),
                     (-5.0, -3.0, 0.4), (0.2, -6.4, 0.45)]:
    cx, cy = mx + dx, my + dy
    ax.add_patch(Ellipse((cx - 0.12*rr, cy - 0.12*rr), 2*rr, 1.7*rr, facecolor=FUNDO,
                         alpha=0.55, edgecolor="none", zorder=8))
    p = arco(cx, cy, rr, 0.85*rr, 0, np.deg2rad(-10), np.deg2rad(110))
    ax.plot(p[:, 0], p[:, 1], color=TINTA, lw=0.4, zorder=9)
# contorno: cheio no limbo iluminado, pontilhado no limbo escuro
lit = rot(np.c_[np.cos(t + np.pi)*mr, np.sin(t + np.pi)*mr])
ax.plot(lit[:, 0], lit[:, 1], color=TINTA, lw=0.7, zorder=10)
ax.plot(sombra[160:, 0], sombra[160:, 1], color=TINTA2, lw=0.45, ls=(0, (0.5, 1.2)), zorder=10)

# ---------------------------------------------------------------- planeta com anéis
px, py, pr, inc = 120.0, 32.0, 5.0, -16
k_b = 0.30
for a_, lw in [(8.6, 0.6), (10.6, 0.6), (9.5, 0.25)]:               # metade de trás
    p = arco(px, py, a_, a_*k_b, inc, np.pi, 2*np.pi)
    ax.plot(p[:, 0], p[:, 1], color=TINTA, lw=lw, zorder=4)
bp.esfera(ax, px, py, pr, tinta=TINTA, cor=AREIA, alpha=0.32, seed=8, z=5)
for off in (-2.4, -1.1, 1.5):                                          # faixas
    hw = pr*np.sqrt(max(0.05, 1 - (off/pr)**2))
    p = arco(px - off*np.sin(np.deg2rad(inc)), py + off*np.cos(np.deg2rad(inc)), hw, 0.7, inc,
             np.deg2rad(95), np.deg2rad(265))
    ax.plot(p[:, 0], p[:, 1], color=TINTA, lw=0.3, alpha=0.75, zorder=7)
outer = arco(px, py, 10.6, 10.6*k_b, inc, 0, np.pi)
inner = arco(px, py, 8.6, 8.6*k_b, inc, 0, np.pi)
band = np.r_[outer, inner[::-1]]
ax.add_patch(Polygon(band, closed=True, facecolor=FUNDO, edgecolor="none", zorder=10))
bp.mancha(ax, band, AREIA, 0.16, z=10)
for i, a_ in enumerate(np.linspace(8.85, 10.35, 6)):                  # hachura do anel
    p = arco(px, py, a_, a_*k_b, inc, np.deg2rad(35), np.deg2rad(180))
    ax.plot(p[:, 0], p[:, 1], color=TINTA, lw=0.26 if i != 3 else 0.12, zorder=11)
for a_ in (8.6, 10.6):
    p = arco(px, py, a_, a_*k_b, inc, 0, np.pi)
    ax.plot(p[:, 0], p[:, 1], color=TINTA, lw=0.6, zorder=11)

# ---------------------------------------------------------------- cometa
hx, hy = 126.0, 11.0
u = np.array([-1.0, -0.22]); u /= np.linalg.norm(u)        # cauda: longe do Sol (fora, à direita)
nrm = np.array([-u[1], u[0]])
rng = np.random.default_rng(12)
segs, al = [], []
for k in range(26):
    off = rng.normal(0, 0.35)
    L = rng.uniform(7, 15) * (1 - 0.5*abs(off))
    curv = 0.018 + rng.normal(0, 0.006)
    s_ = np.linspace(0.6, L, 60)
    pts = (np.array([hx, hy]) + np.outer(s_, u)
           + np.outer(off*(0.6 + 0.10*s_) + curv*s_**2, nrm))
    a_ = np.clip(0.9 - s_/L, 0.05, 0.9)
    for j in range(len(pts) - 1):
        segs.append(pts[j:j+2]); al.append(a_[j])
linhas(segs, 0.25, al, z=6)
coma = bp.circulo(hx, hy, 1.6)
bp.pontilhado(ax, coma, lambda x, y: np.clip(1 - np.hypot(x-hx, y-hy)/1.6, 0, 1), 500,
              np.random.default_rng(4), cor=TINTA, tam=0.2, z=7)
ax.add_patch(Circle((hx, hy), 0.5, facecolor=CEU, alpha=0.6, edgecolor=TINTA, lw=0.45, zorder=8))

# ---------------------------------------------------------------- galáxia espiral
gx, gy, ga, gb, gang = 153.0, 20.0, 10.5, 4.6, -24
rng = np.random.default_rng(7)
pts = []
tmax = 3.4*np.pi/2*1.5
for braco in (0, np.pi):
    th = rng.uniform(0.3, tmax, 2400)
    rr = 0.9*np.exp(0.34*th) / np.exp(0.34*tmax)
    rr = rr + rng.normal(0, 0.03 + 0.05*rr, th.size)
    pts.append(np.c_[rr*np.cos(th + braco), rr*np.sin(th + braco)])
P = np.r_[np.vstack(pts), rng.normal(0, 0.10, (1200, 2))]
d = np.hypot(P[:, 0], P[:, 1]); P = P[d < 1.02]; d = d[d < 1.02]
c, s = np.cos(np.deg2rad(gang)), np.sin(np.deg2rad(gang))
X = gx + c*P[:, 0]*ga - s*P[:, 1]*gb
Y = gy + s*P[:, 0]*ga + c*P[:, 1]*gb
keep = rng.uniform(size=d.size) < np.clip(1.1 - d, 0.2, 1)
ax.scatter(X[keep], Y[keep], s=0.18, c=TINTA, linewidths=0, zorder=5)
ax.add_patch(Ellipse((gx, gy), 2.0, 1.0, angle=gang, facecolor=AREIA, alpha=0.5,
                     edgecolor="none", zorder=4))
# nódulos rosa (regiões de formação estelar) ao longo dos braços
for i in rng.choice(len(pts[0]), 7, replace=False):
    q = pts[i % 2][i]
    if 0.35 < np.hypot(*q) < 0.85:
        ax.add_patch(Circle((gx + c*q[0]*ga - s*q[1]*gb, gy + s*q[0]*ga + c*q[1]*gb), 0.28,
                            facecolor=ROSA, alpha=0.55, edgecolor="none", zorder=4))

# ---------------------------------------------------------------- aglomerado aberto
cx, cy = 146.0, 41.0
# nebulosidade de reflexão: pontilhado céu que rareia para fora
neb = arco(cx, cy, 5.5, 3.6, -10, 0, 2*np.pi, 80)
bp.pontilhado(ax, neb, lambda x, y: 0.5*np.exp(-((x-cx)/3.2)**2 - ((y-cy)/2.1)**2), 1400,
              np.random.default_rng(30), cor=CEU, tam=0.14, z=4)
# estrelas brilhantes do aglomerado (posições fixas, sem sobreposição) + membros fracos
for (dx, dy) in [(-2.2, -1.0), (0.6, -1.8), (1.6, 0.2), (-0.6, 1.0), (3.4, -0.9), (-3.4, 1.4)]:
    ax.add_patch(Circle((cx + dx, cy + dy), 0.42, facecolor=CEU, alpha=0.6, edgecolor="none", zorder=5))
    ax.add_patch(Circle((cx + dx, cy + dy), 0.42, facecolor="none", edgecolor=TINTA, lw=0.4, zorder=6))
rng = np.random.default_rng(31)
for k in range(18):
    r = abs(rng.normal(0, 2.4)); th = rng.uniform(0, 2*np.pi)
    ax.add_patch(Circle((cx + 1.3*r*np.cos(th), cy + 0.8*r*np.sin(th)), rng.uniform(0.1, 0.2),
                        facecolor=TINTA, edgecolor="none", zorder=5))

# ---------------------------------------------------------------- bloco de texto
x0 = 9.0
T(x0, 21.0, "Pedro Esteves", 25)
ax.plot([x0, x0 + 52], [25.2, 25.2], color=TINTA2, lw=0.5)
T(x0, 31.0, "Physics  ·  Astrophysics  ·  Scientific computing", 7.5, color=CEU)
T(x0, 36.4, "Federal University of Santa Catarina (UFSC), Brazil", 6.8,
  color=TINTA2, style="italic")
ys = 42.5
ax.plot([x0, x0 + 52], [ys, ys], color=TINTA2, lw=0.45, alpha=0.7)
for k, xx in enumerate(np.linspace(x0, x0 + 52, 14)):
    ax.plot([xx, xx], [ys, ys - (1.3 if k % 4 == 0 else 0.7)], color=TINTA2, lw=0.45, alpha=0.7)

fig.savefig(OUT / "header.svg", facecolor=FUNDO, metadata={"Date": None})
if os.environ.get("PREVIEW"):
    fig.savefig(os.environ["PREVIEW"], dpi=400, facecolor=FUNDO)
print("ok")
