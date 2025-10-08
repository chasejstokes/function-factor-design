import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Circle
import numpy as np

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain_vals = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use np.nan for missing euro-zone values
ez_vals = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Colors and style
spain_color = "#C62828"   # deep brand red
ez_color = "#1E5FA8"      # muted navy/blue
placeholder_edge = "#BFBFBF"
bg_color = "white"

# Figure setup: portrait 9 x 12 in
fig, ax = plt.subplots(figsize=(9, 12))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# Bar positions and widths
x = np.arange(len(years))
group_width = 0.7
bar_width = 0.32  # each bar about 45% of group
spacing_between_pairs = 0.18

# Offsets for paired bars
offset = bar_width / 2.0 + 0.01
left_positions = x - offset
right_positions = x + offset

# Plot Euro-Zone bars where available
ez_present = ~np.isnan(ez_vals)
ez_heights = np.where(ez_present, ez_vals, 0.0)
ez_bars = ax.bar(right_positions[ez_present], ez_vals[ez_present],
                 width=bar_width, color=ez_color, label='Euro-Zone average', zorder=2)

# Plot Spain bars (actuals and targets)
# Targets are years 2012-2014 (last three years)
target_years_mask = (years >= 2012)
spain_bars = ax.bar(left_positions, spain_vals, width=bar_width,
                    color=spain_color, zorder=3, label='Spain')

# Overlay hatches for target years (2012-2014)
for i, yr in enumerate(years):
    if target_years_mask[i]:
        # Slightly more transparent base
        ax.bar(left_positions[i], spain_vals[i], width=bar_width,
               color=spain_color, alpha=0.92, zorder=3)
        # Overlay hatch bar (no fill) to indicate 'target'
        ax.bar(left_positions[i], spain_vals[i], width=bar_width,
               facecolor='none', edgecolor=spain_color, hatch='////', linewidth=0.7, zorder=4)

# For Euro-Zone missing data (2012-2014) draw pale outlined hatch boxes as placeholders
for i, yr in enumerate(years):
    if not ez_present[i]:
        # Draw a small neutral-height placeholder box centered at right_positions[i]
        box_width = bar_width
        # Place box around central region to indicate "no data" without implying a value:
        box_bottom = -1.6
        box_top = 1.6
        rect = Rectangle((right_positions[i] - box_width/2, box_bottom),
                         box_width, box_top - box_bottom,
                         facecolor='none', edgecolor=placeholder_edge, linewidth=1.0,
                         hatch='...')  # dotted hatch
        ax.add_patch(rect)
        # Add small 'NA' label inside the box
        ax.text(right_positions[i], 0.0, "NA", ha='center', va='center',
                fontsize=14, color=placeholder_edge, zorder=6)

# Y-axis range and gridlines
ax.set_ylim(-12.5, 3.5)
ax.set_xlim(-1, len(years))
ax.yaxis.set_ticks(np.arange(-12, 4, 2))
ax.set_yticklabels([f"{y:g}" for y in np.arange(-12, 4, 2)], fontsize=15)
ax.grid(axis='y', which='major', color='#E6E6E6', linewidth=0.9, zorder=0)
# Stronger zero baseline
ax.axhline(0, color='#222222', linewidth=2.0, zorder=5)

# X-axis setup: year labels horizontal
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=15)
ax.set_xlabel("")  # no extra x-axis label per spec
# Y-axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, labelpad=12)

# Numeric labels: Spain (all years) and EZ where available (selected)
for i, (xs, sp) in enumerate(zip(left_positions, spain_vals)):
    # Determine label position above the bar top (account for negative bars)
    ytext = sp + (0.4 if sp >= 0 else 0.4)
    ax.text(xs, ytext, f"{sp:+.1f}" if sp>=0 else f"{sp:.1f}",
            ha='center', fontsize=15, fontweight='bold', color=spain_color, zorder=7)

for i, (xr, ez) in enumerate(zip(right_positions, ez_vals)):
    if not math.isnan(ez):
        ytext = ez + (0.4 if ez >= 0 else 0.4)
        ax.text(xr, ytext, f"{ez:+.1f}" if ez>=0 else f"{ez:.1f}",
                ha='center', fontsize=14, color=ez_color, zorder=7)

# Compute differences where both present
diffs = []
for i in range(len(years)):
    if not math.isnan(ez_vals[i]):
        diff = spain_vals[i] - ez_vals[i]
        diffs.append((i, diff))
# Sort by absolute difference desc to pick top 4 comparison years
top_diffs = sorted(diffs, key=lambda t: abs(t[1]), reverse=True)[:4]
top_indices = [t[0] for t in top_diffs]

# Annotations for top comparison years (short one-line + numeric difference)
annotation_fontsize = 16
for idx in top_indices:
    yr = years[idx]
    sp = spain_vals[idx]
    ez = ez_vals[idx]
    diff = sp - ez
    sign = "above" if diff > 0 else "below"
    # Compose annotation text short
    ann_text = f"{int(yr)}: Δ = {diff:+.1f} pp"
    # Anchor point near top of Spain bar
    x_ann = left_positions[idx]
    y_ann = sp + (1.2 if sp >= 0 else 1.2)
    # Draw a rounded bbox for text to ensure legibility
    ax.annotate(ann_text,
                xy=(x_ann, sp),
                xytext=(x_ann, y_ann),
                textcoords='data',
                ha='center', va='bottom',
                fontsize=annotation_fontsize,
                bbox=dict(boxstyle="round,pad=0.4", fc=(1,1,1,0.88), ec='none'),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2",
                                color="#6E6E6E", linewidth=1.0),
                zorder=9)

# Trend annotation for 2005-2007 and 2009-2011
# 2005-2007: Spain surpluses; EZ deficits
mask_0507 = (years >= 2005) & (years <= 2007)
x_center_0507 = left_positions[mask_0507].mean()
ax.text(x_center_0507, 2.8, "2005–2007: Spain surpluses; EZ deficits",
        ha='center', va='bottom', fontsize=15, bbox=dict(boxstyle="round,pad=0.35",
                                                          fc=(1,1,1,0.9), ec='none'), zorder=8)

# 2009-2011: Spain underperformed significantly
mask_0911 = (years >= 2009) & (years <= 2011)
x_center_0911 = left_positions[mask_0911].mean()
ax.text(x_center_0911, -4.6, "2009–2011: Spain well below EZ",
        ha='center', va='bottom', fontsize=15, bbox=dict(boxstyle="round,pad=0.35",
                                                          fc=(1,1,1,0.9), ec='none'), zorder=8)

# Add subtle circular halo around the Spain bar top for the largest gap year (first of top_indices)
if len(top_indices) > 0:
    largest_idx = top_indices[0]
    circ_center = (left_positions[largest_idx], spain_vals[largest_idx])
    # radius in data coordinates: width ~ 0.6 in x, height ~ 2.0 in y
    circ = Circle(circ_center, radius=0.6, fill=False, edgecolor=spain_color, linewidth=2.0, alpha=0.28, zorder=6)
    ax.add_patch(circ)

# Draw small vertical/horizontal difference brackets for selected important years (2005,2007,2009,2010 if present)
bracket_years = [2005, 2007, 2009, 2010]
for by in bracket_years:
    if by in years:
        i = int(np.where(years == by)[0][0])
        if not math.isnan(ez_vals[i]):
            sp = spain_vals[i]
            ez = ez_vals[i]
            # positions
            x_sp = left_positions[i]
            x_ez = right_positions[i]
            top_y = max(sp, ez) + 0.6
            bottom_y = min(sp, ez) - 0.2
            # Draw a thin horizontal line between the two bar tops
            ax.plot([x_sp, x_ez], [top_y, top_y], color='#6E6E6E', linewidth=1.0, zorder=6)
            # small vertical ticks down to tops
            ax.plot([x_sp, x_sp], [top_y, sp], color='#6E6E6E', linewidth=1.0, zorder=6)
            ax.plot([x_ez, x_ez], [top_y, ez], color='#6E6E6E', linewidth=1.0, zorder=6)
            # Label delta above the bar
            delta = sp - ez
            ax.text((x_sp + x_ez)/2, top_y + 0.15, f"Δ = {delta:+.1f} pp",
                    ha='center', va='bottom', fontsize=14, color='#4D4D4D', zorder=7)

# Legend (top-right, compact) including 'Spain (target)' and 'Euro-Zone unavailable'
legend_patches = [
    mpatches.Patch(facecolor=spain_color, label='Spain'),
    mpatches.Patch(facecolor=spain_color, hatch='////', edgecolor=spain_color, label='Spain (target)'),
    mpatches.Patch(facecolor=ez_color, label='Euro-Zone average'),
    mpatches.Patch(facecolor='none', hatch='...', edgecolor=placeholder_edge, label='Euro-Zone unavailable')
]
leg = ax.legend(handles=legend_patches, loc='upper right', fontsize=16, frameon=False)
leg.set_zorder(20)

# Title and subtitle with small up/down icon in the subtitle
title = "Spain vs. Euro‑Zone: Budget Deficit and Surplus, 1999–2014"
subtitle = "Final three Spain values are official targets; Euro‑Zone averages unavailable for 2012–2014"
ax.set_title(title, fontsize=32, pad=18, fontweight='semibold')
# Place subtitle as text below title (matplotlib only supports one title; use text)
fig.text(0.5, 0.945, subtitle, ha='center', fontsize=15)

# Add small government logo at top-left (stylized placeholder) and a tiny icon near subtitle
# Logo placeholder: small shield-like patch
logo_x = 0.06
logo_y = 0.945
logo_size = 0.045  # fraction of figure width
# draw a simple crest-like triangle + circle using axes coordinates on the figure
from matplotlib.transforms import Bbox, TransformedBbox
ax_logo = fig.add_axes([0.03, 0.92, 0.06, 0.06], anchor='NW', zorder=22)
ax_logo.axis('off')
# Draw a simple emblem using patches
ax_logo.add_patch(Circle((0.3, 0.6), 0.12, color=spain_color))
ax_logo.add_patch(Rectangle((0.15, 0.12), 0.5, 0.5, angle=15, facecolor='#FFDAB9', edgecolor='#E0A1A1'))
ax_logo.add_patch(Rectangle((0.22, 0.02), 0.36, 0.14, facecolor=spain_color))
# Add tiny up/down arrow icon near subtitle (as text)
fig.text(0.47, 0.943, "↕", ha='left', fontsize=12, color='#4D4D4D')

# Footer (bottom-left) with source and metadata and presenter note bottom-right
footer_text = "Source: [relevant government source] — Euro‑Zone averages as reported / last three Spain values are government targets."
fig.text(0.03, 0.025, footer_text, ha='left', fontsize=11)

# Presenter note (alt text / slide note) bottom-right
presenter_note = ("Presenter note: Spain had surpluses 2005–2007 while euro‑zone averaged deficits; "
                  "Spain plunged most in 2009 to −11.2% vs EZ −6.3%.")
fig.text(0.5, 0.025, presenter_note, ha='center', fontsize=11, color='#333333')

# Tight layout adjustments
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.08, right=0.96)

# Remove top/right spines for a clean government-style look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', length=0)

# Show the plot
plt.savefig("generated/spain_factor3_bar0/spain_factor3_bar0_design.png", dpi=300, bbox_inches="tight")