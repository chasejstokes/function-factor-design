import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np

# Data
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Figure settings
fig_w, fig_h = 9, 12  # inches (900x1200 px at 100 dpi)
fig = plt.figure(figsize=(fig_w, fig_h), dpi=100)
ax = fig.add_axes([0.12, 0.12, 0.82, 0.80])  # left, bottom, width, height

# Fonts and style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
title_fontsize = 30
subtitle_fontsize = 18
axis_label_fontsize = 18
tick_fontsize = 18
value_label_fontsize = 22
annotation_fontsize = 18

# Colors (colorblind-safe-ish): Spain = blue, Euro = warm brown/orange
color_spain = '#1f78b4'  # medium blue
color_euro = '#b35806'   # warm orange-brown
bar_edge = '#666666'

# X positions and bar widths
x = np.arange(len(years))
bar_w = 0.38
offset = bar_w / 2.0

# Background rectangle for 2009 pair highlight (largest divergence)
# Find index of 2009 and 2006 for other halo
idx_2009 = int(np.where(years == 2009)[0][0])
idx_2006 = int(np.where(years == 2006)[0][0])

# Draw vertical translucent highlight band for 2009 (covering both bars)
band_width = 0.9
band_center = x[idx_2009]
band_left = band_center - band_width / 2.0
rect = mpatches.Rectangle((band_left - 0.15, -12.5), band_width + 0.3, 15.5,
                          transform=ax.transData, facecolor='#f9e6e0', edgecolor='none', zorder=0, alpha=0.35)
ax.add_patch(rect)

# Small halo behind 2006 Spain bar (circle)
halo = mpatches.Ellipse((x[idx_2006] - offset, spain[idx_2006] + 0.2), width=0.9, height=1.4,
                        facecolor='#eaf4ff', edgecolor='none', alpha=0.6, zorder=1)
ax.add_patch(halo)

# Bars
bars_spain = ax.bar(x - offset, spain, width=bar_w, color=color_spain,
                    edgecolor=bar_edge, linewidth=1.0, zorder=3)
bars_euro = ax.bar(x + offset, euro, width=bar_w, color=color_euro,
                   edgecolor=bar_edge, linewidth=1.0, zorder=3)

# Y-axis limits and ticks
ax.set_ylim(-12, 3)
yticks = np.arange(-12, 4, 1)  # integers
ax.set_yticks(yticks)
ax.yaxis.set_major_locator(mticker.FixedLocator(yticks))
ax.grid(axis='y', which='major', color='#cccccc', linestyle='-', linewidth=0.7, alpha=0.7, zorder=0)

# X-axis labels
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=tick_fontsize)
# If spacing tight, could show every other year; here we show every year as requested.

# Unit label near Y axis (concise)
# Place small vertical text to the left of the axis
fig.text(0.05, 0.55, "Balance (% of GDP)", rotation='vertical', fontsize=14, va='center')

# Title and subtitle
fig.text(0.5, 0.965, "Budget balance: Spain vs Euro‑Zone (1999–2014)",
         ha='center', va='top', fontsize=title_fontsize, fontweight='medium')
fig.text(0.5, 0.934, "Balance as % of GDP — positive = surplus, negative = deficit.",
         ha='center', va='top', fontsize=subtitle_fontsize, color='#222222')

# Direct small series key in upper-right of plotting area (discrete, minimal)
key_x = 0.98
key_y = 0.92
fig.text(key_x, key_y, '\u25A0 Spain', color=color_spain, fontsize=14, ha='right', va='center',
         transform=fig.transFigure)
fig.text(key_x, key_y - 0.03, '\u25A0 Euro‑Zone avg.', color=color_euro, fontsize=14, ha='right', va='center',
         transform=fig.transFigure)

# Numeric labels on each bar (centered above for positives, just inside top edge for negatives)
for xi, val in zip(x - offset, spain):
    txt = f"{val:.1f}"
    if val >= 0:
        ytxt = val + 0.25
        color_txt = 'black'
        va = 'bottom'
    else:
        # place label slightly inside the top of the negative bar (towards zero), white for contrast
        ytxt = val + 0.25
        color_txt = 'white'
        va = 'bottom'
    ax.text(xi, ytxt, txt, ha='center', va=va, fontsize=value_label_fontsize,
            fontweight='bold' if val <= -9 or val >= 2 else 'normal', color=color_txt, zorder=6)

for xi, val in zip(x + offset, euro):
    txt = f"{val:.1f}"
    if val >= 0:
        ytxt = val + 0.25
        color_txt = 'black'
        va = 'bottom'
    else:
        ytxt = val + 0.25
        color_txt = 'white'
        va = 'bottom'
    ax.text(xi, ytxt, txt, ha='center', va=va, fontsize=value_label_fontsize,
            fontweight='normal', color=color_txt, zorder=6)

# Annotations (anchored with thin connectors and rounded boxes)
# 2006: Spain surplus callout
idx = idx_2006
x_spain_2006 = x[idx] - offset
y_spain_2006 = spain[idx]
ann_x = x_spain_2006 + 0.6  # place box to the right
ann_y = y_spain_2006 + 1.8
bbox_props = dict(boxstyle="round,pad=0.6", fc="white", ec="none", alpha=0.95)
ann_text = "2006: Spain posts surplus (+2.4) while Euro avg ≈ +1.1."
ax.annotate(ann_text, xy=(x_spain_2006, y_spain_2006), xytext=(ann_x, ann_y),
            fontsize=annotation_fontsize, ha='left', va='center',
            arrowprops=dict(arrowstyle="-", color='#666666', linewidth=1.0),
            bbox=bbox_props, zorder=8)

# 2009-2010 cluster annotation (highlight + callout)
# Position box above band
band_box_x = x[idx_2009]
band_box_y = -1.5
ann2_text = r"2009–10: Spain’s deficit far exceeds Euro avg ($\mathbf{-11.2}$ vs $\mathbf{-6.3}$) — peak divergence."
ax.annotate(ann2_text, xy=(x[idx_2009] + 0.1, spain[idx_2009]), xytext=(x[idx_2009] + 1.2, band_box_y),
            fontsize=annotation_fontsize, ha='left', va='center',
            arrowprops=dict(arrowstyle="-", color='#666666', linewidth=1.0),
            bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="none", alpha=0.95),
            zorder=9)

# 2014 annotation: partial recovery
idx = int(np.where(years == 2014)[0][0])
x_spain_2014 = x[idx] - offset
y_spain_2014 = spain[idx]
ann3_text = "2014: gap narrowed (Spain −2.5, Euro −2.0)."
ax.annotate(ann3_text, xy=(x_spain_2014, y_spain_2014), xytext=(x_spain_2014 + 1.0, y_spain_2014 + 2.0),
            fontsize=annotation_fontsize, ha='left', va='center',
            arrowprops=dict(arrowstyle="-", color='#666666', linewidth=1.0),
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="none", alpha=0.95),
            zorder=8)

# Styling tweaks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)  # clean left spine; ticks suffice
ax.spines['bottom'].set_color('#333333')
ax.tick_params(axis='y', which='major', labelsize=tick_fontsize)
ax.tick_params(axis='x', which='major', labelsize=tick_fontsize)

# Minor ticks as small markers for intermediate years (visual subtlety)
ax.xaxis.set_minor_locator(mticker.FixedLocator(x + 0.0))
# Remove minor tick labels, but keep ticks if desired (leave them off to avoid clutter)

# Ensure layout tight and readable
plt.subplots_adjust(top=0.92, bottom=0.07, left=0.08, right=0.96)

# Save high-resolution output suitable for slides (300 dpi)
plt.savefig("spain_vs_eurozone_balance_1999_2014.png", dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig("generated/spain_factor2_bar6/spain_factor2_bar6_design.png", dpi=300, bbox_inches="tight")