import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Data setup (from provided dataset)
data = [
    {"year": 1999, "spain": -1.2, "euro_zone_average": -0.9},
    {"year": 2000, "spain": -0.6, "euro_zone_average": -0.4},
    {"year": 2001, "spain": -0.4, "euro_zone_average": -0.8},
    {"year": 2002, "spain": -1.0, "euro_zone_average": -1.6},
    {"year": 2003, "spain": -0.8, "euro_zone_average": -2.6},
    {"year": 2004, "spain": 0.6, "euro_zone_average": -2.9},
    {"year": 2005, "spain": 1.3, "euro_zone_average": -1.8},
    {"year": 2006, "spain": 2.4, "euro_zone_average": 1.1},
    {"year": 2007, "spain": 1.9, "euro_zone_average": -0.8},
    {"year": 2008, "spain": -4.5, "euro_zone_average": -3.6},
    {"year": 2009, "spain": -11.2, "euro_zone_average": -6.3},
    {"year": 2010, "spain": -9.5, "euro_zone_average": -6.0},
    {"year": 2011, "spain": -7.8, "euro_zone_average": -4.1},
    {"year": 2012, "spain": -4.2, "euro_zone_average": -4.6},
    {"year": 2013, "spain": -5.0, "euro_zone_average": -3.8},
    {"year": 2014, "spain": -2.5, "euro_zone_average": -2.0}
]

years = [d["year"] for d in data]
spain_vals = np.array([d["spain"] for d in data])
ez_vals = np.array([d["euro_zone_average"] for d in data])

# Styling parameters
spain_color = "#C62828"      # saturated warm red
ez_color = "#2E7DB2"         # cool muted blue
grid_color = "#BDBDBD"
zero_line_color = "#757575"

# Canvas: portrait 3:4, using inches for figsize; 900x1200 px ~ (9,12) at dpi=100
fig_w, fig_h = 9, 12
fig = plt.figure(figsize=(fig_w, fig_h), dpi=100)
ax = fig.add_axes([0.08, 0.14, 0.86, 0.78])  # leave space for title/subtitle and caption/metadata

# Bar positions and widths
x = np.arange(len(years))
group_width = 0.8
bar_width = group_width / 2.2  # gives a small gap between the two bars
offset = bar_width / 1.1

# Draw subtle highlight rectangle for 2008-2010 (years 2008 index 9 to 2010 index 11)
start_year = 2008
end_year = 2010
start_idx = years.index(start_year)
end_idx = years.index(end_year)
rect_left = (start_idx - 0.5 * group_width)
rect_right = (end_idx + 0.5 * group_width)
rect_width = rect_right - rect_left
highlight = mpatches.Rectangle(
    (rect_left, ax.get_ylim()[0] if ax.get_ylim() != (0, 1) else -12),  # temp; will update after ylim set
    rect_width,
    1,  # temp height
    transform=ax.transData,
    color="#FFD9D9",  # very pale warm tint to not fight the red/blue bars
    alpha=0.25,
    zorder=0
)
# We'll add the rectangle after setting y-limits so we know height.

# Plot bars
spain_bars = ax.bar(x - offset, spain_vals, width=bar_width, color=spain_color, label="Spain", zorder=3)
ez_bars = ax.bar(x + offset, ez_vals, width=bar_width, color=ez_color, label="Euro‑Zone average", zorder=3)

# Emphasize zero baseline
ymin = min(spain_vals.min(), ez_vals.min())
ymax = max(spain_vals.max(), ez_vals.max())
y_margin = max(1.5, (ymax - ymin) * 0.08)
ax.set_ylim(ymin - y_margin, ymax + y_margin)

# Now finalize and add highlight rectangle with correct height
rect_height = (ax.get_ylim()[1] - ax.get_ylim()[0])
highlight.set_y(ax.get_ylim()[0])
highlight.set_height(rect_height)
ax.add_patch(highlight)

# Zero line
ax.axhline(0, color=zero_line_color, linewidth=1.6, zorder=4)

# Gridlines every 2 percentage points (or 5 if range large)
y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
if y_range <= 30:
    y_step = 2
else:
    y_step = 5
y_ticks = np.arange(np.floor(ax.get_ylim()[0] / y_step) * y_step, np.ceil(ax.get_ylim()[1] / y_step) * y_step + 0.1, y_step)
ax.set_yticks(y_ticks)
ax.yaxis.grid(True, color=grid_color, linewidth=0.8, linestyle='-', zorder=1)
ax.set_axisbelow(False)
for line in ax.get_ygridlines():
    line.set_zorder(1)
    line.set_alpha(0.6)

# Axis labels and ticks styling
ax.set_ylabel("Budget balance (% of GDP)", fontsize=20, fontweight='bold', labelpad=12)
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=15)
ax.tick_params(axis='y', labelsize=15)

# Title and subtitle (large, centered at top)
title_text = "Spain vs Euro‑Zone: Budget deficit / surplus (% of GDP), 1999–2014"
subtitle_text = "Paired bars show annual budget balance; Spain’s large post‑2008 swing is highlighted"

fig.suptitle(title_text, fontsize=40, fontweight='bold', y=0.985)
# Subtitle placed slightly below the title
fig.text(0.5, 0.945, subtitle_text, ha='center', fontsize=24)

# Legend top-right with variable description just below it
legend_handles = [
    mpatches.Patch(color=spain_color, label="Spain (red)"),
    mpatches.Patch(color=ez_color, label="Euro‑Zone average (blue)")
]
legend = ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(0.60, 1.07), frameon=False, fontsize=16)
# Variable descriptor line
fig.text(0.605, 0.895, "Values = % of GDP (negative = deficit, positive = surplus)", fontsize=16)

# Add the one strong annotation: Spain 2009 extreme deficit (-11.2%)
idx_2009 = years.index(2009)
x_2009 = x[idx_2009] - offset
y_2009 = spain_vals[idx_2009]
# Place label slightly above the top of the 2009 Spain bar (since it's negative, "above" i.e., closer to zero)
label_y = y_2009 + (y_margin * 0.6)
ax.text(x_2009, label_y, "-11.2% (2009)", ha='center', va='bottom', fontsize=15, fontweight='bold', color='black', zorder=6)

# Optional subtle euro-zone mean dotted line (muted gray)
ez_mean = ez_vals.mean()
ax.axhline(ez_mean, color="#9E9E9E", linestyle=':', linewidth=1.2, zorder=2)
fig.text(0.945, 0.55, f"EZ mean ≈ {ez_mean:.1f}%", ha='right', fontsize=11, color="#616161")

# Caption (bottom-left) and present-valenced subtext (italic)
caption = ("Data plotted are annual general‑government budget balances as % of GDP (1999–2014). "
           "Spain moves from small surpluses in mid‑2000s to a deep deficit after 2008; peak Spain deficit = −11.2% (2009). "
           "Euro‑Zone average is consistently less extreme.")
present_valenced = "Spain’s post‑2008 plunge reflects the scale of the financial shock and its fiscal impact."
fig.text(0.08, 0.06, caption, ha='left', fontsize=14)
fig.text(0.08, 0.035, present_valenced, ha='left', fontsize=14, style='italic')

# Metadata block (bottom-right)
metadata = ("Source: Provided dataset (1999–2014). Units: percent of GDP. "
            "Chart: grouped bars; zero line indicates balanced budget.")
fig.text(0.95, 0.035, metadata, ha='right', fontsize=12)

# Tidy layout adjustments for presentation spacing
plt.subplots_adjust(top=0.92, bottom=0.12, left=0.08, right=0.96)

# Improve bar aesthetics: subtle edge lines and slight rounding illusion by adding thin edge
for bar in spain_bars + ez_bars:
    bar.set_edgecolor('none')
    # Slightly reduce linewidth; Matplotlib doesn't support rounded bar corners by default in bar()
    bar.set_linewidth(0.5)

# Ensure high-contrast for axis spines and ticks
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='x', which='both', length=0)

# Save and show
plt.savefig("generated/spain_factor1_bar6/spain_factor1_bar6_design.png", dpi=300, bbox_inches="tight")