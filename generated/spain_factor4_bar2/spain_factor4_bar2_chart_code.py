import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib as mpl

# Data setup (explicit, using Python-native numbers; NA as None/np.nan)
years = np.arange(1999, 2015)
spain_vals = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9,
    -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Euro-zone: last three years are NA
euro_vals = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7,
    -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Compute summary metrics for 1999-2011 (indexes 0..12)
valid_idx = np.arange(0, 13)  # 1999-2011 inclusive
spain_avg = np.nanmean(spain_vals[valid_idx])
euro_avg = np.nanmean(euro_vals[valid_idx])
avg_diff = spain_avg - euro_avg  # Spain minus EuroZone (positive = Spain higher/better)
# Largest single-year gap (absolute difference) for 1999-2011
diffs = spain_vals[valid_idx] - euro_vals[valid_idx]
abs_diffs = np.abs(diffs)
max_gap_idx = np.nanargmax(abs_diffs)
max_gap_year = years[valid_idx][max_gap_idx]
max_gap_val = diffs[max_gap_idx]

# Specific callout deltas
callouts = {
    2006: (2.4, -1.3, 2.4 - (-1.3)),   # 2006
    2007: (1.9, -0.7, 1.9 - (-0.7)),   # 2007
    2009: (-11.2, -6.3, -11.2 - (-6.3)),  # 2009
}

# Colors (normalized RGB)
spain_color = (0/255, 87/255, 155/255)
spain_target_face = (0/255, 87/255, 155/255)
euro_color = (140/255, 170/255, 180/255)
delta_accent = (230/255, 85/255, 40/255)  # warm orange for small callouts

# Figure: portrait, approx 1000 x 1333 px at 100 dpi
fig, ax = plt.subplots(figsize=(10, 13.33), dpi=100)

# Bar layout
n_years = len(years)
ind = np.arange(n_years)
group_width = 0.7
bar_width = group_width / 2.2  # slightly slim bars

# Spain bars: full actuals for 1999-2011, patterned lighter for 2012-2014
spain_actual_mask = np.arange(n_years) <= 12  # True for indices 0..12 (1999-2011)
spain_target_mask = ~spain_actual_mask       # 2012-2014

# Plot Spain actual bars
bars_spain_actual = ax.bar(ind[spain_actual_mask] - bar_width/2, spain_vals[spain_actual_mask],
                           width=bar_width, align='center',
                           color=spain_color, edgecolor='black', linewidth=0.6, zorder=3,
                           label='Spain (actual)')

# Plot Spain target bars (2012-2014): same blue but lighter with diagonal hatch and alpha
bars_spain_target = ax.bar(ind[spain_target_mask] - bar_width/2, spain_vals[spain_target_mask],
                           width=bar_width, align='center',
                           color=spain_target_face, edgecolor='black', linewidth=0.6,
                           alpha=0.40, hatch='///', zorder=3,
                           label='Spain (target)')

# Add small "Target" tags above target bars
for i in np.where(spain_target_mask)[0]:
    x = ind[i] - bar_width/2
    y = spain_vals[i]
    ax.text(x + bar_width/2, y + 0.8, "Target", ha='center', va='bottom',
            fontsize=12, fontweight='semibold', color=spain_color)

# Plot Euro-Zone average bars for years with data (1999-2011)
euro_mask_real = ~np.isnan(euro_vals)
bars_euro = ax.bar(ind[euro_mask_real] + bar_width/2, euro_vals[euro_mask_real],
                   width=bar_width, align='center',
                   color=euro_color, edgecolor='black', linewidth=0.6, zorder=2,
                   label='Euro‑Zone average')

# For 2012-2014, draw a pale gray cross-hatched placeholder centered vertically near zero
placeholder_indices = np.where(np.isnan(euro_vals))[0]
# Determine placeholder height as a small visible slab (so it doesn't suggest a value)
placeholder_height = 1.6  # small slab so as not to imply a magnitude
placeholder_ybottom = -placeholder_height / 2.0
for i in placeholder_indices:
    x_left = ind[i] + bar_width/2 - bar_width/2
    # Draw a subtle rectangle with diagonal crosshatch
    rect = Rectangle((ind[i] + bar_width/2 - bar_width/2 - 0.01, placeholder_ybottom),
                     width=bar_width, height=placeholder_height,
                     facecolor=(0.9, 0.9, 0.9, 0.7), edgecolor=(0.85, 0.85, 0.85),
                     hatch='xxx', linewidth=0.6, zorder=1)
    ax.add_patch(rect)
    # Place a small italic N/A label centered
    ax.text(ind[i] + bar_width/2, 0.0, "Euro‑Zone avg:\nN/A", ha='center', va='center',
            fontsize=10, fontstyle='italic', color='gray', zorder=4)

# Axis limits and gridlines
ax.set_ylim(-12, 3)
ax.set_xlim(-0.6, n_years - 0.4)

# Y-axis ticks as specified
y_ticks = [-12, -10, -8, -6, -4, -2, 0, 2]
ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{t}%" for t in y_ticks], fontsize=14)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, labelpad=14)

# X-axis: year labels every year
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=14, rotation=0)
ax.tick_params(axis='x', which='major', pad=8)

# Emphasize 0% baseline
ax.axhline(0, color='black', linewidth=1.6, zorder=4)

# Light horizontal gridlines at major tick intervals (very pale)
ax.yaxis.grid(True, which='major', color=(0.95, 0.95, 0.95), linewidth=1.0, zorder=0)
ax.set_axisbelow(True)

# Title, subtitle, and valenced subtext
title_text = "Spain vs Euro‑Zone: Budget Deficit and Surplus (1999–2014)"
subtitle_text = ("Budget balance as % of GDP. Final three Spain bars (2012–2014) are government targets; "
                 "Euro‑Zone average not reported for 2012–2014.")
valenced_subtext = ("Spain swung from surpluses in the mid‑2000s to a sharply deeper deficit during the financial crisis.")

plt.suptitle(title_text, fontsize=34, fontweight='bold', y=0.96)
# Place subtitle and valenced subtext directly under title within figure (use fig.text for better placement)
fig.text(0.06, 0.90, subtitle_text, fontsize=20, va='top')
fig.text(0.06, 0.875, valenced_subtext, fontsize=14, va='top', color='dimgray')

# Compact legend top-left inside plotting area
from matplotlib.patches import Patch
legend_patches = [
    Patch(facecolor=spain_color, edgecolor='black', label='Spain (actual)'),
    Patch(facecolor=spain_target_face, edgecolor='black', hatch='///', alpha=0.40, label='Spain (target)'),
    Patch(facecolor=euro_color, edgecolor='black', label='Euro‑Zone average')
]
leg = ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(0.01, 0.98),
                fontsize=16, frameon=False)

# Numeric summary box (upper-right inside chart area)
summary_lines = [
    f"1999–2011 averages:",
    f"  Spain ≈ {spain_avg:.2f}% GDP; Euro‑Zone ≈ {euro_avg:.2f}% GDP",
    f"  (difference ≈ {avg_diff:+.2f} pct. pts in Spain’s favor)",
    f"Largest divergence: {int(max_gap_year)} ({spain_vals[valid_idx][max_gap_idx]:+.1f} vs {euro_vals[valid_idx][max_gap_idx]:+.1f} → {max_gap_val:+.1f} pct. pts)"
]
summary_text = "\n".join(summary_lines)
# Place at upper-right within axes coordinates
ax.text(0.98, 0.92, summary_text, ha='right', va='top', fontsize=12,
        bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="gray", linewidth=0.8),
        transform=ax.transAxes)

# Selective callouts for 2006, 2007, 2009, 2010-2011 cluster
annot_style = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", linewidth=0.8)
arrowprops = dict(arrowstyle="-", connectionstyle="arc3", color='gray', linewidth=0.8)

# 2006
x2006 = np.where(years == 2006)[0][0]
sp2006, ez2006, d2006 = callouts[2006]
ax.annotate(f"2006\nSpain {sp2006:+.1f}%\nEZ {ez2006:+.1f}%\nΔ {d2006:+.1f} pct. pts",
            xy=(ind[x2006], max(sp2006, ez2006) + 0.2),
            xytext=(ind[x2006] - 0.6, 1.9),
            fontsize=14, ha='left', va='bottom', bbox=annot_style, arrowprops=arrowprops)

# 2007
x2007 = np.where(years == 2007)[0][0]
sp2007, ez2007, d2007 = callouts[2007]
ax.annotate(f"2007\nSpain {sp2007:+.1f}%\nEZ {ez2007:+.1f}%\nΔ {d2007:+.1f} pct. pts",
            xy=(ind[x2007], max(sp2007, ez2007) + 0.2),
            xytext=(ind[x2007] + 0.25, 1.8),
            fontsize=14, ha='left', va='bottom', bbox=annot_style, arrowprops=arrowprops)

# 2009 - highlighted delta with warm accent
x2009 = np.where(years == 2009)[0][0]
sp2009, ez2009, d2009 = callouts[2009]
ax.annotate(f"2009\nSpain {sp2009:+.1f}%\nEZ {ez2009:+.1f}%\nΔ {d2009:+.1f} pct. pts",
            xy=(ind[x2009], min(sp2009, ez2009) - 0.4),
            xytext=(ind[x2009] + 0.6, -7.0),
            fontsize=14, ha='left', va='bottom',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=delta_accent, linewidth=1.0),
            arrowprops=dict(arrowstyle="-", connectionstyle="angle3,angleA=0,angleB=-90", color=delta_accent, linewidth=1.0))

# 2010-2011 cluster annotation (sustained deep deficits)
x2010 = np.where(years == 2010)[0][0]
x2011 = np.where(years == 2011)[0][0]
# draw a subtle bracket-like line above the two bars
bracket_x = [ind[x2010] + bar_width/2, ind[x2011] + bar_width/2]
bracket_y = -3.8
ax.plot([bracket_x[0], bracket_x[1]], [bracket_y, bracket_y], color='gray', linewidth=0.9)
ax.text((bracket_x[0] + bracket_x[1]) / 2, bracket_y - 0.4, "2010–2011: sustained deep deficits",
        fontsize=13, ha='center', va='top', color='dimgray', bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none"))

# Avoid labeling every bar; add selective tiny value marker only in callouts (done above)
# Clean up spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Footnote bottom-left: data source and transparency on targets/NA
footnote = ("Source: Compiled dataset. Units = % of GDP. "
            "2012–2014 = Spain government targets; Euro‑Zone average not available (NA) for 2012–2014.")
fig.text(0.02, 0.02, footnote, fontsize=10, ha='left', va='bottom')

# Tight layout adjustments
plt.subplots_adjust(top=0.88, left=0.08, right=0.98, bottom=0.06)

# Show the plot
plt.savefig("generated/spain_factor4_bar2/spain_factor4_bar2_design.png", dpi=300, bbox_inches="tight")