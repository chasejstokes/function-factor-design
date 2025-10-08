import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib as mpl
import numpy as np

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Compute summary statistics
diff = spain - ez
largest_gap_idx = np.argmax(np.abs(diff))
largest_gap_year = years[largest_gap_idx]
largest_gap_val = diff[largest_gap_idx]
surplus_years = years[spain > 0]
surplus_range_text = "2004–2007" if (surplus_years.size and np.array_equal(surplus_years, np.array([2004,2005,2006,2007]))) else ", ".join(map(str, surplus_years))
spain_avg = spain.mean()
ez_avg = ez.mean()

# Figure sizing: 900 x 1200 px at 300 dpi -> figsize in inches = (3,4) with dpi=300
dpi = 300
fig_w_px, fig_h_px = 900, 1200
fig = plt.figure(figsize=(fig_w_px/dpi, fig_h_px/dpi), dpi=dpi)
ax = fig.add_subplot(1,1,1)

# Global style
mpl.rcParams['font.family'] = 'DejaVu Sans'
TITLE_FS = 34
SUBTITLE_FS = 17
AXIS_LABEL_FS = 19
TICK_FS = 15
LEGEND_FS = 15
ANNOT_FS = 15
SUMMARY_FS = 15
SOURCE_FS = 12

# Colors (polished palette)
color_spain = "#C4472C"      # saturated warm (deep red/orange)
color_ez = "#6C9AA0"         # desaturated teal/blue-gray
bg_color = "#fbfbfb"         # very light gray background for axes
figure_bg = "#f7f7f7"        # off-white figure background
grid_color = "#e6e6e6"       # light gridlines

fig.patch.set_facecolor(figure_bg)
ax.set_facecolor(bg_color)

# X positions for grouped bars
x = np.arange(len(years))
bar_width = 0.32  # narrow bars
offset = bar_width / 2

# Draw bars
bars_spain = ax.bar(x - offset, spain, width=bar_width, color=color_spain, align='center', zorder=3, label='Spain', edgecolor='none')
bars_ez = ax.bar(x + offset, ez, width=bar_width, color=color_ez, align='center', zorder=3, label='Euro‑Zone average', edgecolor='none')

# Axes formatting
ax.set_xlim(-0.8, len(years)-0.2)
ax.set_xticks(x)
ax.set_xticklabels(years.astype(str), fontsize=TICK_FS, fontweight='bold')
ax.set_ylim(-12, 3)
ax.set_yticks([-12, -10, -8, -6, -4, -2, 0, 2])
ax.set_yticklabels(['-12', '-10', '-8', '-6', '-4', '-2', '0', '2'], fontsize=TICK_FS)
ax.set_ylabel('General government balance (% of GDP)', fontsize=AXIS_LABEL_FS)
ax.yaxis.set_label_coords(-0.06, 0.5)

# Gridlines (horizontal at major ticks)
ax.yaxis.grid(True, color=grid_color, linewidth=0.8, zorder=0)
ax.xaxis.grid(False)

# Emphasize zero baseline
ax.axhline(0, color='#4d4d4d', linewidth=2.2, zorder=4)

# Legend top-right
legend_handles = [
    mpatches.Patch(color=color_spain, label='Spain'),
    mpatches.Patch(color=color_ez, label='Euro‑Zone average')
]
leg = ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(0.98, 0.98), fontsize=LEGEND_FS, frameon=False)

# Title and subtitle
fig.suptitle("Budget deficit and surplus: Spain vs Euro‑Zone average (1999–2014)",
             fontsize=TITLE_FS, fontweight='bold', y=0.975)
ax_title_y = 0.94  # coordinate under the suptitle for subtitle
fig.text(0.5, 0.942, "Year-by-year paired comparison of general government balance (% of GDP)",
         ha='center', fontsize=SUBTITLE_FS)

# Small government icon near title (left of title area) - monochrome simulated via text
fig.text(0.055, 0.98, "🏛", fontsize=18, va='top')

# Source line with logo (lower-left)
# Simulated logo: small filled crest rectangle
logo_ax = fig.add_axes([0.03, 0.03, 0.06, 0.06], anchor='SW')
logo_ax.add_patch(mpatches.FancyBboxPatch((0.15, 0.15), 0.7, 0.7,
                                         boxstyle="round,pad=0.02", color='#2a4a5a'))
logo_ax.axis('off')
fig.text(0.105, 0.055, "Source: National Government / Eurostat (compiled), Years: 1999–2014",
         fontsize=SOURCE_FS, va='center')

# Summary box top-right, below legend
summary_text = (
    f"Largest Spain–EZ gap: {largest_gap_year} ({abs(largest_gap_val):.1f} pp)\n"
    f"Spain years with surplus: {surplus_range_text} (4 years)\n"
    f"Period avg (1999–2014): Spain {spain_avg:.1f}% | EZ {ez_avg:.1f}% (approx.)"
)
summary_box = dict(boxstyle="round,pad=0.6", facecolor='white', edgecolor='#d9d9d9')
fig.text(0.725, 0.90, summary_text, fontsize=SUMMARY_FS, va='top', ha='left', bbox=summary_box)

# Context sentence near the source
fig.text(0.105, 0.03, "Context: Figures are general government balance, % of GDP. Crisis years (2008–2011) show large deterioration across the euro area; Spain’s decline was steeper.",
         fontsize=12, va='bottom')

# Annotated focal years and callouts (use exact copy/paste texts provided)
annotations = {
    2006: {
        "text": "Spain +2.4% | EZ +1.1% — Spain outperforms",
        "xytext": (0.0, 30),  # offset in points
        "xycoords": ("data", "data"),
        "textcoords": "offset points",
        "arrowprops": dict(arrowstyle="-", color='#888888', lw=0.8)
    },
    2009: {
        "text": "Spain −11.2% | EZ −6.3% — largest gap: −4.9 pp",
        "xytext": (10, 45),
        "xycoords": ("data", "data"),
        "textcoords": "offset points",
        "arrowprops": dict(arrowstyle="-", color='#777777', lw=0.8)
    },
    2010: {
        "text": "Spain −9.5% | EZ −6.0%",
        "xytext": (-80, 40),
        "xycoords": ("data", "data"),
        "textcoords": "offset points",
        "arrowprops": dict(arrowstyle="-", color='#777777', lw=0.8)
    },
    2014: {
        "text": "2014: Spain −2.5% | EZ −2.0% — convergence",
        "xytext": (-60, 30),
        "xycoords": ("data", "data"),
        "textcoords": "offset points",
        "arrowprops": dict(arrowstyle="-", color='#777777', lw=0.8)
    }
}

# Helper to convert year -> index
year_to_idx = {int(y): i for i, y in enumerate(years)}

# Draw circular highlights (subtle outlines) around the tops of bars for annotated years (both series)
for yv, props in annotations.items():
    idx = year_to_idx[yv]
    # Spain bar top
    sx = x[idx] - offset
    sy = spain[idx]
    # Euro zone bar top
    ex = x[idx] + offset
    ey = ez[idx]
    # Circle radius: relative to axis units; small
    # We'll convert a small radius in axis coordinates using transform
    circle_radius = 0.18  # in data units (y-axis)
    # Spain circle
    circ_sp = mpatches.Circle((sx, sy), radius=0.28, fill=False, edgecolor=color_spain, linewidth=1.6, alpha=0.9, zorder=6)
    ax.add_patch(circ_sp)
    # EZ circle
    circ_ez = mpatches.Circle((ex, ey), radius=0.28, fill=False, edgecolor=color_ez, linewidth=1.2, alpha=0.9, zorder=6)
    ax.add_patch(circ_ez)
    # Placement of annotation text: anchor near Spain circle with connector
    # Determine a good text placement depending on sign to avoid overlap
    text_offset = props['xytext']
    # Annotate with an anchored text and a subtle rounded bbox behind it
    ann_xy = (sx, sy)
    bbox = dict(boxstyle="round,pad=0.5", fc="white", ec="#e0e0e0", alpha=0.92)
    ax.annotate(props['text'],
                xy=ann_xy,
                xytext=text_offset,
                textcoords=props['textcoords'],
                fontsize=ANNOT_FS,
                fontweight='bold',
                va='center',
                ha='left' if text_offset[0] >= 0 else 'right',
                bbox=bbox,
                arrowprops=props['arrowprops'],
                zorder=8)

# Remove top and right spines, thin left and bottom
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(0.9)
ax.spines['bottom'].set_linewidth(0.9)

# Tight layout adjustments
plt.subplots_adjust(left=0.11, right=0.95, top=0.92, bottom=0.08)

# Save output at requested dimensions/dpi
output_filename = "spain_euro_zone_budget_1999_2014.png"
plt.savefig(output_filename, dpi=dpi, bbox_inches='tight', facecolor=fig.get_facecolor())

# Show figure
plt.savefig("generated/spain_factor3_bar6/spain_factor3_bar6_design.png", dpi=300, bbox_inches="tight")