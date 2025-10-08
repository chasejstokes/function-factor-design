import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib as mpl

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
euro = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Styling parameters (presentation-ready)
TITLE_SIZE = 32
SUBTITLE_SIZE = 20
AXIS_LABEL_SIZE = 18
TICK_LABEL_SIZE = 15
LEGEND_SIZE = 16
CAPTION_SIZE = 15
METADATA_SIZE = 13
ANNOTATION_SIZE = 16

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": TITLE_SIZE,
    "axes.titleweight": "bold",
    "axes.labelsize": AXIS_LABEL_SIZE,
    "xtick.labelsize": TICK_LABEL_SIZE,
    "ytick.labelsize": TICK_LABEL_SIZE,
})

# Figure setup: portrait 3:4 (e.g., 9 x 12 inches)
fig, ax = plt.subplots(figsize=(9, 12))
fig.subplots_adjust(top=0.88, bottom=0.16, left=0.12, right=0.94)

# Positions for grouped bars
n = len(years)
x = np.arange(n)
group_width = 0.8
bar_width = 0.36  # width of each bar within group
offset = bar_width / 2.0

# Colors
spain_color = "#0b67b2"      # deep blue for Spain (primary)
euro_color = "#7d8b93"       # muted grey-blue for Euro-zone (secondary)
na_color = "#b0b4b6"         # faint color for NA markers
zero_line_color = "#222222"

# Draw Euro-zone bars only where data is not NaN
euro_mask = ~np.isnan(euro)
# Spain bars: for the final 3 years (2012-2014), use hatched/target style
target_years_mask = np.array([year >= 2012 for year in years])

# Plot bars
spain_positions = x - offset
euro_positions = x + offset

# Spain observed bars (non-target years)
spain_observed_mask = ~target_years_mask
ax.bar(spain_positions[spain_observed_mask], spain[spain_observed_mask],
       width=bar_width, align='center', color=spain_color, edgecolor='black', linewidth=0.6, zorder=3,
       label='Spain (observed)')

# Spain target bars (2012-2014): same color but hatched and slightly transparent fill
# Matplotlib does not support hatch alpha directly; we set facecolor with alpha and hatch pattern.
for xi, yi, is_target in zip(spain_positions, spain, target_years_mask):
    if is_target:
        ax.bar(xi, yi, width=bar_width, align='center',
               color=spain_color, alpha=0.55, edgecolor=spain_color, linewidth=0.8,
               hatch='////', zorder=3)

# Euro-zone bars where available (observed only)
ax.bar(euro_positions[euro_mask], euro[euro_mask],
       width=bar_width, align='center',
       color=euro_color, edgecolor=euro_color, linewidth=0.6, alpha=0.75, zorder=2,
       label='Euro‑zone average')

# NA markers for Euro-zone in 2012-2014: small faint em-dash above x-axis
na_indices = np.where(~euro_mask)[0]
for idx in na_indices:
    # place the dash just above the x-axis baseline (y = -0.6 of the axis' visible range later)
    ax.text(euro_positions[idx], -0.6, "—", ha='center', va='center', color=na_color, fontsize=12, alpha=0.8)

# Zero baseline (heavier)
ax.axhline(0, color=zero_line_color, linewidth=1.4, zorder=4)

# Horizontal gridlines (light dashed)
ax.yaxis.grid(True, which='major', linestyle='--', linewidth=0.6, color='#d9d9d9')
ax.set_axisbelow(True)

# X-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels(years, rotation=12, ha='center')

# Y-axis label and ticks
ax.set_ylabel("Budget balance (% of GDP)", fontsize=AXIS_LABEL_SIZE)
ax.set_ylim(-12.5, 4.5)
ax.set_yticks(np.arange(-12, 5, 2))
ax.set_yticklabels([f"{int(y)}" for y in np.arange(-12, 5, 2)])

# Annotation for 2009 Spain peak deficit (single concise label)
year_to_annotate = 2009
annot_idx = int(np.where(years == year_to_annotate)[0][0])
annot_x = spain_positions[annot_idx]
annot_y = spain[annot_idx]
# Draw a thin leader line (no arrow) from slightly above the bar bottom to the text
line_x = [annot_x, annot_x]
line_y = [annot_y + 0.8, annot_y + 2.0]  # short vertical line pointing toward the label
ax.plot(line_x, line_y, color='0.15', linewidth=0.6, zorder=5)
ax.text(annot_x + 0.18, annot_y + 2.05, f"2009: Spain peak deficit −11.2%", fontsize=ANNOTATION_SIZE,
        va='bottom', ha='left', color='0.15', zorder=5)

# Legend (compact, upper-right inside plotting area)
legend_elements = [
    Patch(facecolor=spain_color, edgecolor='black', label='Spain (observed)'),
    Patch(facecolor=spain_color, edgecolor=spain_color, hatch='////', label="Spain (targets 2012–2014)"),
    Patch(facecolor=euro_color, edgecolor=euro_color, label='Euro‑zone average')
]
legend = ax.legend(handles=legend_elements, loc='upper right', fontsize=LEGEND_SIZE, frameon=False)
legend.set_title(None)

# Title and subtitle
title = "Spain vs Euro‑Zone: Budget balance (% of GDP), 1999–2014"
subtitle = ("Paired bars show annual budget surpluses (positive) and deficits (negative). "
            "Final three years (2012–2014) are Spain’s targets; Euro‑zone averages unavailable for 2012–2014.")
ax.set_title(title, pad=30)
# Subtitle as separate text below title
fig.text(0.12, 0.84, subtitle, fontsize=SUBTITLE_SIZE, ha='left', va='center', color='#222222')

# Caption and metadata block (two-line) at the bottom full-width
caption_line = ("Spain ran modest deficits in early 2000s, moved to surpluses in mid‑2000s, "
                "then experienced a deep post‑2008 downturn (peak deficit in 2009).")
metadata_line = ("Data: budget balance (% of GDP). Final 3 years are Spain’s government targets (2012–2014). "
                 "Euro‑zone average not available (NA) for 2012–2014. Source: [insert primary data source name].")
fig.text(0.12, 0.06, caption_line, fontsize=CAPTION_SIZE, ha='left', va='center', color='#111111')
fig.text(0.12, 0.035, metadata_line, fontsize=METADATA_SIZE, ha='left', va='center', color='#333333')

# Improve layout and show
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("generated/spain_factor1_bar1/spain_factor1_bar1_design.png", dpi=300, bbox_inches="tight")