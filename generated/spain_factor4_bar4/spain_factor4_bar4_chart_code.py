import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Data provided
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
     1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Use np.nan for missing euro-zone values (2012-2014)
euro = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Compute summary statistics for the summary box
spain_mean = np.nanmean(spain)
euro_mean = np.nanmean(euro)  # this excludes the np.nan entries automatically

# Compute deltas (Spain - Euro) where euro exists
valid_mask = ~np.isnan(euro)
deltas = spain[valid_mask] - euro[valid_mask]
delta_years = years[valid_mask]
# find largest positive delta (Spain advantage) and largest negative (worst underperformance)
largest_positive_idx = np.nanargmax(deltas)
largest_negative_idx = np.nanargmin(deltas)
largest_positive = (delta_years[largest_positive_idx], deltas[largest_positive_idx])
largest_negative = (delta_years[largest_negative_idx], deltas[largest_negative_idx])

# Plot styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'axes.titlesize': 36,
    'axes.titleweight': 'bold'
})

fig, ax = plt.subplots(figsize=(9, 12))  # portrait 3:4 ratio (9x12 inches)

# Positions for clustered bars
x = np.arange(len(years))
width = 0.35

# Colors
spain_color = "#c62828"  # deep Spanish red
euro_color = "#9e9e9e"   # muted gray

# Plot Spain bars
sp_bars = ax.bar(x - width/2, spain, width, label='Spain', color=spain_color, zorder=3)

# Plot Euro bars only where data exists
euro_mask = ~np.isnan(euro)
ez_x = x[euro_mask] + width/2
ez_vals = euro[euro_mask]
ez_bars = ax.bar(ez_x, ez_vals, width, label='Euro‑Zone average', color=euro_color, zorder=2)

# Apply hatch and transparency to Spain's target years (2012-2014 are last 3 entries)
target_indices = np.array([13, 14, 15])  # indices in arrays for 2012,2013,2014
for idx in target_indices:
    # Replace the regular Spain bar with a hatched, semi-transparent bar and dashed edge
    bar = sp_bars[idx]
    # Remove and redraw the bar with appropriate styling
    bar.remove()
    ax.bar(x[idx] - width/2,
           spain[idx],
           width,
           color=spain_color,
           alpha=0.45,
           hatch='///',
           edgecolor='black',
           linewidth=0.8,
           linestyle='--',
           zorder=4)

    # In-bar "Target" label: place slightly above the top of the bar for negative bars, or inside if positive
    val = spain[idx]
    # For negative bars, top is closer to zero; place label slightly above bar top
    if val < 0:
        ypos = val + 0.5
        va = 'bottom'
        txt_color = 'white'
    else:
        ypos = val / 2.0
        va = 'center'
        txt_color = 'white'
    ax.text(x[idx] - width/2, ypos, "Target", ha='center', va=va, fontsize=17, fontweight='bold', color=txt_color, zorder=6)

# Emphasize zero baseline
ax.axhline(0, color='black', linewidth=1.8, zorder=5)

# Gridlines every 2 percentage points
y_min, y_max = -12.5, 4.5
ax.set_ylim(y_min, y_max)
y_ticks = np.arange(-12, 5, 2)
ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{int(t)}" for t in y_ticks], fontsize=20)
ax.yaxis.grid(True, which='major', color='#eeeeee', linewidth=1)
ax.xaxis.grid(False)

# X-axis labels: show year every tick, bold
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=18, fontweight='bold')

# Y-axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=20)

# Title and subtitle
title_text = "Spain vs Euro‑Zone: Budget Balance (% of GDP), 1999–2014"
subtitle_text = ("Spain’s large boom‑to‑bust swing and subsequent deficit targets contrasted with Euro‑Zone averages — "
                 "targets shown for 2012–2014.")
ax.set_title(title_text, pad=26)
# Subtitle placed using fig.text for precise control
fig.text(0.5, 0.93, subtitle_text, ha='center', va='center', fontsize=22)

# Legend: include a patch for Targets (hatch)
sp_patch = mpatches.Patch(color=spain_color, label='Spain')
ez_patch = mpatches.Patch(color=euro_color, label='Euro‑Zone average')
target_patch = mpatches.Patch(facecolor=spain_color, hatch='///', edgecolor='black', label='Spain targets (2012–2014)')
legend = ax.legend(handles=[sp_patch, ez_patch, target_patch],
                   loc='upper left', bbox_to_anchor=(0.02, 1.02), fontsize=16, frameon=False)

# Add "No data" subtle markers for Euro‑Zone missing years (2012-2014)
for idx in target_indices:
    # place a faint marker slightly above zero to indicate missing aggregate
    ax.text(x[idx], 1.6, "No EZ data", ha='center', va='bottom', fontsize=12, color='#9e9e9e', alpha=0.7)

# Selective numeric annotations and delta pills
# 2005-2007 cluster callout (anchor at 2006)
year_2006_idx = np.where(years == 2006)[0][0]
callout_text_2006 = "Spain surplus vs EZ deficit (2005–07)\n2006: Spain 2.4 vs EZ −1.3 (Δ = +3.7)"
# Position the callout to the right of the 2006 cluster
callout_x = x[year_2006_idx] + 1.1
callout_y = 3.5
ax.annotate(callout_text_2006,
            xy=(x[year_2006_idx] - width/2, spain[year_2006_idx]),
            xytext=(callout_x, callout_y),
            fontsize=18,
            ha='left',
            va='top',
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#888888", lw=1),
            arrowprops=dict(arrowstyle="-", color="#888888", lw=0.9, connectionstyle="arc3,rad=0.15"))

# 2009 deepest gap callout
year_2009_idx = np.where(years == 2009)[0][0]
callout_text_2009 = "Deepest gap: 2009 — Spain −11.2 vs EZ −6.3 (Δ = −4.9)"
callout_x2 = x[year_2009_idx] + 1.0
callout_y2 = -3.0
ax.annotate(callout_text_2009,
            xy=(x[year_2009_idx] + width/2, euro[year_2009_idx]),
            xytext=(callout_x2, callout_y2),
            fontsize=18,
            ha='left',
            va='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#888888", lw=1),
            arrowprops=dict(arrowstyle="-", color="#888888", lw=0.9, connectionstyle="arc3,rad=-0.15"))

# Delta pills for 2006 and 2009 placed between paired bars
def add_delta_pill(year_val):
    idx = np.where(years == year_val)[0][0]
    if not np.isnan(euro[idx]):
        delta = spain[idx] - euro[idx]
        x_pos = x[idx]  # center between the two bars
        # y position: slightly above the higher of the two bar tops (closer to zero)
        top_y = max(spain[idx], euro[idx])
        # offset to ensure pill doesn't collide with bar
        y_pos = top_y + (0.6 if top_y >= 0 else 0.6)
        sign = "+" if delta > 0 else ""
        pill_text = f"Δ = {sign}{delta:.1f}"
        ax.text(x_pos, y_pos, pill_text, ha='center', va='center',
                fontsize=16, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", lw=0.8))
# Add for 2006 and 2009
add_delta_pill(2006)
add_delta_pill(2009)

# Summary box top-right
summary_lines = [
    f"Summary: Spain mean (1999–2014) ≈ {spain_mean:.2f}% of GDP",
    f"Euro‑Zone mean (1999–2011) ≈ {euro_mean:.2f}% of GDP",
    f"Largest Spain advantage: {int(largest_positive[0])} (Δ = {largest_positive[1]:+.1f} pp);",
    f"Worst Spain gap: {int(largest_negative[0])} (Δ = {largest_negative[1]:+.1f} pp).",
    "Last three years are government targets, not outturns."
]
summary_text = "\n".join(summary_lines)
# Place box in axes coordinates near top-right
ax.text(0.99, 0.82, summary_text, transform=ax.transAxes,
        ha='right', va='top', fontsize=18, bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#bbbbbb", lw=0.9))

# Footnote at bottom center
footnote = ("Notes: Euro‑Zone aggregate unavailable for 2012–2014. Spain values for 2012–2014 are government targets "
            "(not realized outturns). Data = budget balance (% of GDP).")
fig.text(0.5, 0.02, footnote, ha='center', va='bottom', fontsize=16)

# Polish layout: reduce right margin to make room for summary box
plt.subplots_adjust(top=0.86, right=0.87, left=0.09, bottom=0.08)

# Show plot
plt.savefig("generated/spain_factor4_bar4/spain_factor4_bar4_design.png", dpi=300, bbox_inches="tight")