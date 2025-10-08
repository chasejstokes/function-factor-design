import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.patches import FancyBboxPatch

# Data setup (NA -> np.nan)
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
    {"year": 2014, "spain": -2.8, "euro_zone_average": np.nan},
]

years = [d["year"] for d in data]
spain_vals = np.array([d["spain"] for d in data])
ez_vals = np.array([d["euro_zone_average"] for d in data])

# Colors and styling
color_spain = "#1f5fbf"   # deep blue
color_ez = "#7f7f7f"      # medium gray
target_alpha = 0.40
target_hatch = "//"
placeholder_color = "#dcdcdc"
annotation_line_color = "#4a4a4a"

# Figure and axes - tall layout (3:4 width:height or taller)
fig_w, fig_h = 12, 16  # width x height in inches (1200x1600 px at 100 dpi)
fig = plt.figure(figsize=(fig_w, fig_h), dpi=100)
ax = fig.add_subplot(111)
plt.subplots_adjust(top=0.90, bottom=0.08, left=0.10, right=0.96)

# Fonts and text sizes
title_fontsize = 30
subtitle_fontsize = 17
tick_fontsize = 16
bar_label_fontsize = 16
annotation_fontsize = 19
delta_fontsize = 15
source_fontsize = 10
key_label_fontsize = 15

# X positions and bar widths
n = len(years)
x = np.arange(n)
group_width = 0.8
bar_width = 0.35  # about 35% of group
offset = bar_width / 2.0 + 0.01

# Draw horizontal gridlines (light, low contrast)
ax.yaxis.grid(True, color="#bfbfbf", linewidth=0.8, alpha=0.12)
ax.set_axisbelow(True)

# Plot bars: Spain and EZ
bars_spain = []
bars_ez = []
for i, yr in enumerate(years):
    sx = x[i] - offset
    ex = x[i] + offset
    sval = spain_vals[i]
    ezval = ez_vals[i]
    # Spain: if year is 2012-2014 (targets) apply hatch, alpha, dashed edge
    if yr in (2012, 2013, 2014):
        b = ax.bar(sx, sval, width=bar_width, color=color_spain, alpha=target_alpha,
                   edgecolor=color_spain, hatch=target_hatch, linewidth=1.0, zorder=3)
        # add dashed outline
        for rect in b:
            rect.set_linestyle('--')
            rect.set_linewidth(1.0)
        bars_spain.append(b[0])
    else:
        b = ax.bar(sx, sval, width=bar_width, color=color_spain, zorder=3)
        bars_spain.append(b[0])

    # Euro-zone average: if present plot, else draw thin placeholder at 0 height
    if not np.isnan(ezval):
        b2 = ax.bar(ex, ezval, width=bar_width, color=color_ez, zorder=2)
        bars_ez.append(b2[0])
    else:
        # placeholder: very thin light-gray bar so we show a marker for missing
        placeholder_height = 0.15  # small visible mark near zero
        b2 = ax.bar(ex, placeholder_height, width=bar_width * 0.6, color=placeholder_color,
                    zorder=1)
        # place a centered '—' marker
        ax.text(ex, placeholder_height + 0.1, '—', ha='center', va='bottom', fontsize=bar_label_fontsize - 2,
                color="#6a6a6a", zorder=5)
        bars_ez.append(None)

# Zero baseline emphasized
ax.axhline(0, color="#333333", linewidth=1.6, zorder=4)

# Axis ticks and limits
# Determine y-limits with padding for labels and annotations
all_vals = np.concatenate([spain_vals, ez_vals[~np.isnan(ez_vals)]])
ymin = math.floor(min(all_vals.min(), -12) - 3)  # ensure room for -11.2 spike
ymax = math.ceil(max(all_vals.max(), 3) + 3)
ax.set_ylim(ymin, ymax)

# Y ticks every 2 percentage points if range permits, else 4
range_span = ymax - ymin
if range_span <= 20:
    yticks_step = 2
else:
    yticks_step = 4
yticks = np.arange(ymin, ymax + 0.1, yticks_step)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t:.0f}%" for t in yticks], fontsize=tick_fontsize)

# X ticks: show every year label; rotate only if necessary
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=tick_fontsize)
plt.setp(ax.get_xticklabels(), rotation=0, ha='center')

# In-chart value labels (one per bar) placed at tip
for i, yr in enumerate(years):
    sx = x[i] - offset
    ex = x[i] + offset
    sval = spain_vals[i]
    ezval = ez_vals[i]
    # Spain label
    sval_text = f"{sval:+.1f}%"
    # Place label outside tip: above for positive, below for negative
    if sval >= 0:
        va = 'bottom'
        ytext = sval + 0.25
    else:
        va = 'top'
        ytext = sval - 0.25
    ax.text(sx, ytext, sval_text, ha='center', va=va, fontsize=bar_label_fontsize, color='white' if sval>0 else 'white',
            bbox=dict(boxstyle="round,pad=0.2", facecolor=(0,0,0,0), edgecolor='none'))
    # Euro-zone label or placeholder
    if not np.isnan(ezval):
        ez_text = f"{ezval:+.1f}%"
        if ezval >= 0:
            va_e = 'bottom'
            ytext_e = ezval + 0.25
        else:
            va_e = 'top'
            ytext_e = ezval - 0.25
        ax.text(ex, ytext_e, ez_text, ha='center', va=va_e, fontsize=bar_label_fontsize, color='black')
    else:
        # small "No data" near the placeholder
        ax.text(ex, 0.45, "No data", ha='center', va='bottom', fontsize=12, color="#6a6a6a")

# Integrated key at top-left inside plotting area (small color chips)
key_x = ax.get_xlim()[0] + 0.02 * (ax.get_xlim()[1] - ax.get_xlim()[0])
key_y = ymax - (0.06 * (ymax - ymin))
chip_w = 0.7  # in data units (x-axis)
chip_h = (ymax - ymin) * 0.035
# Draw chips using axes coordinates transformed to data coordinates
trans = ax.transData
# Spain chip
rect_spain = patches.Rectangle((x[0]-0.9, key_y), width=0.7, height=chip_h, transform=trans, color=color_spain)
ax.add_patch(rect_spain)
ax.text(x[0]-0.9 + 1.0, key_y + chip_h / 2.0, "Spain", va='center', fontsize=key_label_fontsize, color="#111111")
# EZ chip
rect_ez = patches.Rectangle((x[0]-0.9, key_y - chip_h*1.7), width=0.7, height=chip_h, transform=trans, color=color_ez)
ax.add_patch(rect_ez)
ax.text(x[0]-0.9 + 1.0, key_y - chip_h*1.7 + chip_h / 2.0, "Euro‑Zone average", va='center', fontsize=key_label_fontsize, color="#111111")

# Annotations (3–5 interpretive) with thin connectors
# 1) 2005–2007 overperformance (attach to 2006 Spain bar cluster)
i_2006 = years.index(2006)
x_anchor = x[i_2006] - offset  # Spain bar
y_anchor = spain_vals[i_2006]
ax.annotate("Spain surplus while\nEZ averages remain negative",
            xy=(x_anchor, y_anchor), xycoords='data',
            xytext=(x_anchor - 1.8, y_anchor + 6.5),
            textcoords='data',
            fontsize=annotation_fontsize, ha='left', va='bottom',
            arrowprops=dict(arrowstyle="-", linewidth=0.9, color=annotation_line_color, alpha=0.35))

# 2) 2009 crisis spike (attach to 2009 Spain bar)
i_2009 = years.index(2009)
x_anchor = x[i_2009] - offset
y_anchor = spain_vals[i_2009]
ax.annotate("Sharp Spain deficit during\nglobal crisis (2008–2011)",
            xy=(x_anchor, y_anchor), xycoords='data',
            xytext=(x_anchor + 1.2, y_anchor - 6.0),
            textcoords='data',
            fontsize=annotation_fontsize, ha='left', va='top',
            arrowprops=dict(arrowstyle="->", linewidth=0.9, color=annotation_line_color, alpha=0.4))

# 3) 2012–2014 targets note (attached to 2014 target cluster)
i_2014 = years.index(2014)
x_anchor = x[i_2014] + offset  # near EZ/target cluster
y_anchor = spain_vals[i_2014]
ax.annotate("Targets, not outturns — policy objectives",
            xy=(x_anchor - 0.3, y_anchor), xycoords='data',
            xytext=(x_anchor - 2.0, y_anchor + 4.5),
            textcoords='data',
            fontsize=annotation_fontsize, ha='left', va='bottom',
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=annotation_line_color, alpha=0.35))

# 4) Short delta annotation example for 2009 (explicit wording anchored)
# We'll also create small delta boxes (rounded) for 2005, 2009, 2010, 2014
delta_years = [2005, 2009, 2010, 2014]
for dy in delta_years:
    i = years.index(dy)
    sx = spain_vals[i]
    ez = ez_vals[i]
    # Choose x location slightly above group
    xpos = x[i]
    # compute difference if possible
    if not np.isnan(ez):
        diff = sx - ez
        # format sign
        sign_pref = f"{diff:+.1f}"
        text = f"Spain − EZ = {sign_pref} pp"
    else:
        text = "Spain − EZ = n/a"
    # position delta box above clusters with slight vertical offset depending on value
    y_box = max(sx, (ez if not np.isnan(ez) else 0)) + 2.5
    # draw a subtle rounded rectangle background using FancyBboxPatch
    bbox = FancyBboxPatch((xpos - 0.9, y_box - 0.8),
                          width=1.8, height=1.2,
                          boxstyle="round,pad=0.3",
                          linewidth=0.5, facecolor=(0.2, 0.2, 0.2, 0.06),
                          edgecolor=(0.2, 0.2, 0.2, 0.12),
                          mutation_aspect=1.0, zorder=6)
    ax.add_patch(bbox)
    ax.text(xpos, y_box - 0.15, text, ha='center', va='center', fontsize=delta_fontsize, color="#111111", zorder=7)

# Additional specific delta-style callout for 2009 to echo the example
# Place an explanatory short line
i9 = years.index(2009)
sp9 = spain_vals[i9]
ez9 = ez_vals[i9]
if not np.isnan(ez9):
    diff9 = sp9 - ez9
    ax.text(x[i9] + 1.7, sp9 - 1.5, f"Spain {sp9:+.1f}% vs EZ {ez9:+.1f}% → Spain {diff9:+.1f} pp worse",
            fontsize=14, color="#222222", ha='left', va='center')

# Annotation about missing EZ data for 2012–2014
ax.annotate("EZ average not available for 2012–2014",
            xy=(x[13], 0.2), xycoords='data',
            xytext=(x[12] - 3.0, 1.8),
            textcoords='data',
            fontsize=annotation_fontsize - 2, ha='left', va='bottom',
            arrowprops=dict(arrowstyle="-", linewidth=0.8, color=annotation_line_color, alpha=0.35))

# Title and subtitle at top center
fig.suptitle("Spain vs Euro‑Zone Budget", fontsize=title_fontsize, fontweight='bold', y=0.985)
ax.set_title("General government balance (% of GDP), 1999–2014. Last three Spain values are targets.",
             fontsize=subtitle_fontsize, fontweight='regular', loc='center', pad=14)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# Keep left and bottom
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Source / note line at bottom
source_text = "Data: [source]. Spain 2012–2014 are policy targets."
fig.text(0.10, 0.03, source_text, fontsize=source_fontsize, color="#555555")

# Tight layout adjustments (preserve space for annotations)
plt.draw()
plt.savefig("generated/spain_factor2_bar3/spain_factor2_bar3_design.png", dpi=300, bbox_inches="tight")