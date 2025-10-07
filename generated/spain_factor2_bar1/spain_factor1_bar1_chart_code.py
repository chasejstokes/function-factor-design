import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Data from the design plan
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
    {"year": 2014, "spain": -2.5, "euro_zone_average": -2.0},
]

years = [d["year"] for d in data]
spain_vals = np.array([d["spain"] for d in data])
euro_vals = np.array([d["euro_zone_average"] for d in data])

# Colors per design: Spain = saturated deep red/orange, Euro-zone = muted steel blue / cool gray
color_spain = "#C7411A"      # deep orange-red
color_euro = "#567A92"       # muted steel blue

# Figure and axes
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "axes.facecolor": "white"
})

fig, ax = plt.subplots(figsize=(12, 6.5))
left = np.arange(len(years))
width = 0.36  # width of each bar in a pair

# Plot grouped bars
bars_spain = ax.bar(left - width/2, spain_vals, width=width, label="Spain",
                    color=color_spain, edgecolor="#444444", linewidth=0.2, zorder=2)
bars_euro = ax.bar(left + width/2, euro_vals, width=width, label="Euro‑zone average",
                   color=color_euro, edgecolor="#444444", linewidth=0.2, zorder=2)

# Emphasize zero baseline
ax.axhline(0, color="#222222", linewidth=1.2, zorder=3)

# Y-axis ticks and grid (major ticks as requested)
y_ticks = [-12, -10, -5, 0, 5]
ax.set_yticks(y_ticks)
ax.set_ylabel("% of GDP", fontsize=10)
ax.grid(axis='y', which='major', color='#dcdcdc', linewidth=0.8, zorder=0)
# Minor gridlines off to keep it clean

# X-axis ticks: show each year
ax.set_xticks(left)
ax.set_xticklabels(years, rotation=0)
ax.set_xlim(left[0] - 1, left[-1] + 1)

# Set y-limits to give breathing room
ax.set_ylim(-13, 3)

# Subtle vertical band for crisis period 2008-2010
# Compute indices for 2008 and 2010
idx_2008 = years.index(2008)
idx_2010 = years.index(2010)
band_left = idx_2008 - 0.5
band_right = idx_2010 + 0.5
ax.axvspan(band_left, band_right, color="grey", alpha=0.12, zorder=1)

# Label for the crisis band just above the x-axis (unobtrusive)
y_min, y_max = ax.get_ylim()
band_label_y = max(y_min + 0.8, -2.0)  # place close to x-axis but above bottom
ax.text((band_left + band_right) / 2, band_label_y, "Global financial crisis (2008–2010)",
        ha="center", va="bottom", fontsize=9, color="#444444", alpha=0.9)

# Minimal numeric labels for Spain's most extreme years: maximum negative (2009) and largest positive (2006)
# Find indices
idx_min_spain = int(np.argmin(spain_vals))  # most negative
idx_max_spain = int(np.argmax(spain_vals))  # most positive

def add_value_label(bar_x_idx, value):
    # Place label slightly toward zero from the bar end for readability
    if value < 0:
        y_pos = value + 0.6  # slightly toward zero
        va = "bottom"
    else:
        y_pos = value + 0.3
        va = "bottom"
    ax.text(bar_x_idx, y_pos, f"{value:+.1f}%", ha="center", va=va,
            fontsize=9, color="#222222", backgroundcolor="white", bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.7))

# Add labels above the Spain bar centers for those years
add_value_label(left[idx_min_spain] - width/2, spain_vals[idx_min_spain])
add_value_label(left[idx_max_spain] - width/2, spain_vals[idx_max_spain])

# Legend top-right inside plot area, compact
legend = ax.legend(loc="upper right", bbox_to_anchor=(0.98, 0.98), frameon=False, fontsize=9)

# Title (top-left) and subtitle (directly under title)
# Use figure text to place title top-left outside axes area for alignment per design
fig.text(0.01, 0.95, "Budget balance: Spain vs Euro‑zone average (1999–2014)",
         fontsize=14, fontweight="bold", ha="left", va="top")
fig.text(0.01, 0.925, "General government balance (% of GDP). Positive = surplus, negative = deficit — annual values.",
         fontsize=10.5, ha="left", va="top", color="#222222")

# Caption / metadata block (two paragraphs) full-width below the chart
caption_takeaway = ("Key takeaway: Spain’s deficit deepened sharply during the 2008–2010 crisis, peaking at −11.2% of GDP in 2009; "
                    "the euro‑zone average was less extreme.")
caption_meta = ("Data: general government fiscal balance (% of GDP), annual values, 1999–2014. Source: IMF - Government Finance Statistics / OECD consolidated fiscal data (aggregated euro‑zone average). "
                "Positive = surplus. Chart by Data Visualization Unit. Last updated: " + datetime.now().strftime("%Y-%m-%d") + ".")

# Place captions
fig.text(0.01, 0.04, caption_takeaway, fontsize=9.5, ha="left", va="bottom")
fig.text(0.01, 0.01, caption_meta, fontsize=8, ha="left", va="bottom", color="#555555")

# Footer right: small author/date
fig.text(0.99, 0.01, "Chart: Data Visualization Unit", fontsize=8, ha="right", va="bottom", color="#555555")

# Tight layout adjustments to make space for title/subtitle and caption
plt.subplots_adjust(left=0.06, right=0.99, top=0.88, bottom=0.12)

# Keep plot flat and professional: remove top and right spines subtly
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Show the plot
plt.savefig("generated/spain_factor1_bar1_design.png", dpi=300, bbox_inches="tight")