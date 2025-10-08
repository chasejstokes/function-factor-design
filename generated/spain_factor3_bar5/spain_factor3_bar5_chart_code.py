import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.lines import Line2D

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Use np.nan to represent missing euro-zone averages for 2012-2014
euro = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Identify target years (Spain 2012-2014)
target_years = {2012, 2013, 2014}
target_idx = [i for i, y in enumerate(years) if y in target_years]

# Figure setup: portrait at least 3:4 (width x height in inches)
fig_w, fig_h = 9, 12  # 900 x 1200 px at dpi=100
fig = plt.figure(figsize=(fig_w, fig_h), dpi=100)
fig.patch.set_facecolor('#f7f7f5')  # very light neutral background

# Axes and panel styling
ax = fig.add_axes([0.08, 0.12, 0.88, 0.80])  # left, bottom, width, height
ax.set_facecolor('#fcfcfb')  # plotting panel off-white
# thin border around plotting panel
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('#bfbfbf')
    spine.set_linewidth(0.8)

# Bar positions
n = len(years)
ind = np.arange(n)
width = 0.38  # width for each bar in a pair
offset = width / 2.0

# Colors and styling
spain_color = '#C62828'  # deep Iberian red
ez_color = '#4A90A4'     # muted blue-gray
shadow_color = '#000000'
target_hatch = '////'

# Draw subtle drop-shadows behind bars (decorative)
shadow_offset = 0.03
for i in range(n):
    # Spain shadow
    x = ind[i] - offset + shadow_offset
    h = spain[i]
    if not np.isnan(h):
        ax.bar(x, h, width=width, color=(0,0,0,0.06), align='center', zorder=1)
    # Euro shadow (only if available)
    ez_h = euro[i]
    xez = ind[i] + offset + shadow_offset
    if not np.isnan(ez_h):
        ax.bar(xez, ez_h, width=width, color=(0,0,0,0.06), align='center', zorder=1)

# Plot Spain bars; for target years use hatched/transparent fill
bars_spain = []
for i in range(n):
    x = ind[i] - offset
    h = spain[i]
    if years[i] in target_years:
        b = ax.bar(x, h, width=width, color=spain_color, alpha=0.65,
                   edgecolor='#8b1f1f', linewidth=1.0, hatch=target_hatch, zorder=3)
    else:
        b = ax.bar(x, h, width=width, color=spain_color, edgecolor='#8b1f1f',
                   linewidth=0.8, zorder=4)
    bars_spain.append(b[0])

# Plot Euro-Zone bars only where data exists
bars_ez = []
for i in range(n):
    x = ind[i] + offset
    h = euro[i]
    if not np.isnan(h):
        b = ax.bar(x, h, width=width, color=ez_color, edgecolor='#396e75',
                   linewidth=0.8, zorder=4)
        bars_ez.append(b[0])
    else:
        bars_ez.append(None)

# Emphasized zero line
ax.axhline(0, color='#333333', linewidth=2.2, zorder=5)

# Gridlines: light horizontal only
ymin = -12.5
ymax = 4.0
ax.set_ylim(ymin, ymax)
# choose ticks every 2.5
yticks = np.arange(-12.5, ymax + 0.1, 2.5)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t:.1f}" if (t % 5 != 0) else f"{int(t)}" for t in yticks],
                   fontsize=14)
ax.grid(axis='y', color='#e9e9e9', linewidth=0.9, zorder=0)
ax.set_axisbelow(True)

# X-axis ticks and labels
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=16, rotation=0)
# Axis labels
ax.set_ylabel("Budget balance (% of GDP)", fontsize=20, labelpad=12)

# Title and subtitle
ax_title = "Budget balance: Spain vs Euro‑Zone average (1999–2014)"
plt.suptitle(ax_title, x=0.08, y=0.975, ha='left', fontsize=32, weight='bold', color='#222222')
subtitle = "Final three years are Spain’s official targets (not actual outcomes)."
plt.title(subtitle, fontsize=18, loc='left', y=1.015)

# Legend (top-right)
# Custom legend handles: Spain (with small flag-like badge) and Euro-Zone (with euro symbol)
flag_patch = patches.Rectangle((0, 0), 1, 1, facecolor=spain_color, edgecolor='#8b1f1f')
ez_patch = patches.Rectangle((0, 0), 1, 1, facecolor=ez_color, edgecolor='#396e75')
legend_elements = [
    (flag_patch, "Spain"),
    (ez_patch, "Euro‑Zone average")
]
# Create legend manually positioned
legend_handles = [patch for patch, label in legend_elements]
legend_labels = [label for patch, label in legend_elements]
leg = ax.legend(legend_handles, legend_labels, fontsize=16, frameon=False,
                loc='upper right', bbox_to_anchor=(0.995, 0.98))
# Add tiny icons next to legend labels (a small yellow stripe for Spain and '€' for EZ)
# Note: placing small text annotations near legend entries
trans = ax.transAxes
# approximate positions using bbox of legend
renderer = fig.canvas.get_renderer()
legbox = leg.get_window_extent(renderer=renderer).transformed(fig.transFigure.inverted())
# Compute text positions relative to axes coordinate
# We'll draw small decorations directly near the legend text objects
for text in leg.get_texts():
    txt = text.get_text()
    bbox = text.get_window_extent(renderer=renderer)
    inv = fig.transFigure.inverted()
    bbox_fig = bbox.transformed(inv)
    # convert fig coords to ax coords
    ax_coords = ax.transAxes.inverted().transform(fig.transFigure.transform(bbox_fig.p0))
    x0, y0 = ax_coords
    # minor offset to position a tiny decoration
    if txt == "Spain":
        # small yellow stripe atop red for a flag feel
        ax.add_patch(patches.Rectangle((bbox_fig.x0 + 0.0035, bbox_fig.y0 + 0.005),
                                       0.018, 0.012, transform=fig.transFigure,
                                       facecolor='#C62828', edgecolor='none', zorder=10))
        ax.add_patch(patches.Rectangle((bbox_fig.x0 + 0.0035, bbox_fig.y0 + 0.01),
                                       0.018, 0.005, transform=fig.transFigure,
                                       facecolor='#FFC107', edgecolor='none', zorder=11))
    else:
        # euro symbol text
        fig.text(bbox_fig.x0 + 0.0035, bbox_fig.y0 + 0.007, "€", fontsize=12, color='#ffffff',
                 bbox=dict(boxstyle="square,pad=0.1", facecolor=ez_color, edgecolor='none'), zorder=11)

# Data value labels and difference labels (show for key years: 2006, 2009, 2011)
highlight_years = [2006, 2009, 2011]
for y in highlight_years:
    i = int(np.where(years == y)[0])
    # Spain value label
    sx = ind[i] - offset
    sy = spain[i]
    ax.text(sx, sy + (0.6 if sy >= 0 else -0.8), f"{sy:+.1f}%", ha='center', va='bottom' if sy >= 0 else 'top',
            fontsize=15, weight='bold', color='#222222', zorder=8)
    # Euro value label if available
    ez_val = euro[i]
    if not np.isnan(ez_val):
        ex = ind[i] + offset
        ey = ez_val
        ax.text(ex, ey + (0.6 if ey >= 0 else -0.8), f"{ey:+.1f}%", ha='center', va='bottom' if ey >= 0 else 'top',
                fontsize=14, color='#222222', zorder=8)
        # difference label
        diff = spain[i] - ez_val
        dx = ind[i]
        dy = max(sy, ey) + 1.1
        ax.text(dx, dy, f"Δ = {diff:+.1f} pp", ha='center', fontsize=14, color='#444444', zorder=9,
                bbox=dict(boxstyle="round,pad=0.3", fc=(1.0, 1.0, 1.0, 0.85), ec='#cfcfcf', lw=0.6))
        # dotted connector between bars
        ax.plot([sx + width/2.0, ex - width/2.0], [sy, ey], linestyle=':', color='#666666', linewidth=1.1, zorder=6)
    else:
        # For missing EZ, mark difference as not available
        dx = ind[i]
        ax.text(dx, spain[i] + 1.1, f"Δ = n.a.", ha='center', fontsize=14, color='#666666', zorder=9,
                bbox=dict(boxstyle="round,pad=0.3", fc=(1.0, 1.0, 1.0, 0.85), ec='#e0e0e0', lw=0.6))

# Hollow circles on annotated bar tops and connector arrows with short callouts
annot_specs = {
    2006: dict(text="Spain +2.4 pp (2006) vs EZ −1.3 pp", xytext=(60, 50)),
    2009: dict(text="2009: Spain −11.2% vs EZ −6.3% → Spain −4.9 pp larger deficit", xytext=(0, -100)),
    2010: dict(text="Crisis years: Spain persistently worse than EZ average (2008–2011)", xytext=(0, -160))
}
for year_key, spec in annot_specs.items():
    if year_key not in years:
        continue
    i = int(np.where(years == year_key)[0])
    sx = ind[i] - offset
    sy = spain[i]
    # circle marker at the top of Spain bar
    ax.scatter(sx, sy, s=90, facecolors='none', edgecolors='#222222', linewidths=1.2, zorder=9)
    # arrow to annotation box; adjust positions
    if year_key == 2006:
        text_xy = (sx + 0.8, sy + 3.2)
        ax.annotate("Spain +2.4 pp (2006) vs EZ −1.3 pp",
                    xy=(sx, sy), xytext=text_xy,
                    fontsize=16, weight='normal',
                    bbox=dict(boxstyle="round,pad=0.4", fc=(1,1,1,0.9), ec='#cfcfcf', lw=0.8),
                    arrowprops=dict(arrowstyle="->", color='#888888', linewidth=1.0),
                    zorder=12)
    elif year_key == 2009:
        text_xy = (ind[i] + 1.0, sy - 2.8)
        ax.annotate("2009: Spain −11.2% vs EZ −6.3% → Spain −4.9 pp",
                    xy=(sx, sy), xytext=text_xy,
                    fontsize=16, weight='normal',
                    bbox=dict(boxstyle="round,pad=0.4", fc=(1,1,1,0.9), ec='#cfcfcf', lw=0.8),
                    arrowprops=dict(arrowstyle="->", color='#888888', linewidth=1.0),
                    zorder=12)
    elif year_key == 2010:
        # Center summary box for crisis period (covering 2008-2011)
        # Place box centrally above the middle of 2009-2010
        mid_index = int(np.where(years == 2009)[0])
        x_mid = ind[mid_index]
        ax.annotate("Crisis years: Spain persistently worse than EZ average (2008–2011)",
                    xy=(x_mid, -6.3), xytext=(x_mid + 2.0, -3.8),
                    fontsize=16, weight='normal',
                    bbox=dict(boxstyle="round,pad=0.6", fc=(1,1,1,0.92), ec='#cfcfcf', lw=0.8),
                    arrowprops=dict(arrowstyle="-", color='#888888', linewidth=0.9),
                    zorder=11)

# Add small hollow circle markers for missing Euro-Zone years with dashed connector to baseline
for i in range(n):
    if np.isnan(euro[i]):
        # place the hollow circle slightly above zero baseline
        x = ind[i] + offset
        y_marker = 1.2  # just above axis for visibility
        ax.scatter(x, y_marker, s=70, facecolors='none', edgecolors='#bdbdbd', linewidths=1.2, zorder=9)
        # dashed connector from marker down to x-axis tick
        ax.plot([x, x - 0.0], [y_marker - 0.4, 0], linestyle='--', color='#bdbdbd', linewidth=1.0, zorder=7)
        # tiny 'no data' label rotated slightly
        ax.text(x, y_marker + 0.5, "No data", ha='center', va='bottom', fontsize=12, color='#7a7a7a', zorder=9)

# Inline 'target' labels for Spain 2012-2014 bars
for i in target_idx:
    sx = ind[i] - offset
    sy = spain[i]
    ax.text(sx, sy + (0.6 if sy >= 0 else -0.8), f"{sy:+.1f}% (target)",
            ha='center', va='bottom' if sy >= 0 else 'top', fontsize=13, color='#2b2b2b', zorder=10)
    # small flag-like icon next to label (simple triangle)
    ax.plot([sx + 0.25], [sy + 0.6 if sy >= 0 else sy - 0.8], marker='^', color=spain_color, markersize=6, zorder=11)

# Values for many bars are omitted to avoid clutter; optionally show small labels for Euro and Spain for a subset
# For visual clarity, add small tick lines and reduce clutter on x-axis
for label in ax.get_xticklabels():
    label.set_fontsize(16)

# Footnote/source and government logo
footnote_text = ("Source: [Agency name], official statistics. "
                 "Spain 2012–2014 are government targets; Euro‑Zone averages not reported for 2012–2014.")
fig.text(0.02, 0.035, footnote_text, fontsize=12, ha='left', va='center', color='#333333')

# Simple government logo: small square with "GOV"
logo_x = 0.95
logo_y = 0.03
logo_size_fig = 0.04  # fraction of figure
fig.text(logo_x - 0.015, logo_y, "", fontsize=10)  # spacer
# Draw a small rectangle and text as a faux logo
fig.patches.append(patches.Rectangle((logo_x - 0.02, logo_y - 0.005), 0.035, 0.035,
                                    transform=fig.transFigure, facecolor='#1f4e79', edgecolor='#0e2a46', zorder=20))
fig.text(logo_x - 0.004, logo_y + 0.02, "GOV", fontsize=10, color='white', weight='bold', ha='center', va='center', zorder=21, transform=fig.transFigure)

# Annotate the panel with a light decorative thin shadow below the axes (subtle)
# (Add a faint rectangle slightly offset behind ax)
shadow_rect = patches.Rectangle((ax.get_position().x0 + 0.005, ax.get_position().y0 - 0.005),
                                ax.get_position().width, ax.get_position().height,
                                transform=fig.transFigure, facecolor=(0,0,0,0.02), edgecolor='none', zorder=0)
fig.patches.insert(0, shadow_rect)

# Tight layout adjustments and show
plt.subplots_adjust(top=0.92, bottom=0.10, left=0.08, right=0.92)
plt.savefig("generated/spain_factor3_bar5/spain_factor3_bar5_design.png", dpi=300, bbox_inches="tight")