import math
import sys
import subprocess

# Ensure required libraries are installed
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

# Data setup (from the provided dataset)
raw_data = [
    {"category": "Russia", "value": 4.0},
    {"category": "Other", "value": 7.0},
    {"category": "Other", "value": 7.2},
    {"category": "Other", "value": 9.0},
    {"category": "Other", "value": 12.0},
    {"category": "France", "value": 15.0},
    {"category": "Other", "value": 18.0},
    {"category": "Britain", "value": 33.0},
    {"category": "Other", "value": 34.0},
    {"category": "Other", "value": 37.0},
    {"category": "Other", "value": 42.0},
    {"category": "China", "value": 49.5},
    {"category": "Other", "value": 60.0},
    {"category": "U.S.", "value": 63.0},
]

# Named countries of interest and color mapping
named_order = ["U.S.", "China", "Britain", "France", "Russia"]  # desired focus order (we'll sort by value)
color_map = {
    "U.S.": "#003f5c",      # deep blue
    "China": "#2f9c95",     # teal
    "Britain": "#ff7c43",   # warm orange
    "France": "#d45087",    # muted red/pink
    "Russia": "#4b0082",    # indigo
}
other_color = "#d3d3d3"     # light gray for Other (de-emphasized)

# Aggregate named countries and 'Other' rows
named_values = {name: None for name in named_order}  # will fill from data
other_values = []
for row in raw_data:
    cat = row["category"]
    val = float(row["value"])
    if cat in named_values:
        named_values[cat] = val
    else:
        other_values.append(val)

# Ensure all named countries found; if missing, set to nan (not expected with given data)
for k in named_values:
    if named_values[k] is None:
        named_values[k] = float("nan")

# Compute Other aggregates for caption and optional display
other_count = len(other_values)
other_sum = sum(other_values)
other_mean = other_sum / other_count if other_count > 0 else float("nan")

# Prepare plotting data: focus chart on the five named countries, sorted descending by value
items = sorted(named_values.items(), key=lambda kv: kv[1], reverse=True)  # list of (country, value)
countries = [it[0] for it in items]
values = [it[1] for it in items]

# We'll append a muted "Other (multiple entries)" bar at the bottom (de-emphasized).
# Per design plan we will label it "Other (multiple entries) — muted" and not emphasize the numeric on-chart.
other_label = "Other (multiple entries) — muted"
# We will not plot the aggregated numeric value on the bar label to keep emphasis on named countries,
# but we compute mean for caption context. The bar's visual presence will be subtle.
countries_plot = countries + [other_label]
# For the bar length of 'Other' we'll use the mean of other values so it fits scale sensibly
# but we will display the label text instead of numeric on the chart, per plan.
values_plot = values + [other_mean if not math.isnan(other_mean) else 0.0]

# Create bar heights: named countries thicker, other thinner
named_bar_height = 0.62
other_bar_height = 0.36
heights = [named_bar_height] * len(values) + [other_bar_height]

# Y positions with increased vertical spacing
n_bars = len(countries_plot)
y_positions = np.arange(n_bars) * 1.2  # larger spacing between bars for legibility

# Colors for bars: map named countries to palette, Other to muted gray
bar_colors = [color_map.get(c, other_color) for c in countries] + [other_color]

# Set up figure
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
})
fig, ax = plt.subplots(figsize=(9, 6.2))
fig.subplots_adjust(top=0.78, bottom=0.215, left=0.28, right=0.97)

# Plot horizontal bars
for i, (y, val, h, col, label) in enumerate(zip(y_positions, values_plot, heights, bar_colors, countries_plot)):
    ax.barh(y, val, height=h, color=col, edgecolor="none", zorder=3)

# Draw unobtrusive horizontal gridlines at major ticks (x-axis)
ax.set_axisbelow(True)
ax.xaxis.grid(True, which="major", color="#eeeeee", linewidth=1.0)
ax.yaxis.grid(False)

# Axis formatting
ax.set_xlabel("USD", fontsize=11)
ax.set_xlim(0, 80)  # ticks at 0,20,40,60,80 per spec
ax.set_xticks([0, 20, 40, 60, 80])
ax.set_yticks(y_positions)
ax.set_yticklabels(countries_plot, fontsize=11)
ax.invert_yaxis()  # so the highest value appears at top (we already sorted desc)

# On-chart numeric labels for named countries (show one decimal place consistently)
for i, (y, val, label) in enumerate(zip(y_positions, values_plot, countries_plot)):
    if label == other_label:
        # For 'Other' bar, show muted label text rather than a numeric value (per instructions)
        ax.text(val + 1.5, y, other_label, va='center', ha='left', fontsize=9, color="#6d6d6d")
    else:
        # Numeric label at end of each named-country bar
        ax.text(val + 1.5, y, f"${val:0.1f}", va='center', ha='left', fontsize=10, fontweight='medium', color="#222222")

# Title and subtitle
title = "Cellphone service cost, 2019 (USD)"
subtitle = "Comparison of named countries (U.S., China, Britain, France, Russia); 'Other' entries aggregated and de-emphasized"
ax.set_title(title, fontsize=16, fontweight='bold', loc='left', pad=14)
# Subtitle using figure text for positioning under the title
fig.text(0.01, 0.735, subtitle, fontsize=11, color="#333333", ha='left')

# Legend (minimal, bottom-left)
named_patch = mpatches.Patch(color="#333333", label="Named countries", alpha=1.0)
# We'll construct legend entries manually to show intended mapping: one saturated entry and one muted
legend_patches = [
    mpatches.Patch(color="#808080", label="Named countries (colored)"),  # descriptive label only
    mpatches.Patch(color=other_color, label="Other (de-emphasized)"),
]
# But create a clarified custom legend showing two entries: colors in a separate small legend
legend_handles = [
    mpatches.Patch(color='#777777', label='Named countries (see color map below)'),
    mpatches.Patch(color=other_color, label='Other (de-emphasized)'),
]
# Place legend bottom-left inside the figure
ax.legend(handles=legend_handles, loc='lower left', bbox_to_anchor=(0.01, -0.18), frameon=False, fontsize=9)

# Color mapping list for the five named countries — include in caption area below
color_mapping_lines = [
    f"Color mapping: U.S. {color_map['U.S.']}, China {color_map['China']}, Britain {color_map['Britain']}, France {color_map['France']}, Russia {color_map['Russia']}.",
]

# Caption (multi-sentence, left-aligned below the chart)
caption_lines = [
    "Variable definition: Cost of cellphone service (USD), 2019. Values are as reported for each listed country.",
    f"Data handling: Multiple 'Other' rows were aggregated for context. {other_count} 'Other' entries were combined (mean = ${other_mean:0.1f}; sum = ${other_sum:0.1f}) and are de-emphasized in the visualization.",
    "Source: [Data source placeholder] — include collector name, collection date, and any caveats here.",
    "Synthesis: U.S. shows the highest listed cost at $63.0; Russia is the lowest at $4.0. Named countries account for the primary comparisons displayed.",
] + color_mapping_lines + [
    "Export recommendation: PNG/SVG for web; include this caption as alt text/long description for accessibility."
]
caption_text = "\n".join(caption_lines)

# Place caption as left-aligned figure text
fig.text(0.01, 0.02, caption_text, fontsize=9, ha='left', va='bottom')

# Make spines subtle
for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)

# Improve layout
plt.tight_layout(rect=[0, 0.05, 1, 0.95])

# Show the plot
plt.savefig("generated/cellphone_factor1_2_design.png", dpi=300, bbox_inches="tight")