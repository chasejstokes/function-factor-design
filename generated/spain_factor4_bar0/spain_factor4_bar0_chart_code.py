try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Patch
    from matplotlib.lines import Line2D
except Exception:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Patch
    from matplotlib.lines import Line2D

# Data setup (cleaned and converted)
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain_values = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Euro-zone average: last three years NA
ez_values = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Identify target years (2012-2014)
target_mask = (years >= 2012)

# Color palette (colorblind friendly)
color_spain = "#D95F02"  # warm orange
color_ez = "#1B9E77"     # teal/green
color_na = "#BFBFBF"     # light gray for "n.a."

# Canvas and layout: 900x1200 px -> 9x12 inches at 100 dpi (3:4 aspect ratio)
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
plt.subplots_adjust(top=0.86, bottom=0.10, left=0.12, right=0.88)

# X positions: widen spacing between year groups for clarity
group_spacing = 1.4
x = np.arange(len(years)) * group_spacing
bar_width = 0.45  # moderate width

# Draw subtle period overlays using axvspan for robust behavior
def year_idx(y):
    return int(np.where(years == y)[0][0])

# 2005-2007 overlay (warm, low opacity)
start_idx = year_idx(2005)
end_idx = year_idx(2007)
xstart = x[start_idx] - 0.6
xend = x[end_idx] + 0.6
ax.axvspan(xstart, xend, ymin=0, ymax=1, facecolor=color_spain, alpha=0.06, zorder=0)

# 2008-2011 overlay (cool, low opacity)
start_idx = year_idx(2008)
end_idx = year_idx(2011)
xstart2 = x[start_idx] - 0.6
xend2 = x[end_idx] + 0.6
ax.axvspan(xstart2, xend2, ymin=0, ymax=1, facecolor=color_ez, alpha=0.06, zorder=0)

# Draw bars: Spain (actual and target styled), Euro-Zone (skip NA)
spain_bars = []
spain_target_bars = []
ez_bars = []

for xi, yr, spv, ezv, is_target in zip(x, years, spain_values, ez_values, target_mask):
    # Spain: separate treatment if target
    if is_target:
        # patterned target bar (same color, diagonal hatch, partial alpha, dashed edge)
        b = ax.bar(xi - bar_width/2, spv, width=bar_width,
                   color=color_spain, ec='#8A3E00', hatch='///',
                   alpha=0.55, linewidth=1.0, zorder=3)
        spain_target_bars.append(b[0])
    else:
        b = ax.bar(xi - bar_width/2, spv, width=bar_width,
                   color=color_spain, ec='none', zorder=3)
        spain_bars.append(b[0])

    # Euro-Zone average: draw only when data present
    if not np.isnan(ezv):
        b2 = ax.bar(xi + bar_width/2, ezv, width=bar_width,
                    color=color_ez, ec='none', zorder=2)
        ez_bars.append(b2[0])
    else:
        # No bar; leave empty. We'll indicate missing in legend only.
        pass

# Axis formatting
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=14)
ax.set_xlim(x[0] - 1.0, x[-1] + 1.0)

# Y-axis ticks: sensible intervals every 2 points
ymin = min(np.nanmin(spain_values), np.nanmin(ez_values)) - 1.5
ymax = max(np.nanmax(spain_values), np.nanmax(ez_values)) + 1.5
# Round to nearest even numbers for nicer grid
ymin = np.floor(ymin / 2) * 2
ymax = np.ceil(ymax / 2) * 2
yticks = np.arange(ymin, ymax + 1, 2)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t:.0f}" for t in yticks], fontsize=16)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18)

# Emphasize zero baseline
ax.axhline(0, color="#444444", linewidth=2.0, zorder=4)

# Light horizontal gridlines
ax.yaxis.grid(True, which='major', color='gray', alpha=0.15, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Title, subtitle, valenced subtext placed in top center area
title = "Spain vs Euro‑Zone: Budget balance (% of GDP), 1999–2014"
subtitle = ("Yearly general government balance. Last three years (2012–2014) are Spain’s policy targets; "
            "Euro‑Zone averages unavailable for those years.")
valenced = "Spain’s fiscal position swings from surpluses mid‑2000s to a dramatic post‑2008 deficit peak."

fig.suptitle(title, fontsize=34, fontweight='bold', y=0.985)
ax.text(0.5, 0.945, subtitle, transform=fig.transFigure,
        ha='center', fontsize=20)
ax.text(0.5, 0.915, valenced, transform=fig.transFigure,
        ha='center', fontsize=16, style='italic', color='#333333')

# Legend (top-right under title block)
legend_elements = [
    Patch(facecolor=color_spain, edgecolor='none', label='Spain'),
    Patch(facecolor=color_ez, edgecolor='none', label='Euro‑Zone avg.'),
    Patch(facecolor=color_spain, hatch='///', edgecolor='#8A3E00', label='Spain (Targets)', alpha=0.6),
    Line2D([0], [0], marker='o', color='w', label='Euro‑Zone: no data (2012–2014)',
           markerfacecolor=color_na, markersize=8)
]
leg = ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.02, 1.06),
                fontsize=14, frameon=False)

# Selective annotations (2006, 2009, 2010–2011 and period labels)
def annotate_callout(year, text, xytext, va='center', ha='left', bgcolor='white', text_color='black'):
    idx = np.where(years == year)[0][0]
    xi = x[idx] - bar_width/2  # point to Spain bar center
    yval = spain_values[idx]
    ax.annotate(text,
                xy=(xi, yval),
                xytext=xytext,
                textcoords='data',
                fontsize=14,
                ha=ha, va=va,
                color=text_color,
                bbox=dict(boxstyle="round,pad=0.3", fc=bgcolor, ec="#666666", alpha=0.95),
                arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.2",
                                color="#666666", linewidth=0.8))

# 2006
annotate_callout(2006, "Spain +2.4% (peak surplus, 2006)",
                 xytext=(x[year_idx(2006)] - 2.0, 3.0), ha='left')

# 2009 detailed comparison
annotate_callout(2009, "Spain −11.2% (2009) — 4.9 pp worse than EZ avg −6.3%",
                 xytext=(x[year_idx(2009)] - 2.2, -9.0), ha='left')

# 2010-2011 persistent deficits (single combined callout pointing near 2010 bar)
annotate_callout(2010, "Persisting large deficits\n(2010–2011)", xytext=(x[year_idx(2010)] + 0.8, -4.0),
                 ha='left')

# Period small boxed labels placed over overlays
# Outperformance 2005-2007
ax.text((x[year_idx(2005)] + x[year_idx(2007)])/2, ymax - 0.6, "Outperformance vs Euro‑Zone",
        ha='center', va='top', fontsize=13, bbox=dict(boxstyle="round,pad=0.3",
                                                       fc=color_spain, ec='none', alpha=0.12))

# Post-crisis 2008-2011 label
ax.text((x[year_idx(2008)] + x[year_idx(2011)])/2, ymax - 0.6, "Post‑crisis large deficits",
        ha='center', va='top', fontsize=13, bbox=dict(boxstyle="round,pad=0.3",
                                                       fc=color_ez, ec='none', alpha=0.10))

# Synthesis box with computed stats (for 1999–2011)
mask_1999_2011 = (years <= 2011)
spain_9911 = spain_values[mask_1999_2011]
ez_9911 = ez_values[mask_1999_2011]

spain_avg = np.nanmean(spain_9911)
ez_avg = np.nanmean(ez_9911)
spain_max_idx = np.nanargmax(spain_9911)
spain_max_val = spain_9911[spain_max_idx]
# Convert index back to year
spain_max_year = years[mask_1999_2011][spain_max_idx]
spain_min_idx = np.nanargmin(spain_9911)
spain_min_val = spain_9911[spain_min_idx]
spain_min_year = years[mask_1999_2011][spain_min_idx]
gap_2009 = spain_values[year_idx(2009)] - ez_values[year_idx(2009)]
gap_2009_pp = gap_2009  # already in percentage points

synth_lines = [
    f"Span. avg (1999–2011): {spain_avg:+.2f}% GDP",
    f"EZ avg (1999–2011): {ez_avg:+.2f}% GDP",
    f"Spain max surplus: {spain_max_val:+.1f}% ({spain_max_year})",
    f"Spain worst deficit: {spain_min_val:+.1f}% ({spain_min_year}) — {abs(gap_2009_pp):.1f} pp worse than EZ"
]

# Draw synthesis box (small boxed module inside plot area, lower-right)
ax_box = fig.add_axes([0.59, 0.56, 0.30, 0.20])  # small inset axes for crisp box placement
ax_box.axis('off')
# Background rectangle
ax_box.add_patch(Rectangle((0, 0), 1, 1, transform=ax_box.transAxes,
                           facecolor='white', edgecolor='#666666', linewidth=0.8, alpha=0.95))
# Text lines
for i, line in enumerate(synth_lines):
    ax_box.text(0.02, 0.85 - i * 0.22, line, transform=ax_box.transAxes,
                fontsize=14, ha='left', va='center', color='#111111')

# Footnote / data source bottom-left
footnote = ("Data: Government budget balance (% GDP). 2012–2014 are Spanish government targets; "
            "Euro‑Zone averages not available for 2012–2014.")
fig.text(0.12, 0.04, footnote, fontsize=12, ha='left', va='center', color='#333333')

# Ensure aspect and layout visually align (taller than wide already)
ax.set_title("")  # main title handled via suptitle

# Tighten layout a bit
plt.draw()

# Show plot
plt.savefig("generated/spain_factor4_bar0/spain_factor4_bar0_design.png", dpi=300, bbox_inches="tight")