import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.lines import Line2D

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Figure layout (portrait 3:4 ratio)
fig, ax = plt.subplots(figsize=(9, 12))
plt.subplots_adjust(top=0.88, bottom=0.12, left=0.12, right=0.95)

# Font settings (sans-serif preference)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Arial', 'Helvetica', 'DejaVu Sans']
title_fs = 28
subtitle_fs = 18
axis_title_fs = 17
tick_fs = 13
annot_fs = 15

# Bar settings
x = np.arange(len(years))
bar_width = 0.38
offset = bar_width / 2.0
color_spain = "#1f77b4"     # medium blue
color_ez = "#8c8c8c"        # neutral gray for Euro-Zone average

# Crisis period band: 2008-2011 (inclusive)
# Determine span in x coordinates: span from mid between 2007 and 2008 to mid between 2011 and 2012
left_span = x[np.where(years==2008)[0][0]] - 0.5
right_span = x[np.where(years==2011)[0][0]] + 0.5
ax.axvspan(left_span, right_span, color='#ffd8b5', alpha=0.22, zorder=0)  # light warm band

# Draw bars
bars_spain = ax.bar(x - offset, spain, width=bar_width, color=color_spain, label='Spain', zorder=3)
bars_ez = ax.bar(x + offset, ez, width=bar_width, color=color_ez, label='Euro‑Zone average', zorder=3)

# Zero line emphasized
ax.axhline(0, color='0.15', linewidth=1.8, zorder=4)

# Y-axis ticks and gridlines
y_ticks = [-12, -10, -8, -6, -4, -2, 0, 2, 4]
ax.set_yticks(y_ticks)
ax.set_ylim(-12.6, 4.5)
ax.yaxis.grid(True, color='#bfbfbf', linestyle='-', linewidth=0.8, alpha=0.35, zorder=0)

# X-axis ticks (every year)
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=tick_fs, rotation=0)
ax.set_xlabel("Year", fontsize=axis_title_fs, labelpad=12)

# Y-axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=axis_title_fs, labelpad=12)

# Title and subtitle
fig.suptitle("Spain vs Euro‑Zone Average — Budget balance (% of GDP), 1999–2014",
             fontsize=title_fs, fontweight='bold', y=0.96)
fig.text(0.5, 0.925,
         "Sharp outperformance in the mid‑2000s (2004–2007), followed by much larger Spanish deficits during the 2008–2011 financial crisis.",
         ha='center', va='center', fontsize=subtitle_fs)

# Legend (inside plot, top-right)
legend_elements = [
    patches.Patch(facecolor=color_spain, edgecolor='none', label='Spain'),
    patches.Patch(facecolor=color_ez, edgecolor='none', label='Euro‑Zone average')
]
leg = ax.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=13, title=None,
                bbox_to_anchor=(0.98, 0.98))
leg.get_frame().set_edgecolor('#dddddd')
leg.get_frame().set_linewidth(0.8)
for text in leg.get_texts():
    text.set_fontweight('bold')

# Selective annotations for key years with subtle leader lines
annotations = {
    2004: "Spain – EZ = +3.5 pp",
    2005: "Spain – EZ = +3.1 pp",
    2009: "Spain – EZ = -4.9 pp",
    2010: "Spain – EZ = -3.5 pp"
}

# Compute annotation positions and draw
for yr, txt in annotations.items():
    idx = np.where(years == yr)[0][0]
    x_center = x[idx]
    sp_val = spain[idx]
    ez_val = ez[idx]
    # place annotation slightly above the less-negative (higher) bar
    top_bar = max(sp_val, ez_val)
    if top_bar >= 0:
        y_ann = top_bar + 0.9
        va = 'bottom'
    else:
        y_ann = top_bar + 1.2
        va = 'bottom'
    # Slight horizontal offset to avoid overlapping bars
    x_ann = x_center + 0.55
    # Leader line pointing to the group center
    ax.annotate(txt,
                xy=(x_center, top_bar), xycoords='data',
                xytext=(x_ann, y_ann), textcoords='data',
                fontsize=annot_fs, color='0.05',
                va=va, ha='left',
                arrowprops=dict(arrowstyle='-',
                                connectionstyle="angle3,angleA=0,angleB=90",
                                color='0.35', linewidth=0.8),
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.0))

# Crisis period label inside band (small text above middle of band)
mid_span = (left_span + right_span) / 2.0
ax.text(mid_span, ax.get_ylim()[1] - 0.6, "2008–2011 crisis period",
        ha='center', va='top', fontsize=11, color='0.15', alpha=0.9, backgroundcolor='none')

# Aggregated synthesis box (lower-right inside axes)
synthesis_text = "1999–2007 mean: Spain ≈ +1.4 pp vs EZ • 2008–2014 mean: Spain ≈ -2.0 pp vs EZ • Full period mean ≈ -0.1 pp."
bbox_props = dict(boxstyle="round,pad=0.6", fc="white", ec="#dddddd", lw=0.8, alpha=0.95)
ax.text(0.98, 0.06, synthesis_text, transform=ax.transAxes,
        fontsize=12.5, ha='right', va='bottom', color='0.05', bbox=bbox_props)

# Context sentence below the chart (outside axes)
fig.text(0.5, 0.045,
         "Data show Spain moving from mid‑2000s surpluses to much larger deficits during the financial crisis; comparisons are in percentage points of GDP.",
         ha='center', va='center', fontsize=12, color='0.05')

# Tidy up spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')

# Ensure bars are on top of grid and band
for bar in bars_spain + bars_ez:
    bar.set_zorder(3)

# Display at high resolution appropriate for slides
plt.savefig("generated/spain_factor4_bar7/spain_factor4_bar7_design.png", dpi=300, bbox_inches="tight")