import matplotlib.pyplot as plt
import numpy as np

# Data setup (from provided data)
named = {
    "Russia": 4.0,
    "France": 15.0,
    "Britain": 33.0,
    "China": 49.5,
    "U.S.": 63.0
}
# Aggregated "Other" entries (9 countries) - use median = 18 as representative
other_label = "Other (9 countries)"
other_value = 18.0

# Combine into list and sort descending by value
categories = list(named.keys()) + [other_label]
values = [named[c] for c in named.keys()] + [other_value]

# Create pairs and sort by value descending
pairs = list(zip(categories, values))
pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)

categories_sorted, values_sorted = zip(*pairs_sorted)
categories_sorted = list(categories_sorted)
values_sorted = list(values_sorted)

# Determine positions
y_pos = np.arange(len(categories_sorted))

# Color mapping (muted, functional)
color_map = {
    "U.S.": "#1f5bb5",     # deep blue
    "China": "#b22222",    # deep red
    "Britain": "#4b0082",  # indigo
    "France": "#008080",   # teal
    "Russia": "#2e8b57",   # green
    other_label: "#bdbdbd" # light gray
}
bar_colors = [color_map.get(cat, "#999999") for cat in categories_sorted]

# Bar thickness: slightly enlarge U.S. bar (+10%)
base_height = 0.6
heights = [base_height] * len(categories_sorted)
# find index of U.S. and increase
if "U.S." in categories_sorted:
    idx_us = categories_sorted.index("U.S.")
    heights[idx_us] = base_height * 1.10

# Plotting
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10
})

fig, ax = plt.subplots(figsize=(9, 6))
bars = ax.barh(y_pos, values_sorted, color=bar_colors, height=heights, edgecolor='none')

# Minimal axis styling
ax.set_yticks(y_pos)
ax.set_yticklabels(categories_sorted, fontsize=10)
ax.invert_yaxis()  # largest on top

# X-axis gridlines at 0,20,40,60
max_val = max(values_sorted) * 1.12
ax.set_xlim(0, max(70, max_val))
ax.set_xticks([0, 20, 40, 60])
ax.grid(axis='x', linestyle='--', color='gray', alpha=0.25)
# remove spines except left baseline for context
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.8)
ax.spines['bottom'].set_color('#444444')

# Title (short, top-left) and subtitle just beneath
fig.suptitle("Cellphone cost, 2019 (USD)", x=0.01, y=0.98, ha='left', fontsize=14, fontweight='medium')
fig.text(0.01, 0.945, "Named countries shown individually; remaining countries aggregated.", fontsize=9, color='#333333')

# Value labels at the end of each bar
for i, (val, bar) in enumerate(zip(values_sorted, bars)):
    x = val
    y = bar.get_y() + bar.get_height() / 2
    label = f"{val:.1f} USD"
    # Slightly bolder for values; emphasize U.S. label more
    if categories_sorted[i] == "U.S.":
        ax.text(x + 1.4, y, label, va='center', fontsize=10, fontweight='semibold', color='#111111')
    else:
        ax.text(x + 1.4, y, label, va='center', fontsize=9.5, fontweight='bold', color='#111111')

# Annotations
bbox_props = dict(boxstyle="round,pad=0.35", fc=(1,1,1,0.85), ec="#888888", lw=0.8)

# 1) U.S. (largest) annotation above the U.S. bar with connector
if "U.S." in categories_sorted:
    i_us = categories_sorted.index("U.S.")
    val_us = values_sorted[i_us]
    y_us = y_pos[i_us]
    # place annotation slightly above the bar
    ann_x = val_us - 10  # put box slightly left of bar end for balance
    ann_y = y_us - 0.35
    ax.annotate(
        "Highest: U.S. — $63.0 (≈3× Russia)",
        xy=(val_us, y_us),
        xytext=(ann_x, ann_y),
        textcoords='data',
        va='center',
        ha='left',
        fontsize=9,
        bbox=bbox_props,
        arrowprops=dict(arrowstyle="->", color='#444444', lw=0.9, alpha=0.6, connectionstyle="arc3,rad=-0.2")
    )

# 2) Russia (lowest) annotation inside/left end of the Russia bar
if "Russia" in categories_sorted:
    i_ru = categories_sorted.index("Russia")
    val_ru = values_sorted[i_ru]
    y_ru = y_pos[i_ru]
    # Place text inside near left end; choose white text if inside colored bar
    ax.text(0.6, y_ru, "Lowest: Russia — $4.0", va='center', ha='left', fontsize=8.5,
            color='white', fontweight='normal', bbox=dict(facecolor=color_map["Russia"], edgecolor='none', pad=0.2))

# 3) China vs Britain callout between those bars pointing to both
if ("China" in categories_sorted) and ("Britain" in categories_sorted):
    i_ch = categories_sorted.index("China")
    i_br = categories_sorted.index("Britain")
    # place central box between their y positions
    y_mid = (y_pos[i_ch] + y_pos[i_br]) / 2.0 + 0.15
    # x position slightly right of Britain's bar end
    x_box = max(values_sorted[i_ch], values_sorted[i_br]) - 10
    txt = f"China $49.5 > Britain $33.0"
    ax.text(x_box, y_mid, txt, va='center', ha='left', fontsize=9, bbox=bbox_props)
    # arrows to each bar end (subtle)
    # to China
    ax.annotate("", xy=(values_sorted[i_ch], y_pos[i_ch]), xytext=(x_box + 0.2, y_mid),
                arrowprops=dict(arrowstyle="-", color='#444444', lw=0.7, alpha=0.5))
    # to Britain
    ax.annotate("", xy=(values_sorted[i_br], y_pos[i_br]), xytext=(x_box + 0.2, y_mid),
                arrowprops=dict(arrowstyle="-", color='#444444', lw=0.7, alpha=0.5))

# 4) Aggregated Others note under the "Other" bar: "Other (9 countries) median $18 — varied range"
if other_label in categories_sorted:
    i_other = categories_sorted.index(other_label)
    y_other = y_pos[i_other]
    # place small note under the bar label (below)
    ax.text(0.5, y_other - 0.28, "median $18 — varied range", va='center', ha='left', fontsize=8.25,
            color='#444444', bbox=dict(boxstyle="round,pad=0.28", facecolor=(0.98,0.98,0.98,0.9), edgecolor='#CCCCCC', lw=0.6))

# Source line bottom-left small
fig.text(0.01, 0.01, "Source: dataset (compiled).", fontsize=8, color='#444444')

# Tight layout adjustments
plt.subplots_adjust(left=0.22, right=0.96, top=0.88, bottom=0.08)

# Show the plot (static)
plt.savefig("generated/cellphone_factor2_2_design.png", dpi=300, bbox_inches="tight")