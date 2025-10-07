import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
import statistics

# Data setup (from provided JSON-like data)
named_entries = [
    {"category": "Russia", "value": 4.0},
    {"category": "France", "value": 15.0},
    {"category": "Britain", "value": 33.0},
    {"category": "China", "value": 49.5},
    {"category": "U.S.", "value": 63.0},
]

other_values = [7.0, 7.2, 9.0, 12.0, 18.0, 34.0, 37.0, 42.0, 60.0]  # n = 9

# Compute aggregated Other stats
other_n = len(other_values)
other_median = statistics.median(other_values)
other_mean = statistics.mean(other_values)
other_min = min(other_values)
other_max = max(other_values)

# Sort named entries descending by value (highest at top)
named_sorted = sorted(named_entries, key=lambda x: x["value"], reverse=True)
categories = [e["category"] for e in named_sorted]
values = [e["value"] for e in named_sorted]

# Y positions: place named countries in top block, leave one unit gap, place Other below
n_named = len(categories)
y_named = np.arange(n_named)  # 0 .. n_named-1 (will invert axis so 0 is top)
other_y = n_named + 1  # leave a gap row between groups
divider_y = n_named - 0.5  # place divider between named block and gap

# Colors: coherent palette with U.S. as warm accent, Russia desaturated
# Map colors to categories after sorting
color_map = {}
# choose palette ordered roughly from medium to cool; override U.S. to warm accent and Russia to desaturated
palette = {
    "U.S.": "#E07A5F",      # warm accent (darker orange)
    "China": "#2A9D8F",     # teal
    "Britain": "#457B9D",   # blue
    "France": "#4A69BD",    # medium blue
    "Russia": "#9FB4C7",    # desaturated blue-gray
}
for cat in categories:
    color_map[cat] = palette.get(cat, "#6C757D")

# Plot setup
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
})
fig_height = 6.0
fig, ax = plt.subplots(figsize=(10, fig_height))

# Plot horizontal bars for named countries
bar_height = 0.7
bars = ax.barh(y_named, values, height=bar_height,
               color=[color_map[cat] for cat in categories],
               edgecolor='none', align='center')

# Add numeric labels at bar ends for named countries
for yi, val, cat, bar in zip(y_named, values, categories, bars):
    x_pos = val + (max(values) * 0.03)  # small offset to the right of bar end
    label_text = f"${val:.1f}"
    txt = ax.text(x_pos, yi, label_text, va='center', ha='left',
                  fontsize=10, fontweight='bold', color=color_map[cat])
    # white halo for legibility
    txt.set_path_effects([
        path_effects.Stroke(linewidth=3, foreground="white", alpha=0.9),
        path_effects.Normal(),
    ])

# Add light divider line separating named countries from Other
ax.axhline(y=divider_y, color='gray', linewidth=0.8, alpha=0.6, xmin=0.02, xmax=0.98)

# Plot the aggregated "Other" element as a narrow, desaturated horizontal boxplot
# Use a single-position horizontal boxplot
boxprops = dict(facecolor="#E9ECEF", edgecolor="#BFC7CC", linewidth=0.9)
medianprops = dict(color="#6C757D", linewidth=1.5)
whiskerprops = dict(color="#BFC7CC", linewidth=0.9)
capprops = dict(color="#BFC7CC", linewidth=0.9)
flierprops = dict(marker='o', markerfacecolor="#AAB0B5", markeredgecolor="#AAB0B5", markersize=3, alpha=0.7)

bp = ax.boxplot(other_values,
                vert=False,
                positions=[other_y],
                widths=0.6,
                patch_artist=True,
                boxprops=boxprops,
                medianprops=medianprops,
                whiskerprops=whiskerprops,
                capprops=capprops,
                flierprops=flierprops,
                manage_ticks=False)

# Small faint ticks for individual Other points (no labels) to show distribution
rng = np.random.default_rng(1)
y_jitter = (rng.random(len(other_values)) - 0.5) * 0.12  # small vertical jitter
ax.scatter(other_values, [other_y + j for j in y_jitter], marker='|', color="#9AA1A6", s=40, alpha=0.9)

# Label for the Other row and aggregated stats text
other_label = f"Other (n={other_n})"
# Compose aggregated stats string per spec
other_stats_str = f"Other (n={other_n}): median ${other_median:.0f}; range ${other_min:.0f}–${other_max:.0f}; mean ${other_mean:.1f}"
# Place the y-tick labels (include named countries + Other)
yticks_positions = list(y_named) + [other_y]
ytick_labels = categories + [other_label]
ax.set_yticks(yticks_positions)
ax.set_yticklabels(ytick_labels, fontsize=11)
# Place the aggregated stats text to the right of the Other boxplot (muted gray)
ax.text(max(values) * 0.55, other_y, other_stats_str, va='center', ha='left', fontsize=10, color="#55595c")

# Small callouts anchored to U.S. and Russia bars (no arrows)
# Find indices of U.S. and Russia in sorted list to place callouts
for cat_name, note in [("U.S.", f"Highest: ${next(v['value'] for v in named_entries if v['category']=='U.S.'):.1f} (2019)"),
                       ("Russia", f"Lowest: ${next(v['value'] for v in named_entries if v['category']=='Russia'):.1f} (2019) — ~{(next(v['value'] for v in named_entries if v['category']=='U.S.')/next(v['value'] for v in named_entries if v['category']=='Russia')):.1f}× difference vs U.S.")]:
    if cat_name in categories:
        idx = categories.index(cat_name)
        # place callout slightly inside the plot area near the bar's mid to avoid clutter
        x_pos_call = values[idx] * 0.55 if values[idx] > max(values) * 0.2 else values[idx] + max(values) * 0.06
        ax.text(x_pos_call, y_named[idx], note, va='center', ha='left', fontsize=9, color="#333333", style='italic', alpha=0.85)

# Axes, grid, and styling
ax.invert_yaxis()  # so highest value (first in sorted list) appears at top
ax.set_xlabel("Cost (USD, 2019)", fontsize=11, labelpad=10)
ax.xaxis.grid(True, linestyle='--', linewidth=0.6, color='gray', alpha=0.4)
ax.set_axisbelow(True)

# X-axis limits with comfortable padding
xmax = max(max(values), other_max)
ax.set_xlim(0, xmax * 1.12)

# Title, subtitle, and synthesis caption per design plan
title = "Cellphone service cost, 2019 (USD)"
subtitle = ("Comparison of named countries; “Other” entries aggregated. Values shown are prices in 2019 USD; "
            f"data highlights differences (median Other = ${other_median:.0f}, range ${other_min}–${other_max}).")
synthesis = ("Takeaway: U.S. and China are among the most expensive (U.S. $63, China $49.5); "
             "Russia is far cheaper at $4 — a more than 15× gap.")

# Place title and subtitle
plt.suptitle(title, fontsize=16, fontweight='bold', y=0.97)
plt.title(subtitle, fontsize=10.5, fontweight='light', color='#444444')  # subtitle placed under main title

# One-line synthesis caption under the chart area
plt.figtext(0.125, 0.02, synthesis, ha='left', fontsize=10, color='#222222')

# Tight layout adjustments
plt.subplots_adjust(top=0.85, bottom=0.12, left=0.18, right=0.95)

# Ensure high contrast readability for bar labels that sit on colored backgrounds (we used halo)
# Remove spines for a cleaner, publication-style look
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CFCFCF')

# Show the figure
plt.savefig("generated/cellphone_factor4_2_design.png", dpi=300, bbox_inches="tight")