import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.text import Annotation
from matplotlib import patheffects
import numpy as np

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors and styles
color_spain = "#C62828"   # warm saturated red
color_euro = "#1976D2"    # cool steel blue
bg_color = "#f5f6f7"      # neutral light gray for plot area
grid_color = "#dcdfe3"

# Figure setup
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
})
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("white")
ax.set_facecolor(bg_color)

# Plot lines (straight-line timeline) with markers at each year
ax.plot(years, spain, color=color_spain, linewidth=3.0, marker='o', markersize=4, markerfacecolor=color_spain, markeredgecolor='white', zorder=3, label='Spain')
ax.plot(years, euro, color=color_euro, linewidth=2.0, marker='o', markersize=4, markerfacecolor=color_euro, markeredgecolor='white', zorder=3, label='Euro‑Zone average')

# Grid and ticks
ax.set_xlim(1998.6, 2014.4)
ax.set_ylim(-12.2, 3.2)
ax.set_yticks([-12, -8, -4, 0, 2])
ax.set_yticklabels(["-12%", "-8%", "-4%", "0%", "2%"])
ax.set_xticks(np.arange(1999, 2015, 2))  # every other year
ax.set_xticks(np.arange(1999, 2015, 1), minor=True)  # minor ticks for intermediate years
ax.tick_params(axis='x', which='major', length=6)
ax.tick_params(axis='x', which='minor', length=3)
ax.grid(which='major', axis='y', linestyle='--', color=grid_color, linewidth=0.8)
ax.grid(which='minor', axis='x', linestyle=':', color=grid_color, linewidth=0.5)

# Emphasize zero baseline
ax.axhline(0, color="#9aa0a6", linewidth=1.8, zorder=2)
# Add label for zero baseline near left
ax.text(1999.0, 0.25, "0 = balanced budget", color="#6d6f71", fontsize=9, va='bottom', ha='left')

# Title and subtitle
ax.set_title("Spain vs Euro‑Zone: Budget balance (% of GDP), 1999–2014", fontsize=17, fontweight='bold', pad=12)
plt.suptitle("", y=0.98)
ax.text(0.5, 1.01, "Annual general government balance; negative = deficit, positive = surplus",
        transform=ax.transAxes, ha='center', va='bottom', fontsize=11)

# Compact legend top-left inside plot
legend_lines = [
    mlines.Line2D([], [], color=color_spain, linewidth=3, label='Spain'),
    mlines.Line2D([], [], color=color_euro, linewidth=2, label='Euro‑Zone average')
]
leg = ax.legend(handles=legend_lines, loc='upper left', frameon=True, facecolor='white', fontsize=10)
leg.get_frame().set_edgecolor("#d6d6d6")
leg.get_frame().set_linewidth(0.6)

# Compute averages for summary
avg_spain = spain.mean()
avg_euro = euro.mean()

# Annotations: 2009 callout (Spain -11.2% vs EZ -6.3%)
x2009 = 2009
y2009 = spain[years.tolist().index(2009)]
circle_2009 = Circle((x2009, y2009), 0.22, transform=ax.transData,
                     edgecolor=color_spain, facecolor=(1,1,1,0.10), lw=1.5, zorder=4)
ax.add_patch(circle_2009)

# Leader line from circle to annotation
ax.annotate("", xy=(2009+0.1, y2009-1.0), xytext=(2009+1.6, y2009-4.4),
            arrowprops=dict(arrowstyle='-', color="#7b7b7b", linewidth=0.9,
                            connectionstyle="arc3,rad=-0.25"), zorder=4)

# Annotation box for 2009
ann2009_text = "2009 — Spain: −11.2% | EZ: −6.3% → Spain −4.9 pp worse"
bbox_props = dict(boxstyle="round,pad=0.35", fc="white", ec="#bfbfbf", lw=0.8, alpha=0.98)
txt2009 = ax.text(2009+1.65, y2009-4.55, ann2009_text, fontsize=9.5, va='center', ha='left', bbox=bbox_props, zorder=5)
# small red downward chevron icon inside box (unicode triangle)
ax.text(2009+1.2, y2009-3.95, "▼", fontsize=13, color="#C62828", weight='bold', zorder=6)

# 2006 callout (Spain +2.4% vs EZ +1.1%)
x2006 = 2006
y2006 = spain[years.tolist().index(2006)]
circle_2006 = Circle((x2006, y2006), 0.22, transform=ax.transData,
                     edgecolor=color_spain, facecolor=(1,1,1,0.10), lw=1.5, zorder=4)
ax.add_patch(circle_2006)

# Leader line to annotation
ax.annotate("", xy=(2006-0.12, y2006+0.35), xytext=(2006-2.0, y2006+1.6),
            arrowprops=dict(arrowstyle='-', color="#7b7b7b", linewidth=0.9,
                            connectionstyle="arc3,rad=0.25"), zorder=4)

ann2006_text = "2006 — Spain: +2.4% | EZ: +1.1% → Spain +1.3 pp higher"
txt2006 = ax.text(2006-2.05, y2006+1.65, ann2006_text, fontsize=9.5, va='center', ha='left', bbox=bbox_props, zorder=5)
# small green upward chevron icon inside box
ax.text(2006-2.34, y2006+2.03, "▲", fontsize=13, color="#2e7d32", weight='bold', zorder=6)

# Period summary box lower-right inside plot
summary_text = f"1999–2014 averages:\nSpain ≈ {avg_spain:.2f}%  ;  Euro‑Zone ≈ {avg_euro:.2f}%"
# Use a subtle box with slight shadow effect
bbox_summary = dict(boxstyle="round,pad=0.4", fc="white", ec="#cccccc", lw=0.8, alpha=0.98)
summary_x = 2013.1
summary_y = -10.3
txt_summary = ax.text(summary_x, summary_y, summary_text, fontsize=9, va='bottom', ha='right', bbox=bbox_summary, zorder=5)
txt_summary.set_path_effects([patheffects.withSimplePatchShadow(offset=(1,-1), alpha=0.15)])

# Contextual tag near 2008–2010 trough region
ctx_x = 2008.6
ctx_y = -6.2
ax.text(ctx_x, ctx_y, "Global financial crisis (2008–09)", fontsize=9, color="#4b4b4b", style='italic', bbox=dict(boxstyle="round,pad=0.2", fc=(1,1,1,0.8), ec='none'), zorder=5)

# Small simulated government logo top-right corner (programmatic placeholder)
logo_ax = fig.add_axes([0.83, 0.93, 0.12, 0.06], anchor='NE')
logo_ax.axis('off')
# Draw a simple emblem: colored stripes and "GOV"
logo_ax.add_patch(mpatches.Rectangle((0.02,0.15), 0.25, 0.65, facecolor="#C62828", transform=logo_ax.transAxes, clip_on=False))
logo_ax.add_patch(mpatches.Rectangle((0.29,0.15), 0.25, 0.65, facecolor="#1976D2", transform=logo_ax.transAxes, clip_on=False))
logo_ax.text(0.58, 0.5, "GOV", fontsize=9, fontweight='bold', va='center', ha='left', transform=logo_ax.transAxes)

# Footer source/metadata
fig.text(0.01, 0.01, "Source: [Official government finance agency / Eurostat]. Notes: % of GDP; annual data.", fontsize=8, color="#4d4d4d")

# Make layout tight and show
plt.subplots_adjust(top=0.88, left=0.07, right=0.95, bottom=0.08)
plt.savefig("generated/spain_factor3_2_design.png", dpi=300, bbox_inches="tight")