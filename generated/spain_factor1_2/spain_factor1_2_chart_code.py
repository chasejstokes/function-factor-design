import sys
import subprocess

# Ensure required packages are installed
def ensure_pkg(pkg_name):
    try:
        __import__(pkg_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        __import__(pkg_name)

ensure_pkg('matplotlib')
ensure_pkg('numpy')

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors and styles
color_spain = "#1f77b4"      # saturated blue
color_euro = "#7f7f7f"       # muted gray
color_pos = "#7fc97f"        # soft green for Spain > Euro
color_neg = "#f28e8c"        # soft red for Spain < Euro
alpha_fill = 0.30

# Figure and axes
# Use a seaborn-like whitegrid style if available; fall back to default otherwise.
try:
    plt.style.use('seaborn-whitegrid')
except Exception:
    plt.style.use('default')

fig, ax = plt.subplots(figsize=(11, 6))

# Divergence fill: green where Spain > Euro, red where Spain < Euro
ax.fill_between(years, spain, euro, where=(spain >= euro), interpolate=True,
                facecolor=color_pos, alpha=alpha_fill, linewidth=0, label='Spain > Euro: green')
ax.fill_between(years, spain, euro, where=(spain < euro), interpolate=True,
                facecolor=color_neg, alpha=alpha_fill, linewidth=0, label='Spain < Euro: red')

# Plot lines
ax.plot(years, spain, color=color_spain, linewidth=2.5, label='Spain')
ax.plot(years, euro, color=color_euro, linewidth=1.5, label='Euro-Zone average')

# Markers only for annotated years and endpoint
annot_years = [2006, 2009, 2014]
annot_idx = [list(years).index(y) for y in annot_years]
ax.plot(years[annot_idx], spain[annot_idx], linestyle='None', marker='o', markersize=6,
        markeredgecolor='white', markerfacecolor=color_spain, zorder=5)

# Zero baseline dashed line
ax.axhline(0, color='black', linestyle='--', linewidth=1.2, alpha=0.9)

# Grid: horizontal only
ax.yaxis.grid(True, which='major', color='0.90')
ax.xaxis.grid(False)

# Axis labels and ticks
ax.set_ylabel("Budget balance (% of GDP)", fontsize=11)
ax.set_xlabel("")  # no x-axis label; years are self-evident
ax.set_xticks(years)
ax.set_xticklabels([str(int(y)) for y in years], rotation=0, fontsize=9)

# Y ticks at interval 2
ymin = np.floor(min(spain.min(), euro.min()) / 2) * 2 - 1
ymax = np.ceil(max(spain.max(), euro.max()) / 2) * 2 + 1
ax.set_ylim(ymin, ymax)
yticks = np.arange(int(ymin), int(ymax)+1, 2)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{ytick:g}" for ytick in yticks], fontsize=9)

# Sparse annotations for 2006 and 2009
# 2006: "2006: Spain peaks above Euro average (2.4% vs 1.1%)."
x2006 = 2006
y2006_spain = float(spain[years == x2006][0])
y2006_euro = float(euro[years == x2006][0])
ann_text_2006 = f"2006: Spain peaks above Euro average\n({y2006_spain:.1f}% vs {y2006_euro:.1f}%)"
ax.annotate(ann_text_2006,
            xy=(x2006, y2006_spain), xycoords='data',
            xytext=(x2006-1.2, y2006_spain+3.0), textcoords='data',
            fontsize=9, va='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.92),
            arrowprops=dict(arrowstyle='-', color='0.5', linewidth=0.8, shrinkA=0, shrinkB=0))

# 2009: "2009: Spain’s deficit far exceeds Euro average (–11.2% vs –6.3%)."
x2009 = 2009
y2009_spain = float(spain[years == x2009][0])
y2009_euro = float(euro[years == x2009][0])
ann_text_2009 = f"2009: Spain’s deficit far exceeds\nEuro average ({y2009_spain:.1f}% vs {y2009_euro:.1f}%)"
ax.annotate(ann_text_2009,
            xy=(x2009, y2009_spain), xycoords='data',
            xytext=(x2009+0.8, y2009_spain-3.5), textcoords='data',
            fontsize=9, va='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.92),
            arrowprops=dict(arrowstyle='-', color='0.5', linewidth=0.8, shrinkA=0, shrinkB=0))

# Title and subtitle
fig.suptitle("Spain vs. Euro‑Zone: Budget Balance (% of GDP), 1999–2014",
             fontsize=16, fontweight='bold', y=0.98)
ax.set_title("Annual budget surplus/deficit (positive = surplus). Emphasis: where Spain outperformed or lagged the Euro‑Zone average.",
             fontsize=11, fontweight='normal', loc='left', pad=6)

# Legend inside plot (top-right)
legend_handles = [
    Line2D([0], [0], color=color_spain, lw=2.5, label='Spain'),
    Line2D([0], [0], color=color_euro, lw=1.5, label='Euro‑Zone average'),
    Patch(facecolor=color_pos, edgecolor='none', alpha=alpha_fill, label='Spain > Euro: green'),
    Patch(facecolor=color_neg, edgecolor='none', alpha=alpha_fill, label='Spain < Euro: red')
]
leg = ax.legend(handles=legend_handles, loc='upper right', frameon=True, framealpha=0.95, fontsize=9)
leg.get_frame().set_edgecolor('0.85')

# Caption (two short paragraphs) — full width below chart
caption = ("This chart shows annual general‑government balance as % of GDP for Spain (blue) and the Euro‑Zone average (gray). "
           "Positive values are surpluses; negative values are deficits.\n\n"
           "Spain outperformed the Euro Zone through the mid‑2000s before suffering a much larger collapse during the 2008–10 crisis — "
           "a divergence with fiscal and political consequences for Spain’s recovery.")
plt.tight_layout(rect=[0, 0.08, 1, 0.94])
fig.text(0.01, 0.045, caption, ha='left', va='bottom', fontsize=9, wrap=True)

# Metadata block (small, bottom-right) with light background
metadata_text = ("Data: general government balance, % of GDP; Euro‑Zone is simple average of constituent countries; "
                 "values rounded to one decimal; years 1999–2014.")
fig.text(0.99, 0.01, metadata_text, ha='right', va='bottom', fontsize=8,
         bbox=dict(boxstyle="round,pad=0.3", fc="0.95", ec="none", alpha=1.0))

# Show plot
plt.savefig("generated/spain_factor1_2_design.png", dpi=300, bbox_inches="tight")