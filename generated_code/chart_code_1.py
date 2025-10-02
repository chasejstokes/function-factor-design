# Check/install required packages
import importlib, subprocess, sys
packages = ['matplotlib', 'numpy', 'pandas']
for pkg in packages:
    if importlib.util.find_spec(pkg) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

# Plotting code
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data
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
df = pd.DataFrame(data)

# Series and styling choices from design plan
years = df['year'].to_numpy()
spain = df['spain'].to_numpy()
ez = df['euro_zone_average'].to_numpy()

spain_color = "#D9534F"        # deep warm red / orange for Spain
ez_color = "#6C88A0"           # muted cool gray-blue for Euro-Zone
pos_fill_color = "#C7E9C0"     # subtle green tint (low opacity)
neg_fill_color = "#F4C7C3"     # subtle red tint (low opacity)

# Figure and axes
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(11, 6))

# Plot lines
ax.plot(years, ez, linestyle=(0, (5, 5)), linewidth=1.6, color=ez_color, zorder=2)  # thinner dashed-like for EZ
ax.plot(years, spain, linestyle='solid', linewidth=2.6, color=spain_color, zorder=3)  # strong Spain line

# Fill between lines: green where Spain > EZ, red where Spain < EZ
above_mask = spain > ez
# Use piecewise fill_between to avoid crossing artifacts
ax.fill_between(years, spain, ez, where=above_mask, interpolate=True, color=pos_fill_color, alpha=0.6, zorder=1)
ax.fill_between(years, spain, ez, where=~above_mask, interpolate=True, color=neg_fill_color, alpha=0.6, zorder=1)

# Emphasize zero baseline
ax.axhline(0, color='#333333', linewidth=1.2, zorder=0)

# Selective markers at annotated years
annot_years = [2004, 2007, 2009, 2014]
annot_x = np.array(annot_years)
annot_idx = [int(np.where(years == y)[0]) for y in annot_years]
ax.scatter(annot_x, spain[annot_idx], color=spain_color, s=40, zorder=4)
ax.scatter(annot_x, ez[annot_idx], color=ez_color, s=30, zorder=4)

# Title (prominent but concise)
ax.set_title("Spain vs Euro‑Zone: Budget Deficit/Surplus (1999–2014)", fontsize=16, weight='semibold', pad=14)

# Axis labels and ticks
ax.set_ylabel("% of GDP", fontsize=11)
ax.set_xlim(years.min() - 0.4, years.max() + 1.2)
ax.set_ylim(min(min(spain), min(ez)) - 1.5, max(max(spain), max(ez)) + 1.5)

# X ticks every 2 years
xticks = list(range(1999, 2015, 2))
ax.set_xticks(xticks)
ax.set_xticklabels([str(x) for x in xticks], fontsize=10)

# Horizontal gridlines only (light)
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.6)
ax.xaxis.grid(False)

# Direct end-line labels (no legend)
# Slight offset to the right of the last data point
x_end = years.max()
x_offset = 0.6
ax.text(x_end + x_offset, spain[-1], "Spain: -2.5% (2014)", color=spain_color, fontsize=10, va='center', fontweight='semibold')
ax.text(x_end + x_offset, ez[-1], "Euro‑Zone avg: -2.0% (2014)", color=ez_color, fontsize=9, va='center')

# Numeric difference labels at selected years: 2004, 2007, 2009, 2014
# 2004 and 2009 get the specified callouts (with arrows)
# 2007 and 2014 get small inline difference labels
# 2004 callout
y2004_spain = float(df.loc[df['year'] == 2004, 'spain'])
y2004_ez = float(df.loc[df['year'] == 2004, 'euro_zone_average'])
ax.annotate("Spain surplus vs Euro deficit — gap ~+3.5 pp",
            xy=(2004, y2004_spain), xycoords='data',
            xytext=(2002.4, y2004_spain + 3.2),
            fontsize=9, color='black',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=spain_color, lw=0.8),
            arrowprops=dict(arrowstyle="->", color=spain_color, lw=0.9),
            zorder=6)

# 2009 callout (prominent)
y2009_spain = float(df.loc[df['year'] == 2009, 'spain'])
y2009_ez = float(df.loc[df['year'] == 2009, 'euro_zone_average'])
ax.annotate("Peak divergence — Spain -11.2% vs EZ -6.3% (gap -4.9 pp)",
            xy=(2009, y2009_spain), xycoords='data',
            xytext=(2005.8, y2009_spain - 6.6),
            fontsize=9.2, color='black',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=spain_color, lw=1.0),
            arrowprops=dict(arrowstyle="->", color=spain_color, lw=1.0),
            zorder=6)

# 2007 small numeric diff label
y2007_spain = float(df.loc[df['year'] == 2007, 'spain'])
y2007_ez = float(df.loc[df['year'] == 2007, 'euro_zone_average'])
diff2007 = y2007_spain - y2007_ez
ax.text(2007 + 0.1, y2007_spain + 0.6, f"{diff2007:+.1f} pp", fontsize=9, color=spain_color, weight='semibold')

# 2014 small numeric diff label near the end labels
diff2014 = float(df.loc[df['year'] == 2014, 'spain'] - df.loc[df['year'] == 2014, 'euro_zone_average'])
ax.text(x_end + x_offset, (spain[-1] + ez[-1]) / 2, f"Gap {diff2014:+.1f} pp", fontsize=9, color='gray', va='center')

# Directionality cue: subtle arrow highlighting steep drop from 2007 to 2009 for Spain
x_from, x_to = 2007, 2009
y_from = float(df.loc[df['year'] == x_from, 'spain'])
y_to = float(df.loc[df['year'] == x_to, 'spain'])
ax.annotate("", xy=(x_to, y_to + 0.4), xytext=(x_from, y_from + 0.7),
            arrowprops=dict(arrowstyle="->", color="#777777", lw=1.0), zorder=5)
ax.text(2007.6, (y_from + y_to) / 2 + 1.2, "Steep drop (2007→2009)", color="#555555", fontsize=8.5)

# Annotations are minimal and anchored to data points; reduce clutter
# Footnote / data source: very small
ax.text(0.01, -0.12, "Source: [dataset], % of GDP", transform=ax.transAxes, fontsize=8, color='gray')

# Tidy layout
plt.tight_layout()
plt.savefig("generated_images/design_1.png", dpi=300, bbox_inches="tight")
plt.show()