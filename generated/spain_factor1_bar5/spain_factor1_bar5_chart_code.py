import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Data setup
data = [
    {"year": 1999, "spain": -1.4, "euro_zone_average": -1.4},
    {"year": 2000, "spain": -1.0, "euro_zone_average": 0.0},
    {"year": 2001, "spain": -0.6, "euro_zone_average": -1.8},
    {"year": 2002, "spain": -0.2, "euro_zone_average": -2.5},
    {"year": 2003, "spain": -0.3, "euro_zone_average": -3.1},
    {"year": 2004, "spain": -0.1, "euro_zone_average": -2.9},
    {"year": 2005, "spain": 1.3, "euro_zone_average": -2.4},
    {"year": 2006, "spain": 2.4, "euro_zone_average": -1.3},
    {"year": 2007, "spain": 1.9, "euro_zone_average": -0.7},
    {"year": 2008, "spain": -4.5, "euro_zone_average": -2.1},
    {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
    {"year": 2010, "spain": -9.3, "euro_zone_average": -6.2},
    {"year": 2011, "spain": -8.9, "euro_zone_average": -4.1},
    {"year": 2012, "spain": -6.3, "euro_zone_average": np.nan},
    {"year": 2013, "spain": -4.5, "euro_zone_average": np.nan},
    {"year": 2014, "spain": -2.8, "euro_zone_average": np.nan}
]
df = pd.DataFrame(data)

# Colors and styles
color_spain = "#1f77b4"   # blue
color_ez = "#ff7f0e"      # orange
color_no_data = "#d3d3d3" # light gray for no-data marker
target_alpha = 0.4

# Figure sizing: 3:4 aspect ratio, high-res for presentation (1600x2133 px)
dpi = 200
fig_width_in = 8.0
fig_height_in = 10.666  # ensures 8 * 200 = 1600 and 10.666 * 200 ~ 2133
fig, ax = plt.subplots(figsize=(fig_width_in, fig_height_in), dpi=dpi)

# Font and rc settings for readability
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
    "axes.edgecolor": "#333333",
})

# X locations
years = df['year'].astype(int).tolist()
x = np.arange(len(years))
bar_width = 0.38

# Masks
is_target = df['year'] >= 2012
ez_available = ~df['euro_zone_average'].isna()

# Plot Spain bars (reported vs targets)
# Reported years (non-target)
reported_mask = ~is_target
ax.bar(x[reported_mask], df.loc[reported_mask, 'spain'],
       width=bar_width, color=color_spain, label="Spain — government budget (% GDP, includes targets for 2012–2014)",
       edgecolor='none', zorder=3)

# Target years (2012-2014): semi-transparent fill + dashed outline
# Plot them at same x positions so groups align
target_x = x[is_target]
target_vals = df.loc[is_target, 'spain'].values
for xi, val in zip(target_x, target_vals):
    # Filled translucent bar
    ax.bar(xi, val, width=bar_width, color=color_spain, alpha=target_alpha, zorder=3)
    # Dashed outline rectangle
    rect = plt.Rectangle((xi - bar_width/2, val if val >= 0 else val), bar_width,
                         abs(val), facecolor="none",
                         edgecolor=color_spain, linewidth=2.0, linestyle='--', zorder=4)
    ax.add_patch(rect)

# Plot Euro-Zone bars only where available
ez_x = x[ez_available]
ez_vals = df.loc[ez_available, 'euro_zone_average'].values
ax.bar(ez_x + bar_width, ez_vals, width=bar_width, color=color_ez, label="Euro‑Zone average — weighted average (% GDP)",
       edgecolor='none', zorder=2)

# Shaded crisis period: 2008–2011 inclusive
# Determine x-range for shading using years positions
year_to_x = dict(zip(years, x))
span_start = year_to_x[2008] - 0.5
span_end = year_to_x[2011] + 0.5
ax.axvspan(span_start, span_end, color='#f0f0f0', alpha=0.7, zorder=0)

# Add small italic label inside the shaded rectangle near top of plotting area
ymin = df[['spain', 'euro_zone_average']].min().min()
ymax = df[['spain', 'euro_zone_average']].max().max()
# pad top a bit
y_top = max(5, np.ceil(ymax + 1))
ax.text((span_start + span_end) / 2, y_top - 0.5, "Crisis period (2008–2011)",
        ha='center', va='top', fontsize=13, style='italic', color='#555555', zorder=5)

# Zero baseline emphasized
ax.axhline(0, color='#333333', linewidth=1.8, zorder=5)

# Horizontal gridlines at every 5 percentage points
min_val = np.nanmin(df[['spain', 'euro_zone_average']].values)
max_val = np.nanmax(df[['spain', 'euro_zone_average']].values)
ytick_min = int(np.floor(min_val / 5.0) * 5)
ytick_max = int(np.ceil(max_val / 5.0) * 5)
# Ensure at least from -15 to +5 to give space if needed
ytick_min = min(ytick_min, -15)
ytick_max = max(ytick_max, 5)
yticks = list(range(ytick_min, ytick_max + 1, 5))
ax.set_yticks(yticks)
ax.set_ylim(ytick_min - 1, ytick_max + 1)
ax.grid(axis='y', color='#e6e6e6', linestyle='-', linewidth=0.8, zorder=0)

# X-axis ticks and labels
ax.set_xticks(x + bar_width / 2)
ax.set_xticklabels([str(y) for y in years], fontsize=16)
ax.tick_params(axis='x', which='major', pad=8)

# Axis labels and ticks font sizes
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18)
ax.tick_params(axis='y', labelsize=18)

# Minimal spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')

# Data labels for two most extreme Spain values: 2009 (-11.2) and 2010 (-9.3)
label_years = [2009, 2010]
for ly in label_years:
    idx = years.index(ly)
    val = df.loc[df['year'] == ly, 'spain'].values[0]
    # For negative bars, place label slightly below the top of the bar tip (which is at 0 if negative)
    if val < 0:
        label_y = val - 0.6
        va = 'top'
    else:
        label_y = val + 0.6
        va = 'bottom'
    ax.text(idx, label_y, f"{val:.1f}", ha='center', va=va, fontsize=14, fontweight='bold', color=color_spain, zorder=6)

# Legend in top-right inside plot area, compact
legend_handles = [
    Patch(facecolor=color_spain, edgecolor='none', label="Spain — government budget (% GDP, includes targets for 2012–2014)"),
    Patch(facecolor=color_ez, edgecolor='none', label="Euro‑Zone average — weighted average (% GDP)"),
    Patch(facecolor=color_no_data, edgecolor='none', alpha=0.6, label="Euro‑Zone — no data (2012–2014)")
]
leg = ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1, 1.03),
                fontsize=16, frameon=False)
leg._legend_box.align = "left"

# Title and subtitle (centered at top)
title = "Spain vs Euro‑Zone: Budget Balance (% of GDP), 1999–2014."
subtitle = ("Annual budget surplus/deficit as a share of GDP. Positive values = surplus; negative values = deficit. "
            "Data through 2011 are reported; 2012–2014 are Spain’s targets.")
# Use figure suptitle for title to ensure center alignment above legend
fig.suptitle(title, fontsize=34, fontweight='bold', y=0.97)
# Subtitle just under title
fig.text(0.5, 0.93, subtitle, ha='center', va='center', fontsize=20, wrap=True)

# Caption area below plot
caption_lines = ("Source: [data source]. Bars show annual budget balance as % of GDP. "
                 "2012–2014 are Spain’s official budget targets, not actual outturns. "
                 "The 2008–2011 period shows a marked divergence in Spain’s deficits versus the Euro‑Zone average.")
# Draw a thin rule/separator above the caption
line = Line2D([0.03, 0.97], [0.125, 0.125], transform=fig.transFigure, color='#bbbbbb', linewidth=0.8, zorder=20)
fig.add_artist(line)
fig.text(0.03, 0.09, caption_lines, fontsize=15, ha='left', va='top', wrap=True)

# Layout adjustments to make room for title, subtitle, legend, and caption
plt.subplots_adjust(top=0.88, bottom=0.18, left=0.08, right=0.86)

# Tighten layout and display
plt.savefig("generated/spain_factor1_bar5/spain_factor1_bar5_design.png", dpi=300, bbox_inches="tight")