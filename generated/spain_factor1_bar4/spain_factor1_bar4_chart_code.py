import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Data setup (from provided dataset)
years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# euro_zone_average has missing values for 2012-2014; represent as np.nan
euro_zone = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Styling parameters
color_spain = "#D95F02"      # warm orange
color_ez = "#1B9E77"         # teal/blue-green
hatch_pattern = "////"       # 45-degree-like hatch
target_alpha = 0.6           # opacity for target bars

# Figure size: ensure at least 1920x2560 px (3:4). Use dpi=200 and figsize accordingly.
dpi = 200
fig_w_inches = 9.6   # 9.6*200 = 1920 px
fig_h_inches = 12.8  # 12.8*200 = 2560 px
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "axes.titleweight": "bold"
})
fig = plt.figure(figsize=(fig_w_inches, fig_h_inches), dpi=dpi)
ax = fig.add_subplot(1, 1, 1)

# Positions for grouped bars
x = np.arange(len(years))
bar_width = 0.36
offset = bar_width / 2.0

# Compute y-limits with tidy padding; ensure default about -12 to +3 if data allow
all_vals = np.concatenate([spain[~np.isnan(spain)], euro_zone[~np.isnan(euro_zone)]])
min_val = np.nanmin(all_vals)
max_val = np.nanmax(all_vals)
y_min = min(-12, math.floor(min_val) - 1)
y_max = max(3, math.ceil(max_val) + 1)
ax.set_ylim(y_min, y_max)

# Plot Euro-Zone bars only where data is present
ez_mask = ~np.isnan(euro_zone)
ez_x = x[ez_mask]
ez_vals = euro_zone[ez_mask]
ez_bars = ax.bar(ez_x - offset, ez_vals, width=bar_width, color=color_ez, label="Euro‑Zone average", zorder=2)

# Spain observed (1999-2011) and Spain targets (2012-2014)
# We'll plot Spain observed for all years, but visually modify last 3 bars
spain_bars = []
for idx, (xi, val, yr) in enumerate(zip(x, spain, years)):
    if yr >= 2012:
        # Target years: same hue but hatched and semi-transparent
        b = ax.bar(xi + offset, val, width=bar_width, color=color_spain, edgecolor=color_spain,
                   hatch=hatch_pattern, alpha=target_alpha, label="_nolegend_", zorder=3)
        spain_bars.append(b[0])
    else:
        b = ax.bar(xi + offset, val, width=bar_width, color=color_spain, edgecolor=color_spain,
                   label="_nolegend_", zorder=3)
        spain_bars.append(b[0])

# Shaded vertical band behind 2012-2014 groups (very light gray transparent overlay)
first_target_idx = np.where(years == 2012)[0][0]
last_target_idx = np.where(years == 2014)[0][0]
band_start = x[first_target_idx] - (bar_width + 0.2)
band_end = x[last_target_idx] + (bar_width + 0.2)
ax.axvspan(band_start, band_end, color="lightgray", alpha=0.12, zorder=0)

# Boundary line at the 2012 tick (between 2011 and 2012)
boundary_x = x[first_target_idx] - 0.5
ax.axvline(boundary_x, color="gray", linewidth=1.0, alpha=0.8, zorder=4)

# Emphasize zero baseline
ax.axhline(0.0, color="dimgray", linewidth=2.0, zorder=5)

# Horizontal gridlines: light gray, sparse (every 2 percentage points where appropriate)
y_range = y_max - y_min
# choose step 2 if range > 8 else 1
step = 2 if y_range > 8 else 1
yticks = np.arange(math.ceil(y_min / step) * step, y_max + step, step)
ax.set_yticks(yticks)
ax.yaxis.grid(True, which='major', color='lightgray', linestyle='-', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# X axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=14)
ax.tick_params(axis='x', which='major', pad=6)
ax.tick_params(axis='y', labelsize=14)

# Axis labels
ax.set_ylabel("Budget balance (% of GDP)", fontsize=20, fontweight='bold', labelpad=12)

# Title and subtitle (top-centered)
title = "Budget balance (% of GDP): Spain vs Euro‑Zone average, 1999–2014"
subtitle = ("Negative values = deficit. Spain’s values for 2012–2014 are government targets; "
            "Euro‑Zone averages unavailable for those years.")
fig.suptitle(title, fontsize=36, y=0.975)
fig.text(0.5, 0.935, subtitle, ha='center', fontsize=20)

# Legend top-right inside plotting area with three items:
# - Spain (solid)
# - Euro‑Zone average
# - Spain (targets) patterned
legend_elements = [
    Patch(facecolor=color_spain, edgecolor=color_spain, label="Spain"),
    Patch(facecolor=color_ez, edgecolor=color_ez, label="Euro‑Zone average"),
    Patch(facecolor=color_spain, edgecolor=color_spain, hatch=hatch_pattern, alpha=target_alpha, label="Spain (target)")
]
leg = ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.95), fontsize=14, frameon=False)
for text in leg.get_texts():
    text.set_fontsize(14)

# Minimal in-plot numeric annotations for extremes: Spain 2009 (-11.2) and Spain 2006 (2.4)
# Find indices
def annotate_bar(idx, text, color_text='white'):
    bar = spain_bars[idx]
    h = bar.get_height()
    x_pos = bar.get_x() + bar.get_width() / 2
    # If negative, place label slightly below the bar tip; if positive, slightly above
    if h < 0:
        va = 'top'
        y_pos = h - 0.3
    else:
        va = 'bottom'
        y_pos = h + 0.3
    ax.text(x_pos, y_pos, text, ha='center', va=va, fontsize=12, color=color_text, fontweight='bold', zorder=6)

# Spain 2009 index
idx_2009 = int(np.where(years == 2009)[0][0])
annotate_bar(idx_2009, "-11.2", color_text='white')

# Spain 2006 positive peak label
idx_2006 = int(np.where(years == 2006)[0][0])
# Choose dark text for light bar top
annotate_bar(idx_2006, "2.4", color_text='black')

# Optionally place a small direct label for "Spain" near the 2011 observed bar (to indicate series)
idx_2011 = int(np.where(years == 2011)[0][0])
bar2011 = spain_bars[idx_2011]
x_pos_label = bar2011.get_x() + bar2011.get_width() / 2 + 0.5  # nudged right
y_pos_label = bar2011.get_height()
ax.text(x_pos_label, y_pos_label, "Spain", fontsize=12, fontweight='bold', ha='left', va='center', color=color_spain, zorder=6)

# Caption below chart with required elements: definition, data status, source, synthesis
caption = ("Values are budget balance as % of GDP. Spain 2012–2014 are government targets; Euro‑Zone averages not available "
           "for 2012–2014. Source: Eurostat / national authorities — original series; missing values left blank. "
           "Spain moved from small deficits in the early 2000s to surpluses in the mid‑2000s, then experienced a sharp "
           "deterioration after 2008 (peak deficit in 2009).")
fig.text(0.5, 0.035, caption, ha='center', fontsize=14, wrap=True)

# Small footnote / micro-note under caption
footnote = "Euro‑Zone average = simple average of member states available that year."
fig.text(0.5, 0.015, footnote, ha='center', fontsize=10, color='gray')

# Tight layout adjustments to ensure title/subtitle and caption fit
plt.subplots_adjust(top=0.90, bottom=0.10, left=0.12, right=0.94)

# Remove top and right spines for a cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Show the plot
plt.savefig("generated/spain_factor1_bar4/spain_factor1_bar4_design.png", dpi=300, bbox_inches="tight")