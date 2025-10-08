import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D
import matplotlib as mpl

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Use np.nan for missing euro data
euro = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Identify indices for target years (2012-2014)
target_years = [2012, 2013, 2014]
target_mask = np.isin(years, target_years)

# Figure and axes (portrait 3:4 aspect ratio)
fig = plt.figure(figsize=(9, 12), dpi=120)
# Main axes takes most of the left area to leave room for summary on the right
ax = fig.add_axes([0.06, 0.14, 0.70, 0.80])

# Colors and styling
spain_color = "#B00020"          # deep crimson for Spain
spain_edge = "#7f0016"
euro_color = "#6E7B8B"           # muted slate grey-blue for Euro-Zone average
euro_edge = "#4f5b59"
placeholder_color = "#d6d6d6"     # very light grey for missing Euro placeholders

bar_width = 0.38
x = np.arange(len(years))
x_spain = x - bar_width / 2
x_euro = x + bar_width / 2

# Background grid and y axis limits
ax.set_ylim(-12, 3)
ax.yaxis.grid(True, color=(0.2, 0.2, 0.2, 0.12), linewidth=0.8, linestyle='-')
ax.set_axisbelow(True)

# Draw bars: Spain (with special styling for targets) and Euro (with placeholders)
spain_bars = []
euro_bars = []
for i, yr in enumerate(years):
    # Spain bar
    if target_mask[i]:
        # Projected target: use fill with hatch and partial transparency
        bar = ax.bar(
            x_spain[i],
            spain[i],
            width=bar_width,
            color=spain_color,
            edgecolor=spain_edge,
            linewidth=0.9,
            hatch='////',
            alpha=0.75,
            zorder=3
        )
    else:
        bar = ax.bar(
            x_spain[i],
            spain[i],
            width=bar_width,
            color=spain_color,
            edgecolor=spain_edge,
            linewidth=0.9,
            zorder=3
        )
    spain_bars.append(bar[0])

    # Euro bar or placeholder when missing
    if np.isnan(euro[i]):
        # Place a very light semi-transparent rectangle to preserve grouping alignment
        rect = Rectangle(
            (x_euro[i] - bar_width / 2, -12),
            bar_width,
            15,  # covers from -12 to +3
            facecolor=placeholder_color,
            alpha=0.28,
            edgecolor='none',
            zorder=1
        )
        ax.add_patch(rect)
        # Add thin dashed guideline at the euro position
        ax.vlines(
            x_euro[i],
            -12, 3,
            colors=(0.4, 0.4, 0.4, 0.25),
            linestyles='dashed',
            linewidth=0.8,
            zorder=2
        )
        # Add small "no data" label above zero baseline within that group
        ax.text(
            x_euro[i], 1.5, "no data",
            ha='center', va='center',
            fontsize=11, color='gray',
            zorder=4
        )
        euro_bars.append(None)
    else:
        bar = ax.bar(
            x_euro[i],
            euro[i],
            width=bar_width,
            color=euro_color,
            edgecolor=euro_edge,
            linewidth=0.9,
            alpha=0.95,
            zorder=2
        )
        euro_bars.append(bar[0])

# Simulate rounded corners by adding small circles at bar tops (positive) or bottoms (negative)
def add_round_caps(bars, color, edgecolor):
    for bar in bars:
        if bar is None:
            continue
        x0 = bar.get_x()
        w = bar.get_width()
        h = bar.get_height()
        cx = x0 + w / 2
        # For positive heights, place cap at top; for negative, place cap at bottom (top of shape)
        if h >= 0:
            cy = h
        else:
            cy = h
        # Add a small circle to soften the top/bottom appearance
        radius = w * 0.5 * 0.7
        circle = Circle(
            (cx, cy),
            radius=radius,
            facecolor=color,
            edgecolor=edgecolor,
            linewidth=0.9,
            zorder=4
        )
        ax.add_patch(circle)

add_round_caps(spain_bars, spain_color, spain_edge)
# For euro bars only add caps to non-missing ones
add_round_caps(euro_bars, euro_color, euro_edge)

# Zero baseline stronger
ax.axhline(0, color='black', linewidth=2.0, zorder=5)

# X-axis labels and ticks
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=14)
ax.set_xlabel("Year", fontsize=18, labelpad=12)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, labelpad=12)

# Legend (custom handles)
legend_handles = [
    Rectangle((0, 0), 1, 1, facecolor=spain_color, edgecolor=spain_edge, linewidth=0.9),
    Rectangle((0, 0), 1, 1, facecolor=euro_color, edgecolor=euro_edge, linewidth=0.9),
    Rectangle((0, 0), 1, 1, facecolor=spain_color, edgecolor=spain_edge, linewidth=0.9, hatch='////', alpha=0.75)
]
legend_labels = ["Spain", "Euro‑Zone average", "Projected target (Spain)"]
legend = ax.legend(
    legend_handles,
    legend_labels,
    loc='upper right',
    fontsize=16,
    frameon=False,
    bbox_to_anchor=(0.98, 0.96),
    handlelength=1.2,
    handletextpad=0.6
)

# Title and subtitle
title = "Spain vs Euro‑Zone: Budget balance (% of GDP), 1999–2014"
subtitle = (
    "Paired bars show Spain (left) and the Euro‑Zone average (right) each year; "
    "positive = surplus, negative = deficit.\n"
    "Final three Spain bars (2012–2014) are government targets (not outturns); "
    "Euro‑Zone averages unavailable for those years."
)
fig.suptitle(title, fontsize=34, fontweight='bold', y=0.975)
fig.text(0.06, 0.925, subtitle, fontsize=20, va='top')

# Selective callouts for key points: 2006 (2.4), 2009 (-11.2), and 2005 (1.3)
callouts = [
    {"year": 2006, "value": 2.4, "text": "2006: Spain = 2.4%"},
    {"year": 2009, "value": -11.2, "text": "2009: Spain = -11.2%"},
    {"year": 2005, "value": 1.3, "text": "2005: Spain = 1.3% (outperforming EZ)"}
]
for c in callouts:
    idx = int(np.where(years == c["year"])[0][0])
    x_pos = x_spain[idx] + bar_width / 2  # center of Spain bar
    y_val = spain[idx]
    # Position the annotation offset points to not overlap crowded bars
    if y_val >= 0:
        xytext = (25, 18) if c["year"] != 2006 else (28, 28)
    else:
        xytext = (-80, -32)  # place below for deep negative
    ax.annotate(
        c["text"],
        xy=(x_pos, y_val),
        xytext=xytext,
        textcoords='offset points',
        fontsize=12,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", lw=0.7, alpha=0.95),
        arrowprops=dict(arrowstyle="-", lw=0.9, color='gray'),
        ha='center',
        va='center',
        zorder=10
    )

# Compact difference annotation for the large Spain-Euro discrepancy (2009)
# Provide factual comparative text near the 2009 cluster
ann_text = "2009: Spain −11.2 vs Euro −6.3 — gap = 4.9 pp"
ax.text(
    x[np.where(years == 2009)[0][0]] + 0.9,
    -2.0,
    ann_text,
    fontsize=12.5,
    color='black',
    bbox=dict(boxstyle="round,pad=0.3", fc='white', ec='none', alpha=0.9),
    zorder=11
)

# Right-side synthesis summary (prominent but not dominant)
summary_x = 0.79  # figure-relative coordinates (to the right area)
summary_y = 0.68
summary_text = (
    "Summary: Spain moved from modest deficits into surpluses (2005–2007) then plunged\n"
    "to a max deficit of -11.2% in 2009 during the crisis; targets (2012–2014) indicate\n"
    "planned recovery. 2009–2011 show the largest Spain vs Euro gaps (see note)."
)
fig.text(
    summary_x, summary_y, summary_text,
    fontsize=16, fontweight='semibold', va='top', ha='left'
)

# Small provenance footnote at bottom
footnote = "Data: Government budgets; Spain 2012–2014 are official targets. Euro‑Zone average not available for 2012–2014."
fig.text(0.06, 0.05, footnote, fontsize=12, va='bottom', ha='left', color='gray')

# Fine-tune layout, tick formatting and appearance
ax.tick_params(axis='x', which='major', labelsize=14)
ax.tick_params(axis='y', which='major', labelsize=14)
# Ensure y ticks are at tidy intervals
ax.set_yticks(np.arange(-12, 4, 2))
ax.set_yticklabels([f"{t}%" for t in np.arange(-12, 4, 2)], fontsize=14)

# Tighten spacing for presentation clarity
plt.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.08)

# Display the plot
plt.savefig("generated/spain_factor4_bar5/spain_factor4_bar5_design.png", dpi=300, bbox_inches="tight")