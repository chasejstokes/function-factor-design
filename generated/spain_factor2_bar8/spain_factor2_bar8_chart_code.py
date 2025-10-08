import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patheffects as path_effects
import numpy as np

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
spain_vals = [d["spain"] for d in data]
ez_vals = [d["euro_zone_average"] for d in data]

# Colors
color_spain = "#8B0000"  # dark crimson
color_ez = "#003366"     # navy/blue
highlight_halo = (0.85, 0.82, 0.80, 0.5)  # warm translucent gray for 2009 halo

# Figure: portrait aspect >= 3:4 (width x height). Use presentation-ready size.
fig_w, fig_h = 7.5, 10  # inches (approx 900x1200 px at 120 dpi)
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.12, right=0.95)

x = np.arange(len(years))
n = len(years)

# Bar geometry: group width = 0.6, two bars per group -> each bar 0.3
bar_width = 0.30
offset = bar_width / 2.0
x_spain = x - offset
x_ez = x + offset

# Y-axis limits and ticks
ymin, ymax = -12.5, 3.0
ax.set_ylim(ymin, ymax)
yticks = np.arange(-12, 4, 2)
ax.set_yticks(yticks)
ax.set_ylabel("Percent of GDP", fontsize=16, fontweight='regular', family='sans-serif')

# Light horizontal gridlines
ax.grid(axis='y', linestyle='-', linewidth=0.6, color='#DDDDDD', zorder=0)
ax.set_axisbelow(True)

# Zero baseline emphasis
ax.axhline(0, color='#666666', linewidth=2.2, zorder=2)

# Remove default bars; we'll draw rounded rectangles for slight corner radius
rounding_size = 3  # in points
for xi, val in zip(x_spain, spain_vals):
    if val >= 0:
        y0 = 0
        height = val
    else:
        y0 = val
        height = -val
    # Fancy rounded rectangle
    patch = FancyBboxPatch(
        (xi - bar_width/2, y0),
        bar_width,
        height,
        boxstyle=f"round,pad=0,rounding_size={rounding_size}",
        linewidth=0,
        facecolor=color_spain,
        edgecolor='none',
        mutation_aspect=1,
        zorder=4
    )
    ax.add_patch(patch)

for xi, val in zip(x_ez, ez_vals):
    if val >= 0:
        y0 = 0
        height = val
    else:
        y0 = val
        height = -val
    patch = FancyBboxPatch(
        (xi - bar_width/2, y0),
        bar_width,
        height,
        boxstyle=f"round,pad=0,rounding_size={rounding_size}",
        linewidth=0,
        facecolor=color_ez,
        edgecolor='none',
        zorder=3
    )
    ax.add_patch(patch)

# X-axis years
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=14, rotation=0, family='sans-serif')

# Data labels on each bar (one decimal). Place at tip of each bar.
for xi, val in zip(x_spain, spain_vals):
    label = f"{val:.1f}%"
    if val >= 0:
        # place label above bar (outside) with dark text
        ypos = val + 0.35
        txt = ax.text(xi, ypos, label, ha='center', va='bottom',
                      fontsize=13, color='black', family='sans-serif', zorder=6)
        # subtle stroke for readability
        txt.set_path_effects([path_effects.Stroke(linewidth=1, foreground='white', alpha=0.6), path_effects.Normal()])
    else:
        # place label inside negative bar near top of the negative region
        ypos = val + 0.35
        txt = ax.text(xi, ypos, label, ha='center', va='bottom',
                      fontsize=13, color='white', family='sans-serif', zorder=6)
        txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black', alpha=0.45), path_effects.Normal()])

for xi, val in zip(x_ez, ez_vals):
    label = f"{val:.1f}%"
    if val >= 0:
        ypos = val + 0.35
        txt = ax.text(xi, ypos, label, ha='center', va='bottom',
                      fontsize=13, color='black', family='sans-serif', zorder=5)
        txt.set_path_effects([path_effects.Stroke(linewidth=1, foreground='white', alpha=0.6), path_effects.Normal()])
    else:
        ypos = val + 0.35
        txt = ax.text(xi, ypos, label, ha='center', va='bottom',
                      fontsize=13, color='white', family='sans-serif', zorder=5)
        txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black', alpha=0.45), path_effects.Normal()])

# Inline series labels near first year's bars
first_x = x[0]
label_y_pos = ymax - 0.25*(ymax - ymin)  # somewhere near top-left area of plotting region
# small colored square + text
square_side = 0.18
sq_sp = Rectangle((first_x - 0.7, label_y_pos), square_side, square_side, facecolor=color_spain, transform=ax.get_xaxis_transform(), clip_on=False)
sq_ez = Rectangle((first_x - 0.7, label_y_pos - 0.25), square_side, square_side, facecolor=color_ez, transform=ax.get_xaxis_transform(), clip_on=False)
# Using transform in axes coordinates: convert x positions in axes coords
# Instead, place using data coordinates relative to axes:
ax.add_patch(Rectangle((first_x - 0.7, label_y_pos), square_side, square_side, facecolor=color_spain, transform=None, zorder=7))
ax.text(first_x - 0.7 + square_side + 0.05, label_y_pos + square_side*0.05, "Spain", fontsize=12, color=color_spain, family='sans-serif', zorder=8)
ax.add_patch(Rectangle((first_x - 0.7, label_y_pos - 0.45), square_side, square_side, facecolor=color_ez, transform=None, zorder=7))
ax.text(first_x - 0.7 + square_side + 0.05, label_y_pos - 0.45 + square_side*0.05, "Euro‑Zone avg", fontsize=12, color=color_ez, family='sans-serif', zorder=8)

# Faded repetition near top-right
ax.text(x[-1] + 0.6, ymax - 0.6, "Spain", color=color_spain, fontsize=11, alpha=0.65, family='sans-serif', zorder=9)
ax.text(x[-1] + 0.6, ymax - 1.2, "Euro‑Zone avg", color=color_ez, fontsize=11, alpha=0.65, family='sans-serif', zorder=9)

# Title and subtitle
ax.set_title("Budget Balance (GDP %)", fontsize=30, fontweight=600, pad=18, family='sans-serif')
ax.text(0.5, 0.92, "Spain vs. Euro‑Zone average, 1999–2014", transform=fig.transFigure,
        ha='center', fontsize=17, family='sans-serif')

# Annotations
# Pre-crisis surpluses (2004-2007) pointing to 2006 pair
idx_2006 = years.index(2006)
x_2006 = x[idx_2006]
# annotation box coordinates in data coords
ann_pre_text = "Pre‑crisis surpluses (2004–2007): Spain > EZ avg"
ax.annotate(
    ann_pre_text,
    xy=(x_2006 - offset, spain_vals[idx_2006]), xycoords='data',
    xytext=(x_2006 - 2.2, 1.8), textcoords='data',
    fontsize=14, family='sans-serif',
    bbox=dict(boxstyle="round,pad=0.4", fc='white', alpha=0.75, ec='none'),
    arrowprops=dict(arrowstyle="-", color='#777777', linewidth=1),
    zorder=11
)

# 2009 crisis spike annotation with arrow to Spain 2009 bar and highlight halo behind the year
idx_2009 = years.index(2009)
x_2009 = x[idx_2009]
# highlight halo behind group (rectangle spanning both bars)
halo_width = 0.9
halo = Rectangle((x_2009 - halo_width/2, ymin), halo_width, ymax - ymin,
                 facecolor=highlight_halo, edgecolor='none', zorder=1)
ax.add_patch(halo)

ann_main = "2009: Spain −11.2% vs EZ −6.3% (largest gap)"
ann_sub = "Crisis years deepen deficits"
ax.annotate(
    ann_main + "\n" + ann_sub,
    xy=(x_2009 - offset, spain_vals[idx_2009]), xycoords='data',
    xytext=(x_2009 + 1.0, -3.5), textcoords='data',
    fontsize=14, family='sans-serif', va='center',
    bbox=dict(boxstyle="round,pad=0.5", fc='white', alpha=0.8, ec='none'),
    arrowprops=dict(arrowstyle="->", color='#555555', linewidth=1.2),
    zorder=12
)

# 2014: deficits narrowed note near final pair
idx_2014 = years.index(2014)
x_2014 = x[idx_2014]
ax.annotate(
    "2014: deficits narrowed",
    xy=(x_2014 + offset, ez_vals[idx_2014]), xycoords='data',
    xytext=(x_2014 - 2.4, -6.6), textcoords='data',
    fontsize=13, family='sans-serif',
    bbox=dict(boxstyle="round,pad=0.4", fc='white', alpha=0.75, ec='none'),
    arrowprops=dict(arrowstyle="-", color='#777777', linewidth=1),
    zorder=11
)

# Aesthetic adjustments
ax.set_xlim(-0.6, n - 0.4)
ax.set_xlabel("")  # x-axis label not required other than ticks (years)
# emphasize zero with label on the left
ax.text(-0.5, 0.15, "0%", transform=ax.get_yaxis_transform(), fontsize=12, color='#333333', family='sans-serif')

# Tidy up spines and borders; keep a neutral, journalistic style
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Ensure good layout
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save high-resolution image (uncomment to write file)
# fig.savefig("budget_balance_spain_ez_1999_2014.png", dpi=300)

plt.savefig("generated/spain_factor2_bar8/spain_factor2_bar8_design.png", dpi=300, bbox_inches="tight")