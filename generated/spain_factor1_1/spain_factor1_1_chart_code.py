import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FuncFormatter
import textwrap

# Data (converted from the provided dataset)
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

years = np.array([d["year"] for d in data])
spain = np.array([d["spain"] for d in data])
ez = np.array([d["euro_zone_average"] for d in data])

# Styling variables
spain_color = "#1565C0"     # deep saturated blue
ez_color = "#9E9E9E"        # muted gray
blue_fill = spain_color
red_fill = "#ef9a9a"        # pale red/pink
grid_color = "#eaeaea"
baseline_color = "#424242"  # stronger baseline at y=0
title_fontsize = 20
subtitle_fontsize = 13
legend_fontsize = 10
caption_fontsize = 9
footnote_fontsize = 8

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
fig.subplots_adjust(top=0.78, bottom=0.16, left=0.09, right=0.96)

# Plot the lines
ax.plot(years, spain, color=spain_color, linewidth=2.5, label="Spain", zorder=3)
ax.plot(years, ez, color=ez_color, linewidth=1.5, label="Euro-Zone average", zorder=2)

# Difference band: Spain > EZ -> pale blue; Spain < EZ -> pale red
# Use where parameter to only fill segments where condition holds
ax.fill_between(years, spain, ez, where=(spain >= ez),
                interpolate=True, color=blue_fill, alpha=0.12, linewidth=0, zorder=1)
ax.fill_between(years, spain, ez, where=(spain < ez),
                interpolate=True, color=red_fill, alpha=0.12, linewidth=0, zorder=1)

# Highlighted period band 2008-2010 (very subtle)
ax.axvspan(2008 - 0.5, 2010 + 0.5, color='gray', alpha=0.06, zorder=0)

# Emphasize 0 baseline and add light horizontal gridlines at 2.5% increments
ax.yaxis.set_major_locator(MultipleLocator(2.5))
ax.grid(axis='y', color=grid_color, linewidth=0.8, zorder=0)
ax.axhline(0, color=baseline_color, linewidth=1.2, zorder=4)

# Axis formatting
ax.set_xlim(years.min() - 0.5, years.max() + 0.5)
ymin = np.floor(min(spain.min(), ez.min()) / 2.5) * 2.5 - 0.0
ymax = np.ceil(max(spain.max(), ez.max()) / 2.5) * 2.5 + 0.0
ax.set_ylim(ymin, ymax)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=10)

# Y-axis formatter to show percent sign
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:.1f}%".rstrip('0').rstrip('.') + "%"))

# Remove top and right spines for a cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Mark and annotate the 2009 Spain point with a small inline label (no arrow)
year_2009_idx = np.where(years == 2009)[0][0]
x2009 = years[year_2009_idx]
y2009 = spain[year_2009_idx]
ax.scatter([x2009], [y2009], color=spain_color, s=40, zorder=5)
label_text = "Spain −11.2% (2009)"
# Place label slightly above the point, with a subtle white bbox for legibility
ax.text(x2009 + 0.25, y2009 + 1.0, label_text,
        fontsize=9, color=spain_color, verticalalignment='center',
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.6),
        zorder=6)

# Legend (top-right inside the plot area, compact)
legend = ax.legend(loc='upper right', frameon=False, fontsize=legend_fontsize)
for text in legend.get_texts():
    text.set_family('sans-serif')

# Title (top-left) and subtitle directly under it (placed in figure coordinates)
fig.text(0.01, 0.95, "Government budget balance: Spain vs Euro‑Zone average (1999–2014)",
         ha='left', va='top', fontsize=title_fontsize, weight='bold', family='sans-serif')
fig.text(0.01, 0.915,
         "Budget surplus (+) / deficit (–) as % of GDP — divergence before and after the 2008 financial crisis, with Spain’s large swing in 2008–2010 highlighted",
         ha='left', va='top', fontsize=subtitle_fontsize, family='sans-serif')

# Caption / metadata block (full-width, directly beneath the chart; multi-line)
caption = (
    "Lines show government budget balance (percent of GDP) for Spain and the Euro‑Zone average, 1999–2014. "
    "Positive values indicate surplus; negative indicate deficit. Variables: ‘Spain’ = national general government balance; "
    "‘Euro‑Zone average’ = aggregated average. Data: provided dataset (annual values). Source: [insert official source such as Eurostat/IMF]. "
    "Notable: Spain ran surpluses 2004–2007 and a deep deficit in 2009 (−11.2% of GDP)."
)
# Wrap caption to a readable width
wrapped_caption = textwrap.fill(caption, 120)
fig.text(0.01, 0.06, wrapped_caption, ha='left', va='top', fontsize=caption_fontsize, family='sans-serif')

# Small footnote line beneath caption
footnote = "Unit: % of GDP. Chart prepared for comparative analysis; verify official source before publication. 2008–2010: financial crisis period."
fig.text(0.01, 0.03, footnote, ha='left', va='top', fontsize=footnote_fontsize, family='sans-serif', color="#444444")

# Tight layout adjustments and show
plt.savefig("generated/spain_factor1_1_design.png", dpi=300, bbox_inches="tight")