# Ensure required packages are installed (if running in an environment where pip is available)
import sys
import subprocess

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
    from matplotlib import ticker
    import numpy as np
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
    from matplotlib import ticker
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

years = np.array([d["year"] for d in data])
spain = np.array([d["spain"] for d in data])
ez = np.array([d["euro_zone_average"] for d in data])

# Colors (government-friendly, colorblind-safe contrast)
color_spain = "#D9534F"   # warm saturated reddish-orange
color_ez = "#2E76B6"      # desaturated blue

# Plot setup
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 16,
    "axes.titleweight": "bold"
})

fig, ax = plt.subplots(figsize=(11, 6.2), dpi=120)
fig.patch.set_facecolor("white")

# Shaded bands: positive and negative
ymin = -12.5
ymax = 3
ax.set_ylim(ymin, ymax)
ax.set_xlim(years.min() - 0.5, years.max() + 0.5)

# Create boolean mask arrays matching the x-length for fill_between 'where' parameter
full_mask = np.ones_like(years, dtype=bool)

# Shade positive area across the full x range
ax.fill_between(years, 0, ymax, where=full_mask, facecolor="#eaf6ef", alpha=0.6, interpolate=True)  # light greenish
# Shade negative area across the full x range
ax.fill_between(years, ymin, 0, where=full_mask, facecolor="#f4f7fb", alpha=1.0, interpolate=True)  # very light cool grey-blue

# Plot lines
ln_spain, = ax.plot(years, spain, color=color_spain, linewidth=2.5, solid_capstyle='round', label="Spain", zorder=3)
ln_ez, = ax.plot(years, ez, color=color_ez, linewidth=2.0, linestyle='--', solid_capstyle='round', label="Euro-Zone avg.", zorder=2)

# Emphasize zero baseline
ax.axhline(0, color="#666666", linewidth=1.6, zorder=1)

# Horizontal gridlines at every 2 percentage points
yticks = np.arange(-12, 4, 2)
ax.set_yticks(yticks)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d%%'))
ax.grid(axis='y', color='#e6e6e6', linewidth=0.8, zorder=0)
# Make the gridlines lighter except zero which is emphasized above
for yline in ax.get_ygridlines():
    yline.set_linestyle('-')
    yline.set_alpha(0.6)

# X-axis ticks every 1 or 2 years; label every 1 for clarity but not heavy
ax.set_xticks(years)
ax.set_xticklabels([str(int(y)) for y in years], rotation=0)
for label in ax.xaxis.get_ticklabels()[::2]:
    label.set_visible(True)

# Highlighted circles (hollow) on key years
highlight_years = [2004, 2006, 2007, 2009, 2014]
hx = [np.where(years == y)[0][0] for y in highlight_years]
ax.scatter([years[i] for i in hx], spain[[np.where(years == y)[0][0] for y in highlight_years]],
           facecolors='none', edgecolors=color_spain, s=80, linewidths=1.6, zorder=4)
ax.scatter([years[i] for i in hx], ez[[np.where(years == y)[0][0] for y in highlight_years]],
           facecolors='none', edgecolors=color_ez, s=80, linewidths=1.6, zorder=3)

# Numeric labels for selected points (2006 peak, 2009 crisis, 2014)
def label_point(year, series, text, xytext):
    xi = years.tolist().index(year)
    yi = series[xi]
    bbox = dict(boxstyle="round,pad=0.3", fc=(color_spain if series is spain else color_ez), ec=(color_spain if series is spain else color_ez), alpha=0.12)
    ax.annotate(text, xy=(year, yi), xytext=xytext, textcoords='data',
                fontsize=10, ha='center', va='center',
                bbox=bbox, color=(color_spain if series is spain else color_ez),
                arrowprops=dict(arrowstyle="-", lw=0.9, color=(color_spain if series is spain else color_ez),
                                connectionstyle="arc3,rad=0.2"), zorder=6)

# 2006 Spain peak
label_point(2006, spain, "Spain +2.4% — peak surplus", (2006, 3.0))
# 2007 Spain > EZ
label_point(2007, spain, "Spain still > Euro avg", (2007, 2.6))
# 2004 Spain surplus vs EZ
label_point(2004, spain, "2004: Spain 0.6% vs EZ −2.9%", (2004, 1.8))
# 2014 comparison
label_point(2014, spain, "By 2014 gaps narrowed", (2014, 0.6))

# Detailed comparison bracket and label for 2009
year_cmp = 2009
ix = years.tolist().index(year_cmp)
y_spain_2009 = spain[ix]
y_ez_2009 = ez[ix]
diff = y_spain_2009 - y_ez_2009
# vertical bracket between the two series at 2009
bracket_x = year_cmp
ax.annotate("", xy=(bracket_x + 0.03, y_spain_2009), xytext=(bracket_x + 0.03, y_ez_2009),
            arrowprops=dict(arrowstyle='|-|', lw=1.0, color='#7f7f7f', shrinkA=0, shrinkB=0), zorder=5)
# label for the difference near the bracket
label_text = f"2009: Spain {y_spain_2009:+.1f}% vs EZ {y_ez_2009:+.1f}% = {diff:+.1f} pp"
ax.text(bracket_x + 0.35, (y_spain_2009 + y_ez_2009) / 2, label_text, fontsize=10, color='#4a4a4a',
        va='center', bbox=dict(boxstyle="round,pad=0.25", fc='white', ec='#dddddd', alpha=0.9), zorder=6)

# Summary callouts (left and right)
callout_bbox = dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#cccccc", alpha=0.95)
ax.text(1999.2, 2.7, "Spain swung from surplus (2004–07)\nto a deeper crisis deficit in 2009",
        fontsize=12, va='top', ha='left', bbox=callout_bbox, zorder=7)
ax.text(2011.8, -11.9, "By 2014 both remained in deficit\nbut gaps smaller.",
        fontsize=12, va='bottom', ha='right', bbox=callout_bbox, zorder=7)

# Legend (compact) top-right with small pictorial icons drawn nearby
legend_handles = [
    Line2D([0], [0], color=color_spain, lw=2.5),
    Line2D([0], [0], color=color_ez, lw=2.0, linestyle='--')
]
leg = ax.legend(legend_handles, ["Spain", "Euro‑Zone avg."], loc='upper right', frameon=False, fontsize=10)
# Add small illustrative icons near legend (simulated flag and euro circle)
# Position icons relative to axes coordinates near legend
trans = ax.transAxes
# Spain small flag: three vertical stripes (simulated simple flag)
flag_width = 0.025
flag_height = 0.05
flag_x = 0.84
flag_y = 0.92
ax.add_patch(Rectangle((flag_x, flag_y), flag_width, flag_height, transform=trans,
                       facecolor="#D9534F", edgecolor="#B33A2F", linewidth=0.6, zorder=10))
ax.add_patch(Rectangle((flag_x + flag_width / 3, flag_y), flag_width / 3, flag_height, transform=trans,
                       facecolor="#F0C419", edgecolor="#C39A16", linewidth=0.0, zorder=11))
# Euro icon: blue circle with € symbol using text
circle_center_x = 0.84
circle_center_y = 0.835
circle_radius = 0.025
ax.add_patch(Circle((circle_center_x, circle_center_y), circle_radius, transform=trans, facecolor=color_ez, edgecolor='#1f587f', linewidth=0.6, zorder=10))
ax.text(circle_center_x, circle_center_y - 0.008, "€", transform=trans, fontsize=9, ha='center', va='center', color='white', zorder=11)

# Title and very short subtitle
ax.set_title("Spain vs Euro‑Zone: Budget Balance, 1999–2014", pad=12)
ax.text(0.02, 0.98, "% of GDP", transform=ax.transAxes, fontsize=10, va='top', ha='left', color='#333333')

# Axis labels
ax.set_ylabel("Budget balance (% of GDP)")
ax.set_xlabel("Year")

# Source metadata (bottom-left) and simulated government logo bottom-right
source_text = "Source: Ministry of Finance, consolidated budget figures (1999–2014)."
fig.text(0.02, 0.02, source_text, ha='left', va='bottom', fontsize=9, color='#444444')

# Simulated government logo as a small rectangle with text (bottom-right)
logo_w = 0.10
logo_h = 0.06
logo_x = 0.88
logo_y = 0.02
# white rectangle with border
fig.patches.extend([Rectangle((logo_x, logo_y), logo_w, logo_h, transform=fig.transFigure,
                              facecolor="#f7f7f7", edgecolor="#cfcfcf", linewidth=0.8, zorder=20)])
fig.text(logo_x + 0.015, logo_y + 0.025, "MINISTRY\nOF FINANCE", transform=fig.transFigure,
         fontsize=8, ha='left', va='center', color='#2b2b2b', zorder=21)

# Tidy layout with breathing room for annotations and logo
plt.subplots_adjust(left=0.07, right=0.95, top=0.88, bottom=0.12)

# Make spines lighter
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color("#dcdcdc")

# Final rendering
plt.savefig("generated/spain_factor3_1_design.png", dpi=300, bbox_inches="tight")