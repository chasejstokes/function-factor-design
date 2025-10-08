import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez =    np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Presentation parameters
DPI = 120
FIG_W, FIG_H = 7.5, 10  # inches (approx 900x1200 px at 120 dpi)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 32,
    "axes.titleweight": "bold",
    "axes.labelsize": 16,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
})

# Colors (gov palette, colorblind-friendly)
color_spain = "#D84B2A"  # warm vermilion
color_ez = "#1F4E79"     # navy blue
bg_color = "#F7F7F7"     # very light gray background
grid_color = "#E6E6E6"
axis_text_color = "#333333"

# Compute darker edge color (~25% darker)
def darken(hex_color, factor=0.75):
    h = hex_color.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    r = int(max(0, min(255, r * factor)))
    g = int(max(0, min(255, g * factor)))
    b = int(max(0, min(255, b * factor)))
    return f"#{r:02x}{g:02x}{b:02x}"

edge_spain = darken(color_spain, 0.75)
edge_ez = darken(color_ez, 0.75)

# Hatch option for print/grayscale fallback
USE_HATCH = False
hatch_spain = '//' if USE_HATCH else None
hatch_ez = '\\\\' if USE_HATCH else None

# Create figure
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor(bg_color)
ax.set_facecolor("white")

# X positions for grouped bars
n = len(years)
indices = np.arange(n)
bar_width = 0.38
offset = bar_width / 2.0
pos_spain = indices - offset
pos_ez = indices + offset

# Plot shaded band for crisis years 2008-2011 (indices 9 to 12)
start_idx = np.where(years == 2008)[0][0]
end_idx = np.where(years == 2011)[0][0]
band_left = start_idx - 0.6
band_right = end_idx + 0.6
ax.axvspan(band_left, band_right, color="#FDEDEC", alpha=0.6, zorder=0)  # very pale red

# Plot bars
bars_spain = ax.bar(pos_spain, spain, width=bar_width, label="Spain",
                    color=color_spain, edgecolor=edge_spain, linewidth=1.2,
                    hatch=hatch_spain, zorder=3)
bars_ez = ax.bar(pos_ez, ez, width=bar_width, label="Euro-zone average",
                 color=color_ez, edgecolor=edge_ez, linewidth=1.2,
                 hatch=hatch_ez, zorder=3)

# Prominent zero line
ax.axhline(0, color="#333333", linewidth=2.0, zorder=4)

# Minor vertical dividers between years
for i in indices:
    ax.vlines(i, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], colors=grid_color, linestyles='-', linewidth=0.8, alpha=0.9, zorder=0)

# X-axis labels and styling
ax.set_xticks(indices)
ax.set_xticklabels(years, rotation=0)
ax.tick_params(axis='x', which='major', pad=8)
ax.set_xlim(indices[0] - 0.8, indices[-1] + 0.8)

# Y-axis ticks and limits
ymin, ymax = -13.5, 4
ax.set_ylim(ymin, ymax)
yticks = list(range(-12, 6, 2))
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t}" for t in yticks])
ax.yaxis.grid(True, color=grid_color, linewidth=0.9, zorder=0)
ax.tick_params(axis='y', colors=axis_text_color)

# Title (top center)
ax.set_title("Spain vs Euro‑Zone: Budget Balance (1999–2014)", pad=26)

# Legend top-right (large swatches)
legend_handles = [
    mpatches.Patch(facecolor=color_spain, edgecolor=edge_spain, label="Spain"),
    mpatches.Patch(facecolor=color_ez, edgecolor=edge_ez, label="Euro‑zone average"),
]
legend = ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.02, 1.04),
                   frameon=False, fontsize=17, handlelength=1.8, handleheight=1.8)

# Top-left government logo placeholder and one-line source aligned with it
# Create a small inset axes for a logo rectangle
logo_ax = fig.add_axes([0.055, 0.93, 0.12, 0.055], anchor='NW')
logo_ax.add_patch(mpatches.Rectangle((0,0),1,1, facecolor="#2E6B2E"))
logo_ax.text(0.5, 0.5, "GOV\nLOGO", color="white", ha="center", va="center", fontsize=10, weight='bold')
logo_ax.axis('off')

# Source line aligned with logo (inline)
fig.text(0.22, 0.955, "Source: Government agency / Eurostat  •  Prepared by [Agency]", fontsize=12.5, color=axis_text_color, va='center')

# Summary box (top-right under legend)
summary_text = (
    "Average difference (1999–2014): Spain −0.1 pp vs Euro‑zone (roughly parity)\n"
    "Peak underperformance: 2009 — Spain −11.2 vs EZ −6.3 (−4.9 pp)"
)
summary_box = dict(boxstyle="round,pad=0.7", facecolor="white", edgecolor="#DDDDDD")
fig.text(0.725, 0.86, summary_text, fontsize=15, ha="left", va="top", bbox=summary_box, color=axis_text_color)

# Short contextual bullets under summary
context_text = "• 2007–2011: Global financial crisis and fiscal impacts"
fig.text(0.725, 0.80, context_text, fontsize=14, ha="left", va="top", color=axis_text_color)

# Selective value labels for annotated years: 2004, 2006, 2009, 2010, 2011
annot_years = [2004, 2006, 2009, 2010, 2011]
for yr in annot_years:
    idx = np.where(years == yr)[0][0]
    x = pos_spain[idx]
    val = spain[idx]
    if val >= 0:
        va = 'bottom'
        y_text = val + 0.35
    else:
        va = 'top'
        y_text = val - 0.35
    ax.text(x, y_text, f"{val:.1f}%", fontsize=15, fontweight='bold', ha='center', va=va, color=axis_text_color, zorder=5)

# Annotations with circular callouts and leaders
def draw_circle_callout(ax, xdata, ydata, text, text_xy, arrow_offset=(0,0), circle_radius=0.9, circle_color="#666666", icon=None, bold_delta=None):
    # Circle
    circ = mpatches.Circle((xdata, ydata), radius=circle_radius, fill=False, linewidth=2.0, edgecolor=circle_color, zorder=6)
    ax.add_patch(circ)
    # Connector (arrowless line)
    ax.annotate("", xy=(xdata, ydata), xytext=text_xy, arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.15", color=circle_color, linewidth=1.2), zorder=6)
    # Text box
    bbox = dict(boxstyle="round,pad=0.4", fc="white", ec="#DDDDDD")
    ax.text(text_xy[0], text_xy[1], text, fontsize=14, va='center', ha='left', bbox=bbox, zorder=7, color=axis_text_color)
    # Optionally draw icon near text (unicode)
    if icon:
        ax.text(text_xy[0]-0.03, text_xy[1], icon, fontsize=16, va='center', ha='right', color=circle_color, zorder=8)
    # If bold_delta provided, place as bold separate piece (attempt)
    if bold_delta:
        ax.text(text_xy[0] + 0.0005, text_xy[1]-0.18, bold_delta, fontsize=14, va='top', ha='left', fontweight='bold', color=axis_text_color, zorder=8)

# 2004 annotation (Spain surplus)
idx_2004 = np.where(years == 2004)[0][0]
x_2004 = pos_spain[idx_2004]
y_2004 = spain[idx_2004]
draw_circle_callout(ax, x_2004, y_2004, "Spain +0.6% (3.5 pp better than EZ)", text_xy=(x_2004-1.2, y_2004+1.8), circle_radius=0.55, circle_color="#9B2E1D", icon="▲")

# 2006 annotation (strong surplus)
idx_2006 = np.where(years == 2006)[0][0]
x_2006 = pos_spain[idx_2006]
y_2006 = spain[idx_2006]
# small callout above bar with upward arrow
ax.annotate("Spain 2.4% vs EZ 1.1% (+1.3 pp)  ▲",
            xy=(x_2006, y_2006), xytext=(x_2006+0.6, y_2006+2.2),
            fontsize=14, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#DDDDDD"),
            arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=-0.15", color="#9B2E1D", linewidth=1.2),
            zorder=7)

# 2009 extreme deficit annotation
idx_2009 = np.where(years == 2009)[0][0]
x_2009 = pos_spain[idx_2009]
y_2009 = spain[idx_2009]
draw_circle_callout(ax, x_2009, y_2009, "Spain −11.2; EZ −6.3 → Spain −4.9 pp worse", text_xy=(x_2009+0.8, y_2009-3.0), circle_radius=0.9, circle_color="#8B1C1C", icon="▼")
# Bold the numeric delta separately (placed nearby)
ax.text(x_2009+2.0, y_2009-3.0+0.02, "−4.9 pp", fontsize=14, fontweight='bold', color=axis_text_color)

# Banded annotation above the shaded band
band_mid_x = (band_left + band_right) / 2.0
ax.text(band_mid_x, ymax - 0.5, "Crisis years — deep deficits (peak 2009)  ⚠", fontsize=15, ha='center', va='top', bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#DDDDDD"))

# 2014 concluding annotation
idx_2014 = np.where(years == 2014)[0][0]
x_2014 = pos_spain[idx_2014]
y_2014 = spain[idx_2014]
ax.annotate("Partial recovery but still near EZ average",
            xy=(x_2014, y_2014), xytext=(x_2014-2.4, y_2014+2.2),
            fontsize=14, ha='left', va='center',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#DDDDDD"),
            arrowprops=dict(arrowstyle="-", connectionstyle="arc3,rad=0.2", color="#666666", linewidth=1.0),
            zorder=7)

# Adjust tick and spine colors
for spine in ["top","right","left","bottom"]:
    ax.spines[spine].set_color("#CCCCCC")
ax.spines['left'].set_color("#666666")
ax.spines['bottom'].set_color("#CCCCCC")

# Make sure legend entries are large and readable
for text in legend.get_texts():
    text.set_fontsize(17)

# Tight layout with extra top and right margin for summary/legend
plt.subplots_adjust(top=0.92, right=0.88, left=0.08)

# Show
plt.savefig("generated/spain_factor3_bar8/spain_factor3_bar8_design.png", dpi=300, bbox_inches="tight")