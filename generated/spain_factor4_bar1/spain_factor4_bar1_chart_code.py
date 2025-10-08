import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9,
                  -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use np.nan to represent missing EZ values
ez = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
               -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Colors and style choices
color_spain = "#d95f02"       # deep orange
color_ez = "#6c7aa0"          # desaturated cool (muted blue/gray)
shade_missing = "#efefef"     # very light gray for EZ-unavailable columns
hatch_style = "///"           # diagonal hatch for Spain targets (2012-2014)

# Figure: portrait orientation, presentation resolution
fig_width, fig_height = 6, 8   # inches
dpi = 150
fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

# X positions for grouped bars
x = np.arange(len(years))
bar_width = 0.36

# Y-axis limits per spec
ymin, ymax = -12.5, 3.5
ax.set_ylim(ymin, ymax)

# Draw background shaded columns for EZ missing years (2012-2014)
missing_mask = np.isnan(ez)
for xi, missing in zip(x, missing_mask):
    if missing:
        # cover slightly beyond the bar group width for visual separation
        ax.axvspan(xi - 0.5, xi + 0.5, ymin=0, ymax=1,
                   facecolor=shade_missing, alpha=0.6, zorder=0)

# Plot bars: Spain (including target years with hatch and translucency), Euro-zone where available
bars_spain = []
bars_ez = []
for xi, s_val, ez_val, yr in zip(x, spain, ez, years):
    # Spain bar; apply hatch + lower alpha for target years (2012-2014)
    if yr >= 2012:
        b_sp = ax.bar(xi - bar_width/2, s_val, width=bar_width,
                      color=color_spain, alpha=0.30,
                      edgecolor=color_spain, linewidth=0.8,
                      hatch=hatch_style, zorder=3)
    else:
        b_sp = ax.bar(xi - bar_width/2, s_val, width=bar_width,
                      color=color_spain, alpha=1.0,
                      edgecolor=color_spain, linewidth=0.8, zorder=3)
    bars_spain.append(b_sp[0])
    # Euro-zone bar only if data available
    if not np.isnan(ez_val):
        b_ez = ax.bar(xi + bar_width/2, ez_val, width=bar_width,
                      color=color_ez, alpha=1.0,
                      edgecolor=color_ez, linewidth=0.8, zorder=3)
        bars_ez.append(b_ez[0])
    else:
        bars_ez.append(None)

# Axes styling per spec: thick high-contrast axis lines and ticks
for spine in ['left', 'bottom', 'right', 'top']:
    ax.spines[spine].set_linewidth(1.6)
    ax.spines[spine].set_color("#222222")

# Gridlines: horizontal lines for each major tick (every 2.5)
ax.yaxis.set_major_locator(MultipleLocator(2.5))
ax.yaxis.set_minor_locator(MultipleLocator(1.0))
ax.xaxis.set_major_locator(plt.FixedLocator(x))
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years],
                   fontsize=14, rotation=0)
ax.tick_params(axis='y', which='major', length=7, width=1.5, labelsize=16)
ax.tick_params(axis='y', which='minor', length=4, width=1.0)
ax.tick_params(axis='x', which='major', length=6, width=1.2)

ax.grid(axis='y', which='major', linestyle='-', linewidth=0.9, color='#d0d0d0', zorder=0)
ax.set_ylabel("Fiscal balance (% of GDP)", fontsize=18, fontweight='regular', labelpad=12)

# Baseline at 0 thicker
ax.axhline(0, color='#444444', linewidth=1.6, zorder=2)

# Title and subtitle
title = "Spain vs Euro‑Zone: Fiscal balance (% of GDP), 1999–2014"
subtitle = ("Spain outperformed the euro‑zone average in the mid‑2000s, then plunged during the crisis; "
            "2012–2014 show government targets, not reported EZ averages.")
fig.suptitle(title, fontsize=34, fontweight='bold', y=0.975)
ax.set_title(subtitle, fontsize=18, loc='center', pad=8, fontweight='normal')

# Legend: create custom patches including hatch explanation and EZ-unavailable indicator
legend_patches = [
    Rectangle((0, 0), 1, 1, facecolor=color_spain, edgecolor=color_spain, label='Spain'),
    Rectangle((0, 0), 1, 1, facecolor=color_ez, edgecolor=color_ez, label='Euro‑zone average'),
    Rectangle((0, 0), 1, 1, facecolor=color_spain, edgecolor=color_spain, hatch=hatch_style, alpha=0.30, label='Spain targets (2012–2014)'),
    Patch(facecolor=shade_missing, edgecolor='#cfcfcf', label='EZ data unavailable (2012–2014)')
]
legend = ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(0.01, 1.02),
                   fontsize=14, frameon=False)

# Selective numeric annotations
# 2009: Spain -11.2 and EZ -6.3 with computed gap
ix2009 = int(np.where(years == 2009)[0][0])
sp2009 = spain[ix2009]
ez2009 = ez[ix2009]
gap_2009 = round(abs(sp2009 - ez2009), 1)  # 4.9
# Points to annotate (bar tops)
sp2009_top = sp2009
ez2009_top = ez2009

# Annotation box style (light rounded rectangle)
bbox_style = dict(boxstyle="round,pad=0.4", fc="#ffffff", ec="#bdbdbd", lw=1)

# 2009 comparison callout
ax.annotate(
    f"2009: Spain {sp2009:.1f}% vs EZ {ez2009:.1f}%\nGap {gap_2009:.1f} pp",
    xy=(ix2009, (sp2009 + ez2009) / 2.0),
    xytext=(ix2009 + 1.1, -4.5),
    arrowprops=dict(arrowstyle="->", linewidth=0.9, color="#555555", shrinkA=5, shrinkB=5),
    fontsize=13,
    bbox=bbox_style,
    horizontalalignment='left',
    verticalalignment='center',
    zorder=6
)

# 2005-2007 surpluses callout (combined one-line summary)
ix2005 = int(np.where(years == 2005)[0][0])
ix2007 = int(np.where(years == 2007)[0][0])
mid_2005_2007 = (ix2005 + ix2007) / 2.0
ax.annotate(
    "Surpluses in 2005–2007\n(Spain > 0; EZ negative)",
    xy=(mid_2005_2007, 1.9),
    xytext=(mid_2005_2007, 2.8),
    arrowprops=dict(arrowstyle="-", linewidth=0.8, color="#555555", shrinkA=0, shrinkB=0),
    fontsize=13,
    bbox=bbox_style,
    horizontalalignment='center',
    verticalalignment='bottom',
    zorder=6
)

# 2010-2011 notable deficits callout
ix2010 = int(np.where(years == 2010)[0][0])
ix2011 = int(np.where(years == 2011)[0][0])
ax.annotate(
    "Large deficits in 2010–2011",
    xy=(ix2010 + 0.6, spain[ix2010]),
    xytext=(ix2011 + 1.0, -10.5),
    arrowprops=dict(arrowstyle="-", linewidth=0.8, color="#555555"),
    fontsize=12.5,
    bbox=bbox_style,
    horizontalalignment='left',
    verticalalignment='center',
    zorder=6
)

# 2012-2014 targets & EZ missing callout (lightweight, pointing to shaded region)
ix2013 = int(np.where(years == 2013)[0][0])
ax.annotate(
    "2012–2014 are government targets;\nEZ averages not reported",
    xy=(ix2013, spain[ix2013]),
    xytext=(ix2013 + 1.2, -2.0),
    arrowprops=dict(arrowstyle="-", linewidth=0.8, color="#555555"),
    fontsize=13,
    bbox=bbox_style,
    horizontalalignment='left',
    verticalalignment='center',
    zorder=6
)

# Synthesis box (top-right of plot area inside axes)
synth_text = (
    r"• Peak Spain deficit: $\mathbf{-11.2\%}$ (2009).\n"
    r"• Largest gap vs EZ: $\mathbf{4.9}$ percentage points (2009).\n"
    r"• Spain ran small surpluses 2005–2007; subsequent deficits exceeded EZ where reported."
)
# Place inside axes at top-right
ax.text(0.98, 0.94, synth_text,
        transform=ax.transAxes,
        fontsize=14,
        ha='right', va='top',
        bbox=dict(boxstyle="round,pad=0.6", fc="#ffffff", ec="#bdbdbd", lw=1),
        zorder=7)

# Footnote (bottom-left outside axes area)
fig.text(0.02, 0.02,
         "Notes: Euro‑zone averages not reported for 2012–2014. Spain 2012–2014 are government targets, not actual values. Source: [your source].",
         fontsize=11, ha='left', va='bottom')

# Tight layout but leave room for suptitle
plt.subplots_adjust(top=0.92, left=0.08, right=0.97, bottom=0.08)

# Show plot
plt.savefig("generated/spain_factor4_bar1/spain_factor4_bar1_design.png", dpi=300, bbox_inches="tight")