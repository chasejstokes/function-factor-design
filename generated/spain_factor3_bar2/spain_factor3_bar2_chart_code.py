# Ensure required libraries are installed and importable
import sys
import subprocess

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines
    from matplotlib import rcParams
    import numpy as np
except Exception:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.lines as mlines
    from matplotlib import rcParams
    import numpy as np

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Euro-zone has NA for 2012-2014
euro = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Styling parameters
spain_color = "#c1272d"        # muted Spain red
euro_color = "#2a6f9e"         # EU blue
placeholder_gray = "#bdbdbd"   # for NA placeholders
bg_offwhite = "#fbfbfb"
grid_color = "#e6e6e6"
text_color = "#111111"

# Font sizes
title_fs = 30
subtitle_fs = 14
axis_label_fs = 17
tick_fs = 15
annotation_fs = 15
footnote_fs = 12
legend_fs = 15
data_label_fs = 15

# Build x positions with extra spacing every 4 years
base_gap = 1.0
extra_gap = 0.4
x_centers = []
current_x = 0.0
for i in range(len(years)):
    x_centers.append(current_x)
    current_x += base_gap
    if (i + 1) % 4 == 0:
        current_x += extra_gap
x_centers = np.array(x_centers)

# Bar positions (paired bars around each center)
bar_width = 0.35
pair_offset = bar_width / 1.8

spain_x = x_centers - pair_offset
euro_x = x_centers + pair_offset

# Figure setup (portrait, tall) - aspect ratio at least 3:4 (taller than wide)
fig, ax = plt.subplots(figsize=(9, 12))
fig.patch.set_facecolor(bg_offwhite)
ax.set_facecolor(bg_offwhite)

# Y limits determined from data with margin
ymin = min(np.nanmin(euro[np.isfinite(euro)]), spain.min()) - 2
ymax = max(np.nanmax(euro[np.isfinite(euro)]), spain.max()) + 2
ax.set_ylim(ymin, ymax)

# Subtle shading above/below zero
ax.axhspan(0, ymax, facecolor="#f6fff6", alpha=0.08, zorder=0)
ax.axhspan(ymin, 0, facecolor="#fff6f6", alpha=0.05, zorder=0)

# Thicker zero baseline
ax.axhline(0, color="#222222", linewidth=2.2, zorder=5)

# Gridlines
ax.yaxis.grid(True, color=grid_color, linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# Plot Spain bars (including target hatch for 2012-2014)
targets_mask = (years >= 2012)
spain_bars = []
for xi, val, is_target in zip(spain_x, spain, targets_mask):
    if is_target:
        b = ax.bar(xi, val, width=bar_width, color=spain_color, edgecolor="#7a0006",
                   linewidth=1.0, zorder=6, hatch='////', alpha=0.65)
    else:
        b = ax.bar(xi, val, width=bar_width, color=spain_color, edgecolor="#7a0006",
                   linewidth=1.0, zorder=6)
    spain_bars.append(b[0])

# Plot Euro-zone bars; where NA, draw faded placeholder rectangle and "NA" label
euro_bars = []
for xi, val, yr in zip(euro_x, euro, years):
    if np.isnan(val):
        # Draw a faint placeholder box at zero-level to indicate missing/NA
        placeholder_height = (ymax - ymin) * 0.03  # small visual indicator
        rect = mpatches.Rectangle((xi - bar_width/2, 0),
                                  bar_width, placeholder_height,
                                  facecolor=placeholder_gray, alpha=0.25,
                                  edgecolor=None, zorder=4)
        ax.add_patch(rect)
        euro_bars.append(None)
        # NA text just above the x-axis tick
        ax.text(xi, placeholder_height + 0.3, "NA", ha="center", va="bottom",
                fontsize=tick_fs-1, color="#4a4a4a", fontweight='bold')
    else:
        b = ax.bar(xi, val, width=bar_width, color=euro_color, edgecolor="#123b53",
                   linewidth=0.8, zorder=5)
        euro_bars.append(b[0])

# X-axis: ticks are centered on pairs (x_centers)
ax.set_xticks(x_centers)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=tick_fs, rotation=0, color=text_color)
ax.set_xlim(x_centers[0] - 0.9, x_centers[-1] + 0.9)

# Y-axis label
ax.set_ylabel("Budget balance (% of GDP)", fontsize=axis_label_fs, color=text_color, labelpad=12)

# Title and subtitle (subtitle short)
plt_title = "Spain vs. Euro‑Zone: Budget surplus/deficit (% of GDP), 1999–2014"
plt_sub = "Focus: differences between Spain and the Euro‑zone average"
fig.suptitle(plt_title, fontsize=title_fs, fontweight='bold', y=0.96, color=text_color)
ax.set_title(plt_sub, fontsize=subtitle_fs, loc='center', pad=8, color=text_color)

# Legend top-right inside plot area with large symbols
# Create custom legend handles
spain_handle = mpatches.Patch(facecolor=spain_color, edgecolor="#7a0006", label="Spain")
euro_handle = mpatches.Patch(facecolor=euro_color, edgecolor="#123b53", label="Euro‑zone avg")
target_handle = mpatches.Patch(facecolor=spain_color, edgecolor="#7a0006", hatch='////', alpha=0.7, label="Spain targets (2012–2014)")
na_handle = mpatches.Patch(facecolor=placeholder_gray, alpha=0.25, label="Euro‑zone NA")
legend = ax.legend(handles=[spain_handle, euro_handle, target_handle, na_handle],
                   fontsize=legend_fs, frameon=False, loc='upper right', bbox_to_anchor=(1.02, 0.98))
for text in legend.get_texts():
    text.set_color(text_color)

# Selective data labels and annotations for key years
annot_years = [2005, 2006, 2007, 2009]  # plus the 2012-2014 targets group
annot_indices = [int(np.where(years == y)[0]) for y in annot_years]
for idx in annot_indices:
    # Spain label
    sx = spain_x[idx]
    sy = spain[idx]
    ax.text(sx, sy + (0.6 if sy >= 0 else -0.6), f"{sy:+.1f}%", ha='center',
            va='bottom' if sy >= 0 else 'top', fontsize=data_label_fs, fontweight='bold', color=text_color, zorder=10)
    # Euro label if exists
    if not np.isnan(euro[idx]):
        ex = euro_x[idx]
        ey = euro[idx]
        ax.text(ex, ey + (0.6 if ey >= 0 else -0.6), f"{ey:+.1f}%", ha='center',
                va='bottom' if ey >= 0 else 'top', fontsize=data_label_fs, fontweight='bold', color=text_color, zorder=10)
    # Difference annotation: Δ = spain - euro
    if not np.isnan(euro[idx]):
        diff = spain[idx] - euro[idx]
        # Place annotation to the right of the pair with a connector
        ann_x = x_centers[idx] + 0.7
        ann_y = max(sy, (ey if not np.isnan(euro[idx]) else sy)) + 1.2
        arrowprops = dict(arrowstyle="-", color="#666666", linewidth=0.8)
        ax.annotate(f"Δ = {diff:+.1f} pp", xy=(x_centers[idx], ann_y - 0.2),
                    xytext=(ann_x, ann_y), fontsize=annotation_fs, color=text_color,
                    ha='left', va='center', arrowprops=arrowprops)
    # Small circle around Spain bar
    circ = mpatches.Circle((sx, sy), radius=0.35, fill=False, edgecolor="#444444", linewidth=1.2, zorder=11)
    ax.add_patch(circ)
    # Small icon: up or down arrow
    icon = "↑" if spain[idx] > 0 else "↓"
    icon_color = "#2a8a2a" if spain[idx] > 0 else "#b22222"
    # compute ann_y in case it wasn't set (for safety)
    try:
        _ann_y = ann_y
    except NameError:
        _ann_y = sy + 1.0
    ax.text(x_centers[idx] + 0.7, _ann_y + 0.5, f"{icon}", color=icon_color, fontsize=14)

# Annotation and highlight for 2012-2014 target bars
target_idxs = [int(np.where(years == y)[0]) for y in [2012,2013,2014]]
# Group annotation box
group_x = np.mean(x_centers[target_idxs])
group_y = spain[target_idxs].max() + 2.2
ax.text(group_x + 0.6, group_y+0.2, "Government targets\n(not actuals)", fontsize=annotation_fs,
        ha='left', va='center', color=text_color, fontweight='normal')
# Connector line from text to middle target bars area
ax.annotate("", xy=(group_x+0.1, group_y - 0.2), xytext=(group_x+0.9, group_y+0.6),
            arrowprops=dict(arrowstyle="-", color="#888888", linewidth=0.9))

# Add circle highlights around each target Spain bar
for idx in target_idxs:
    sx = spain_x[idx]
    sy = spain[idx]
    circ = mpatches.Circle((sx, sy), radius=0.4, fill=False, edgecolor="#444444", linewidth=1.0, zorder=11, linestyle='-')
    ax.add_patch(circ)
    # add numeric labels for these targets above bars
    ax.text(sx, sy + 0.6, f"{sy:+.1f}%", ha='center', va='bottom', fontsize=data_label_fs, fontweight='bold')

# Additional specific annotations for 2005 and 2009 with short phrases and numeric comparisons
# 2005
i2005 = int(np.where(years == 2005)[0])
diff2005 = spain[i2005] - euro[i2005]
ax.annotate(f"Spain +1.3% vs EZ −2.4%\n→ Spain ahead by {diff2005:.1f} pp",
            xy=(spain_x[i2005], spain[i2005]), xytext=(spain_x[i2005]-1.1, spain[i2005]+3.2),
            fontsize=annotation_fs, ha='left', va='center',
            arrowprops=dict(arrowstyle="->", color="#666666", linewidth=0.9), bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#dddddd", alpha=0.9))
# 2009
i2009 = int(np.where(years == 2009)[0])
diff2009 = spain[i2009] - euro[i2009]
ax.annotate(f"Spain −11.2% vs EZ −6.3%\n→ Spain deficit larger by {diff2009:.1f} pp",
            xy=(spain_x[i2009], spain[i2009]), xytext=(spain_x[i2009]+0.4, spain[i2009]-6.0),
            fontsize=annotation_fs, ha='left', va='center',
            arrowprops=dict(arrowstyle="->", color="#666666", linewidth=0.9), bbox=dict(boxstyle="round,pad=0.3", fc="#ffffff", ec="#dddddd", alpha=0.95))

# Footer: source left and small logo repeat bottom-right
fig.text(0.02, 0.02, "Source: [Government Agency], Fiscal Accounts. 2012–2014 are Spain’s government targets; euro‑zone averages not available for these years (NA).",
         fontsize=footnote_fs, ha='left', va='bottom', color="#333333")
# Simple small logo mock in bottom-right (subtle)
fig.text(0.98, 0.02, "GOV", fontsize=12, ha='right', va='bottom', color="#444444", fontweight='bold',
         bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor="#dddddd", alpha=0.9))

# Accessibility caption (in slide notes area represented below plot in small italic)
fig.text(0.5, 0.005, "Caption: Spain posted surpluses in 2005–2007 while the Euro‑zone averaged deficits; Spain experienced a much larger deficit in 2009. 2012–2014 are government targets.",
         fontsize=11, ha='center', va='bottom', color="#222222", style='italic')

# Tidy up axes spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color("#666666")
ax.spines['bottom'].set_color("#666666")
ax.tick_params(axis='y', colors="#333333")

# Adjust layout to respect the tall figure and title space
plt.subplots_adjust(top=0.90, bottom=0.06, left=0.08, right=0.95)

plt.savefig("generated/spain_factor3_bar2/spain_factor3_bar2_design.png", dpi=300, bbox_inches="tight")