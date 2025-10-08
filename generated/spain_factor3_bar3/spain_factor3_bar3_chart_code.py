import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.lines import Line2D

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use np.nan for unavailable euro-zone averages (2012-2014)
euro_zone = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Highlight years (for Δ labels and annotations)
delta_years = [2005, 2006, 2009, 2010, 2011]
annotation_points = {
    2006: {"text": "Spain surpluses mid-2000s", "xy_year": 2006},
    2009: {"text": "Sharp deterioration after 2007 crisis", "xy_year": 2009},
    2013: {"text": "Targets, not actuals (2012–2014)", "xy_year": 2013}
}
circle_years = [2006, 2009, 2014]  # add halos on these years

# Colors and style
color_spain = "#C0392B"   # deep red
color_ez = "#2E86AB"      # teal/blue
neutral_gray = "#666666"
bg_color = "white"

# Figure: portrait 3:4 aspect ratio. Use inches such that DPI*size ~ 900x1200, but figsize in inches suffices.
fig = plt.figure(figsize=(7.5, 10))  # approx 900x1200 px at 120 dpi
# Use GridSpec to create main chart and right-side summary box
gs = fig.add_gridspec(nrows=1, ncols=12, left=0.06, right=0.98, top=0.92, bottom=0.10, wspace=0.02)
ax = fig.add_subplot(gs[:, :9])   # main plotting area (larger)
side_ax = fig.add_subplot(gs[:, 10:12])  # summary box area (narrow)
side_ax.axis("off")

# Font settings
title_fontsize = 32
subtitle_fontsize = 15
axis_label_fontsize = 18
tick_fontsize = 14
annotation_fontsize = 16
summary_fontsize = 16
metadata_fontsize = 12
legend_fontsize = 16

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Helvetica']

# X positions for grouped bars
x = np.arange(len(years))
group_width = 0.8
bar_width = 0.35  # approx 35-40% of group width
inter_gap = 0.05

left_positions = x - (bar_width/2 + inter_gap/2)
right_positions = x + (bar_width/2 + inter_gap/2)

# Draw bars: Spain left, Euro-zone right. For target years (2012-2014), Spain bars are semi-transparent + hatch
target_years = [2012, 2013, 2014]
is_target = np.isin(years, target_years)

# Plot Spain bars
sp_bars = ax.bar(left_positions, spain, width=bar_width, color=color_spain,
                 label="Spain (actual / target)", linewidth=0, zorder=3)
# Apply styling for target bars: reduced opacity and hatch
for i, rect in enumerate(sp_bars):
    if is_target[i]:
        rect.set_alpha(0.5)
        rect.set_hatch("//")
        rect.set_edgecolor(color_spain)
        rect.set_linewidth(0.8)

# Plot Euro-zone bars, handling NA values: where NA, draw an outlined placeholder and annotate "n.a."
ez_bars = []
for i, val in enumerate(euro_zone):
    xpos = right_positions[i]
    if np.isnan(val):
        # Draw an outlined placeholder rectangle at zero height with a dashed border to indicate missing data
        placeholder_height = 0.6  # small visible box to show placeholder (in % GDP units)
        # Place the placeholder at a small positive height above zero to avoid covering zero line
        rect = patches.Rectangle((xpos - bar_width/2, 0.0), bar_width, placeholder_height,
                                 linewidth=1.0, edgecolor=neutral_gray, facecolor='none',
                                 linestyle='dashed', zorder=2)
        ax.add_patch(rect)
        # Add "n.a." label centered
        ax.text(xpos, placeholder_height/2, "n.a.", ha='center', va='center', color=neutral_gray, fontsize=12)
    else:
        rects = ax.bar(xpos, val, width=bar_width, color=color_ez, label="Euro‑zone average", linewidth=0, zorder=2)
        ez_bars.append(rects[0])

# Zero line emphasized
ax.axhline(0, color='#333333', linewidth=2.0, zorder=4)

# Gridlines: horizontal only
# Choose y-limits based on data
min_y = min(np.nanmin(spain), np.nanmin(euro_zone[np.isfinite(euro_zone)]))
max_y = max(np.nanmax(spain), np.nanmax(euro_zone[np.isfinite(euro_zone)]))
# Add some padding
y_pad = max(1.5, (max_y - min_y) * 0.1)
ylim_low = np.floor(min_y - y_pad)
ylim_high = np.ceil(max_y + y_pad)
ax.set_ylim(ylim_low, ylim_high)

# Choose y-ticks every 2 or 5 depending on range
yrange = ylim_high - ylim_low
if yrange <= 20:
    y_step = 2
else:
    y_step = 5
yticks = np.arange(ylim_low, ylim_high + 1, y_step)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{y:g}" for y in yticks], fontsize=tick_fontsize, color=neutral_gray)
ax.grid(axis='y', color='#DDDDDD', linewidth=0.8, zorder=0)
# Subtler grid (make zero line already emphasized)
ax.set_axisbelow(True)

# X-axis labels: years every 1 year but rotate if crowded
ax.set_xticks(x)
# Label every year, but if overlap, reduce rotation
ax.set_xticklabels([str(int(y)) for y in years], fontsize=tick_fontsize, rotation=0, color=neutral_gray)

# Axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=axis_label_fontsize, color=neutral_gray)
ax.yaxis.set_label_coords(-0.08, 0.5)  # shift left slightly

# Title and subtitle
fig.suptitle("Spain vs Euro‑Zone Average: Budget balance (% of GDP), 1999–2014",
             fontsize=title_fontsize, fontweight='bold', x=0.56, y=0.98, ha='center')
fig.text(0.56, 0.945, "Final 3 years are Spain’s targets; Euro‑zone average not available for 2012–2014",
         ha='center', fontsize=subtitle_fontsize, color=neutral_gray)

# Legend: custom to avoid duplicate labels; place near top-right under title
legend_elements = [
    Line2D([0], [0], color=color_spain, lw=8, label="Spain (actual / target)"),
    Line2D([0], [0], color=color_ez, lw=8, label="Euro‑zone average")
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.02, 1.02), frameon=False, fontsize=legend_fontsize)

# Δ labels for specified years and small value labels for highlighted years
for dy in delta_years:
    idx = np.where(years == dy)[0]
    if len(idx) == 0:
        continue
    i = idx[0]
    sp_val = spain[i]
    ez_val = euro_zone[i]
    if np.isnan(ez_val):
        continue
    diff = sp_val - ez_val
    diff_str = f"Δ = {diff:+.1f} pp"
    # place between the two bars
    x_mid = (left_positions[i] + right_positions[i]) / 2
    # y position above the higher of the two bars by a fraction of the y-range
    y_ref = max(sp_val, ez_val)
    y_offset = (ylim_high - ylim_low) * 0.03
    y_text = y_ref + y_offset
    ax.text(x_mid, y_text, diff_str, ha='center', va='bottom', fontsize=12, color=neutral_gray, fontweight='semibold', zorder=6)
    # small faint value labels at top of bars for highlighted years
    ax.text(left_positions[i], sp_val + y_offset/2, f"{sp_val:+.1f}", ha='center', va='bottom', fontsize=10, color=color_spain, zorder=6)
    ax.text(right_positions[i], ez_val + y_offset/2, f"{ez_val:+.1f}", ha='center', va='bottom', fontsize=10, color=color_ez, zorder=6)

# Annotations with connector lines (2-4 short inline annotations)
# 1) Spain surpluses mid-2000s (anchor to 2006)
ay = annotation_points[2006]
i = np.where(years == ay["xy_year"])[0][0]
x_anno = right_positions[i] + 0.4  # place text to the right of pair
y_anchor = max(spain[i], euro_zone[i])  # attach to top of higher bar
ax.annotate(ay["text"], xy=(right_positions[i], y_anchor), xytext=(x_anno, y_anchor + 2.0),
            fontsize=annotation_fontsize, fontweight='bold', color=neutral_gray,
            arrowprops=dict(arrowstyle="-", color=neutral_gray, linewidth=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.0))

# 2) Sharp deterioration after 2007 crisis (anchor to 2009)
ay = annotation_points[2009]
i = np.where(years == ay["xy_year"])[0][0]
x_anno = left_positions[i] - 1.1
y_anchor = min(spain[i], euro_zone[i])
ax.annotate(ay["text"], xy=(left_positions[i], y_anchor), xytext=(x_anno, y_anchor - 2.0),
            fontsize=annotation_fontsize, fontweight='bold', color=neutral_gray,
            arrowprops=dict(arrowstyle="-", color=neutral_gray, linewidth=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.0), ha='right')

# 3) Targets note (anchor to 2013 target pair)
ay = annotation_points[2013]
i = np.where(years == ay["xy_year"])[0][0]
x_anno = right_positions[i] + 0.6
y_anchor = spain[i]
ax.annotate(ay["text"], xy=(left_positions[i], y_anchor), xytext=(x_anno, y_anchor + 1.0),
            fontsize=annotation_fontsize, fontweight='bold', color=neutral_gray,
            arrowprops=dict(arrowstyle="-", color=neutral_gray, linewidth=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.0), ha='left')

# Circular halos and connector lines on 2006, 2009, 2014
for cy in circle_years:
    idx = np.where(years == cy)[0]
    if len(idx) == 0:
        continue
    i = idx[0]
    # center x between bars (for 2014 EZ missing, center near Spain bar)
    if np.isnan(euro_zone[i]):
        center_x = left_positions[i]
        top_y = spain[i]
    else:
        center_x = (left_positions[i] + right_positions[i]) / 2
        top_y = max(spain[i], euro_zone[i])
    # position circle slightly above top_y
    center_y = top_y + (ylim_high - ylim_low) * 0.08
    # radius in data coordinates: a fraction of x-axis spacing and y-range
    radius_x = 0.8
    radius_y = (ylim_high - ylim_low) * 0.10
    circ = patches.Ellipse((center_x, center_y), width=radius_x*1.6, height=radius_y*1.6,
                           edgecolor=neutral_gray, facecolor='none', linewidth=1.5, zorder=5)
    ax.add_patch(circ)
    # connector line to annotation if exists (for example 2006 and 2009 already have annotations)
    if cy in [2006, 2009]:
        # draw a thin line to the annotation text position (we used xytext above)
        if cy == 2006:
            text_xy = (right_positions[i] + 0.4, max(spain[i], euro_zone[i]) + 2.0)
        else:
            text_xy = (left_positions[i] - 1.1, min(spain[i], euro_zone[i]) - 2.0)
        line = Line2D([center_x, text_xy[0]], [center_y - 0.05, text_xy[1]], linewidth=0.9, color=neutral_gray, zorder=4)
        ax.add_line(line)

# Target icons (small bullseye) above 2012-2014 Spain bars
for ty in target_years:
    i = np.where(years == ty)[0][0]
    x_pos = left_positions[i]
    y_top = spain[i]
    icon_center_y = y_top + (ylim_high - ylim_low) * 0.04
    # Draw small target: two concentric circles
    outer = patches.Circle((x_pos, icon_center_y), 0.08, edgecolor=color_spain, facecolor='none', linewidth=1.2, zorder=8)
    inner = patches.Circle((x_pos, icon_center_y), 0.04, edgecolor=color_spain, facecolor=color_spain, linewidth=0.8, zorder=9)
    ax.add_patch(outer)
    ax.add_patch(inner)
    # tiny label "target" above icon
    ax.text(x_pos, icon_center_y + 0.12, "target", ha='center', va='bottom', fontsize=9, color=neutral_gray, zorder=9)

# Vertical thin divider between main chart and summary box
divider_x = 0.905  # in figure coordinates approximate; use side_ax position
fig.subplots_adjust(right=0.98)
# Draw a thin divider line using fig.lines in figure coordinates
fig.lines.append(Line2D([0.84, 0.84], [0.12, 0.88], transform=fig.transFigure, color='#E0E0E0', linewidth=1.5, zorder=2))

# Summary box content on right side (side_ax)
# Draw a rounded rectangle as background for the summary box
sb_x0, sb_y0, sb_w, sb_h = 0.0, 0.08, 1.0, 0.84
rect = patches.FancyBboxPatch((sb_x0, sb_y0), sb_w, sb_h,
                              boxstyle="round,pad=0.4", ec='none', fc='none', transform=side_ax.transAxes)
side_ax.add_patch(rect)

# Compose summary lines
avg_diff = np.nanmean(spain[:13] - euro_zone[:13])  # 1999-2011 average diff
avg_str = f"Average Spain − Euro‑Zone (1999–2011): ≈ {avg_diff:+.1f} pp"
peaks = [(2005, spain[years.tolist().index(2005)] - euro_zone[years.tolist().index(2005)]),
         (2006, spain[years.tolist().index(2006)] - euro_zone[years.tolist().index(2006)])]
# find largest positive gap and largest negative gap across 1999-2011
diffs_1999_2011 = (spain[:13] - euro_zone[:13])
max_pos_idx = np.nanargmax(diffs_1999_2011)
max_neg_idx = np.nanargmin(diffs_1999_2011)
max_pos_year = int(years[max_pos_idx])
max_neg_year = int(years[max_neg_idx])
max_pos_val = diffs_1999_2011[max_pos_idx]
max_neg_val = diffs_1999_2011[max_neg_idx]
line2 = f"Largest positive gap: {max_pos_val:+.1f} pp ({max_pos_year}). Largest negative gap: {max_neg_val:+.1f} pp ({max_neg_year})."

# Data source small line
line3 = "Data source: Government agency name/logo. Euro‑zone averages unavailable 2012–2014."

# Place text inside side_ax
side_ax.text(0.02, 0.78, avg_str, fontsize=summary_fontsize, color=neutral_gray, va='top', wrap=True)
side_ax.text(0.02, 0.60, line2, fontsize=summary_fontsize, color=neutral_gray, va='top', wrap=True)
side_ax.text(0.02, 0.45, line3, fontsize=12, color=neutral_gray, va='top', wrap=True)

# Add a thin vertical colored accent bar to align with government brand color
side_ax.add_patch(patches.Rectangle((-0.035, 0.05), 0.02, 0.9, transform=side_ax.transAxes, color=color_spain, alpha=0.12, clip_on=False))

# Source & metadata line bottom-left of figure
fig.text(0.06, 0.05, "Government of Spain • Compiled 2015 • Final 3 years are targets, not actuals",
         fontsize=metadata_fontsize, color=neutral_gray, ha='left')

# Logo / branding: place a modest placeholder logo at lower-right corner
logo_ax = fig.add_axes([0.82, 0.03, 0.12, 0.06])  # in figure coordinates
logo_ax.axis('off')
# Represent a simple government crest with a box and text (placeholder)
logo_ax.add_patch(patches.Rectangle((0.02, 0.15), 0.96, 0.7, facecolor='#F2F2F2', edgecolor='#CCCCCC'))
logo_ax.text(0.5, 0.5, "GOV\nLOGO", ha='center', va='center', fontsize=10, fontweight='bold', color=neutral_gray)

# Tight layout adjustments
plt.subplots_adjust(left=0.08, right=0.84, top=0.94, bottom=0.10)

# Ensure everything renders cleanly
plt.savefig("generated/spain_factor3_bar3/spain_factor3_bar3_design.png", dpi=300, bbox_inches="tight")