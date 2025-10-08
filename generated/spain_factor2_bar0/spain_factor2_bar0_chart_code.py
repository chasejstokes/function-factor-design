import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Data setup
years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
                  2008, 2009, 2010, 2011, 2012, 2013, 2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9,
                  -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use np.nan for missing euro-zone averages
euro = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7,
                 -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Styling constants
spain_color = "#0B6FC6"
euro_color = "#7B8EA3"
target_alpha = 0.4
target_hatch = "///"

# Figure: portrait orientation, 9x12 inches (900x1200 px at 100 dpi)
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
plt.subplots_adjust(top=0.88, bottom=0.08, left=0.12, right=0.96)

# X positions
x = np.arange(len(years))
total_width = 0.8  # width allocated per year
bar_width = 0.32   # each bar width ~32% per year (within 80% bin)

# Draw subtle vertical shading for selected years of notable divergence
# As specified: shade 2000, 2005-2007 (light tint of Spain color at ~6% opacity)
shade_years = [2000, 2005, 2006, 2007]
for yr in shade_years:
    if yr in years:
        idx = np.where(years == yr)[0][0]
        # compute left and right edges for the year's band
        left = x[idx] - total_width/2
        width = total_width
        rect = Rectangle((left - 0.01, ax.get_ylim()[0] if ax.get_ylim() != (0, 1) else -12),
                         width, 1000, transform=ax.transData,
                         color=spain_color, alpha=0.06, zorder=0)
        ax.add_patch(rect)

# Plot bars: Spain and Euro-zone
# Spain bars
spain_pos = x - bar_width/2
# For targets (2012-2014), apply special styling: indices where year >= 2012
target_mask = years >= 2012

# Plot Spain bars in two passes: non-targets and targets
non_target_mask = ~target_mask
ax.bar(spain_pos[non_target_mask], spain[non_target_mask],
       width=bar_width, color=spain_color, edgecolor='none', zorder=3)

# Target bars: same color but 40% opacity, dashed edge and hatch
ax.bar(spain_pos[target_mask], spain[target_mask],
       width=bar_width, color=spain_color, alpha=target_alpha,
       edgecolor=spain_color, linewidth=2, hatch=target_hatch, zorder=3)

# Euro-zone bars (skip nan values)
euro_pos = x + bar_width/2
euro_mask = ~np.isnan(euro)
ax.bar(euro_pos[euro_mask], euro[euro_mask],
       width=bar_width, color=euro_color, edgecolor='none', zorder=2)

# Axis limits and ticks
ymin = min(np.nanmin(euro[np.isfinite(euro)]) if np.any(np.isfinite(euro)) else 0, spain.min()) - 2
ymax = max(spain.max(), np.nanmax(euro[np.isfinite(euro)]) if np.any(np.isfinite(euro)) else spain.max()) + 2
# Constrain reasonable bounds for this dataset
ymin = min(ymin, -13)
ymax = max(ymax, 4)
ax.set_ylim(ymin, ymax)

# X-axis labels
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=12)

# Y-axis label and ticks every 5 points
ax.set_ylabel("% of GDP (surplus / deficit)", fontsize=16, labelpad=12)
y_ticks = np.arange(-15, 11, 5)
ax.set_yticks(y_ticks)
ax.set_yticklabels([f"{int(t)}" for t in y_ticks], fontsize=12)

# Draw sparse horizontal gridlines at major ticks
ax.yaxis.grid(True, which='major', color='0.85', linewidth=0.8)
ax.xaxis.grid(False)

# Emphasize the 0 baseline with a darker dashed line
ax.axhline(0, color='0.2', linewidth=1.5, linestyle='--', zorder=4)

# Direct value labels on each bar (one decimal, with % sign)
def format_label(val):
    return f"{val:+.1f}%" if val < 0 else f"{val:.1f}%"

# For Spain bars
for xi, val, is_target in zip(spain_pos, spain, target_mask):
    label = f"{val:.1f}%"
    if val >= 0:
        y_pos = val + 0.25
        va = 'bottom'
    else:
        y_pos = val - 0.25
        va = 'top'
    # Choose label color for contrast: use white for positive tall bars if needed; otherwise dark
    text_color = 'black'
    ax.text(xi, y_pos, label, ha='center', va=va, fontsize=14, fontweight='bold', color=text_color, zorder=6)

# For Euro-zone bars
for xi, val in zip(euro_pos[euro_mask], euro[euro_mask]):
    label = f"{val:.1f}%"
    if val >= 0:
        y_pos = val + 0.25
        va = 'bottom'
    else:
        y_pos = val - 0.25
        va = 'top'
    ax.text(xi, y_pos, label, ha='center', va=va, fontsize=14, fontweight='bold', color='black', zorder=5)

# Small embedded color swatches + inline labels at top-left of plotting area (axes coordinates)
# We'll draw small squares using axes coordinates transform
swatch_x = 0.02
swatch_y = 0.95
swatch_size = 0.02  # fraction of axes
# Spain swatch
ax_inset_spain = fig.add_axes([0.12 + swatch_x*(0.96-0.12), 0.88 + (swatch_y-0.88)*(0.92-0.88), 0.04, 0.04], frameon=False)
ax_inset_spain.add_patch(Rectangle((0, 0), 1, 1, color=spain_color))
ax_inset_spain.set_xticks([])
ax_inset_spain.set_yticks([])
ax_inset_spain.patch.set_alpha(0)

# Put the labels near the swatches using axes text (relative to main axes)
ax.text(0.03, 0.945, "Spain", transform=ax.transAxes, fontsize=14, fontweight='bold', va='center', ha='left', color='black')
ax.text(0.16, 0.945, "Euro‑zone avg", transform=ax.transAxes, fontsize=14, fontweight='bold', va='center', ha='left', color='black')

# Draw a small colored rectangle for Euro-zone swatch using axes coordinates patches
euro_swatch = Rectangle((0, 0), 1, 1, color=euro_color)
ax.add_patch(Rectangle((0, 0), 0, 0, transform=ax.transAxes, facecolor='none'))  # dummy to ensure transforms
ax.text(0.135, 0.945, "", transform=ax.transAxes)  # spacing
# Place swatches using ax.add_patch with transform=ax.transAxes
ax.add_patch(Rectangle((0.02, 0.93), 0.03, 0.03, transform=ax.transAxes, facecolor=spain_color, edgecolor='none'))
ax.add_patch(Rectangle((0.12, 0.93), 0.03, 0.03, transform=ax.transAxes, facecolor=euro_color, edgecolor='none'))

# Title and subtitle
plt.suptitle("Spain vs Euro‑Zone: Budget (% GDP)", fontsize=40, fontweight='bold', y=0.985)
ax.set_title("Annual budget surplus/deficit, 1999–2014 (last 3 years = Spain targets)", fontsize=22, fontweight='regular', pad=12)

# Annotations with boxes and leader lines
bbox_props = dict(boxstyle='round,pad=0.4', fc='rgba(1,1,1,0.95)', ec='0.6', lw=1)
# Since 'rgba' string not directly supported in bbox, create near-white fill using facecolor tuple
bbox_face = (0.98, 0.98, 0.98)
bbox_style = dict(boxstyle='round,pad=0.4', facecolor=bbox_face, edgecolor='0.6', linewidth=1)

# 1) 2005–2007 cluster (anchor year 2006): "Spain in surplus while Euro‑zone remained in deficit"
anchor_x = np.where(years == 2006)[0][0]
anchor_bar_x = x[anchor_x] - bar_width/2  # point to Spain bar
annotation_text = "Spain in surplus\nwhile Euro‑zone remained\nin deficit"
ax.annotate(annotation_text,
            xy=(anchor_bar_x, spain[anchor_x]),
            xycoords='data',
            xytext=(anchor_bar_x - 1.2, 3.8),
            textcoords='data',
            fontsize=14,
            va='top',
            ha='left',
            bbox=bbox_style,
            arrowprops=dict(arrowstyle='-', linewidth=1, color='0.4', connectionstyle="arc3,rad=-0.2", alpha=0.9)
            )

# 2) 2008–2011 crisis peak (anchor 2009): "Sharp drop in Spain after 2008 financial shock (2009 = -11.2%)"
anchor_x = np.where(years == 2009)[0][0]
anchor_bar_x = x[anchor_x] - bar_width/2
annotation_text = "Sharp drop in Spain\nafter 2008 financial shock\n(2009 = -11.2%)"
ax.annotate(annotation_text,
            xy=(anchor_bar_x, spain[anchor_x]),
            xycoords='data',
            xytext=(anchor_bar_x + 0.6, -2.6),
            textcoords='data',
            fontsize=14,
            va='bottom',
            ha='left',
            bbox=bbox_style,
            arrowprops=dict(arrowstyle='-', linewidth=1, color='0.4', connectionstyle="angle3,angleA=0,angleB=-90", alpha=0.9)
            )

# 3) 2012–2014 targets (anchored above each target bar cluster): "Government targets (projections)"
# Place one annotation centered above the three target years pointing down to middle
target_center_idx = np.where(years == 2013)[0][0]
target_center_x = x[target_center_idx]
annotation_text = "Government targets\n(projections)"
ax.annotate(annotation_text,
            xy=(target_center_x, max(spain[target_mask]) if np.any(target_mask) else 0),
            xycoords='data',
            xytext=(target_center_x, 1.6),
            textcoords='data',
            fontsize=14,
            va='bottom',
            ha='center',
            bbox=bbox_style,
            arrowprops=dict(arrowstyle='-', linewidth=1, color='0.4', connectionstyle="arc3,rad=0", alpha=0.9)
            )

# Data source at bottom-right (neutral phrasing)
fig.text(0.98, 0.02, "Data: Eurostat; Spain targets = national projections.",
         ha='right', va='bottom', fontsize=12, color='0.15')

# Tidy up spines and layout
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(False)

# Ensure bars do not get clipped by annotation boxes or swatches
ax.set_xlim(x[0] - 0.6, x[-1] + 0.6)

# Show plot
plt.savefig("generated/spain_factor2_bar0/spain_factor2_bar0_design.png", dpi=300, bbox_inches="tight")