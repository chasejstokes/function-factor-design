import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.patheffects as path_effects
import numpy as np

# Data setup
data = [
    {"year": 1999, "spain": -1.2, "euro_zone_average": -0.9},
    {"year": 2000, "spain": -0.6, "euro_zone_average": -0.4},
    {"year": 2001, "spain": -0.4, "euro_zone_average": -0.8},
    {"year": 2002, "spain": -1.0, "euro_zone_average": -1.6},
    {"year": 2003, "spain": -0.8, "euro_zone_average": -2.6},
    {"year": 2004, "spain": 0.6, "euro_zone_average": -2.9},
    {"year": 2005, "spain": 1.3, "euro_zone_average": -1.8},
    {"year": 2006, "spain": 2.4, "euro_zone_average": 1.1},
    {"year": 2007, "spain": 1.9, "euro_zone_average": -0.8},
    {"year": 2008, "spain": -4.5, "euro_zone_average": -3.6},
    {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
    {"year": 2010, "spain": -9.5, "euro_zone_average": -6.0},
    {"year": 2011, "spain": -7.8, "euro_zone_average": -4.1},
    {"year": 2012, "spain": -4.2, "euro_zone_average": -4.6},
    {"year": 2013, "spain": -5.0, "euro_zone_average": -3.8},
    {"year": 2014, "spain": -2.5, "euro_zone_average": -2.0}
]

years = np.array([d["year"] for d in data])
spain = np.array([d["spain"] for d in data])
euro = np.array([d["euro_zone_average"] for d in data])
diff = spain - euro  # Spain minus Euro-Zone

# Compute summary statistics
mean_spain = spain.mean()
mean_euro = euro.mean()
# Largest Spain deficit (most negative spain value)
idx_largest_deficit = np.argmin(spain)
year_largest_deficit = years[idx_largest_deficit]
value_largest_deficit = spain[idx_largest_deficit]
# Largest positive and negative Spain - Euro gap
idx_max_gap = np.argmax(diff)
idx_min_gap = np.argmin(diff)
year_max_gap = years[idx_max_gap]
gap_max = diff[idx_max_gap]
year_min_gap = years[idx_min_gap]
gap_min = diff[idx_min_gap]

# Selective annotation years (as requested)
annot_years = [2004, 2006, 2009]  # includes largest gap years as well (2004,2009)
annot_idx = [int(np.where(years == y)[0][0]) for y in annot_years]

# Colors
color_spain = "#C0392B"   # deep warm red
color_euro = "#2C3E50"    # cool navy blue
color_pos = "#1ABC9C"     # teal for Spain better than EZ
color_neg = "#E74C3C"     # red tint for Spain worse than EZ

# Create figure with two vertically stacked axes (main + small diff band)
fig = plt.figure(figsize=(11, 6))
gs = gridspec.GridSpec(100, 1, figure=fig)
ax_main = fig.add_subplot(gs[0:78, 0])
ax_diff = fig.add_subplot(gs[78:86, 0], sharex=ax_main)

# Main lines
ax_main.plot(years, spain, color=color_spain, linewidth=2.5, label="Spain")
ax_main.plot(years, euro, color=color_euro, linewidth=1.8, label="Euro‑Zone average")

# Markers only at selected points
ax_main.scatter(years[annot_idx], spain[annot_idx], color=color_spain, edgecolor='white',
                s=50, zorder=5)

# Horizontal gridlines on main axis
yticks = [-12, -8, -4, 0, 4]
ax_main.set_yticks(yticks)
ax_main.grid(axis='y', linestyle='-', color='#DDDDDD', linewidth=0.8, zorder=0)
ax_main.set_xlim(years.min() - 0.3, years.max() + 0.3)
ax_main.set_ylim(min(-12.5, spain.min() - 1), 4.5)

# Legend inside top-right of main plot
legend = ax_main.legend(loc='upper right', frameon=False, fontsize=10)

# Axis labels
ax_main.set_ylabel("Budget balance (% of GDP)", fontsize=10)
ax_main.set_xlabel("Year", fontsize=10)

# Title and subtitle
title_text = "Spain vs. Euro‑Zone: Budget Balance (% of GDP), 1999–2014"
subtitle_text = ("Spain swung from surpluses in the mid‑2000s to a dramatic deficit peak after "
                 "the 2008 crisis; while the Euro‑Zone also fell, Spain’s losses were larger and more volatile.")
fig.suptitle(title_text, fontsize=18, fontweight='bold', y=0.98)
fig.text(0.5, 0.935, subtitle_text, ha='center', fontsize=11, color='#555555')

# Small difference area chart in ax_diff (Spain - EZ)
ax_diff.axhline(0, color="#666666", linewidth=0.8)
ax_diff.set_xlim(ax_main.get_xlim())

# Fill positive and negative areas separately for diverging colors
positives = np.where(diff >= 0, diff, 0)
negatives = np.where(diff < 0, diff, 0)
ax_diff.fill_between(years, 0, positives, where=positives >= 0, interpolate=True,
                     color=color_pos, alpha=0.25, linewidth=0)
ax_diff.fill_between(years, 0, negatives, where=negatives <= 0, interpolate=True,
                     color=color_neg, alpha=0.25, linewidth=0)

ax_diff.set_ylim(min(diff.min() - 1, -6), max(diff.max() + 1, 6) if diff.max() > 0 else 4)
ax_diff.set_yticks([])  # keep it minimal to emphasize direction only
ax_diff.spines['top'].set_visible(False)
ax_diff.spines['right'].set_visible(False)
ax_diff.spines['left'].set_visible(False)
ax_diff.spines['bottom'].set_color('#CCCCCC')
ax_diff.tick_params(axis='x', which='both', labelsize=9)

# Keep only year ticks on x-axis at integer locations
ax_diff.set_xticks(years)
ax_diff.set_xticklabels([str(int(y)) for y in years], rotation=0, fontsize=9)

# Add subtle fill between on main chart (very light) for context (optional, low opacity)
ax_main.fill_between(years, spain, euro, where=(spain >= euro), interpolate=True,
                     color=color_pos, alpha=0.08, linewidth=0)
ax_main.fill_between(years, spain, euro, where=(spain < euro), interpolate=True,
                     color=color_neg, alpha=0.08, linewidth=0)

# Selective callouts near points with rounded bbox
callouts = {
    2004: f"2004: Spain {spain[years == 2004][0]:+.1f}%\n(gap {diff[years == 2004][0]:+.1f} pts vs EZ)",
    2006: f"2006: Spain {spain[years == 2006][0]:+.1f}%\n(peak surplus)",
    2009: f"2009: Spain {spain[years == 2009][0]:+.1f}%\n(largest deficit)"
}

# Place callouts. Coordinates chosen to avoid overlap; nudged in x/y as needed.
offsets = {
    2004: (0.2, 0.9),
    2006: (-0.6, 0.9),
    2009: (0.4, -0.25)
}

for y_val, text in callouts.items():
    idx = int(np.where(years == y_val)[0][0])
    x_pt = years[idx]
    y_pt = spain[idx]
    dx, dy = offsets[y_val]
    # Compute annotation position in data coords
    ann_x = x_pt + dx
    ann_y = y_pt + dy * (ax_main.get_ylim()[1] - ax_main.get_ylim()[0]) * 0.06
    bbox_props = dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", lw=0.7, alpha=0.95)
    txt = ax_main.text(ann_x, ann_y, text, fontsize=9, va='center', ha='left', bbox=bbox_props, zorder=10)
    # subtle path effect for slight drop shadow
    txt.set_path_effects([path_effects.withSimplePatchShadow(offset=(1,-1), shadow_rgbFace=(0,0,0), alpha=0.12)])

# Summary statistics box top-left inside main plot
summary_lines = [
    f"Mean 1999–2014: Spain {mean_spain:.2f}% GDP, Euro‑Zone {mean_euro:.2f}% GDP",
    f"Largest Spain deficit: {year_largest_deficit}, {value_largest_deficit:.1f}% (Spain {diff[idx_largest_deficit]:+.1f} pts vs EZ)",
    f"Largest Spain advantage: {year_max_gap}, {gap_max:+.1f} pts vs Euro‑Zone"
]
summary_text = "\n".join(summary_lines)
bbox_summary = dict(boxstyle="round,pad=0.5", fc="#FFFFFF", ec="#DDDDDD", lw=0.8, alpha=0.92)
ax_main.text(0.02, 0.93, summary_text, transform=ax_main.transAxes,
             fontsize=9, va='top', ha='left', bbox=bbox_summary, zorder=20)

# Footnote and source
footnote = ("Sharp deterioration after 2008 reflects the global financial crisis and Spain’s "
            "banking/sovereign revenue shock.")
fig.text(0.02, 0.02, "Source: [dataset], author calculation.", fontsize=8, ha='left', color='#333333')
fig.text(0.5, 0.02, footnote, fontsize=9, ha='center', color='#444444')

# Tight layout adjustments
plt.subplots_adjust(left=0.06, right=0.98, top=0.92, bottom=0.06)

# Improve appearance: remove top/right spines from main axis
ax_main.spines['top'].set_visible(False)
ax_main.spines['right'].set_visible(False)

# Ensure x-axis labels are only on the lower small axis (already set)
plt.setp(ax_main.get_xticklabels(), visible=False)

# Display
plt.savefig("generated/spain_factor4_2_design.png", dpi=300, bbox_inches="tight")