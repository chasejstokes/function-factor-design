import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

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
euro_vals = np.array([d["euro_zone_average"] for d in data])

# Figure configuration (portrait 3:4)
# Use inches so that saving is exact: 9 x 12 inches
fig_width, fig_height = 9, 12
fig = plt.figure(figsize=(fig_width, fig_height), constrained_layout=False)
ax = fig.add_axes([0.08, 0.22, 0.90, 0.66])  # leave room at top for title/subtitle and bottom for caption

# Typography and colors
plt.rcParams['font.family'] = 'DejaVu Sans'
title_fontsize = 30
subtitle_fontsize = 18
legend_fontsize = 14
axis_label_fontsize = 17
tick_label_fontsize = 14
caption_fontsize = 15
metadata_fontsize = 12

color_spain = "#0b4f6c"        # deep teal/navy-like saturated color
color_euro = "#7f9fb3"         # muted gray-blue
grid_color = "#e6e6e6"
zero_line_color = "#4a4a4a"
muted_text = "#6d6d6d"

# X positions and bar widths
x = np.arange(len(years))
pair_gap = 0.02
bar_width = 0.36
offset = bar_width / 2.0 + pair_gap / 2.0

# Optional subtle shaded crisis band 2008-2013
# Determine span in x coordinates (center positions)
year_to_x = {year: xi for year, xi in zip(years, x)}
start_year, end_year = 2008, 2013
if start_year in year_to_x and end_year in year_to_x:
    span_left = year_to_x[start_year] - (bar_width + pair_gap)
    span_right = year_to_x[end_year] + (bar_width + pair_gap)
    ax.axvspan(span_left - 0.5*bar_width, span_right + 0.5*bar_width,
               color="#cfcfcf", alpha=0.06, zorder=0)

# Identify years where |Spain - Euro| >= 3 for subtle emphasis
diffs = np.abs(spain_vals - euro_vals)
highlight_years = diffs >= 3.0
highlight_indices = np.where(highlight_years)[0]

# Draw background "halo" for highlighted Spain bars (slightly wider, low opacity)
for idx in highlight_indices:
    xi = x[idx] - offset
    ax.bar(xi, spain_vals[idx],
           width=bar_width + 0.06,
           color=color_spain,
           alpha=0.12,
           linewidth=0,
           zorder=1,
           align='center')

# Plot Spain bars (slightly thicker edge)
spain_bars = ax.bar(x - offset, spain_vals, width=bar_width,
                    color=color_spain, edgecolor="#05323d", linewidth=0.8, zorder=3, label="Spain")

# Plot Euro-zone bars
euro_bars = ax.bar(x + offset, euro_vals, width=bar_width,
                   color=color_euro, edgecolor="none", zorder=2, label="Euro‑Zone average")

# Zero baseline emphasized
ax.axhline(0, color=zero_line_color, linewidth=1.6, zorder=4)
# Light horizontal gridlines
ax.yaxis.grid(True, which='major', color=grid_color, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Axis labels and ticks
ax.set_ylabel("Budget balance (% of GDP)", fontsize=axis_label_fontsize, labelpad=12)
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=tick_label_fontsize)
ax.tick_params(axis='y', labelsize=tick_label_fontsize)
# Set y limits with some margin
y_min = min(spain_vals.min(), euro_vals.min())
y_max = max(spain_vals.max(), euro_vals.max())
y_margin = max(1.5, (y_max - y_min) * 0.08)
ax.set_ylim(y_min - y_margin, y_max + y_margin)

# Major yticks every 2 or 5 points depending on range
yrange = y_max - y_min
if yrange <= 12:
    yticks = np.arange(int(np.floor(y_min/2)*2), int(np.ceil(y_max/2)*2)+1, 2)
else:
    yticks = np.arange(int(np.floor(y_min/5)*5), int(np.ceil(y_max/5)*5)+1, 5)
ax.set_yticks(yticks)

# Label the zero baseline explicitly (placed at left of plot)
ax.text(-0.02, 0, "0 = balance", va='center', ha='right',
        transform=ax.get_yaxis_transform(), fontsize=12, color=muted_text)

# Data labels for critical Spain outliers: 2009 (-11.2) and 2006 (2.4) as specified
critical_years = [2009, 2006]
for cy in critical_years:
    if cy in year_to_x:
        idx = year_to_x[cy]
        val = spain_vals[idx]
        xi = x[idx] - offset
        # Place label slightly above positive bars, slightly below negative bars
        if val >= 0:
            ytext = val + 0.6
            va = 'bottom'
        else:
            ytext = val - 0.6
            va = 'top'
        ax.text(xi, ytext, f"{val:.1f}", fontsize=13, fontweight='bold',
                color='black', ha='center', va=va, zorder=5)

# Compact legend top-right inside plotting area
legend_patches = [
    mpatches.Patch(color=color_spain, label="Spain"),
    mpatches.Patch(color=color_euro, label="Euro‑Zone average")
]
leg = ax.legend(handles=legend_patches, loc='upper right', fontsize=legend_fontsize,
                frameon=False, bbox_to_anchor=(0.98, 0.98), borderaxespad=0.)
# Make Spain entry slightly emphasized in legend by bold text
for text, patch in zip(leg.get_texts(), legend_patches):
    if patch.get_label() == "Spain":
        text.set_fontweight('bold')

# Title and subtitle (centered above axes)
fig.suptitle("Spain vs Euro‑Zone: Budget Balance (% of GDP), 1999–2014",
             fontsize=title_fontsize, fontweight='bold', y=0.955)
fig.text(0.5, 0.91,
         "Paired bars show each year’s general‑government budget balance as a percent of GDP. "
         "Positive = surplus; negative = deficit. Emphasis below on years where Spain diverges from the euro‑zone average.",
         ha='center', va='top', fontsize=subtitle_fontsize, wrap=True, color='#222222')

# Caption block under the plot
caption = ("Spain ran larger deficits than the euro‑zone average after 2008, peaking at −11.2% in 2009; "
           "Spain also posted surpluses in 2004–2006, while the euro zone remained more often in deficit. "
           "Spain’s deeper post‑2008 downturn led to significantly larger deficits than the euro‑zone average.")
fig.text(0.08, 0.12, caption, ha='left', va='top', fontsize=caption_fontsize, wrap=True, color='#111111')

# Metadata/provenance line (muted)
metadata = ("Source: Eurostat (general government net lending/borrowing, % of GDP). "
            "Years: 1999–2014. Chart: paired bars by year; years with notable divergence highlighted.")
fig.text(0.08, 0.085, metadata, ha='left', va='top', fontsize=metadata_fontsize, color=muted_text)

# Improve layout and ensure caption fits
plt.subplots_adjust(top=0.89, bottom=0.08, left=0.08, right=0.96)

# Export high-resolution PNG and an extra larger slide-optimized export
# Primary export (900x1200 px at 100 dpi -> 9x12 inches)
fig.savefig("spain_vs_eurozone_budget_900x1200.png", dpi=100, facecolor='white')
# Slide-optimized export (double resolution)
fig.savefig("spain_vs_eurozone_budget_slide@2x.png", dpi=200, facecolor='white')

# Also show the plot in interactive environments
plt.savefig("generated/spain_factor1_bar7/spain_factor1_bar7_design.png", dpi=300, bbox_inches="tight")