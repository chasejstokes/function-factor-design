import math
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
import matplotlib.patheffects as path_effects

# Ensure seaborn is available for consistent "whitegrid" style
try:
    import seaborn as sns
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "seaborn"])
    import seaborn as sns

# Use seaborn whitegrid style
sns.set_style("whitegrid")

# Data setup (as provided)
raw_entries = [
    ("Russia", 4.0),
    ("Other", 7.0),
    ("Other", 7.2),
    ("Other", 9.0),
    ("Other", 12.0),
    ("France", 15.0),
    ("Other", 18.0),
    ("Britain", 33.0),
    ("Other", 34.0),
    ("Other", 37.0),
    ("Other", 42.0),
    ("China", 49.5),
    ("Other", 60.0),
    ("U.S.", 63.0)
]

# Extract named countries and aggregate "Other"
named = {}
other_vals = []
for cat, val in raw_entries:
    if cat == "Other":
        other_vals.append(val)
    else:
        named[cat] = val

# Aggregate "Other" stats
other_n = len(other_vals)
other_median = float(np.median(other_vals)) if other_n > 0 else float('nan')
other_mean = float(np.mean(other_vals)) if other_n > 0 else float('nan')

# Format mean to match design plan's concise "mean $25"
other_mean_display = f"{round(other_mean):.0f}"

# Prepare plotting order:
# Highest named countries first (descending), then place "Other countries ..." as the last bar (muted)
# Named countries only: Russia, France, Britain, China, U.S.
# We'll order named countries descending by value for visual impact (U.S. top)
named_order = sorted(named.items(), key=lambda x: x[1], reverse=True)
# Build final lists: named in descending order, then Other at the bottom
categories = [c for c, v in named_order] + [f"Other countries (n={other_n}): median ${int(other_median)}, mean ${other_mean_display}"]
values = [v for c, v in named_order] + [other_mean]  # for plotting, use mean as representative for position

# Colors: restrained, harmonized palette with increasing saturation as cost increases; Other is muted grey
colors_named = {
    # from lower cost to higher cost mapping, but we'll assign according to the descending order
    "Russia": "#4C72B0",   # cool blue (low)
    "France": "#55A868",   # muted teal
    "Britain": "#DD8452",  # warm orange
    "China": "#C44E52",    # stronger red
    "U.S.": "#8172B2"      # saturated accent (purple)
}
color_other = "#B0B0B0"    # muted grey

bar_colors = []
for cat in categories:
    if cat.startswith("Other countries"):
        bar_colors.append(color_other)
    else:
        bar_colors.append(colors_named.get(cat, "#7F7F7F"))

# Plot parameters
fig, ax = plt.subplots(figsize=(10, 6))

y_pos = np.arange(len(categories))
bar_height = 0.6

# Draw horizontal bars
bars = ax.barh(y_pos, values, height=bar_height, color=bar_colors, edgecolor='none', align='center', zorder=3)

# X-axis configuration
ax.set_xlabel("Cost (USD)", fontsize=11)
ax.set_xlim(0, 70)
ax.set_xticks(np.arange(0, 71, 10))
ax.xaxis.grid(True, color="#DDDDDD", linewidth=0.8, zorder=0)
ax.invert_yaxis()  # highest on top as per plan

# Y tick labels: use the category names (country or aggregated "Other" with stats)
ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontsize=10)

# Title and subtitle
title_text = "Cellphone service cost by country, 2019 (USD)"
subtitle_text = "U.S. consumers paid the most in 2019—$63 on average—well above China ($49.5) and Britain ($33). Other countries are aggregated (n=9, median $18)."

ax.set_title(title_text, fontsize=16, fontweight='bold', pad=12)
# Subtitle slightly smaller and directly under title
fig.text(0.5, 0.93, subtitle_text, ha='center', va='top', fontsize=11)

# On-bar numeric labels (only for named countries and the aggregate "Other")
for i, (cat, val, bar) in enumerate(zip(categories, values, bars)):
    # Display the value as USD rounded to 1 decimal if needed, but prefer whole dollars for consistency
    if cat.startswith("Other countries"):
        label = f"${int(round(np.mean(other_vals))):d}"
    else:
        # use the original named value
        orig_val = named[cat]
        # show 1 decimal for China and others with decimal
        if abs(orig_val - round(orig_val)) > 0.05:
            label = f"${orig_val:.1f}"
        else:
            label = f"${int(round(orig_val))}"
    x_val = val
    y_coord = bar.get_y() + bar.get_height() / 2
    # Place numeric label slightly to the right end of the bar
    ax.text(x_val + 1.5, y_coord, label, va='center', ha='left', fontsize=10, color='black', zorder=6,
            bbox=dict(boxstyle="square,pad=0.2", fc=(1,1,1,0.0), ec='none'))

# Country names are already on the y-axis adjacent to bars (left). This matches the "labels adjacent to bars" requirement.

# Two compact comparison callouts with thin arrows
# Identify y positions for U.S. and China
def find_ypos_for_category(cat_name):
    for idx, cat in enumerate(categories):
        if cat == cat_name:
            return idx
    return None

y_us = find_ypos_for_category("U.S.")
y_china = find_ypos_for_category("China")

# Callout A near U.S. bar: "U.S. $63 — highest in sample"
if y_us is not None:
    val_us = named["U.S."]
    text_A = "U.S. $63 — highest in sample"
    # position to the right of U.S. bar
    text_x_A = val_us + 6
    text_y_A = y_us
    bbox_props = dict(boxstyle="round,pad=0.35", fc=(1,1,1,0.85), ec="#CFCFCF", lw=0.8)
    # thin, low-contrast arrow
    ax.annotate(text_A,
                xy=(val_us, text_y_A), xycoords='data',
                xytext=(text_x_A, text_y_A + 0.0), textcoords='data',
                va='center', ha='left', fontsize=9, bbox=bbox_props,
                arrowprops=dict(arrowstyle='-|>', color='0.35', lw=0.8, shrinkA=0, shrinkB=6, mutation_scale=8),
                zorder=7)

    # add a slim colored left border to the callout to tie to the U.S. bar color
    # approximate the left border position and height in data coordinates
    left_border_x = text_x_A - 0.08 * 70  # offset relative to axis width
    # draw a small vertical line segment to act as a colored left border
    ax.plot([left_border_x, left_border_x],
            [text_y_A - 0.18, text_y_A + 0.18],
            color=colors_named["U.S."], linewidth=3, solid_capstyle='butt', zorder=8, alpha=0.95)

# Callout B between U.S. and China: "U.S. ≈ $13.5 more than China"
if (y_us is not None) and (y_china is not None):
    val_china = named["China"]
    diff = named["U.S."] - named["China"]
    # Round diff to 1 decimal if not integer
    if abs(diff - round(diff)) > 0.05:
        diff_text = f"{diff:.1f}"
    else:
        diff_text = f"{int(round(diff))}"
    text_B = f"U.S. ≈ ${diff_text} more than China"
    # Position between the two bars, slightly right of China bar
    mid_y = (y_us + y_china) / 2.0
    text_x_B = val_china + 6
    bbox_props_B = dict(boxstyle="round,pad=0.35", fc=(1,1,1,0.85), ec="#CFCFCF", lw=0.8)
    ax.annotate(text_B,
                xy=(val_china, y_china), xycoords='data',
                xytext=(text_x_B, mid_y), textcoords='data',
                va='center', ha='left', fontsize=9, bbox=bbox_props_B,
                arrowprops=dict(arrowstyle='-|>', color='0.35', lw=0.7, shrinkA=0, shrinkB=6, mutation_scale=8),
                zorder=7)
    # add small colored left border tied to U.S. to visually link emphasis (subtle)
    left_border_x_B = text_x_B - 0.08 * 70
    ax.plot([left_border_x_B, left_border_x_B],
            [mid_y - 0.18, mid_y + 0.18],
            color=colors_named["U.S."], linewidth=3, solid_capstyle='butt', zorder=8, alpha=0.9)

# Auxiliary summary box (lower-right)
summary_text = ("Main takeaway: U.S. costs are highest in this set ($63); Russia is the lowest ($4). "
                "Other countries (aggregated) sit near the middle (median $18).")
# place in axis coordinates (0-1)
summary_x_ax = 0.72
summary_y_ax = 0.10
# draw background box with a subtle border and slight transparency
summary_box = dict(boxstyle="round,pad=0.4", facecolor=(1,1,1,0.9), edgecolor="#D0D0D0", linewidth=0.8)
fig.text(summary_x_ax, summary_y_ax, summary_text, fontsize=9, ha='left', va='bottom', bbox=summary_box)

# Source / contextual note bottom-left
source_text = ("Values are per‑country average monthly cellphone service cost, year = 2019. "
               "'Other' aggregated from remaining samples (n=9). Source: dataset provided.")
fig.text(0.02, 0.02, source_text, fontsize=8, ha='left', va='bottom', color="#333333")

# Aesthetics: remove top/right spines, keep left spine thin
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_linewidth(0.8)
ax.tick_params(axis='y', which='both', length=0)  # hide y tick marks (labels suffice)

# Adjust layout to make room for subtitle and source note
plt.subplots_adjust(left=0.32, right=0.96, top=0.88, bottom=0.12)

plt.savefig("generated/cellphone_factor4_1_design.png", dpi=300, bbox_inches="tight")