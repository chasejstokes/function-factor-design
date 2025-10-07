import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D
import numpy as np
import matplotlib as mpl

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2,-0.6,-0.4,-1.0,-0.8,0.6,1.3,2.4,1.9,-4.5,-11.2,-9.5,-7.8,-4.2,-5.0,-2.5])
euro = np.array([-0.9,-0.4,-0.8,-1.6,-2.6,-2.9,-1.8,1.1,-0.8,-3.6,-6.3,-6.0,-4.1,-4.6,-3.8,-2.0])
diff = spain - euro  # Spain minus Euro-Zone

# Styling colors
spain_color = "#8B1E1E"       # deep Rioja red
spain_edge = "#5F1212"
euro_color = "#17325B"        # muted navy
euro_edge = "#0f2439"
amber = "#D9822B"             # highlight amber
warm_gray = "#777777"
bg_color = "white"

# Matplotlib rc settings for a clean, government-branded look
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
    "figure.dpi": 100,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "axes.titlelocation": "center"
})

# Figure and axis
fig = plt.figure(figsize=(14, 7), facecolor=bg_color)
ax = fig.add_axes([0.07, 0.14, 0.86, 0.78], facecolor=bg_color)  # generous left/right margins

x = np.arange(len(years))
bar_w = 0.35

# Plot bars
bars_spain = ax.bar(x - bar_w/2, spain, width=bar_w, color=spain_color, edgecolor=spain_edge, linewidth=1.2,
                    label="Spain", zorder=3, hatch=None)
# subtle hatch accessibility fallback (commented out visually subtle)
# for b in bars_spain:
#     b.set_hatch('//')
bars_euro = ax.bar(x + bar_w/2, euro, width=bar_w, color=euro_color, edgecolor=euro_edge, linewidth=1.2,
                   label="Euro‑Zone average", zorder=3)

# Y-axis limits and gridlines (only at specified positions)
ax.set_ylim(-12.5, 4.5)
grid_y = [-12, -8, -4, 0, 4]
for gy in grid_y:
    ax.axhline(gy, color="#e6e6e6", linewidth=0.9 if gy != 0 else 1.4, zorder=0)
# Emphasize zero line
ax.axhline(0, color="#bdbdbd", linewidth=1.4, zorder=2)

# X-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=9, color=warm_gray)
ax.tick_params(axis='x', which='both', length=0)

# Y-axis labels
ax.set_ylabel("Percent of GDP", fontsize=11, color=warm_gray)
ax.set_yticks(grid_y)
ax.set_yticklabels([f"{y}%" for y in grid_y], fontsize=10, color=warm_gray)

# Title and subtitle
title_text = "Spain vs Euro‑Zone: Budget deficit and surplus (1999–2014)"
subtitle_text = "Percent of GDP — annual"
ax.set_title(title_text, fontsize=16, fontweight='bold', pad=18)
ax.text(0.5, 0.935, subtitle_text, transform=fig.transFigure, ha='center', fontsize=10, color=warm_gray)

# Legend (compact) and small flag icons drawn as inset axes
legend_handles = [
    mpatches.Patch(color=spain_color, label='Spain', edgecolor=spain_edge),
    mpatches.Patch(color=euro_color, label='Euro‑Zone average', edgecolor=euro_edge)
]
leg = ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(0.98, 0.98),
                frameon=False, fontsize=9)
# mini flags as tiny inset axes near legend (top-right)
# Spain flag: horizontal stripes red-yellow-red
ax_flag_sp = fig.add_axes([0.78, 0.86, 0.04, 0.03])
ax_flag_sp.add_patch(Rectangle((0, 0.66), 1, 0.34, color="#C8102E"))
ax_flag_sp.add_patch(Rectangle((0, 0.33), 1, 0.33, color="#FFD400"))
ax_flag_sp.add_patch(Rectangle((0, 0.0), 1, 0.33, color="#C8102E"))
ax_flag_sp.set_xticks([]); ax_flag_sp.set_yticks([])
ax_flag_sp.set_frame_on(False)

# EU flag: blue with circle of small yellow dots
ax_flag_eu = fig.add_axes([0.86, 0.86, 0.04, 0.03])
ax_flag_eu.add_patch(Rectangle((0, 0), 1, 1, color="#003399"))
# approximate circle of stars with small dots
theta = np.linspace(0, 2*np.pi, 12, endpoint=False)
r = 0.32
cx, cy = 0.5, 0.5
for t in theta:
    ax_flag_eu.add_patch(Circle((cx + r*np.cos(t), cy + r*np.sin(t)), 0.035, color="#FFCC00"))
ax_flag_eu.set_xticks([]); ax_flag_eu.set_yticks([])
ax_flag_eu.set_frame_on(False)

# Annotations for selected years: 2009 (largest Spain shortfall), 2004 (Spain outperformance), and 2011 (post-crisis gap)
annotations = [
    {
        "year": 2009,
        "text": "Spain −11.2% (vs EZ −6.3%) = −4.9 pp",
        "idx": int(np.where(years == 2009)[0][0]),
        "xytext": (-80, -30),
        "align": "left"
    },
    {
        "year": 2004,
        "text": "Spain +0.6% vs EZ −2.9% = +3.5 pp",
        "idx": int(np.where(years == 2004)[0][0]),
        "xytext": (-10, 35),
        "align": "center"
    },
    {
        "year": 2011,
        "text": "Post‑crisis gap remains: −3.7 pp",
        "idx": int(np.where(years == 2011)[0][0]),
        "xytext": (40, 10),
        "align": "left"
    }
]

for ann in annotations:
    i = ann["idx"]
    # coordinates of Spain bar top (end)
    xbar = x[i] - bar_w/2
    ybar = spain[i]
    # Circular halo around the Spain bar tip (use Ellipse to better encircle tall bars)
    if ybar < 0:
        # center at bar tip
        circ = Ellipse((xbar, ybar), width=0.9, height=2.2, edgecolor=amber, facecolor='none',
                       linewidth=2.0, zorder=5)
    else:
        circ = Ellipse((xbar, ybar), width=0.9, height=1.2, edgecolor=amber, facecolor='none',
                       linewidth=2.0, zorder=5)
    ax.add_patch(circ)
    # Connector line from halo to annotation text
    # place text relative to figure in display coords
    ann_x_disp, ann_y_disp = ax.transData.transform((xbar, ybar))
    # target text position in data coords (offset)
    text_offset = ann["xytext"]
    # Convert display offset to data coordinates for the endpoint of the arrow
    inv = ax.transData.inverted()
    text_point_data = inv.transform((ann_x_disp + text_offset[0], ann_y_disp + text_offset[1]))
    # curved arrow
    arrow = FancyArrowPatch((xbar, ybar), (text_point_data[0], text_point_data[1]),
                            connectionstyle="arc3,rad=0.18", arrowstyle="-", linewidth=1.0,
                            color=warm_gray, zorder=4)
    ax.add_patch(arrow)
    # small circle terminator at bar
    term = Circle((xbar, ybar), 0.055, color=amber, zorder=6, alpha=0.9)
    ax.add_patch(term)
    # add annotation text in a bbox
    ax.text(text_point_data[0], text_point_data[1], ann["text"], fontsize=9, color=warm_gray,
            ha='left' if ann["align"] == "left" else 'center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#e6e6e6", linewidth=0.7),
            zorder=7)

# Optionally label bars with numeric values when |value| > 5%
for i, val in enumerate(spain):
    if abs(val) > 5:
        ax.text(x[i] - bar_w/2, val + (0.4 if val > 0 else -0.6), f"{val:.1f}%", ha='center', va='bottom' if val>0 else 'top',
                fontsize=9, fontweight='bold', color=spain_color, zorder=6)
for i, val in enumerate(euro):
    if abs(val) > 5:
        ax.text(x[i] + bar_w/2, val + (0.4 if val > 0 else -0.6), f"{val:.1f}%", ha='center', va='bottom' if val>0 else 'top',
                fontsize=9, fontweight='bold', color=euro_color, zorder=6)

# Inset sparkline (bottom-right) for Spain - Euro difference
ax_in = fig.add_axes([0.68, 0.12, 0.25, 0.16], facecolor='white')
ax_in.plot(years, diff, color=amber, linewidth=1.6, zorder=6)
ax_in.scatter(years, diff, color=amber, s=18, zorder=7)
ax_in.axhline(0, color="#e0e0e0", linewidth=0.7)
ax_in.set_xlim(years.min()-0.5, years.max()+0.5)
ax_in.set_xticks([2000,2005,2010,2014])
ax_in.set_xticklabels([2000,2005,2010,2014], fontsize=8, color=warm_gray)
ax_in.set_yticks([])
ax_in.set_title("Spain − Euro‑Zone (pp)", fontsize=9, color=warm_gray, pad=6)
# highlight extremes with small markers
imax = np.argmax(diff)
imin = np.argmin(diff)
ax_in.scatter(years[imax], diff[imax], color='#005B9A', s=35, edgecolor='white', zorder=8)
ax_in.scatter(years[imin], diff[imin], color='#8B1E1E', s=35, edgecolor='white', zorder=8)

# Summary panel (bottom-left) with 2–3 bullet-like one-line statements
summary_text = [
    "• Largest Spain deficit: 2009, −11.2% (vs EZ −6.3% → −4.9 pp)",
    "• Spain outperformed EZ most in 2004: +0.6% vs −2.9% (+3.5 pp)",
    "• Post‑2008: persistent Spain deficit gap through 2011"
]
summary_box = FancyBboxPatch((0.07, 0.06), 0.43, 0.07, boxstyle="round,pad=0.02", transform=fig.transFigure,
                             facecolor="#fbfbfb", edgecolor="#e6e6e6", linewidth=0.8, zorder=9)
fig.patches.append(summary_box)  # add background box
# place text inside
for i, line in enumerate(summary_text):
    fig.text(0.09, 0.125 - i*0.023, line, fontsize=9, color=warm_gray)

# Source/metadata strip (bottom-right) with small government logo
# draw small 'logo' rectangle and source text
logo_ax = fig.add_axes([0.86, 0.06, 0.06, 0.045], facecolor='none')
logo_ax.add_patch(Rectangle((0.02, 0.12), 0.96, 0.76, color="#0b4f6c", ec="#073241", lw=0.8))
logo_ax.text(0.5, 0.5, "GOV", color="white", ha="center", va="center", fontsize=9, fontweight='bold')
logo_ax.axis('off')

source_line = "Source: Government Agency, Fiscal accounts; measure: general government balance (% of GDP). Coverage: 1999–2014. Last update: 2015"
fig.text(0.74, 0.07, source_line, fontsize=8, color=warm_gray)

# Contextual single-line caption under the chart
context = "Context: Spain’s post‑2008 fiscal shock widened its deficit relative to the Euro‑Zone average, peaking in 2009."
fig.text(0.5, 0.05, context, ha='center', fontsize=9, color=warm_gray)

# Tighten layout and show
plt.box(False)
plt.savefig("generated/spain_factor3_bar1_design.png", dpi=300, bbox_inches="tight")