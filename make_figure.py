"""Draw board-progress.svg: validation-board score of each adopted step.

Scores are the validation-board scores listed in README.md. Needs matplotlib:
    python make_figure.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (label, validation score). The zero-effect baseline (-0.2696) is quoted in
# the text and left off the axis so the later steps stay readable.
STEPS = [
    ("First transfer\nmodel", 0.0636),
    ("Unshrunk mean,\n+ iPSC source", 0.1028),
    ("+ Orion sources,\ndonor weights", 0.1267),
    ("Effect amplitude\n× 1.3", 0.1362),
    ("Union gene axis", 0.1471),
    ("Score-aware\nemission*", 0.1822),
    ("Control-axis\ndeflation (k=10)", 0.1876),
    ("Bulk amplitude\n0.6", 0.1926),
    ("Rank-16 residual,\ndeflation k=20", 0.1945),
]
PEERS_LOW, PEERS_HIGH = 0.30, 0.31  # the informative peer entries compared in the text

assert all(b[1] > a[1] for a, b in zip(STEPS, STEPS[1:])), "adopted steps must rise"

fig, ax = plt.subplots(figsize=(10, 4.6))
x = range(len(STEPS))
y = [s for _, s in STEPS]
ax.axhspan(PEERS_LOW, PEERS_HIGH, color="#d9d9d9", lw=0)
ax.text(0, PEERS_HIGH + 0.004, "peer entries compared in the text (0.30–0.31)", fontsize=9, color="#555555")
ax.axhline(0, color="#888888", lw=0.8, ls="--")
ax.text(len(STEPS) - 1, 0.004, "official zero: context-mean response", fontsize=9, color="#555555", ha="right")
ax.plot(x, y, marker="o", color="#1f5fa8", lw=1.8)
for i, s in zip(x, y):
    ax.annotate(f"{s:.4f}", (i, s), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9)
ax.set_xticks(list(x), [label for label, _ in STEPS], fontsize=8)
ax.set_ylabel("Validation-board score (mean of 6 scaled metrics)")
ax.set_ylim(-0.02, 0.34)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
out = Path(__file__).with_name("board-progress.svg")
fig.savefig(out)
print(out)
