import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Data setup (from provided dataset)
data = [
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

# Identify named countries and others
named_set = {"Russia", "France", "Britain", "China", "U.S."}
named = [d for d in data if d["category"] in named_set]
others = [d for d in data if d["category"] not in named_set]

# Sort named countries in descending order (for comparison emphasis)
named_sorted = sorted(named, key=lambda x: x["value"], reverse=True)

# Sort Others in ascending order and cluster them below
others_sorted = sorted(others, key=lambda x: x["value"])

# Combine into final plotting order: named group at top, then others
plot_order = named_sorted + others_sorted

categories = [d["category"] for d in plot_order]
values = [d["value"] for d in plot_order]

# Compute summary stats for named group
named_values = [d["value"] for d in named_sorted]
named_avg = sum(named_values) / len(named_values)
named_min = min(named_values)
named_max = max(named_values)

# Visual parameters
fig_w, fig_h = 10, 7
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
fig.patch.set_facecolor("white")

# Colors
navy = "#0b3d91"           # deep navy for highlighted bars
muted_gray = "#bdbdbd"     # pale gray for Others
accent = "#007f7f"         # teal accent for callouts and summary box
dark_text = "#222222"

# Layout padding so we can place initials and logo
max_val = max(values) * 1.12
left_pad = -max_val * 0.14
ax.set_xlim(left_pad, max_val)

# Y positions
n = len(values)
y_positions = np.arange(n)[::-1]  # top to bottom

# Heights: named bars thicker
heights = []
for cat in categories:
    if cat in named_set:
        heights.append(0.6)  # thicker
    else:
        heights.append(0.35)  # thinner

# Draw bars
for i, (y, val, h, cat) in enumerate(zip(y_positions, values, heights, categories)):
    if cat in named_set:
        ax.barh(y, val, height=h, color=navy, edgecolor="#082a60", linewidth=1.2, zorder=3)
    else:
        ax.barh(y, val, height=h, color=muted_gray, alpha=0.4, edgecolor="#9e9e9e", linewidth=0.6, zorder=1)

# Y labels: show category names aligned slightly right of the left padded area
for y, cat in zip(y_positions, categories):
    ax.text(left_pad + (max_val * 0.01), y, cat if cat in named_set else "", va="center",
            ha="left", fontsize=10, color=dark_text)

# Add small country initials/icons left of named labels (simple initials in small squares)
initials_map = {"U.S.": "US", "China": "CN", "Britain": "GB", "France": "FR", "Russia": "RU"}
icon_box_size = (max_val * 0.01)
for y, cat in zip(y_positions, categories):
    if cat in named_set:
        init = initials_map.get(cat, cat[:2].upper())
        # draw a small rectangle as pseudo-flag background
        rect_x = left_pad + (max_val * 0.003)
        rect_w = icon_box_size
        rect_h = heights[categories.index(cat)] * 0.8
        ax.add_patch(patches.FancyBboxPatch((rect_x, y - rect_h/2),
                                            rect_w, rect_h,
                                            boxstyle="round,pad=0.02",
                                            linewidth=0.6,
                                            edgecolor="#333333",
                                            facecolor="#f0f0f0",
                                            zorder=4))
        ax.text(rect_x + rect_w/2, y, init, va="center", ha="center",
                fontsize=8, weight="bold", color="#333333", zorder=5)

# Numeric callouts (circles + text) for named countries only
for y, val, cat in zip(y_positions, values, categories):
    if cat in named_set:
        # Position the circle near the end of the bar
        circle_x = val + (max_val * 0.015)
        # Keep circle inside the plotting area if space allows, otherwise outside slightly
        circle = patches.Circle((circle_x, y), max_val*0.012, color=accent, zorder=6)
        ax.add_patch(circle)
        # Text inside circle, white, formatted
        label_text = f"{cat} ${val:.1f}"
        ax.text(circle_x, y, f"${val:.1f}", va="center", ha="center",
                fontsize=9, color="white", weight="bold", zorder=7)

        # Also add small thin leader line connecting end of bar to circle if circle is a bit away
        bar_end_x = val
        ax.plot([bar_end_x, circle_x - max_val*0.011], [y, y], color="#666666", linewidth=0.7, zorder=5)

# Annotations: targeted short comparisons with leader lines
# 1) U.S. highest
us_idx = categories.index("U.S.")
us_y = y_positions[us_idx]
annotation_us = "Highest — $63.0 (≈ $13.5 more than China)"
ax.annotate(annotation_us,
            xy=(values[us_idx], us_y),
            xytext=(values[us_idx] + max_val*0.08, us_y + 0.9),
            fontsize=9, color=dark_text, ha="left",
            bbox=dict(boxstyle="round,pad=0.3", fc=(1,1,1,0.85), ec=accent, lw=0.8),
            arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8),
            zorder=8)

# 2) Russia lowest named
ru_idx = categories.index("Russia")
ru_y = y_positions[ru_idx]
annotation_ru = "Lowest named country — $4.0"
ax.annotate(annotation_ru,
            xy=(values[ru_idx], ru_y),
            xytext=(values[ru_idx] + max_val*0.07, ru_y - 0.9),
            fontsize=9, color=dark_text, ha="left",
            bbox=dict(boxstyle="round,pad=0.3", fc=(1,1,1,0.85), ec=accent, lw=0.8),
            arrowprops=dict(arrowstyle="->", color="#666666", lw=0.8),
            zorder=8)

# Summary stat box (top-right)
summary_text = f"Named avg ≈ ${named_avg:.1f} • Range ${named_min:.0f}–${named_max:.0f}"
# Place using axes coordinates
ax_x = 0.98  # axes fraction
ax_y = 0.95
fig.text(ax_x, ax_y, summary_text, ha="right", va="top",
         fontsize=10, weight="bold", color=dark_text,
         bbox=dict(boxstyle="round,pad=0.4", fc=(1,1,1,0.95), ec=accent, lw=1.0))

# Title placed in top-left quadrant aligned near small logo
title_x = left_pad + (max_val * 0.18)
title_y = n + 0.8
fig.text(0.12, 0.95, "Cellphone service cost (2019, USD)",
         fontsize=17, weight="bold", color=dark_text)

# Small logo at top-left (pseudo government logo)
logo_ax = fig.add_axes([0.02, 0.905, 0.055, 0.055], anchor='NW')
logo_ax.add_patch(patches.Rectangle((0,0),1,1, facecolor=navy))
logo_ax.text(0.5,0.5, "GOV", color="white", ha="center", va="center", weight="bold", fontsize=10)
logo_ax.axis("off")

# Source/metadata line at lower-left
fig.text(0.02, 0.02, "Source: Official dataset, 2019", fontsize=9, color="#444444")

# Axis styling
ax.set_yticks([])  # hide y ticks (we used text labels)
ax.set_xlabel("Cost (USD)", fontsize=11, color=dark_text)
ax.xaxis.set_ticks_position('bottom')
ax.tick_params(axis='x', colors=dark_text, labelsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', linestyle='--', linewidth=0.5, color="#e6e6e6", zorder=0)

# Tight layout adjustment
plt.subplots_adjust(left=0.14, right=0.95, top=0.88, bottom=0.08)

# Show the chart
plt.savefig("generated/cellphone_factor3_1_design.png", dpi=300, bbox_inches="tight")