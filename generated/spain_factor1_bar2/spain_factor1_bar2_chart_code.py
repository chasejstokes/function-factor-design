import importlib
import subprocess
import sys

# Ensure required packages are installed
required_packages = ["numpy", "matplotlib"]
for pkg in required_packages:
    try:
        importlib.import_module(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

# Data setup
years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
                  2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
                  1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use np.nan for missing euro-zone averages in 2012-2014
euro = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
                 -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Visual parameters
bg_color = "#fafafa"
grid_color = "#e6e6e6"
spain_color = "#c0392b"
euro_color = "#2b7bb9"
target_hatch = "////"  # diagonal hatch
target_alpha = 0.6
vertical_band_color = "#dcdcdc"  # warm light gray for crisis band
vertical_band_alpha = 0.20

# Figure - portrait orientation, presentation scale (3:4 aspect ratio)
fig, ax = plt.subplots(figsize=(9, 12), dpi=150)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# X positions
x = np.arange(len(years))
# Bar width and offsets for grouped bars
bar_width = 0.38  # relatively thick
offset = bar_width / 2.0

# Plot Euro-zone bars only where data exists
valid_euro_mask = ~np.isnan(euro)
# Spain bars: for years with targets (2012-2014), use hatched style and reduced opacity
target_years_mask = (years >= 2012) & (years <= 2014)
spain_colors = [spain_color if not t else spain_color for t in target_years_mask]

# Draw crisis vertical band for 2008--2011
# compute span in x coordinates covering those years fully
start_year = 2008
end_year = 2011
# center-based x coordinates: each year is at integer x[i]
start_idx = np.where(years == start_year)[0][0] - 0.5
end_idx = np.where(years == end_year)[0][0] + 0.5
ax.axvspan(start_idx, end_idx, color=vertical_band_color, alpha=vertical_band_alpha, zorder=0)

# Draw Euro-zone bars
ax.bar(x[valid_euro_mask] - offset, euro[valid_euro_mask], width=bar_width, align='center',
       color=euro_color, edgecolor='none', zorder=3, label='Euro‑zone average')

# Draw Spain bars: regular and targets (with hatch and alpha)
for xi, val, is_target in zip(x, spain, target_years_mask):
    if is_target:
        # hatched target bar
        ax.bar(xi + offset, val, width=bar_width, align='center',
               color=spain_color, edgecolor=spain_color, hatch=target_hatch,
               linewidth=0.8, alpha=target_alpha, zorder=4)
    else:
        ax.bar(xi + offset, val, width=bar_width, align='center',
               color=spain_color, edgecolor='none', zorder=4)

# Zero line emphasized
ax.axhline(0, color="#7f7f7f", linewidth=2.0, zorder=5)

# Horizontal gridlines at specific values
y_ticks = np.array([-12, -8, -4, 0, 4, 8])
# Set y limits slightly beyond data range for breathing room
ymin = min(-12.5, np.nanmin(np.concatenate([spain, euro[np.where(~np.isnan(euro))]])) - 1.0)
ymax = 4.5
ax.set_ylim(ymin, ymax)
ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{int(t)}" for t in y_ticks], fontsize=16)
for y in y_ticks:
    lw = 2.0 if y == 0 else 0.7
    line_color = "#7f7f7f" if y == 0 else grid_color
    ax.hlines(y, xmin=-0.5, xmax=len(years)-0.5, colors=line_color, linewidth=lw, zorder=1)

# X-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=15, fontweight='bold')
ax.tick_params(axis='x', which='both', length=0)

# Y-axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=17, labelpad=12, rotation=90)

# Title and subtitle
title = "Spain vs. Euro‑zone: Budget balance (% of GDP), 1999–2014"
subtitle = ("Grouped by year; positive = surplus, negative = deficit. "
            "Final three years (2012–2014) are Spain’s official targets, not actual outturns.")
ax.set_title(title, fontsize=30, fontweight='bold', pad=18, loc='center')
# subtitle as text below title
ax.text(0.5, 1.00, subtitle, transform=ax.transAxes, fontsize=18,
        ha='center', va='bottom', color="#333333")

# Legend in upper-right inside plotting area
legend_elements = [
    Patch(facecolor=spain_color, edgecolor=spain_color, label='Spain', linewidth=0.5),
    Patch(facecolor=spain_color, edgecolor=spain_color, label='Spain (targets)', hatch=target_hatch, alpha=target_alpha, linewidth=0.5),
    Patch(facecolor=euro_color, edgecolor=euro_color, label='Euro‑zone average')
]
legend = ax.legend(handles=legend_elements, fontsize=16, loc='upper right', bbox_to_anchor=(0.98, 0.98),
                   frameon=False, title=None)
# Make sure hatch shows in legend (matplotlib handles hatch on Patch)

# Numeric labels for key extremes: Spain 2009 (-11.2%) and Spain 2006 (2.4%)
# Find indices
idx_2009 = np.where(years == 2009)[0][0]
idx_2006 = np.where(years == 2006)[0][0]
annotations = [
    (idx_2009 + offset, spain[idx_2009], f"-11.2%"),
    (idx_2006 + offset, spain[idx_2006], f"2.4%")
]
for xpos, ypos, txt in annotations:
    # place label slightly above bar for positive, slightly above (less negative) for negative
    y_off = 0.35 if ypos >= 0 else -0.45
    text_y = ypos + y_off
    tx = ax.text(xpos, text_y, txt, fontsize=13, fontweight='bold', color="#222222",
                 ha='center', va='bottom' if ypos >= 0 else 'top', zorder=10)
    # add subtle contrast halo for projector visibility
    tx.set_path_effects([pe.Stroke(linewidth=3, foreground='white', alpha=0.8), pe.Normal()])

# Caption block at bottom-left with light rule separating it from plotting area
caption_lines = [
    "Data: Eurostat & Spanish Ministry of Finance (compiled by [publisher]), series expressed as % of GDP.",
    "Euro‑zone averages unavailable for 2012–2014; Spain’s 2012–2014 bars are official government targets.",
    "Notice the sharp divergence during the 2008–2011 crisis: Spain’s deficit deepened more than the Euro average."
]
# Adjust layout to make room for caption
plt.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.16)

# Draw a light rule (horizontal line) separating chart and caption (figure coordinates)
line_y_fig = 0.16  # a little above the bottom margin
fig_line = Line2D([0.06, 0.95], [line_y_fig, line_y_fig], transform=fig.transFigure,
                  color="#d8d8d8", linewidth=1.0)
fig.add_artist(fig_line)

# Add caption text left-aligned beneath the plot area
caption_text = "\n".join(caption_lines)
fig.text(0.06, 0.06, caption_text, fontsize=15, va='top', ha='left', color="#333333")

# Tighten and show
plt.tight_layout(rect=[0, 0.08, 1, 0.96])
plt.savefig("generated/spain_factor1_bar2/spain_factor1_bar2_design.png", dpi=300, bbox_inches="tight")