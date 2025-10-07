import math
import numpy as np
import matplotlib.pyplot as plt

# Data setup (from provided input)
records = [
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

# Collapse "Other" rows into a single aggregated value (median), and keep count n
other_values = [r["value"] for r in records if r["category"] == "Other"]
other_median = float(np.median(other_values)) if other_values else None
other_n = len(other_values)

# Extract named countries (keep unique categories that are not "Other")
named_map = {}
for r in records:
    if r["category"] != "Other":
        named_map[r["category"]] = r["value"]

# Build combined dataset: named countries + single "Other (multiple countries)"
combined = []
for cat, val in named_map.items():
    combined.append({"category": cat, "value": val, "is_other": False})
if other_median is not None:
    combined.append({"category": "Other (multiple)", "value": other_median, "is_other": True})

# Sort by value descending so comparisons are immediate
combined_sorted = sorted(combined, key=lambda x: x["value"], reverse=True)

# Prepare plotting lists
categories = [c["category"] for c in combined_sorted]
values = [c["value"] for c in combined_sorted]
is_other_flags = [c["is_other"] for c in combined_sorted]

# Colors: deep blue for named countries, orange for U.S., light gray for Other
deep_blue = "#0c4da2"
highlight_orange = "#ff8c00"
other_gray = "#d3d3d3"
colors = []
for c in combined_sorted:
    if c["is_other"]:
        colors.append(other_gray)
    elif c["category"] == "U.S.":
        colors.append(highlight_orange)
    else:
        colors.append(deep_blue)

# Plotting parameters
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
})

fig_height = 6.0 + 0.4 * len(categories)  # give generous vertical space depending on number of bars
fig = plt.figure(figsize=(10, fig_height), dpi=120)
ax = fig.add_subplot(1, 1, 1)

y_pos = np.arange(len(categories))

bar_height = 0.6
ax.barh(y_pos, values, height=bar_height, color=colors, edgecolor="none")

# Numeric labels at the right end of each bar
for i, (v, y) in enumerate(zip(values, y_pos)):
    ax.text(v + max(values) * 0.01, y, f"{v:.1f}", va="center", ha="left", fontsize=10, color="#111111")

# Minimal annotation on U.S. bar (2-3 small words)
# Find index of U.S. if present
if "U.S." in categories:
    idx_us = categories.index("U.S.")
    # Place a small label slightly above the bar end
    ax.text(values[idx_us], y_pos[idx_us] + bar_height * 0.6, "Highest cost",
            fontsize=9, fontstyle="normal", color="#333333", ha="right", va="bottom", alpha=0.9)

# Distribution hint for collapsed "Other": small faint tick marks showing spread of original Other values
if other_values:
    # find index of Other collapsed bar
    try:
        other_idx = categories.index("Other (multiple)")
        # jitter the vertical position slightly for visibility
        jitter = (np.random.RandomState(42).rand(len(other_values)) - 0.5) * (bar_height * 0.6)
        xs = np.array(other_values)
        ys = np.full_like(xs, y_pos[other_idx], dtype=float) + jitter
        ax.scatter(xs, ys, marker='|', s=80, color="#8c8c8c", alpha=0.6, linewidths=1)
    except ValueError:
        pass

# Axes formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=11)
ax.invert_yaxis()  # highest values at top
ax.set_xlabel("Cost (USD)", fontsize=12, labelpad=12)
ax.xaxis.set_ticks_position('bottom')

# X ticks at reasonable intervals
max_tick = math.ceil(max(values) / 20) * 20
xticks = np.arange(0, max_tick + 1, 20)
if len(xticks) < 2:
    xticks = np.linspace(0, max(values), 3)
ax.set_xticks(xticks)
ax.set_xticklabels([f"{int(x)}" for x in xticks], fontsize=10)

# Light vertical gridlines
ax.xaxis.grid(True, linestyle='-', linewidth=0.6, color="#e6e6e6")
ax.set_axisbelow(True)

# Title and subtitle (typographic hierarchy)
title = "Cellphone service cost, 2019 (USD)"
subtitle = ("Selected named countries highlighted; “Other” entries collapsed into a single category "
            "(median shown). Values are reported in 2019 U.S. dollars.")
fig.suptitle(title, fontsize=18, fontweight='bold', y=0.96)
ax.set_title(subtitle, fontsize=11, fontweight='normal', loc='center', pad=8)

# Remove top and right spines for a clean, news-style look
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')

# Caption and metadata beneath the chart
caption_lines = [
    f"Among the highlighted countries, the U.S. has the highest reported cost ({named_map.get('U.S.', 0):.1f} USD) "
    f"and Russia the lowest ({named_map.get('Russia', 0):.1f} USD).",
    f"The collapsed 'Other' category shows the median of remaining observations ({other_median:.1f} USD) to reduce clutter.",
    "This gap indicates substantially higher consumer costs in the U.S. compared with several other countries shown."
]
caption_text = " ".join(caption_lines)

metadata_text = (f"Data source: [insert authoritative source]. Method: values as reported in 2019 USD; "
                 f"Other aggregated by median (n = {other_n}).")

# Place caption and metadata using figure text (full width)
fig.text(0.5, 0.05, caption_text, ha='center', va='center', fontsize=9)
fig.text(0.5, 0.02, metadata_text, ha='center', va='center', fontsize=8, color="#666666")

# Improve layout to fit caption/metadata
plt.subplots_adjust(left=0.18, right=0.96, top=0.90, bottom=0.12)

plt.savefig("generated/cellphone_factor1_1_design.png", dpi=300, bbox_inches="tight")