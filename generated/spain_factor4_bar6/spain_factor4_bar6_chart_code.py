import matplotlib.pyplot as plt
import numpy as np

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors (colorblind-friendly pair)
color_spain = "#D1493E"   # warm deep orange/red
color_ez = "#2A9D8F"      # cool deep teal/blue

# Figure: portrait orientation, ~900x1200 px at 100 dpi -> 9x12 inches
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.12, right=0.95)

# Positions and bar settings
x = np.arange(len(years))
bar_width = 0.36
gap_between_pairs = 0.3  # implicit via bar_width and tick spacing

# Draw bars (Spain left, Euro Zone right)
bars_spain = ax.bar(x - bar_width/2, spain, width=bar_width, color=color_spain, label="Spain", zorder=3)
bars_ez = ax.bar(x + bar_width/2, ez, width=bar_width, color=color_ez, label="Euro Zone average", zorder=3)

# Axis limits and ticks
ax.set_ylim(-12.5, 3.5)
ax.set_xlim(-0.6, len(years)-0.4)

y_ticks = [-12, -10, -8, -6, -4, -2, 0, 2]
ax.set_yticks(y_ticks)
ax.set_yticklabels([str(t) for t in y_ticks], fontsize=15)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=17, labelpad=14)

# X axis ticks: one per year, centered under each pair
ax.set_xticks(x)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=15)
ax.tick_params(axis='x', which='both', length=0)

# Gridlines: horizontal only
ax.yaxis.grid(True, linestyle='-', color='#e6e6e6', linewidth=1, zorder=0)
ax.xaxis.grid(False)

# Emphasize zero baseline
ax.axhline(0, color='#666666', linewidth=1.6, zorder=4)

# Title and subtitle (top center)
fig.suptitle("Budget balance (% of GDP) — Spain vs Euro Zone average (1999–2014)",
             fontsize=34, fontweight='bold', y=0.975)
fig.text(0.5, 0.94,
         "Spain shows larger swings across the cycle, with a sharp plunge in 2009 and outperformance in the mid‑2000s.",
         ha='center', fontsize=20)

# Legend: compact top-right inside plot
leg = ax.legend(loc='upper right', fontsize=17, frameon=False, bbox_to_anchor=(0.98, 0.98))
for text in leg.get_texts():
    text.set_fontsize(17)

# Remove top/right spines, keep left and bottom subtle
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Selective callouts for diagnostic years: 2004, 2009, and 2006 (optional)
callouts = [
    # year, formatted text, text_x_offset, text_y_offset
    (2004, f"Spain 0.6%  |  EZ −2.9%", 0.9, 1.3),
    (2009, f"Spain −11.2%  |  EZ −6.3%", 0.9, -1.0),
    (2006, f"Spain 2.4%  |  EZ 1.1%", 0.9, 1.4)
]

for year_val, txt, dx, dy in callouts:
    idx = int(np.where(years == year_val)[0])
    # anchor point: middle of the pair (x position)
    anchor_x = x[idx]
    # pick anchor y near the Spain bar value for leader target
    anchor_y = spain[idx]
    # compute text position slightly to the right of the pair, with a vertical offset (in data coords)
    text_x = anchor_x + dx
    text_y = anchor_y + dy

    # draw thin leader line (no arrowhead)
    ax.annotate("",
                xy=(anchor_x - bar_width/2, anchor_y), xycoords='data',
                xytext=(text_x - 0.05, text_y), textcoords='data',
                arrowprops=dict(arrowstyle='-', color='#7f7f7f', linewidth=0.8, connectionstyle="angle3"))
    # small boxed label
    bbox_props = dict(boxstyle="round,pad=0.35", fc="#f7f7f7", ec="#bdbdbd", lw=0.8)
    ax.text(text_x, text_y, txt, fontsize=15, va='center', ha='left', bbox=bbox_props, zorder=10)

# Synthesis box (lower-right inside axes)
synth_text = ("Synthesis (1999–2014): Spain average = −2.66% of GDP; Euro‑Zone average = −2.57% of GDP. "
              "Largest divergence: 2009 (Spain −11.2% vs EZ −6.3, gap = −4.9 pp). "
              "Spain shows bigger cyclical swings: stronger mid‑2000s surpluses and deeper crisis deficits.")
ax.text(0.98, 0.06, synth_text, transform=ax.transAxes, fontsize=15,
        va='bottom', ha='right',
        bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#bdbdbd", lw=0.9))

# Final aesthetic tweaks
ax.set_axisbelow(True)  # gridlines below bars
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save or show
plt.savefig("generated/spain_factor4_bar6/spain_factor4_bar6_design.png", dpi=300, bbox_inches="tight")