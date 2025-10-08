import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.4,-1.0,-0.6,-0.2,-0.3,-0.1,1.3,2.4,1.9,-4.5,-11.2,-9.3,-8.9,-6.3,-4.5,-2.8])
# Euro zone has NA for 2012-2014 -> represent with np.nan
euro = np.array([-1.4,0.0,-1.8,-2.5,-3.1,-2.9,-2.4,-1.3,-0.7,-2.1,-6.3,-6.2,-4.1,np.nan,np.nan,np.nan])

# Figure and axes: portrait layout, large for presentation
fig, ax = plt.subplots(figsize=(9,12))

# Colors: Spain deep burnt orange, Euro muted slate blue/gray
color_spain = "#C84B31"  # deep burnt orange
color_euro = "#6E88A3"   # slate blue-gray
edge_spain = "#5A261B"   # dark outline for hatched targets

# Bar positions and width
x = np.arange(len(years))
bar_width = 0.36

# Plot Spain bars; for 2012-2014 we will overlay hatched semi-transparent bars
spain_bars = ax.bar(x - bar_width/2, spain, width=bar_width,
                    color=color_spain, zorder=3, label='Spain',
                    edgecolor='none')

# Plot Euro bars only where data is available
valid_euro = ~np.isnan(euro)
euro_bars = ax.bar(x[valid_euro] + bar_width/2, euro[valid_euro], width=bar_width,
                   color=color_euro, zorder=2, edgecolor='none', label='Euro-Zone average')

# Overlay hatched targets for Spain 2012-2014 (last three bars)
target_idx = np.where((years >= 2012) & (years <= 2014))[0]
# Draw hatched rectangles on top of the existing Spain bars for the target years
for i in target_idx:
    # get bar rectangle coords
    xi = x[i] - bar_width/2
    height = spain[i]
    # For bars that are negative, rectangle y should be height, and height_abs is -height
    if height >= 0:
        y0 = 0
        h = height
    else:
        y0 = height
        h = -height
    # Create a hatched rectangle with alpha overlay and thin dark outline
    hatch_rect = patches.Rectangle((xi, y0), bar_width, h,
                                   facecolor=color_spain, alpha=0.5,
                                   hatch='///', edgecolor=edge_spain, linewidth=0.8, zorder=4)
    ax.add_patch(hatch_rect)

# Emphasize zero line
ax.axhline(0, color='black', linewidth=1.2, zorder=1)

# Horizontal gridlines at every 2 percentage points
y_ticks = np.array([-12, -10, -8, -6, -4, -2, 0, 2])
ax.set_yticks(y_ticks)
ax.set_ylim(-12.5, 3.0)
ax.yaxis.grid(True, which='major', color='#DDDDDD', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Axis labels and title/subtitle
ax.set_ylabel('% of GDP', fontsize=15, labelpad=10)
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=12)
ax.tick_params(axis='y', labelsize=13)

# Title and subtitle
ax.set_title("Budget Balance (% of GDP)", fontsize=26, fontweight='semibold', pad=20)
plt.suptitle("Spain vs Euro‑Zone average, 1999–2014", y=0.945, fontsize=15, color='gray')  # subtitle just under title

# Numeric value labels for every bar (Spain and Euro-Zone where present)
def label_bar(ax, rects, series_name):
    for rect in rects:
        height = rect.get_height()
        xloc = rect.get_x() + rect.get_width() / 2
        # Format label
        lbl = f"{height:.1f}"
        # Placement rules:
        if height >= 0:
            y = height + 0.18  # just above
            color = 'black'
            va = 'bottom'
        else:
            # negative: place just below the tip (more negative)
            # if the bar is quite small in magnitude, place outside for legibility
            if abs(height) < 0.5:
                y = height - 0.25
                color = 'black'
                va = 'top'
            else:
                y = height - 0.18
                color = 'white'
                va = 'top'
        ax.text(xloc, y, lbl, ha='center', va=va, fontsize=13, fontweight='normal', color=color, zorder=6)

label_bar(ax, spain_bars, 'Spain')
label_bar(ax, euro_bars, 'Euro')

# Inline series labels (replace legend)
# Spain label near top-right of last Spain bar (2014)
last_spain_x = x[-1] - bar_width/2 + bar_width*0.95
last_spain_y = spain[-1]
# Place label slightly above bar tip for readability
ax.text(last_spain_x, last_spain_y + 0.25, "Spain", fontsize=13, fontweight='semibold', color=color_spain,
        ha='right', va='bottom')

# Euro label near the top-right of the last available Euro bar (2011)
# find last non-nan index
last_euro_idx = np.where(valid_euro)[0][-1]
last_euro_x = x[last_euro_idx] + bar_width/2 + bar_width*0.05
last_euro_y = euro[last_euro_idx]
ax.text(last_euro_x, last_euro_y + 0.25, "Euro‑Zone average", fontsize=12, fontweight='semibold', color=color_euro,
        ha='left', va='bottom')

# Inline key for "Spain (target)" with hatched swatch near top-right inside plot
# Position near top-right corner inside axes coordinates
ax_x_limits = ax.get_xlim()
ax_y_limits = ax.get_ylim()
# compute location in data coords
sw_x = ax_x_limits[1] - 1.5  # slightly inset from right
sw_y = ax_y_limits[1] - 0.4  # top area
# Draw a small swatch rectangle with hatch
swatch = patches.Rectangle((sw_x - 0.25, sw_y - 0.15), 0.45, 0.6,
                           facecolor=color_spain, alpha=0.5, hatch='///', edgecolor=edge_spain, linewidth=0.8, zorder=6, transform=ax.transData)
ax.add_patch(swatch)
ax.text(sw_x + 0.4, sw_y + 0.15, "Spain (target)", fontsize=11, va='center', ha='left', color='black')

# Add small "—" marker for NA years at x-axis (above the tick) for 2012-2014
for i in target_idx:
    ax.text(x[i], -0.7, "—", color='#999999', ha='center', va='center', fontsize=14)

# Annotations (anchored callouts) with connectors
# Use the exact provided verbatim annotation texts

# 2006 callout anchored to 2006 Spain bar
i_2006 = np.where(years == 2006)[0][0]
ax.annotate("Mid‑2000s: Spain posts a surplus (2006: +2.4%) while the Euro‑Zone average remains negative (-1.3).",
            xy=(x[i_2006] - bar_width/2 + bar_width/2, spain[i_2006]),
            xytext=(x[i_2006]-2.2, 1.6),
            fontsize=14, ha='left', va='top',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#777777", linewidth=0.8),
            arrowprops=dict(arrowstyle='-', color='#777777', linewidth=0.9, connectionstyle="angle3"))

# 2009 callout anchored to 2009 Spain bar
i_2009 = np.where(years == 2009)[0][0]
ax.annotate("2009 peak deficit: Spain -11.2% vs EZ average -6.3% (Δ -4.9 pp).",
            xy=(x[i_2009] - bar_width/2 + bar_width/2, spain[i_2009]),
            xytext=(x[i_2009]+0.6, -8.5),
            fontsize=14, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#777777", linewidth=0.8),
            arrowprops=dict(arrowstyle='-', color='#777777', linewidth=0.9, connectionstyle="arc3,rad=0.2"))

# 2011 callout anchored to 2011 Spain bar
i_2011 = np.where(years == 2011)[0][0]
ax.annotate("2011: Spain remains deeper in deficit (-8.9%) than the Euro‑Zone (-4.1%).",
            xy=(x[i_2011] - bar_width/2 + bar_width/2, spain[i_2011]),
            xytext=(x[i_2011]+0.8, -4.0),
            fontsize=14, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#777777", linewidth=0.8),
            arrowprops=dict(arrowstyle='-', color='#777777', linewidth=0.9, connectionstyle="arc3,rad=0.0"))

# 2012-2014 grouped target callout anchored to those Spain bars (place box above the three bars, connector to middle bar)
mid_target_x = x[target_idx].mean()
mid_target_y = spain[target_idx].min()  # anchor near the deepest of targets
ax.annotate("2012–2014 shown as government targets (not actuals). Euro‑Zone average data are unavailable (NA) for these years.",
            xy=(mid_target_x, spain[target_idx].mean()),
            xytext=(mid_target_x+1.6, -1.6),
            fontsize=14, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="#777777", linewidth=0.8),
            arrowprops=dict(arrowstyle='-', color='#777777', linewidth=0.9, connectionstyle="angle3"))

# De-emphasized source note lower-left
ax.text(ax.get_xlim()[0] + 0.2, ax.get_ylim()[0] + 0.2, "Data: provided dataset", fontsize=9, color='#666666', ha='left', va='bottom')

# Remove typical legend to honor direct labeling (but leave if needed)
ax.legend_.remove() if ax.get_legend() else None

# Tight layout and show
plt.subplots_adjust(top=0.88, right=0.96, left=0.12, bottom=0.08)
plt.savefig("generated/spain_factor2_bar5/spain_factor2_bar5_design.png", dpi=300, bbox_inches="tight")