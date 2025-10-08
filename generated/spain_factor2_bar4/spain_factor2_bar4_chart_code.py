import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib as mpl

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain_vals = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Euro-zone has missing data for 2012-2014
euro_vals = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Visual constants
spain_color = "#1f77b4"        # medium-dark blue
euro_color = "#7f8c8d"         # muted slate/gray-blue
annotation_border = "#333232"  # dark neutral for annotation boxes
bg_color = "white"
fig_w, fig_h = 9, 12           # inches (portrait 3:4)
bar_width = 0.38

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "axes.edgecolor": "#333333",
})

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

x = np.arange(len(years))
x_spain = x - bar_width/2
x_euro = x + bar_width/2

# Y-axis limits and gridlines
ymin, ymax = -12.5, 3.0
ax.set_ylim(ymin, ymax)
ax.set_xlim(-0.6, len(years)-0.4)
ax.set_yticks(np.arange(-12, 4, 2))
ax.set_ylabel("Budget balance (% of GDP)", fontsize=22)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='x', labelsize=18)

# Strong zero baseline
ax.axhline(0, color="#222222", linewidth=1.8, zorder=1)

# Subtle horizontal gridlines
for y in np.arange(-12, 4, 2):
    ax.axhline(y, color="#e6e6e6", linewidth=0.9, zorder=0)

# Highlight band behind 2012-2014 to indicate targets
# Indices 2012->index 13, 2013->14, 2014->15
targets_start_idx = 13
targets_end_idx = 15
# Compute rectangle extents in x data coordinates: from left edge of 2012 Spain bar to right edge of 2014 euro slot
rect_x = x_spain[targets_start_idx] - 0.02
rect_width = (x_euro[targets_end_idx] + bar_width/2) - rect_x + 0.02
rect = Rectangle(
    (rect_x, ymin), rect_width, ymax - ymin,
    linewidth=1.0, edgecolor="#666666", facecolor="#cbd5e1", alpha=0.07,
    linestyle='dashed', zorder=0
)
ax.add_patch(rect)
# Label for target band
ax.text(
    (rect_x + rect_x + rect_width) / 2, ymax - 0.6, "Targets",
    ha="center", va="top", fontsize=18, color="#333333", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.0)
)

# Plot Spain bars. For target years, use lighter fill + hatch and dashed edge to indicate targets.
bars_spain = []
for i, (xp, val) in enumerate(zip(x_spain, spain_vals)):
    if i >= targets_start_idx:  # target years (2012-2014)
        b = ax.bar(xp, val, width=bar_width, color=spain_color, alpha=0.72,
                   edgecolor=spain_color, linewidth=1.2, hatch='////', zorder=3)
        # Add a dashed edge by overlaying a rectangle (thin) - using bar's edge style
        # Matplotlib draws hatch over facecolor; keep it subtle
    else:
        b = ax.bar(xp, val, width=bar_width, color=spain_color, zorder=3)
    bars_spain.append(b[0])

# Plot Euro-zone bars only where data exists
bars_euro = []
for i, (xe, val) in enumerate(zip(x_euro, euro_vals)):
    if not np.isnan(val):
        b = ax.bar(xe, val, width=bar_width, color=euro_color, zorder=2)
        bars_euro.append((i, b[0]))
    else:
        # Draw a very pale dashed vertical filler to indicate missing data slot (very light)
        filler = Rectangle(
            (xe - bar_width/2, ymin * 0.05), bar_width, (ymax - ymin)*0.015 + 0.001,
            facecolor=euro_color, alpha=0.04, hatch=None, linewidth=1.0,
            edgecolor=euro_color, linestyle='dashed', zorder=1
        )
        ax.add_patch(filler)
        bars_euro.append((i, None))

# X-axis labels
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=18)

# Inline small series labels near the first bars
# Spain label inside first Spain bar
first_spain_bar = bars_spain[0]
sp_height = first_spain_bar.get_height()
sp_x = first_spain_bar.get_x() + first_spain_bar.get_width()/2
# Place label slightly above center of bar if there's space, else above bar
if sp_height < 0:
    txt_y = sp_height - 0.25
    va = 'top'
else:
    txt_y = sp_height / 2
    va = 'center'
ax.text(sp_x, txt_y, "Spain", color="white", fontsize=12, ha="center", va=va, fontweight='bold', zorder=6)

# Euro-zone label adjacent to first euro bar (if bar exists)
first_euro_idx, first_euro_bar = bars_euro[0]
if first_euro_bar is not None:
    eu_height = first_euro_bar.get_height()
    eu_x = first_euro_bar.get_x() + first_euro_bar.get_width()/2
    # place label inside if enough vertical space and contrast, else above
    if eu_height > 0.8:
        ax.text(eu_x, eu_height/2, "Euro‑Zone avg", color="white", fontsize=12, ha="center", va="center", fontweight='regular', zorder=6)
    else:
        ax.text(eu_x, eu_height + 0.2, "Euro‑Zone avg", color=euro_color, fontsize=12, ha="center", va="bottom", fontweight='regular', zorder=6)
else:
    # place adjacent near the first euro slot top area
    eu_xslot = x_euro[0]
    ax.text(eu_xslot, ymax - 0.6, "Euro‑Zone avg", color=euro_color, fontsize=12, ha="center", va="top", fontweight='regular')

# Data labels on each Spain bar
for i, bar in enumerate(bars_spain):
    h = bar.get_height()
    xloc = bar.get_x() + bar.get_width()/2
    # Format label, add (target) suffix for last three years
    if i >= targets_start_idx:
        label = f"{h:.1f}% (target)"
    else:
        label = f"{h:.1f}%"
    if h >= 0:
        yloc = h + 0.25
        va = 'bottom'
    else:
        yloc = h - 0.35
        va = 'top'
    ax.text(xloc, yloc, label, ha="center", va=va, fontsize=16, fontweight='bold', color="#111111", zorder=7)

# Data labels on Euro bars (or 'n/a' for missing)
for (i, bar) in bars_euro:
    xslot = x_euro[i]
    if bar is not None:
        h = bar.get_height()
        label = f"{h:.1f}%"
        if h >= 0:
            yloc = h + 0.25
            va = 'bottom'
        else:
            yloc = h - 0.35
            va = 'top'
        ax.text(xslot, yloc, label, ha="center", va=va, fontsize=16, fontweight='bold', color="#111111", zorder=6)
    else:
        # Place a small "n/a" label where bar would be
        ax.text(xslot, -0.4, "n/a", ha="center", va="top", fontsize=14, color="#666666", fontstyle='italic', zorder=5)

# Annotations (verbatim texts required)
# 1. 2009 crisis annotation anchored to Spain 2009 bar
year_idx_2009 = list(years).index(2009)
bar_2009 = bars_spain[year_idx_2009]
x_2009 = bar_2009.get_x() + bar_2009.get_width() + 0.15
y_2009 = bar_2009.get_height() - 1.0  # position above the negative bar (more negative)
ax.annotate(
    "2009: Spain deficit reaches -11.2% — largest gap of the period vs. Euro‑Zone.",
    xy=(bar_2009.get_x() + bar_2009.get_width()/2, bar_2009.get_height()),
    xytext=(x_2009, -6.0),
    fontsize=18, color=annotation_border,
    ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color=annotation_border, lw=1.2, shrinkA=2, shrinkB=5),
    bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=annotation_border, lw=0.9, alpha=0.95),
    zorder=9
)

# 2. Mid-2000s divergence (2005–2007)
# We'll place the annotation above the cluster 2005-2007
start_idx = list(years).index(2005)
end_idx = list(years).index(2007)
cluster_x = (x_spain[start_idx] + x_euro[end_idx]) / 2
ax.annotate(
    "2005–2007: Spain ran surpluses while the Euro‑Zone remained in deficit.",
    xy=(cluster_x, 2.6),
    xytext=(cluster_x, 2.6),
    fontsize=18, color=annotation_border, ha="center",
    bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=annotation_border, lw=0.9, alpha=0.98),
    arrowprops=dict(arrowstyle="-", color=annotation_border, lw=1.0, shrinkA=0, shrinkB=0),
    zorder=9
)
# Draw a thin bracket-like line under the annotation to visually span the 2005-2007 cluster
ax.plot([x_spain[start_idx]-0.1, x_euro[end_idx]+0.1], [2.45, 2.45], color=annotation_border, linewidth=1.0, zorder=8)

# 3. Missing Euro‑Zone data after 2011 and targets explanation spanning 2012-2014
ax.annotate(
    "2012–2014: Spain national targets. Euro‑Zone average data unavailable after 2011.",
    xy=(x_spain[targets_start_idx] + (rect_width/4), ymax - 1.2),
    xytext=(x_spain[targets_start_idx] + 0.6, ymax - 1.2),
    fontsize=18, color=annotation_border,
    ha="left", va="top",
    bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=annotation_border, lw=0.9, alpha=0.98),
    arrowprops=dict(arrowstyle="->", color=annotation_border, lw=1.0, shrinkA=2, shrinkB=8),
    zorder=9
)

# 4. Zero baseline explanation near y=0 axis
ax.text(
    -0.3, 0.18, "Positive = surplus; Negative = deficit.",
    fontsize=18, color="#333333", va="bottom", ha="left", bbox=dict(fc="white", ec="none", alpha=0.0), zorder=10
)

# Chart title (short)
ax.set_title("Spain vs Euro‑Zone Budget Balance (%)", fontsize=36, fontweight='bold', pad=18)

# Slight layout adjustments
plt.subplots_adjust(top=0.94, bottom=0.06, left=0.10, right=0.98)

# Turn off the frame spines on top and right for a clean look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Ensure ticks go across bottom only
ax.xaxis.set_tick_params(length=6)
ax.yaxis.set_tick_params(length=6)

# Show plot
plt.savefig("generated/spain_factor2_bar4/spain_factor2_bar4_design.png", dpi=300, bbox_inches="tight")