import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])
diff = spain - ez

# Colors
color_spain = "#1f77b4"   # deep blue
color_ez = "#ff7f0e"      # muted orange
color_pos = "#2ca02c"     # green for spain > EZ
color_neg = "#d62728"     # red for spain < EZ

# Figure and axis
fig, ax = plt.subplots(figsize=(11, 6))
plt.subplots_adjust(top=0.84, right=0.88, left=0.10, bottom=0.12)

# Plot lines
ax.plot(years, spain, color=color_spain, linewidth=2, zorder=5)
ax.plot(years, ez, color=color_ez, linewidth=2, zorder=5)

# Plot markers with white halo
ax.scatter(years, spain, s=36, color=color_spain, edgecolor='white', linewidth=1, zorder=6)
ax.scatter(years, ez, s=36, color=color_ez, edgecolor='white', linewidth=1, zorder=6)

# Base difference band (low opacity)
ax.fill_between(years, spain, ez, where=(diff>0), interpolate=True, color=color_pos, alpha=0.18, zorder=2)
ax.fill_between(years, spain, ez, where=(diff<=0), interpolate=True, color=color_neg, alpha=0.18, zorder=2)

# Overlay segmented fills with alpha scaled by magnitude, emphasizing 2008-2010
max_abs_diff = np.max(np.abs(diff))
for i in range(len(years)-1):
    x_seg = years[i:i+2]
    y1_seg = spain[i:i+2]
    y2_seg = ez[i:i+2]
    avg_abs = np.mean(np.abs(y1_seg - y2_seg))
    # map to alpha between 0.12 and 0.30
    alpha = 0.12 + 0.18 * (avg_abs / max_abs_diff)
    # emphasize crisis years 2008-2010 a bit more
    if (x_seg.min() <= 2010 and x_seg.max() >= 2008):
        alpha = min(alpha + 0.08, 0.40)
    mid_sign = np.mean(y1_seg - y2_seg)
    color_fill = color_pos if mid_sign > 0 else color_neg
    ax.fill_between(x_seg, y1_seg, y2_seg, color=color_fill, alpha=alpha, zorder=3)

# Axes styling
ax.set_xlim(years.min()-0.6, years.max()+0.8)
ymin = -12.5
ymax = 4.5
ax.set_ylim(ymin, ymax)
ax.set_yticks([-12, -8, -4, 0, 4])
ax.set_ylabel("% of GDP", fontsize=11, color='0.2')
ax.yaxis.set_tick_params(labelsize=10, colors='0.25')
ax.xaxis.set_tick_params(labelsize=10, colors='0.25')
ax.set_xticks(years[::1])
ax.set_xticklabels([str(int(y)) for y in years], rotation=0)

# Gridlines
ax.grid(axis='y', color='0.9', linewidth=1)
ax.grid(axis='x', color='none')

# Title and subtitle
ax.set_title("Spain vs Euro‑Zone Budget", fontsize=17, fontweight='700', pad=8)
ax.text(0.5, 0.92, "Deficit/surplus (% of GDP), 1999–2014",
        transform=fig.transFigure, ha='center', va='center',
        fontsize=12, color='0.35')

# Inline end-of-line labels (no legend)
# Spain label
x_end = years[-1] + 0.3
ax.scatter([x_end-0.05], [spain[-1]], s=45, color=color_spain, edgecolor='white', linewidth=1, zorder=6)
ax.text(x_end, spain[-1], "Spain", color=color_spain, fontsize=11, va='center', fontweight='600')
# Euro-Zone label
ax.scatter([x_end-0.05], [ez[-1]-0.35], s=45, color=color_ez, edgecolor='white', linewidth=1, zorder=6)
ax.text(x_end, ez[-1]-0.35, "Euro‑Zone average", color=color_ez, fontsize=11, va='center', fontweight='500')

# Value labels for each point (staggered)
for i, (x, y_s, y_e) in enumerate(zip(years, spain, ez)):
    # Spain label
    vs = f"{y_s:.1f}%"
    # stagger above/below alternating
    offset_s = 0.55 if (i % 2 == 0) else -0.65
    label_y_s = y_s + offset_s
    bbox_kw = dict(boxstyle="round,pad=0.24", fc="white", ec=(0.92,0.92,0.92), alpha=0.9)
    txts = ax.text(x, label_y_s, vs, fontsize=9, ha='center', va='center', color='0.15', bbox=bbox_kw, zorder=8)
    # subtle connector if moved
    if abs(offset_s) > 0.001:
        ax.plot([x, x], [y_s, label_y_s - (0.06 if offset_s>0 else -0.06)], color='0.4', linewidth=0.8, alpha=0.35, zorder=7)

    # Euro-Zone label (offset opposite to avoid overlap)
    ve = f"{y_e:.1f}%"
    offset_e = -0.65 if (i % 2 == 0) else 0.55
    label_y_e = y_e + offset_e
    ax.text(x, label_y_e, ve, fontsize=9, ha='center', va='center', color='0.15', bbox=bbox_kw, zorder=8)
    if abs(offset_e) > 0.001:
        ax.plot([x, x], [y_e, label_y_e - (0.06 if offset_e>0 else -0.06)], color='0.4', linewidth=0.8, alpha=0.35, zorder=7)

# Annotations (3 anchored callouts)
# 1) 2006-2007 surplus peak (anchored to 2006/2007 Spain)
ann_xy = (2006, spain[years.tolist().index(2006)])
ann_text = "Strong surplus years for Spain (2006–07)"
ax.annotate(ann_text, xy=ann_xy, xytext=(2002.8, 3.6),
            fontsize=10, color='0.12',
            bbox=dict(boxstyle="round,pad=0.3", fc=color_spain, ec=(0.6,0.6,0.6), alpha=0.20),
            arrowprops=dict(arrowstyle="->", color=color_spain, linewidth=1, alpha=0.35),
            zorder=9)

# 2) 2009 sharp fall (Spain extreme deficit)
yr2009_idx = years.tolist().index(2009)
ann_xy2 = (2009, spain[yr2009_idx])
ann_text2 = f"Sharp fall in 2009: Spain {spain[yr2009_idx]:.1f}%"
ax.annotate(ann_text2, xy=ann_xy2, xytext=(2010.2, -9.6),
            fontsize=10, color='0.12',
            bbox=dict(boxstyle="round,pad=0.3", fc=color_neg, ec=(0.6,0.6,0.6), alpha=0.20),
            arrowprops=dict(arrowstyle="->", color=color_neg, linewidth=1, alpha=0.35),
            zorder=9)

# 3) 2014 partial recovery
ann_xy3 = (2014, spain[-1])
ann_text3 = "Partial recovery by 2014"
ax.annotate(ann_text3, xy=ann_xy3, xytext=(2010.8, -1.8),
            fontsize=10, color='0.12',
            bbox=dict(boxstyle="round,pad=0.3", fc=color_spain, ec=(0.6,0.6,0.6), alpha=0.20),
            arrowprops=dict(arrowstyle="->", color=color_spain, linewidth=1, alpha=0.35),
            zorder=9)

# Source note (bottom-left, unobtrusive)
source_text = "Source: [data source], 1999–2014. Visualization: [designer/company]"
fig.text(0.10, 0.03, source_text, fontsize=9, color='0.45')

# Tidy up spines
for spine in ['top','right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('0.85')
ax.spines['bottom'].set_color('0.85')

# Ensure layout and show
plt.tight_layout(rect=[0, 0.025, 1, 0.95])
plt.savefig("generated/spain_factor2_2_design.png", dpi=300, bbox_inches="tight")