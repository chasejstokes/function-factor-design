import math
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Data setup
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

# Separate named countries and aggregate "Other"
named_values = {}
other_values = []
for r in records:
    cat = r["category"]
    val = float(r["value"])
    if cat == "Other":
        other_values.append(val)
    else:
        named_values[cat] = val

# Compute aggregate summary for Other (n=9)
other_count = len(other_values)
other_min = min(other_values)
other_max = max(other_values)
other_median = float(statistics.median(other_values))
other_mean = float(statistics.mean(other_values))

# Use mean as the plotted aggregated value (de-emphasized visually)
other_label = f"Other countries (n={other_count})"
other_plot_value = other_mean

# Combine for plotting: named countries individually + aggregated Other
plot_entries = []
for k, v in named_values.items():
    plot_entries.append({"category": k, "value": v, "is_other": False})
plot_entries.append({"category": other_label, "value": other_plot_value, "is_other": True})

# Sort descending by value
plot_entries = sorted(plot_entries, key=lambda x: x["value"], reverse=True)

# Prepare plotting lists
categories = [e["category"] for e in plot_entries]
values = [e["value"] for e in plot_entries]
is_other_flags = [e["is_other"] for e in plot_entries]

# Colors: deep blue for named countries, slightly stronger for U.S., muted gray for Other
base_blue = "#1f77b4"  # colorblind-safe blue
us_color = "#08306b"   # darker blue to subtly emphasize U.S.
named_color = base_blue
other_color = "#9e9e9e"  # muted gray

bar_colors = []
for cat, is_other in zip(categories, is_other_flags):
    if is_other:
        bar_colors.append(other_color)
    else:
        if cat == "U.S.":
            bar_colors.append(us_color)
        else:
            bar_colors.append(named_color)

# Plotting
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.facecolor": "white"
})

fig, ax = plt.subplots(figsize=(9, 5.5))
y_pos = np.arange(len(categories))[::-1]  # invert to have highest at top when plotting horizontally

# Plot bars as horizontal bars
bars = ax.barh(y_pos, values[::-1], color=np.array(bar_colors)[::-1], height=0.65)

# Title and subtitle (top-left)
title_x = 0.01
ax_text_x = 0.01
plt.suptitle("Cellphone cost — 2019 (USD)", x=0.01, ha="left", va="top",
             fontsize=14, fontweight="bold", y=0.98)
plt.title("Named countries shown individually; remaining countries are aggregated (range, median indicated).",
          fontsize=10, fontweight="regular", loc="left", pad=8)

# Remove spines and ticks to keep minimal axes
for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)
ax.xaxis.set_visible(False)  # hide conventional x-axis ticks/labels
ax.yaxis.set_visible(False)  # hide default y-axis tick labels

# Add country labels to the left of each bar (direct labels)
for yi, label in zip(y_pos, categories[::-1]):
    ax.text(-0.5, yi, label, va="center", ha="left", fontsize=10)

# Value labels at the end of each bar (monospaced-like alignment)
for bar, val in zip(bars, values[::-1]):
    w = bar.get_width()
    yi = bar.get_y() + bar.get_height() / 2
    # Format numeric label with one decimal place
    label_text = f"{w:.1f}"
    ax.text(w + max(values) * 0.01, yi, label_text, va="center", ha="left",
            fontsize=10, fontfamily="DejaVu Sans Mono")

# Subtle gridlines for scale reference (vertical lines every 20 USD)
max_x = math.ceil(max(values) / 10) * 10
ax.set_xlim(0, max_x)
major_locator = MultipleLocator(20)
ax.xaxis.set_major_locator(major_locator)
ax.xaxis.grid(True, which='major', color='#bcbcbc', linestyle='-', alpha=0.18, linewidth=0.8)
# draw a faint baseline behind bars for subtle separation
for yi in y_pos:
    ax.hlines(yi, xmin=0, xmax=max_x, color='none')

# Add a small USD scale label at the top-right of the plotting area
ax.text(0.995, 1.02, "USD", transform=ax.transAxes, ha="right", va="bottom", fontsize=9, alpha=0.9)

# Annotations: U.S., Russia, and Other aggregate
# Find indices and coordinates for annotations
def find_index(category_name):
    for i, cat in enumerate(categories):
        if cat == category_name:
            return i
    return None

# Because we reversed ordering for plotting, map index to y position
def y_for_index(idx):
    # idx is in categories list (descending order), we plotted reversed, so compute position:
    plotted_idx = len(categories) - 1 - idx
    return y_pos[plotted_idx]

# U.S. annotation
us_idx = find_index("U.S.")
if us_idx is not None:
    us_y = y_for_index(us_idx)
    us_val = named_values["U.S."]
    ax.annotate(
        "U.S. highest among named countries at $63 — ~$13 more than China.",
        xy=(us_val, us_y),
        xytext=(us_val + max_x * 0.05, us_y + 0.25),
        fontsize=10.5,
        va="center",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cfcfcf", lw=0.6),
        arrowprops=dict(arrowstyle="-", lw=0.7, color="#6e6e6e", shrinkA=0, shrinkB=2),
        wrap=True
    )

# Russia annotation
rus_idx = find_index("Russia")
if rus_idx is not None:
    rus_y = y_for_index(rus_idx)
    rus_val = named_values["Russia"]
    # Place inside or adjacent depending on bar length; Russia is small so place to right of bar
    ax.annotate(
        "Russia lowest among named countries at $4 — substantially lower than the sample median.",
        xy=(rus_val, rus_y),
        xytext=(rus_val + max_x * 0.10, rus_y - 0.18),
        fontsize=10.0,
        va="center",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#dedede", lw=0.6),
        arrowprops=dict(arrowstyle="-", lw=0.7, color="#8a8a8a", shrinkA=0, shrinkB=2),
        wrap=True
    )

# Other aggregate annotation (use exact requested phrasing)
other_idx = find_index(other_label)
if other_idx is not None:
    other_y = y_for_index(other_idx)
    other_val = other_plot_value
    other_text = (f"Other countries span ${other_min:.0f}–{other_max:.0f} "
                  f"(median ≈ ${other_median:.0f}; mean ≈ ${other_mean:.0f}). "
                  "These values are aggregated to keep focus on named countries.")
    # Place annotation near the Other bar, slightly to its right
    ax.annotate(
        other_text,
        xy=(other_val, other_y),
        xytext=(other_val + max_x * 0.03, other_y + 0.28),
        fontsize=10.0,
        va="center",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.32", fc="white", ec="#dadada", lw=0.6),
        arrowprops=dict(arrowstyle="-", lw=0.7, color="#999999", shrinkA=0, shrinkB=2),
        wrap=True
    )

# Fine print source line at bottom-left
plt.figtext(0.01, 0.01, "Source: 2019 cost survey", ha="left", fontsize=8, color="#6b6b6b")

# Tight layout adjustments
plt.subplots_adjust(left=0.16, right=0.98, top=0.86, bottom=0.08)

# Invert y-axis so highest value is at the top (we already arranged positions)
ax.invert_yaxis()

# Display the plot
plt.savefig("generated/cellphone_factor2_1_design.png", dpi=300, bbox_inches="tight")