import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain_values = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Euro-zone values: use np.nan for NA
euro_values = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Styling parameters
spain_color = '#0B5FFF'   # dark blue
euro_color = '#028F88'    # dark teal
na_box_edge = '#BEBEBE'   # light gray for N/A placeholder
fig_w, fig_h = 9, 12      # inches (900x1200 px at 100 dpi)
dpi = 100

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "axes.edgecolor": "#333333"
})

fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)

# X positions for pairs
x = np.arange(len(years))
bar_width = 0.36
offset = bar_width / 2.0

# Draw Euro-zone bars (where available)
euro_mask = ~np.isnan(euro_values)
ax.bar(x[euro_mask] + offset, euro_values[euro_mask],
       width=bar_width, color=euro_color, edgecolor='none', zorder=2)

# Draw Spain bars
# Determine which years are targets (2012-2014)
target_years_mask = (years >= 2012)
observed_mask = ~target_years_mask

# Observed Spain bars
ax.bar(x[observed_mask] - offset, spain_values[observed_mask],
       width=bar_width, color=spain_color, edgecolor='none', zorder=3)

# Target Spain bars (2012-2014): semi-transparent with hatch and label above
for xi, val, is_target in zip(x, spain_values, target_years_mask):
    if is_target:
        # Draw the bar with hatch and reduced opacity
        ax.bar(xi - offset, val, width=bar_width,
               color=spain_color, edgecolor='none', alpha=0.5,
               hatch='///', zorder=3)
        # Inline small label above each target bar
        label_y = val + (0.6 if val >= 0 else -0.6)
        # Position slightly above positive bars, slightly below negative bar tops (so it's readable)
        ax.text(xi - offset, label_y, "Target (not actual)",
                ha='center', va='bottom' if val >= 0 else 'top',
                fontsize=10, color="#222222", alpha=0.9)

# Euro-zone NA placeholders for 2012-2014: dashed light gray outline box with "N/A"
na_indices = np.where(np.isnan(euro_values))[0]
# Box height center around 0, small and unobtrusive
na_box_halfheight = 1.5  # percent points above/below zero
for idx in na_indices:
    box_x = (idx + offset) - bar_width / 2.0
    rect = patches.Rectangle(
        (box_x, -na_box_halfheight),
        bar_width,
        na_box_halfheight * 2,
        linewidth=1.2,
        edgecolor=na_box_edge,
        facecolor='none',
        linestyle=(0, (5, 5)),
        zorder=1
    )
    ax.add_patch(rect)
    # N/A centered
    ax.text(idx + offset, 0, "N/A", ha='center', va='center',
            fontsize=14, color="#666666", zorder=5)

# Value labels for every bar (Spain and Euro-zone where present)
def draw_value_label(xpos, ypos, text, positive):
    txt = ax.text(xpos, ypos, text,
                  ha='center', va='bottom' if positive else 'top',
                  fontsize=16, fontweight='bold', color='#111111', zorder=6)
    # Add halo for readability
    txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='white'),
                          path_effects.Normal()])

# Spain labels
for xi, val in zip(x, spain_values):
    if val >= 0:
        ypos = val + 0.25
        draw_value_label(xi - offset, ypos, f"{val:.1f}%", True)
    else:
        ypos = val - 0.25
        draw_value_label(xi - offset, ypos, f"{val:.1f}%", False)

# Euro-zone labels
for xi, val in zip(x, euro_values):
    if np.isnan(val):
        continue
    if val >= 0:
        ypos = val + 0.25
        draw_value_label(xi + offset, ypos, f"{val:.1f}%", True)
    else:
        ypos = val - 0.25
        draw_value_label(xi + offset, ypos, f"{val:.1f}%", False)

# Title and subtitle
title_text = "Budget balance: Spain vs Euro‑Zone"
subtitle_text = "Percent of GDP, 1999–2014"
ax.set_title(title_text, fontsize=34, fontweight='bold', pad=20)
ax.text(0.01, 0.96, subtitle_text, transform=ax.transAxes,
        fontsize=20, va='top', ha='left', color='#222222')

# Direct inline mapping chips and labels on the first year pair
chip_y = 0.98  # relative axes coords
chip_x_start = 0.01
chip_size = 0.015
# Spain chip
ax.add_patch(patches.Rectangle(
    (chip_x_start, chip_y - chip_size / 2),
    chip_size, chip_size,
    transform=fig.transFigure, color=spain_color, zorder=10
))
fig.text(chip_x_start + chip_size + 0.005, chip_y, "Spain",
         transform=fig.transFigure, fontsize=14, va='center', fontweight='bold')
# Euro-zone chip
ez_chip_x = chip_x_start + 0.12
ax.add_patch(patches.Rectangle(
    (ez_chip_x, chip_y - chip_size / 2),
    chip_size, chip_size,
    transform=fig.transFigure, color=euro_color, zorder=10
))
fig.text(ez_chip_x + chip_size + 0.005, chip_y, "Euro‑Zone avg",
         transform=fig.transFigure, fontsize=14, va='center', fontweight='bold')

# Axis labels, ticks, grid
ax.set_ylabel("Percent of GDP", fontsize=18)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=14, rotation=45)
ax.tick_params(axis='y', labelsize=16)
# Y limits and ticks
ax.set_ylim(-12.5, 3.5)
ax.set_yticks(np.arange(-12, 4, 2))
ax.grid(axis='y', color='#CCCCCC', alpha=0.25, linewidth=1, zorder=0)
# Emphasize zero baseline
ax.axhline(0, color='#000000', linewidth=1.8, zorder=4)

# Annotations with light connector lines
# 1) 2006 (above 2006 Spain bar)
year_idx = list(years).index(2006)
ax.annotate(
    "2005–2007: Spain posts surpluses while Euro‑Zone averages remain negative.",
    xy=(year_idx - offset, spain_values[year_idx]),
    xytext=(year_idx - 1.2, 2.6),
    fontsize=16,
    ha='left',
    va='bottom',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9),
    arrowprops=dict(arrowstyle="-", color="#777777", linewidth=1, shrinkA=0, shrinkB=5),
    zorder=8
)

# 2) 2009 (callout near 2009 pair)
year_idx = list(years).index(2009)
ax.annotate(
    "2009 peak: Spain −11.2% vs Euro‑Zone −6.3%.",
    xy=(year_idx + 0.1, spain_values[year_idx]),
    xytext=(year_idx + 1.2, -7.5),
    fontsize=16,
    ha='left',
    va='center',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9),
    arrowprops=dict(arrowstyle="-", color="#777777", linewidth=1, shrinkA=0, shrinkB=5),
    zorder=8
)

# 3) 2011 (near 2011 bars)
year_idx = list(years).index(2011)
ax.annotate(
    "2010–2011: deep deficits persist during recovery.",
    xy=(year_idx - 0.1, spain_values[year_idx]),
    xytext=(year_idx - 2.6, -9.8),
    fontsize=16,
    ha='left',
    va='center',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9),
    arrowprops=dict(arrowstyle="-", color="#777777", linewidth=1, shrinkA=0, shrinkB=5),
    zorder=8
)

# 4) 2012–2014 (near target bars)
# Place one annotation pointing to the cluster of targets (around 2013)
year_idx = list(years).index(2013)
ax.annotate(
    "2012–2014: Spain targets (not observed).",
    xy=(year_idx - offset, spain_values[year_idx]),
    xytext=(year_idx + 1.1, -3.0),
    fontsize=16,
    ha='left',
    va='center',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.95),
    arrowprops=dict(arrowstyle="-", color="#777777", linewidth=1, shrinkA=0, shrinkB=5),
    zorder=8
)

# Short annotation pointing to an N/A placeholder: "Euro‑Zone avg unavailable"
na_anno_idx = list(years).index(2013)
ax.annotate(
    "Euro‑Zone avg unavailable",
    xy=(na_anno_idx + offset, 0.8),
    xytext=(na_anno_idx + 2.0, 1.5),
    fontsize=14,
    ha='left',
    va='center',
    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.95),
    arrowprops=dict(arrowstyle="-", color="#777777", linewidth=1, shrinkA=0, shrinkB=5),
    zorder=8
)

# Footnote / Data note at bottom center-left
footnote = ("Note: 2012–2014 are Spain’s targets. Euro‑Zone average unavailable 2012–2014 (NA). "
            "Data compiled from aggregated reporting.")
fig.text(0.5, 0.02, footnote, ha='center', va='bottom', fontsize=12, color='#333333')

# Layout adjustments
plt.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.08)

# Remove spines on top and right for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig("generated/spain_factor2_bar1/spain_factor2_bar1_design.png", dpi=300, bbox_inches="tight")