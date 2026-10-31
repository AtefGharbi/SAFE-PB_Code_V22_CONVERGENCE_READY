import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE, ORANGE, AQUA, GRAY, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#0b0b0b", "#52514e"
VIOLET = "#6250d6"
plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 8.5, "axes.titlesize": 9,
    "axes.labelsize": 8.5, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": "#e4e3df",
    "grid.linewidth": 0.6, "legend.frameon": False, "savefig.dpi": 600,
    "lines.linewidth": 2,
})
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paper_outputs", "figs")


def save(fig, name):
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, f"{name}.png"), bbox_inches="tight")
    fig.savefig(os.path.join(FIG_DIR, f"{name}.pdf"), bbox_inches="tight")
    plt.close(fig)
