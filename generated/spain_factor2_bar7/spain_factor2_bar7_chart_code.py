import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib as mpl
import numpy as np

# Data
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Styling and fonts
mpl.rcParams['font.family'] = 'DejaVu Sans'
title_fs = 30
subtitle_fs = 18
axis_label_fs = 18
tick_label_fs = 15
data_label_fs = 16
annotation_fs = 14
source_fs = 11

# Colors
color_spain = '#1f5fa8'  # deep blue
color_euro = '#6e6e6e'   # neutral dark gray
zero_line_color = '#7f7f7f'
annotation_box_edge = '#999999'

# Figure size: portrait 900x1200 px equivalent (9 x 12 inches at 100 DPI)
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

n = len(years)
ind = np.arange(n)  # group positions
width = 0.35  # width of each bar

# Bar positions (Spain left, Euro right)
pos_spain = ind - width/2
pos_euro = ind + width/2

# Draw rounded bars manually using FancyBboxPatch for small rounding
def draw_rounded_bar(ax, x, y, w, height, color, rounding_size=2):
    # y is bottom (could be negative), height is absolute height (positive)
    # Use FancyBboxPatch for rounded corners
    box = mpatches.FancyBboxPatch(
        (x, y),
        w,
        height,
        boxstyle=mpatches.BoxStyle("Round", pad=0.02, rounding_size=rounding_size),
        linewidth=0,
        facecolor=color,
        edgecolor=color
    )
    ax.add_patch(box)

# Plot bars
for xi, h in zip(pos_spain, spain):
    bottom = min(0, h)
    height = abs(h)
    draw_rounded_bar(ax, xi, bottom, width, height, color_spain, rounding_size=2)

for xi, h in zip(pos_euro, euro):
    bottom = min(0, h)
    height = abs(h)
    draw_rounded_bar(ax, xi, bottom, width, height, color_euro, rounding_size=2)

# X-axis: years as ticks
ax.set_xticks(ind)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=tick_label_fs)
ax.tick_params(axis='x', which='major', pad=8)

# Y-axis: percent of GDP
ax.set_ylabel('Percent of GDP', fontsize=axis_label_fs)
ax.set_ylim(-12.5, 4.0)
ax.set_yticks(np.arange(-12, 4, 2))
ax.set_yticklabels([f'{int(t)}%' for t in np.arange(-12, 4, 2)], fontsize=tick_label_fs)
ax.grid(axis='y', linestyle='--', linewidth=1, color='#e6e6e6')

# Emphasize zero line
ax.axhline(0, color=zero_line_color, linewidth=1.5, zorder=5)

# Title and subtitle
plt.suptitle("Budget balance — Spain vs Euro‑Zone (1999–2014)", fontsize=title_fs, y=0.96, weight='bold')
ax_title = fig.add_axes([0, 0, 1, 1], frameon=False)
ax_title.set_xticks([])
ax_title.set_yticks([])
# Subtitle placed under the title using fig.text for precise placement
fig.text(0.5, 0.915, "Share of GDP (negative = deficit)", ha='center', va='center', fontsize=subtitle_fs, color='#333333')

# Inline series chips near the first cluster (1999) and repeat at top-right
chip_x = pos_spain[0] - 0.15
chip_y = 3.3  # near top of canvas
# Left chips near first bars
ax.add_patch(mpatches.Rectangle((chip_x - 0.05, chip_y - 0.15), 0.04, 0.04, facecolor=color_spain, transform=ax.transData, clip_on=False))
ax.text(chip_x + 0.01, chip_y - 0.13, 'Spain', fontsize=12, va='bottom', ha='left')
ax.add_patch(mpatches.Rectangle((chip_x + 0.18, chip_y - 0.15), 0.04, 0.04, facecolor=color_euro, transform=ax.transData, clip_on=False))
ax.text(chip_x + 0.24, chip_y - 0.13, 'Euro‑Zone avg.', fontsize=12, va='bottom', ha='left')

# Repeat small labels near top-right as backup
ax.add_patch(mpatches.Rectangle((ind[-1] + 0.25, chip_y - 0.15), 0.04, 0.04, facecolor=color_spain, transform=ax.transData, clip_on=False))
ax.text(ind[-1] + 0.31, chip_y - 0.13, 'Spain', fontsize=12, va='bottom', ha='left')
ax.add_patch(mpatches.Rectangle((ind[-1] + 0.48, chip_y - 0.15), 0.04, 0.04, facecolor=color_euro, transform=ax.transData, clip_on=False))
ax.text(ind[-1] + 0.54, chip_y - 0.13, 'Euro‑Zone avg.', fontsize=12, va='bottom', ha='left')

# Data labels: one decimal place with percent sign, placed at bar tip just outside the bar
for xi, h in zip(pos_spain, spain):
    if h >= 0:
        y_text = h + 0.25
        va = 'bottom'
        color = '#000000'
    else:
        y_text = h - 0.25
        va = 'top'
        color = '#000000'
    ax.text(xi + width/2, y_text, f'{h:.1f}%', ha='center', va=va, fontsize=data_label_fs, fontweight='bold')

for xi, h in zip(pos_euro, euro):
    if h >= 0:
        y_text = h + 0.25
        va = 'bottom'
        color = '#000000'
    else:
        y_text = h - 0.25
        va = 'top'
        color = '#000000'
    ax.text(xi - width/2, y_text, f'{h:.1f}%', ha='center', va=va, fontsize=data_label_fs, fontweight='bold')

# Annotations (4 anchored callouts)
bbox_props = dict(boxstyle="round,pad=0.5", fc=(1,1,1,0.78), ec=annotation_box_edge, lw=0.9)

# 1) 2004: Spain surplus vs EZ deficit — anchor to 2004 bars
i2004 = int(np.where(years == 2004)[0][0])
x_anchor_spain = pos_spain[i2004] + width/2
x_anchor_euro = pos_euro[i2004] - width/2
y_anchor_spain = spain[i2004]
y_anchor_euro = euro[i2004]
ann_text_2004 = "Spain posts a surplus (+0.6%); Euro‑Zone remains in deficit (−2.9%)."
ax.annotate(
    ann_text_2004,
    xy=(x_anchor_spain, y_anchor_spain),
    xytext=(ind[i2004]-1.2, 1.8),
    textcoords='data',
    fontsize=annotation_fs,
    va='center',
    ha='left',
    bbox=bbox_props,
    arrowprops=dict(arrowstyle='-', color='#666666', lw=1.0,
                    connectionstyle="arc3,rad=-0.15")
)

# 2) 2006: Peak Spanish surplus — anchor to 2006 Spain bar
i2006 = int(np.where(years == 2006)[0][0])
x_anchor = pos_spain[i2006] + width/2
y_anchor = spain[i2006]
ann_text_2006 = "Peak Spanish surplus (+2.4%) vs weak Euro average (+1.1%)."
ax.annotate(
    ann_text_2006,
    xy=(x_anchor, y_anchor),
    xytext=(ind[i2006]+0.6, 2.6),
    textcoords='data',
    fontsize=annotation_fs,
    va='bottom',
    ha='left',
    bbox=bbox_props,
    arrowprops=dict(arrowstyle='-', color=color_spain, lw=1.0,
                    connectionstyle="angle3,angleA=0,angleB=-90")
)

# 3) 2009–2010 crisis: bracket spanning 2009–2010 and combined note
i2009 = int(np.where(years == 2009)[0][0])
i2010 = int(np.where(years == 2010)[0][0])
# positions for bracket
left_bracket_x = pos_spain[i2009] - 0.05
right_bracket_x = pos_euro[i2010] + width + 0.05
bracket_y = -3.2
# horizontal bracket line
ax.add_line(mlines.Line2D([left_bracket_x, right_bracket_x], [bracket_y, bracket_y], color='#777777', linewidth=1.0))
# little vertical ticks at ends
ax.add_line(mlines.Line2D([left_bracket_x, left_bracket_x], [bracket_y, bracket_y+0.12], color='#777777', linewidth=1.0))
ax.add_line(mlines.Line2D([right_bracket_x, right_bracket_x], [bracket_y, bracket_y+0.12], color='#777777', linewidth=1.0))

ann_text_crisis = ("Financial crisis: Spain falls to −11.2% (2009) and remains markedly below Euro average, "
                   "highlighting sharper short‑term deterioration.")
# Place the annotation box above the bracket
ax.annotate(
    ann_text_crisis,
    xy=((left_bracket_x + right_bracket_x) / 2, bracket_y),
    xytext=(ind[i2009]-1.6, -1.6),
    textcoords='data',
    fontsize=annotation_fs,
    va='top',
    ha='left',
    bbox=bbox_props,
    arrowprops=dict(arrowstyle='-', color='#777777', lw=1.0,
                    connectionstyle="angle3,angleA=0,angleB=90")
)

# 4) 2014: Recovery trend note anchored to 2014 cluster
i2014 = int(np.where(years == 2014)[0][0])
x_anchor = ind[i2014]
y_anchor = min(spain[i2014], euro[i2014])
ann_text_2014 = "Recovery trend: deficits reduce for both; Spain at −2.5% vs Euro −2.0%."
ax.annotate(
    ann_text_2014,
    xy=(x_anchor, y_anchor),
    xytext=(ind[i2014]-2.5, 1.1),
    textcoords='data',
    fontsize=annotation_fs,
    va='center',
    ha='left',
    bbox=bbox_props,
    arrowprops=dict(arrowstyle='-', color='#666666', lw=1.0,
                    connectionstyle="arc3,rad=0.18")
)

# Fine-tune layout
ax.set_xlim(-1, n)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(False)

# Source note (bottom-right)
fig.text(0.98, 0.03, "Source: Eurostat", ha='right', va='bottom', fontsize=source_fs, color='#444444')

# Ensure layout fits
plt.subplots_adjust(top=0.88, bottom=0.06, left=0.12, right=0.95)

plt.savefig("generated/spain_factor2_bar7/spain_factor2_bar7_design.png", dpi=300, bbox_inches="tight")