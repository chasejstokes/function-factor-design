import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import numpy as np
from matplotlib import rcParams

# Data setup
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

# Compute averages for the caption
avg_spain = spain_vals.mean()
avg_ez = ez_vals.mean()

# Colors and styling
color_spain = "#C6453B"   # warm saturated
color_ez = "#3B7BC6"      # cool muted
grid_color = "#E6E6E6"
zero_line_color = "#4D4D4D"  # dark gray for baseline
callout_box_face = "#F2F2F2"  # very pale gray for callouts
callout_edge = "#BFBFBF"

# Helper to slightly darken a hex color for bar edge
def darker(hexcolor, factor=0.85):
    hexcolor = hexcolor.lstrip('#')
    r = int(hexcolor[0:2], 16)
    g = int(hexcolor[2:4], 16)
    b = int(hexcolor[4:6], 16)
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"

edge_spain = darker(color_spain, 0.8)
edge_ez = darker(color_ez, 0.9)

# Figure setup
rcParams.update({"font.size": 10})
fig, ax = plt.subplots(figsize=(12, 6.5))
fig.subplots_adjust(top=0.86, bottom=0.19, left=0.11, right=0.96)

# Positions for grouped bars
n = len(years)
indices = np.arange(n)
bar_width = 0.35  # per-bar width
offset = bar_width / 2.0

# Shaded band for global financial crisis (2008-2010)
# find indices for years
year_to_index = {y: i for i, y in enumerate(years)}
start_idx = year_to_index[2008] - 0.5
end_idx = year_to_index[2010] + 0.5
ax.axvspan(start_idx, end_idx, color='lightgray', alpha=0.12, zorder=0)

# Draw bars (Spain left, EZ right)
bars_spain = ax.bar(indices - offset, spain_vals, width=bar_width,
                    color=color_spain, edgecolor=edge_spain, linewidth=1.2, zorder=3, label="Spain")
bars_ez = ax.bar(indices + offset, ez_vals, width=bar_width,
                 color=color_ez, edgecolor=edge_ez, linewidth=0.9, alpha=0.95, zorder=3, label="Euro‑Zone Average")

# Zero baseline emphasized
ax.axhline(0, color=zero_line_color, linewidth=1.5, zorder=4)

# Horizontal gridlines at specific ticks
yticks = [-12, -9, -6, -3, 0, 3]
ax.set_yticks(yticks)
ax.set_ylim(-12.5, 3.0)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f'))
ax.grid(axis='y', color=grid_color, linewidth=0.9, zorder=0)

# X-axis labels and ticks
ax.set_xticks(indices)
ax.set_xticklabels(years)
ax.set_xlabel("Year", labelpad=8)
ax.set_ylabel("Budget balance (% of GDP); positive = surplus, negative = deficit", labelpad=10, rotation=90)

# Title and subtitle
title_text = "Spain vs. Euro‑Zone: Budget Balance (% of GDP), 1999–2014"
subtitle_text = ("Spain outperformed the euro‑zone average in the mid‑2000s but recorded substantially "
                 "larger deficits after the 2008 crisis")
ax.set_title(title_text, fontsize=14, fontweight='bold', pad=18)
# Subtitle slightly smaller and medium weight placed under title
fig.text(0.5, 0.915, subtitle_text, ha='center', va='center', fontsize=11)

# Legend: compact inside top-right of plot area
legend = ax.legend(loc='upper right', frameon=True, fontsize=9, framealpha=0.9,
                   borderpad=0.4, handlelength=1.2, handletextpad=0.6)
legend.get_frame().set_edgecolor("#DDDDDD")
legend.get_frame().set_linewidth(0.8)
legend.get_frame().set_facecolor("white")

# Selective numeric labels for extremes (2006 positive, 2009 negative for Spain)
# 2006 label above Spain bar
i2006 = year_to_index[2006]
sp2006 = spain_vals[i2006]
ax.annotate(f"+{sp2006:.1f}%", xy=(i2006 - offset, sp2006), xytext=(0, 4),
            textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='normal', color=edge_spain, zorder=6)
# 2009 label below Spain bar
i2009 = year_to_index[2009]
sp2009 = spain_vals[i2009]
ax.annotate(f"{sp2009:.1f}%", xy=(i2009 - offset, sp2009), xytext=(0, -6),
            textcoords="offset points", ha='center', va='top', fontsize=9, fontweight='normal', color=edge_spain, zorder=6)

# Comparison callouts for 2006 and 2009
# 2006: "Spain +1.3 pp above EZ" (Spain 2.4 vs EZ 1.1)
diff_2006 = sp2006 - ez_vals[i2006]
call_2006_text = f"Spain +{diff_2006:.1f} pp above EZ\n(2.4% vs 1.1%)"
# Place the callout text in axes fraction coords to avoid overlap, with a subtle connector
ax.annotate(call_2006_text,
            xy=(i2006, sp2006), xycoords='data',
            xytext=(0.66, 0.78), textcoords='axes fraction',
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc=callout_box_face, ec=callout_edge, lw=0.7),
            arrowprops=dict(arrowstyle='-', color="#7F7F7F", lw=0.8, shrinkA=0, shrinkB=0),
            zorder=8)

# Add small colored dot inside the callout to link to Spain color (placed in axes fraction)
ax.scatter([0.635], [0.78], transform=ax.transAxes, s=30, c=[color_spain], edgecolors=[edge_spain], linewidths=0.8, zorder=9)

# 2009: "Spain −4.9 pp worse than EZ" (Spain -11.2 vs EZ -6.3)
diff_2009 = sp2009 - ez_vals[i2009]
call_2009_text = f"Spain {diff_2009:.1f} pp worse than EZ\n(-11.2% vs -6.3%)"
ax.annotate(call_2009_text,
            xy=(i2009, sp2009), xycoords='data',
            xytext=(0.28, 0.22), textcoords='axes fraction',
            fontsize=9, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc=callout_box_face, ec=callout_edge, lw=0.7),
            arrowprops=dict(arrowstyle='-', color="#7F7F7F", lw=0.8, shrinkA=0, shrinkB=0),
            zorder=8)
ax.scatter([0.31], [0.22], transform=ax.transAxes, s=30, c=[color_spain], edgecolors=[edge_spain], linewidths=0.8, zorder=9)

# Minor styling tweaks
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color(grid_color)
ax.spines['bottom'].set_color(grid_color)
ax.tick_params(axis='x', which='both', length=4)
ax.tick_params(axis='y', which='both', length=4)

# Executive summary caption below the chart (2-3 sentences)
caption = (f"Across 1999–2014 average budget balances are similar (Spain ≈ {avg_spain:.2f}% GDP; "
           f"Euro‑Zone ≈ {avg_ez:.2f}% GDP). Spain shows marked outperformance 2004–2007 "
           f"(peaking at +2.4% in 2006) and far larger shortfalls in 2008–2010 (largest gap in 2009: "
           f"Spain −11.2% vs EZ −6.3%, difference ≈ −4.9 percentage points).")
fig.text(0.5, 0.08, caption, ha='center', va='center', fontsize=9)

# Small footer note about shaded area
fig.text(0.5, 0.045, "Shaded area = period of global financial crisis and major fiscal adjustments.", 
         ha='center', va='center', fontsize=8, color="#4D4D4D")

# Footer small data source / method note
fig.text(0.01, 0.02, "Data: budget balance (% of GDP). Method: percentage points (pp) difference = Spain − Euro‑Zone Average.",
         ha='left', va='center', fontsize=7, color="#6E6E6E")

plt.savefig("generated/spain_factor4_bar1_design.png", dpi=300, bbox_inches="tight")