import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle, Circle
import numpy as np

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain_vals = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Euro-zone has NA for last 3 years
ez_vals = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Styling parameters (colors and fonts)
bg_color = "#FAFBFC"
spain_color = "#B22234"      # deep red
ez_color = "#2E6DA4"         # muted steel blue
accent_color = "#D4A017"     # warm gold for callouts
placeholder_gray = "#BFBFBF" # for NA placeholders

plt.rcParams.update({
    "figure.facecolor": bg_color,
    "axes.facecolor": bg_color,
    "savefig.facecolor": bg_color,
    "font.family": "DejaVu Sans",
})

# Figure: portrait, 6x8 inches (900x1200 px at 150 dpi)
fig, ax = plt.subplots(figsize=(6,8), dpi=150)
fig.subplots_adjust(top=0.88, left=0.10, right=0.96, bottom=0.12)

# X positions for grouped bars
n = len(years)
ind = np.arange(n)
width = 0.35

# Plot actual Euro-zone bars only where data exists
ez_mask = ~np.isnan(ez_vals)
ax.bar(ind[ez_mask] - width/2, ez_vals[ez_mask], width=width,
       color=ez_color, edgecolor='none', label='Euro‑Zone average', zorder=2)

# Plot Spain bars (all years). For target years (2012-2014) use hatched, semi-transparent bars
target_mask = years >= 2012
# Actual Spain bars
for i in range(n):
    x = ind[i] + width/2
    h = spain_vals[i]
    if target_mask[i]:
        # hatched to indicate target & semi-transparent
        ax.bar(x, h, width=width, color=spain_color, edgecolor=spain_color,
               alpha=0.6, hatch='///', zorder=3)
    else:
        ax.bar(x, h, width=width, color=spain_color, edgecolor='none', zorder=3)

# Euro-zone placeholder dashed rectangles for NA years (2012-2014)
# Draw a light dashed rectangle where a bar would be (height aligned to Spain target for position only)
for i in range(n):
    if np.isnan(ez_vals[i]):
        # draw dashed hollow rectangle matching where an EZ bar would be
        x = ind[i] - width/2
        # use the Spain bar height at that year as a reference for where the top should be (visual placeholder)
        ref_h = spain_vals[i]
        # rectangle y from 0 down/up to ref_h (handles negative or positive ref_h)
        y0 = min(0, ref_h)
        height = abs(ref_h - 0)
        rect = Rectangle((x - 0.005, y0), width=width - 0.01, height=height,
                         linewidth=1.2, edgecolor=placeholder_gray, facecolor='none',
                         linestyle='--', zorder=1)
        ax.add_patch(rect)
        # small "no data" circle-dash icon above or near the placeholder
        cx = x + (width/2)
        cy = y0 + height/2
        icon = Circle((x + width*0.1, y0 + (0.02 if ref_h >= 0 else -0.02)), radius=0.07,
                      edgecolor=placeholder_gray, facecolor='none', linewidth=1.2, zorder=6, transform=ax.get_xaxis_transform())
        # Because transform is axis transform, it's not ideal; instead place a tiny circle in data coords near top
        icon = Circle((x + width*0.08, y0 + height*0.05), radius=0.18, edgecolor=placeholder_gray,
                      facecolor='none', linewidth=1.2, zorder=6)
        ax.add_patch(icon)
        # small dash inside circle
        ax.plot([x + width*0.0, x + width*0.16], [y0 + height*0.05, y0 + height*0.05], color=placeholder_gray, linewidth=1.2, zorder=7)

# Axes limits and grid
ax.set_ylim(-12.5, 3.0)
ax.set_xlim(-0.6, n - 0.4)
ax.yaxis.set_ticks(np.arange(-12, 4, 2))
ax.grid(axis='y', linestyle='--', linewidth=0.7, color='#DDDDDD', zorder=0)
ax.set_axisbelow(True)

# X-axis labels: every year
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=14, rotation=90)
ax.tick_params(axis='y', labelsize=14)

# Title and subtitle
ax_title = "Spain vs Euro‑Zone: Budget Balance (% of GDP), 1999–2014"
ax_sub = "Final 3 years are Spain targets"

fig.suptitle(ax_title, fontsize=34, fontweight='bold', y=0.96)
ax.annotate(ax_sub, xy=(0.5, 0.92), xycoords='figure fraction',
            fontsize=15, ha='center')

# Contextual annotation block (top-left under title)
context_text = "Data are % of GDP. 2012–2014 Euro‑zone average unavailable; Spain values are government targets (2012–2014)."
ax.text(0.02, 0.87, context_text, transform=fig.transFigure, fontsize=16, ha='left', va='top')

# Legend (compact, upper-left)
# Custom legend handles to reflect hatch/placeholder
spain_patch = mpatches.Patch(facecolor=spain_color, edgecolor=spain_color, label='Spain', alpha=1.0)
spain_target_patch = mpatches.Patch(facecolor=spain_color, edgecolor=spain_color, label='Spain (target)', hatch='///', alpha=0.6)
ez_patch = mpatches.Patch(facecolor=ez_color, edgecolor=ez_color, label='Euro‑Zone average')
ez_na_patch = mpatches.Patch(facecolor='none', edgecolor=placeholder_gray, linestyle='--', label='Euro‑Zone (data unavailable)')
legend = ax.legend(handles=[spain_patch, spain_target_patch, ez_patch, ez_na_patch],
                   loc='upper left', bbox_to_anchor=(0.01, 1.03), fontsize=16, frameon=False)

# Small government logo (monochrome rectangle) top-right
logo_w = 0.055
logo_h = 0.035
logo_x = 0.92
logo_y = 0.95
# Axes for logo using figure coordinates
fig.patches.append(Rectangle((logo_x, logo_y - logo_h), logo_w, logo_h, transform=fig.transFigure,
                             facecolor='#444444', edgecolor='none', alpha=0.85, zorder=10))
fig.text(logo_x + logo_w + 0.005, logo_y - logo_h/2, "Source: Government Agency", transform=fig.transFigure,
         fontsize=12, va='center', color='#333333')

# Selected years for annotations and highlights
highlight_years = [2005, 2006, 2007, 2009, 2010, 2011, 2012, 2013, 2014]
# Create small circles around selected paired bars and add connector lines and numeric labels
for y in highlight_years:
    idx = int(np.where(years == y)[0][0])
    # center between the two bars for that year
    x_spain = ind[idx] + width/2
    x_ez = ind[idx] - width/2
    sp_val = spain_vals[idx]
    ez_val = ez_vals[idx]
    # circle center roughly centered on the pair, slightly above the higher of the two bars to avoid covering bars
    top_y = max(sp_val if not np.isnan(sp_val) else -12, ez_val if not np.isnan(ez_val) else -12)
    circle_center_x = ind[idx]
    circle_center_y = top_y + 0.9  # offset above the bar tops
    circle_radius_x = width * 1.2
    circle_radius_y = 1.4
    # Use ellipse-like circle via Circle scaled might distort; keep as Circle with modest radius
    circ = Circle((circle_center_x, circle_center_y), radius=0.9, edgecolor=accent_color,
                  facecolor=accent_color, linewidth=1.5, alpha=0.12, zorder=4)
    ax.add_patch(circ)
    # Connector line from annotation text to the circle (thin, subtle)
    # Place annotation text near top-left for earlier years, top-right for later years to avoid overlap
    if y in [2005,2006,2007]:
        text_x = circle_center_x - 0.8
        ha = 'right'
    else:
        text_x = circle_center_x + 0.8
        ha = 'left'
    text_y = circle_center_y + 0.5
    # Compose annotation strings for specific years
    if y in [2005,2006,2007]:
        # Combined short annotation
        if y == 2006:
            diff = sp_val - ez_val
            ann = f"Spain surplus vs EZ deficit\nΔ = {diff:.1f} pp ({y})"
        else:
            ann = "Spain surplus vs EZ deficit"
    elif y == 2009:
        ann = f"Crisis peak: Spain {sp_val:.1f}% vs EZ {ez_val:.1f}%"
    elif y in [2010,2011]:
        ann = f"{y}: Spain {sp_val:.1f}% vs EZ {ez_val:.1f}%"
    else:  # target years 2012-2014
        ann = "Target"
    # Draw connector line
    ax.annotate("", xy=(circle_center_x, circle_center_y - 0.6), xytext=(text_x, text_y),
                arrowprops=dict(arrowstyle='-', color='#777777', linewidth=1.0, connectionstyle="arc3,rad=0.2"),
                zorder=5)
    # Add annotation text (multi-line where needed)
    ax.text(text_x, text_y + 0.02, ann, fontsize=16, ha=ha, va='bottom', color='#333333', zorder=6)
    # Numeric labels: add Spain and EZ numeric labels near their bars for these highlighted years
    # Spain label
    ax.text(x_spain, sp_val + (0.18 if sp_val >= 0 else -0.6), f"Spain {sp_val:+.1f}%", fontsize=13, ha='center', va='bottom' if sp_val >=0 else 'top', color=spain_color, fontweight='bold', zorder=7)
    # Euro-zone label if present
    if not np.isnan(ez_val):
        ax.text(x_ez, ez_val + (0.18 if ez_val >= 0 else -0.6), f"EZ {ez_val:+.1f}%", fontsize=13, ha='center', va='bottom' if ez_val >=0 else 'top', color=ez_color, fontweight='bold', zorder=7)
    else:
        # mark data unavailable label near placeholder bar
        ax.text(x_ez, (sp_val*0.35), "data unavailable", fontsize=11, ha='center', va='center', color=placeholder_gray, rotation=90, zorder=7)

    # Draw arrow between paired bars to show magnitude/direction if both exist
    if not np.isnan(ez_val):
        # arrow from EZ bar top to Spain bar top
        start_y = ez_val
        end_y = sp_val
        # small offset horizontally to draw arrow between bars
        arr_x = ind[idx]
        # draw arrow with accent color, semi-transparent
        ax.annotate("", xy=(arr_x + 0.15, end_y), xytext=(arr_x - 0.15, start_y),
                    arrowprops=dict(arrowstyle='->,head_length=6,head_width=4', color=accent_color, linewidth=1.4, alpha=0.9),
                    zorder=6)
        # also add a small comparison label at mid-point
        mid_y = (start_y + end_y)/2
        diff_pp = sp_val - ez_val
        ax.text(arr_x + 0.22, mid_y, f"{diff_pp:+.1f} pp", fontsize=12, color=accent_color, zorder=8)

# Footnote / source line bottom-left
footnote = "Source: Government Agency. Data = % of GDP. Euro‑Zone averages missing 2012–2014."
fig.text(0.01, 0.02, footnote, fontsize=12, ha='left', va='bottom', color='#333333')

# Axis label for Y
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18)
ax.yaxis.set_label_coords(-0.07, 0.5)

# Remove top and right spines for a cleaner look
for spine in ['top','right']:
    ax.spines[spine].set_visible(False)
# Make left and bottom spines subtle
ax.spines['left'].set_color('#444444')
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_color('#444444')
ax.spines['bottom'].set_linewidth(0.8)

# Tight layout adjustments and show
plt.savefig("generated/spain_factor3_bar1/spain_factor3_bar1_design.png", dpi=300, bbox_inches="tight")