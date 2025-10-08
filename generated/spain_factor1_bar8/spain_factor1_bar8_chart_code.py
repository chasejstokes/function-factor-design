import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb

# Data (from provided JSON-like input)
years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
                  2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4,
                  1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1,
                 -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors
color_spain = "#D6453A"   # warm Spanish red / orange
color_euro = "#2E86AB"    # deep teal/blue
# darker outline for Spain (~15% darker)
def darken(hex_color, amount=0.15):
    r, g, b = to_rgb(hex_color)
    r *= (1 - amount)
    g *= (1 - amount)
    b *= (1 - amount)
    return (r, g, b)

edge_spain = darken(color_spain, 0.15)

# Figure size: portrait 3:4 aspect ratio, e.g., 9 x 12 inches
fig_w, fig_h = 9, 12
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)

# Layout adjustments to leave space for title/subtitle/legend/caption/metadata
plt.subplots_adjust(top=0.82, bottom=0.16, left=0.10, right=0.95)

# X positions
indices = np.arange(len(years))
group_width = 0.8  # total width allocated to each year group
bar_width = 0.34
sep = 0.04  # small separation between paired bars

pos_spain = indices - (bar_width / 2 + sep/2)
pos_euro = indices + (bar_width / 2 + sep/2)

# Crisis band: 2008-2010 inclusive
yr_start = 2008
yr_end = 2010
# compute span extents based on group indices
start_idx = np.where(years == yr_start)[0][0]
end_idx = np.where(years == yr_end)[0][0]
x_start = start_idx - 0.5
x_end = end_idx + 0.5
ax.axvspan(x_start, x_end, facecolor="#f7efe8", alpha=0.12, zorder=0)

# Bars
bars_spain = ax.bar(pos_spain, spain, width=bar_width, label="Spain",
                    color=color_spain, edgecolor=edge_spain, linewidth=1.0,
                    hatch='//', zorder=3)
bars_euro = ax.bar(pos_euro, euro, width=bar_width, label="Euro‑Zone average",
                   color=color_euro, edgecolor='none', linewidth=0, zorder=3)

# Y axis settings
ax.set_ylim(-12.5, 3)
yticks = [-12, -10, -8, -6, -4, -2, 0, 2]
ax.set_yticks(yticks)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, fontweight='normal', labelpad=12)

# Emphasize zero line
ax.axhline(0, color='#444444', linewidth=1.6, zorder=2)

# Light horizontal gridlines for reference (except zero which is emphasized above)
ax.yaxis.grid(True, which='major', color='#dcdcdc', linewidth=0.8, zorder=1)
# Ensure the zero gridline isn't duplicated visually
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_color('#444444')
ax.spines['bottom'].set_color('#444444')

# X axis ticks and labels
ax.set_xticks(indices)
ax.set_xticklabels(years.astype(str), fontsize=15)
ax.tick_params(axis='x', which='both', length=0)

# Legend: top-right inside chart area, just under title block
legend = ax.legend(loc='upper right', bbox_to_anchor=(0.98, 0.88),
                   fontsize=16, frameon=False)

# Title and subtitle as figure-level text (top center)
title_text = "Spain vs Euro‑Zone: Budget Balance (% of GDP), 1999–2014"
subtitle_text = ("Paired bars show yearly budget deficits (negative) and surpluses (positive); "
                 "focus on differences between Spain and the Euro‑Zone average")

fig.suptitle(title_text, fontsize=32, fontweight='bold', y=0.96)
fig.text(0.5, 0.92, subtitle_text, ha='center', fontsize=20, weight='medium')

# Caption (1-2 concise sentences) under the chart, spanning full width
caption = ("Spain’s balance tracks close to the Euro‑Zone average in the early 2000s, then "
           "diverges sharply during and after the 2008 crisis (peak deficit: Spain −11.2% in 2009). "
           "Data: % of GDP; years shown: 1999–2014. See metadata box for source and calculation notes.")
fig.text(0.5, 0.11, caption, ha='center', fontsize=14)

# Metadata box bottom-left under the caption
meta_lines = [
    "Source: Eurostat / national accounts (placeholder)",
    "Measure: Budget balance as % of GDP (negative = deficit)",
    "Processing: yearly observations, Spain vs unweighted Euro‑Zone average",
    "Chart prepared for presentation"
]
meta_text = "\n".join(meta_lines)
textbox_props = dict(boxstyle="round,pad=0.5", facecolor="#f2f2f2", edgecolor="#d9d9d9", alpha=0.95)
fig.text(0.02, 0.04, meta_text, fontsize=12, va='bottom', ha='left', bbox=textbox_props)

# Accessibility: add small diagonal pattern on Spain already; ensure edge contrast
for bar in bars_spain:
    bar.set_zorder(4)

# Maintain equal visual spacing between year groups by setting x-limits
ax.set_xlim(-0.75, len(years)-1 + 0.75)

# Annotate y-ticks font size
for label in ax.get_yticklabels():
    label.set_fontsize(14)

# Save high-resolution outputs for presentation
plt.savefig("spain_vs_eurozone_budget_balance_1999_2014.png", dpi=300, bbox_inches='tight')
plt.savefig("spain_vs_eurozone_budget_balance_1999_2014.pdf", bbox_inches='tight')

# Show the plot
plt.savefig("generated/spain_factor1_bar8/spain_factor1_bar8_design.png", dpi=300, bbox_inches="tight")