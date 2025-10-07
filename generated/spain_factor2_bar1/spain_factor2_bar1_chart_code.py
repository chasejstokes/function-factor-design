import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib import ticker
import matplotlib as mpl

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors (accessible, contrastive)
color_spain = "#D95F02"   # burnt orange
color_ez = "#4E79A7"      # muted blue
edge_alpha = 0.9

# Setup figure
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
    "axes.grid": False
})
fig, ax = plt.subplots(figsize=(13,6))

# X positions
x = np.arange(len(years))
bar_width = 0.38
offset = bar_width / 2.0

# Background subtle highlight for 2009-2010 (largest differences)
# Determine approximate x span for 2009-2010 groups
idx_2009 = list(years).index(2009)
idx_2010 = list(years).index(2010)
x0 = x[idx_2009] - bar_width
x1 = x[idx_2010] + bar_width
ax.axvspan(x0 - 0.25, x1 + 0.25, color='grey', alpha=0.06, zorder=0)

# Bars
bars_spain = ax.bar(x - offset, spain, width=bar_width, color=color_spain,
                    edgecolor="k", linewidth=0.8, alpha=0.98, label='Spain', zorder=3)
bars_ez = ax.bar(x + offset, ez, width=bar_width, color=color_ez,
                 edgecolor="k", linewidth=0.8, alpha=0.98, label='Euro-Zone avg.', zorder=3)

# Y limits and gridlines
ymin = min(spain.min(), ez.min()) - 1.5
ymax = max(spain.max(), ez.max()) + 1.5
ax.set_ylim(ymin, ymax)
# Horizontal gridlines every 2.5 percentage points
major_step = 2.5
ax.yaxis.set_major_locator(ticker.MultipleLocator(major_step))
ax.grid(axis='y', color='#dddddd', linewidth=0.8, zorder=0)
# Emphasize zero baseline
ax.axhline(0, color='#888888', linewidth=1.6, zorder=4)

# X-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=9)
ax.tick_params(axis='x', which='both', length=0)

# Y-axis percentage formatter
def pct(x, pos):
    # Add percent sign
    return f"{x:.0f}%"
ax.yaxis.set_major_formatter(ticker.FuncFormatter(pct))
ax.tick_params(axis='y', labelsize=9)

# Title and subtitle
title_text = "Spain vs Euro‑Zone budget balance (1999–2014)"
subtitle_text = "Percent of GDP — negative = deficit"
ax.set_title(title_text, fontsize=13, fontweight='bold', pad=8)
# Subtitle via text
ax.text(0.5, 1.01, subtitle_text, transform=ax.transAxes, ha='center', va='bottom',
        fontsize=10, color='#555555')

# Remove top/right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Value labels on every bar (one decimal), above positives, below negatives
for rect in bars_spain:
    h = rect.get_height()
    xpos = rect.get_x() + rect.get_width() / 2
    label = f"{h:.1f}"
    if h >= 0:
        va = 'bottom'
        y = h + 0.12
    else:
        va = 'top'
        y = h - 0.12
    ax.text(xpos, y, label, ha='center', va=va, fontsize=8.5, zorder=6)

for rect in bars_ez:
    h = rect.get_height()
    xpos = rect.get_x() + rect.get_width() / 2
    label = f"{h:.1f}"
    if h >= 0:
        va = 'bottom'
        y = h + 0.12
    else:
        va = 'top'
        y = h - 0.12
    ax.text(xpos, y, label, ha='center', va=va, fontsize=8.5, zorder=6)

# Direct series labels near last-year bars (2014)
last_idx = -1
x_spain_last = x[last_idx] - offset
x_ez_last = x[last_idx] + offset
# small color squares
square_size = 0.018  # in axis fraction (we'll transform)
# Use annotation coordinates in data and transform with offset
ax.text(x_spain_last + 0.6, spain[last_idx], " Spain", color='#333333',
        fontsize=9, va='center', ha='left', bbox=dict(boxstyle="square,pad=0.2", facecolor='none', edgecolor='none'))
ax.scatter([x_spain_last + 0.45], [spain[last_idx]], s=90, marker='s', color=color_spain, edgecolor='k', linewidth=0.6, zorder=7)

ax.text(x_ez_last + 0.6, ez[last_idx], " Euro‑Zone avg.", color='#333333',
        fontsize=9, va='center', ha='left', bbox=dict(boxstyle="square,pad=0.2", facecolor='none', edgecolor='none'))
ax.scatter([x_ez_last + 0.45], [ez[last_idx]], s=90, marker='s', color=color_ez, edgecolor='k', linewidth=0.6, zorder=7)

# Comparative labels between pairs where abs(diff) >= 2.0 (in percentage points)
diffs = spain - ez
for i, d in enumerate(diffs):
    if abs(d) >= 2.0:
        # position between the two bars horizontally
        x_center = x[i]
        # vertical position just above the higher bar tip (for positive) or just below the less negative (for negatives),
        # aim to place in the middle of the two bar tops for clarity
        top_sp = spain[i]
        top_ez = ez[i]
        y_text = (top_sp + top_ez) / 2.0
        # Slight shift outward so not overlapping bars
        # Create rounded rectangle box
        txt = f"{d:+.1f} pp"
        bbox_props = dict(boxstyle="round,pad=0.25", fc="#ffffff", ec="#cccccc", lw=0.6, alpha=0.9)
        ax.text(x_center, y_text, txt, ha='center', va='center', fontsize=8.5, bbox=bbox_props, zorder=8)
        # draw a thin dashed connector between the two bar tops
        y0 = top_sp
        y1 = top_ez
        # Make connector slightly above/below the bars to avoid overlap
        con_y0 = y0
        con_y1 = y1
        # draw line
        ax.plot([x[i]-offset + bar_width/2.0, x[i]+offset - bar_width/2.0], [con_y0, con_y1],
                color='#888888', linestyle='--', linewidth=0.9, alpha=0.45, zorder=7)

# Focus annotations for 2006, 2009, 2014
annotations = [
    # (year index, text, xy for arrow (x,y at bar tip), text offset)
    (list(years).index(2006),
     f"Spain +{(spain[7]-ez[7]):.1f} pp vs EZ",
     (x[7]-offset, spain[7]),
     (-40, 18)),
    (list(years).index(2009),
     f"Sharp gap: Spain {spain[10]:+.1f} vs EZ {ez[10]:+.1f}",
     (x[10]-offset, spain[10]),
     (-10, -50)),
    (list(years).index(2014),
     "Improving since 2013",
     (x[15]-offset, spain[15]),
     (8, -40)),
]

for idx, text, (bx, by), (dx, dy) in annotations:
    # Convert data coords to display for bbox placement
    # We'll place text in axes fraction offset relative to data point
    # Using annotate with FancyBboxPatch via bbox in annotate
    ann = ax.annotate(
        text,
        xy=(bx, by),
        xytext=(bx + dx/72.0, by + dy/72.0),  # small offset in inches scaled to data approx
        textcoords='data',
        fontsize=9,
        ha='left' if dx>0 else 'right',
        va='center',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffffff", edgecolor="#dcdcdc", lw=0.8, alpha=0.95),
        arrowprops=dict(arrowstyle='-', connectionstyle="angle,angleA=0,angleB=90,rad=3",
                        color='#888888', linewidth=0.9, alpha=0.8),
        zorder=9
    )

# Tighten layout and add footnote
ax.text(0.01, -0.12, "Source: national & Euro‑Area fiscal data", transform=ax.transAxes,
        fontsize=8.5, color='#666666', va='bottom')

# Reduce chart margins so that right-side direct labels are visible
plt.subplots_adjust(left=0.06, right=0.95, top=0.88, bottom=0.14)

# Minor aesthetic tweaks
for spine in ['left','bottom']:
    ax.spines[spine].set_color('#aaaaaa')

# Show the plot
plt.savefig("generated/spain_factor2_bar1_design.png", dpi=300, bbox_inches="tight")