import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# Data input (as provided)
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

# Aggregate "Other" entries into a single de-emphasized group (mean + count)
other_values = [d["value"] for d in raw_data if d["category"] == "Other"]
other_count = len(other_values)
other_mean = sum(other_values) / other_count if other_count else 0.0
# We'll use the mean to represent the "Other (various)" row
aggregated = {
    "Russia": 4.0,
    "France": 15.0,
    "Britain": 33.0,
    "China": 49.5,
    "U.S.": 63.0,
    "Other (various)": other_mean,
}

# Prepare lists and sort descending by value (highest first)
items = list(aggregated.items())
# Keep named countries emphasized; Other remains a category and will be placed according to its value
items_sorted = sorted(items, key=lambda x: x[1], reverse=True)

categories = [it[0] for it in items_sorted]
values = [it[1] for it in items_sorted]

# Styling constants
highlight_color = "#0D6EFD"      # for named countries
accent_edge_color = "#0A58CA"    # slightly darker for top value (U.S.)
other_gray = "#D9D9D9"           # de-emphasized other
bg_grid = "#F2F2F2"
circle_alpha = 0.30
title_fontsize = 17
label_fontsize = 11
annotation_fontsize = 10
footnote_fontsize = 9

# Figure setup
fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

y_pos = np.arange(len(categories))[::-1]  # reverse for top-to-bottom highest-first

# Map categories to colors: named countries -> highlight_color; Other -> gray
bar_colors = []
edge_colors = []
linewidths = []
for cat in categories:
    if cat == "Other (various)":
        bar_colors.append(other_gray)
        edge_colors.append(other_gray)
        linewidths.append(0.8)
    else:
        bar_colors.append(highlight_color)
        # Accent top value (U.S.) with slightly heavier/darker edge
        if cat == "U.S.":
            edge_colors.append(accent_edge_color)
            linewidths.append(1.8)
        else:
            edge_colors.append(highlight_color)
            linewidths.append(0.8)

# Horizontal bars
bar_container = ax.barh(y_pos, values, color=bar_colors, edgecolor=edge_colors, linewidth=linewidths, height=0.6)

# Light vertical grid lines for value reference
ax.xaxis.grid(True, color=bg_grid, linewidth=1, zorder=0)
ax.set_axisbelow(True)

# Remove default y-ticks; we'll add left-aligned labels with small "flag" icons
ax.set_yticks(y_pos)
ax.set_yticklabels([""] * len(categories))  # blank; we'll draw our own labels
ax.invert_yaxis()  # highest at top (already ensured by reverse y_pos)

# X-axis limits and ticks
xmax = max(values) * 1.25
ax.set_xlim(0, xmax)
ax.set_xlabel("")  # no axis label per design
ax.tick_params(axis='x', labelsize=10)

# Add numeric labels at the end of each named-country bar (bold compact)
for i, (cat, val) in enumerate(zip(categories, values)):
    y = y_pos[i]
    x = val
    label = f"${int(val) if val == int(val) else val:g}"
    ax.text(x + xmax * 0.01, y, label, va='center', ha='left', fontsize=label_fontsize, fontweight='bold', color='black')

# Add country labels left of the bars with small pseudo-flag icons for named countries
# We'll draw a small colored rectangle and 2-letter ISO text to simulate a flag/icon
flag_box_width = xmax * 0.03
for i, cat in enumerate(categories):
    y = y_pos[i]
    x_text = -xmax * 0.02  # slightly left of axis
    # Short iso codes mapping for simple icon
    iso = ""
    if cat.startswith("U.S"):
        iso = "US"
    elif cat.startswith("China"):
        iso = "CN"
    elif cat.startswith("Britain"):
        iso = "GB"
    elif cat.startswith("France"):
        iso = "FR"
    elif cat.startswith("Russia"):
        iso = "RU"
    # Draw flag/icon only for named countries
    if iso:
        # Colored small rectangle as flag background (use highlight color)
        flag_x = -xmax * 0.055
        rect = mpatches.FancyBboxPatch((flag_x, y - 0.22), flag_box_width, 0.44,
                                      boxstyle="round,pad=0.02", linewidth=0.6,
                                      facecolor="#ffffff", edgecolor=highlight_color)
        ax.add_patch(rect)
        ax.text(flag_x + flag_box_width / 2, y, iso, va='center', ha='center', fontsize=9, fontweight='bold', color=highlight_color)
        # Country name label next to the icon
        ax.text(flag_x + flag_box_width + xmax * 0.01, y, cat, va='center', ha='left', fontsize=label_fontsize, color='black')
    else:
        # No flag for Other; display de-emphasized text
        ax.text(-xmax * 0.01, y, cat, va='center', ha='left', fontsize=label_fontsize, color='#6c6c6c')

# Title (top center-left) with optional small phone icon (simple unicode)
ax.text(0.005, 1.03, "📱 Cellphone service cost, 2019 (USD per month)",
        transform=ax.transAxes, fontsize=title_fontsize, fontweight='semibold', va='top', ha='left')

# Short subtitle omitted per design (keeping minimal)
# Add small circles (callout anchors) around endpoints of U.S., China, Russia
# Find indices for those categories
cat_to_index = {cat: i for i, cat in enumerate(categories)}
anchors = []
for key in ["U.S.", "China", "Russia"]:
    if key in cat_to_index:
        idx = cat_to_index[key]
        y = y_pos[idx]
        x = values[idx]
        circle = mpatches.Circle((x, y), 0.35, transform=ax.transData, facecolor='none',
                                 edgecolor=highlight_color, linewidth=2, alpha=circle_alpha)
        ax.add_patch(circle)
        anchors.append((key, x, y))

# Comparative callouts (anchored annotations)
# 1) Next to U.S.: "U.S. — $63 (highest; +$13.5 vs China)"
if "U.S." in cat_to_index and "China" in cat_to_index:
    us_idx = cat_to_index["U.S."]
    china_idx = cat_to_index["China"]
    us_x = values[us_idx]
    us_y = y_pos[us_idx]
    china_x = values[china_idx]
    # Difference
    diff = us_x - china_x
    diff_text = f"+${diff:g}" if diff == int(diff) or diff % 1 != 0 else f"+${int(diff)}"
    callout_text_us = f"U.S. — ${int(us_x) if us_x==int(us_x) else us_x:g} (highest; {diff_text} vs China)"
    # Place annotation to the right/top of U.S. circle with leader line
    ax.annotate(callout_text_us,
                xy=(us_x, us_y), xycoords='data',
                xytext=(us_x + xmax * 0.06, us_y + 0.7), textcoords='data',
                fontsize=annotation_fontsize, va='center', ha='left',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#e6e6e6", lw=0.6),
                arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.0", color="#9b9b9b", lw=0.9))

# 2) Between Russia and Britain: "Russia is ~15.8× cheaper than the U.S."
# We'll place this between Russia and Britain bars; compute ratio U.S./Russia
if "Russia" in cat_to_index and "U.S." in cat_to_index:
    r_idx = cat_to_index["Russia"]
    b_idx = cat_to_index["Britain"] if "Britain" in cat_to_index else None
    r_x = values[r_idx]
    r_y = y_pos[r_idx]
    us_val = aggregated["U.S."]
    ratio = us_val / aggregated["Russia"] if aggregated["Russia"] != 0 else float('inf')
    ratio_text = f"Russia is ~{ratio:.1f}× cheaper than the U.S."
    # Put annotation to the left of midpoint between Russia and Britain for clarity
    place_x = r_x + xmax * 0.02
    place_y = r_y + 0.9
    ax.annotate(ratio_text,
                xy=(r_x, r_y), xycoords='data',
                xytext=(place_x, place_y), textcoords='data',
                fontsize=annotation_fontsize, va='center', ha='left',
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#e6e6e6", lw=0.6),
                arrowprops=dict(arrowstyle="-", connectionstyle="angle,angleA=0,angleB=90", color="#9b9b9b", lw=0.9))

# 3) Optional thin difference connector between U.S. and China endpoints with inline label "+$13.5"
# Draw a horizontal bar/connector between endpoints
if "U.S." in cat_to_index and "China" in cat_to_index:
    us_x = aggregated["U.S."]
    china_x = aggregated["China"]
    us_y = y_pos[cat_to_index["U.S."]]
    china_y = y_pos[cat_to_index["China"]]
    # Place connector at a small offset between the two bars (use y between their y positions)
    connector_y = (us_y + china_y) / 2.0 + 0.15
    # Draw line
    line = Line2D([china_x, us_x], [connector_y, connector_y], color="#6c6c6c", linewidth=1.0)
    ax.add_line(line)
    # Small vertical ticks
    ax.add_line(Line2D([china_x, china_x], [connector_y - 0.08, connector_y + 0.08], color="#6c6c6c", linewidth=1.0))
    ax.add_line(Line2D([us_x, us_x], [connector_y - 0.08, connector_y + 0.08], color="#6c6c6c", linewidth=1.0))
    # Difference label
    diff_val = us_x - china_x
    diff_label = f"+${diff_val:g}"
    ax.text((china_x + us_x) / 2.0, connector_y + 0.08, diff_label, ha='center', va='bottom', fontsize=annotation_fontsize, color="#3d3d3d")

# Add the specific short annotation strings near the respective bars as concise one-line notes (per design)
annotation_texts = {
    "U.S.": "U.S. — $63 (highest; +$13.5 vs China)",
    "China": "China — $49.5",
    "Britain": "Britain — $33",
    "France": "France — $15",
    "Russia": "Russia — $4 (lowest among named)",
    "Other (various)": f"Other (various) — multiple observations ({other_count}), de-emphasized"
}

# Position these small annotations to the right of each bar, slightly offset vertically to avoid overlap
for cat, txt in annotation_texts.items():
    if cat in cat_to_index:
        idx = cat_to_index[cat]
        y = y_pos[idx]
        x = values[idx]
        # Slight vertical offset so the numeric label (already present) and annotation don't overlap
        y_offset = -0.25 if cat in ["U.S.", "China"] else -0.18
        ax.text(x + xmax * 0.09, y + y_offset, txt, fontsize=annotation_fontsize, color=("#6c6c6c" if cat == "Other (various)" else "#222222"))

# Footnote / metadata bottom-left
footnote = "Prices in USD; 2019. Source: National Communications Agency."
ax.text(0.01, -0.08, footnote, transform=ax.transAxes, fontsize=footnote_fontsize, va='bottom', ha='left', color="#666666")

# Small government logo placeholder bottom-right (simple badge)
logo_x = 0.92
logo_y = -0.12
# Draw a simple circular emblem
logo_circle = mpatches.Circle((logo_x, logo_y + 0.02), 0.015, transform=fig.transFigure, facecolor="#0D6EFD", edgecolor="#0A58CA", linewidth=1.0)
fig.patches.append(logo_circle)
fig.text(logo_x + 0.025, logo_y + 0.005, "Source: National Communications Agency", fontsize=footnote_fontsize, ha='left', va='center', color="#444444")

# Tidy up layout
plt.subplots_adjust(left=0.18, right=0.92, top=0.88, bottom=0.16)

# Remove spines that are not needed to keep the design clean
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_color("#e6e6e6")

# Ensure adequate whitespace and show
plt.savefig("generated/cellphone_factor3_2_design.png", dpi=300, bbox_inches="tight")