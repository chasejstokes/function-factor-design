import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib import rcParams

# Data
data = [
    {"year": 1999, "spain": -1.2, "euro_zone_average": -0.9},
    {"year": 2000, "spain": -0.6, "euro_zone_average": -0.4},
    {"year": 2001, "spain": -0.4, "euro_zone_average": -0.8},
    {"year": 2002, "spain": -1.0, "euro_zone_average": -1.6},
    {"year": 2003, "spain": -0.8, "euro_zone_average": -2.6},
    {"year": 2004, "spain": 0.6, "euro_zone_average": -2.9},
    {"year": 2005, "spain": 1.3, "euro_zone_average": -1.8},
    {"year": 2006, "spain": 2.4, "euro_zone_average": 1.1},
    {"year": 2007, "spain": 1.9, "euro_zone_average": -0.8},
    {"year": 2008, "spain": -4.5, "euro_zone_average": -3.6},
    {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
    {"year": 2010, "spain": -9.5, "euro_zone_average": -6.0},
    {"year": 2011, "spain": -7.8, "euro_zone_average": -4.1},
    {"year": 2012, "spain": -4.2, "euro_zone_average": -4.6},
    {"year": 2013, "spain": -5.0, "euro_zone_average": -3.8},
    {"year": 2014, "spain": -2.5, "euro_zone_average": -2.0}
]

years = [d["year"] for d in data]
spain = np.array([d["spain"] for d in data])
euro = np.array([d["euro_zone_average"] for d in data])

# Compute aggregates
spain_mean = spain.mean()
euro_mean = euro.mean()
spain_peak_deficit = spain.min()  # most negative
euro_peak_deficit = euro.min()

# Visual parameters
rcParams['font.family'] = 'DejaVu Sans'
figsize = (9, 12)  # portrait orientation (inches)
fig, ax = plt.subplots(figsize=figsize)

# Colors (colorblind-friendly)
color_spain = "#D95F02"    # warm orange
color_euro = "#1B9E77"     # teal/green-blue
zero_line_color = "#4a4a4a"
grid_color = "#d6d6d6"

# X positions for grouped bars
n = len(years)
ind = np.arange(n)
total_group_width = 0.8
bar_width = total_group_width / 2.0
offset = bar_width / 2.0

# Highlight ranges: map years to index ranges
def year_to_index(y):
    return years.index(y)

# Plot background highlights (axvspan uses x coordinates in data space (indices))
# 2004–2007 highlight (surplus period)
start_idx = year_to_index(2004) - 0.5
end_idx = year_to_index(2007) + 0.5
ax.axvspan(start_idx, end_idx, color=color_spain, alpha=0.10, zorder=0)

# 2008–2010 highlight (crisis period)
start_idx2 = year_to_index(2008) - 0.5
end_idx2 = year_to_index(2010) + 0.5
ax.axvspan(start_idx2, end_idx2, color=color_euro, alpha=0.08, zorder=0)

# Plot bars
bars_spain = ax.bar(ind - offset, spain, width=bar_width, color=color_spain, label='Spain', zorder=3)
bars_euro = ax.bar(ind + offset, euro, width=bar_width, color=color_euro, label='Euro‑Zone average', zorder=3)

# Zero baseline emphasized
ax.axhline(0, color=zero_line_color, linewidth=1.8, zorder=4)

# Gridlines (horizontal) at 2.5% increments (covers data range)
ymin = min(-12.5, spain.min() - 1)
ymax = max(4, spain.max() + 1)
ax.set_ylim(ymin, ymax)
y_major = 2.5
ax.yaxis.set_major_locator(MultipleLocator(y_major))
ax.grid(axis='y', color=grid_color, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# X-axis ticks and labels (show every year)
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=16)
plt.setp(ax.get_xticklabels(), rotation=0)  # keep vertical space; portrait layout allows full labels

# Axis labels and title/subtitle
title = "Budget balance (% of GDP): Spain vs Euro‑Zone average, 1999–2014"
subtitle = ("Spain moves from small surpluses in the mid‑2000s to a deep post‑2008 deficit; "
            "comparison highlights where Spain diverged from the euro‑area average.")
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, labelpad=12)
fig.suptitle(title, fontsize=32, fontweight='bold', y=0.955)
# Subtitle as centered text below title
fig.text(0.5, 0.92, subtitle, ha='center', va='center', fontsize=20, wrap=True)

# Legend top-right
legend = ax.legend(loc='upper right', fontsize=14, frameon=False, bbox_to_anchor=(0.98, 0.98))

# Selective numeric labels
def annotate_bar(bar, text, color, y_offset=0.35):
    h = bar.get_height()
    x = bar.get_x() + bar.get_width() / 2
    if h < 0:
        va = 'top'
        y = h - 0.15  # slightly below negative bar tip
    else:
        va = 'bottom'
        y = h + 0.15
    ax.text(x, y, text, ha='center', va=va, fontsize=14, fontweight='bold', color=color, zorder=6)

# Label Spain 2009 (-11.2), Spain 2006 (2.4), Euro 2009 (-6.3)
# Find corresponding bar objects
idx_2009 = year_to_index(2009)
idx_2006 = year_to_index(2006)
# Spain bars are bars_spain; each bar corresponds to position in same order
annotate_bar(bars_spain[idx_2009], "2009: −11.2%", color_spain)
annotate_bar(bars_spain[idx_2006], "2006: +2.4%", color_spain)
annotate_bar(bars_euro[idx_2009], "2009: −6.3%", color_euro)

# Mean dashed horizontal lines for each series (with labels at right end)
ax.hlines(spain_mean, xmin=-0.5, xmax=n - 0.5, colors=color_spain, linestyles='--', alpha=0.6, linewidth=1.2, zorder=2)
ax.hlines(euro_mean, xmin=-0.5, xmax=n - 0.5, colors=color_euro, linestyles='--', alpha=0.6, linewidth=1.2, zorder=2)
# Place labels for mean lines at the right side (just outside last group)
x_label_pos = n - 0.15
ax.text(x_label_pos, spain_mean, f"Mean Spain: {spain_mean:.1f}%", color=color_spain, fontsize=12, va='center', ha='left', alpha=0.9)
ax.text(x_label_pos, euro_mean, f"Mean EZ: {euro_mean:.1f}%", color=color_euro, fontsize=12, va='center', ha='left', alpha=0.9)

# Synthesis box lower-left (in axes fraction coordinates)
synthesis_text = (
    f"Key synthesis: Spain averaged {spain_mean:.1f}% (1999–2014) with a peak deficit of {spain_peak_deficit:.1f}% in 2009; "
    f"Euro‑Zone averaged {euro_mean:.1f}% with a peak deficit of {euro_peak_deficit:.1f}%.\n"
    "Spain’s deficits exceed the euro-area average mainly 2008–2014; Spain recorded surpluses 2004–2007."
)
ax.text(0.02, 0.03, synthesis_text, transform=ax.transAxes, fontsize=16,
        va='bottom', ha='left',
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="#cccccc", alpha=0.95))

# Inset sparkline for difference (Spain - Euro) at top-left
left, bottom, width, height = 0.06, 0.78, 0.22, 0.12
inset_ax = fig.add_axes([left, bottom, width, height])
difference = spain - euro
inset_ax.plot(ind, difference, color="#6C757D", linewidth=1.8)
inset_ax.fill_between(ind, difference, 0, where=(difference >= 0), interpolate=True, color="#6C757D", alpha=0.12)
inset_ax.axhline(0, color='#777777', linewidth=0.6)
inset_ax.set_xticks([])
inset_ax.set_yticks([])
inset_ax.set_title("Spain − Euro diff.", fontsize=10, pad=4)
for spine in inset_ax.spines.values():
    spine.set_visible(False)

# Aesthetic tweaks
ax.tick_params(axis='y', labelsize=16)
ax.tick_params(axis='x', labelsize=16)
ax.set_xlabel("")  # no xlabel text (years are on ticks)
ax.set_xlim(-0.8, n - 0.2)

# Ensure tight layout and render
plt.tight_layout(rect=[0, 0, 1, 0.96])  # leave space for suptitle
plt.savefig("generated/spain_factor4_bar8/spain_factor4_bar8_design.png", dpi=300, bbox_inches="tight")