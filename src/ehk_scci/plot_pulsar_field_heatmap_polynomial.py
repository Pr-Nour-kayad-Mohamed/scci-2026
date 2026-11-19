import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

CSV = "pulsar_field_sweep_polynomial_results.csv"
PNG = "pulsar_field_sensitivity_heatmap_polynomial.png"
SEUIL = 1.0e-13

with open(CSV, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

etas = sorted({round(float(r["eta"]), 8) for r in rows})
phis = sorted({round(float(r["phi0"]), 8) for r in rows})

ei = {v: i for i, v in enumerate(etas)}
pi = {v: i for i, v in enumerate(phis)}

Z = np.full((len(phis), len(etas)), np.nan)
excl = np.zeros(Z.shape, dtype=bool)
jauge = np.zeros(Z.shape, dtype=bool)
couplage = np.zeros(Z.shape, dtype=bool)

for r in rows:
    e = round(float(r["eta"]), 8)
    p = round(float(r["phi0"]), 8)
    i, j = pi[p], ei[e]
    s = r["status"]

    if s == "hors_domaine_perturbatif":
        jauge[i, j] = True
        excl[i, j] = True
    elif s == "couplage_non_perturbatif":
        couplage[i, j] = True
        excl[i, j] = True
    else:
        Z[i, j] = max(abs(float(r["dP_dt_dipole"])), 1e-30)

E, P = np.meshgrid(etas, phis)
Zm = np.ma.masked_array(Z, mask=excl)

fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

vals = Z[~excl & np.isfinite(Z)]
norm = LogNorm(vmin=vals.min(), vmax=vals.max())

cf = ax.contourf(
    E, P, Zm,
    levels=np.logspace(np.log10(vals.min()), np.log10(vals.max()), 24),
    norm=norm,
    cmap="viridis",
    extend="both"
)

cbar = fig.colorbar(cf, ax=ax, pad=0.02)
cbar.set_label(r"$|\dot P_b^{\mathrm{dip}}|$ (s/s)")

try:
    cs = ax.contour(
        E, P, Zm,
        levels=[SEUIL],
        colors=["cyan"],
        linewidths=2,
        linestyles="--"
    )
    ax.clabel(cs, inline=True, fontsize=8, fmt=r"$10^{-13}$ s/s")
except Exception:
    pass

if jauge.any():
    ax.pcolormesh(
        E, P,
        np.ma.masked_less(jauge.astype(float), 0.5),
        cmap="Greys",
        alpha=0.35,
        shading="auto"
    )

if couplage.any():
    ax.pcolormesh(
        E, P,
        np.ma.masked_less(couplage.astype(float), 0.5),
        cmap="Reds",
        alpha=0.35,
        shading="auto"
    )

ax.set_xscale("log")
ax.set_xlabel(r"$\eta$")
ax.set_ylabel(r"$\phi_0$")
ax.set_title(
    "Branche polynomiale\n"
    r"Domaine doublement perturbatif : "
    r"$\eta\Phi_{\max}^2\leq0.1$, $|\Delta\alpha|\leq0.1$"
)

fig.text(
    0.5, 0.01,
    r"Seuil methodologique : $10^{-13}$ s/s. "
    r"Zones grises : hors domaine de jauge. "
    r"Zones rouges : couplage non perturbatif.",
    ha="center", fontsize=8, style="italic"
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(PNG)
plt.close(fig)

print(f"[*] Carte generee : {PNG}")
print(f"[*] Grille : {len(phis)} x {len(etas)}")
