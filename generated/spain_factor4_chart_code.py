"""
Chart: Spain vs Euro‑Zone Average: Budget Balance, 1999–2014
Design follows provided specification: dual-series line chart with selective labels,
difference ribbon (green when Spain > EZ, red when Spain < EZ), inline end-of-line labels,
targeted annotations, reduced grid/tick clutter, and a prominent title.

This script requires: matplotlib, numpy. It checks for and installs them if missing.
Run as a standalone Python script or in a notebook cell.
"""

# --- checks / install (if needed) ---
import importlib
import subprocess
import sys

def ensure_package(pkg):
    try:
        importlib.import_module(pkg)
    except Exception:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_package("matplotlib")
ensure_package("numpy")

# --- plotting code ---
import numpy as np
import matplotlib.pyplot as plt

# Robust style selection: try to use seaborn-white if available, otherwise fall back gracefully
preferred_styles = ['seaborn-white', 'seaborn-whitegrid', 'seaborn', 'default']
for s in preferred_styles:
    if s in plt.style.available:
        plt.style.use(s)
        break

# Data (from the provided JSON-like input)
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Compute differences and identify points for labeling/markers/annotations
diff = spain - ez
# label years where |diff| >= 2.0 OR the specified special years (2006 largest Spain value, 2009 deepest trough)
label_mask = (np.abs(diff) >= 2.0)
special_years = {2006, 2009}
for i, y in enumerate(years):
    if y in special_years:
        label_mask[i] = True

# Colors (colorblind-safe-ish)
color_spain = "#084c8f"            # saturated dark blue for Spain (primary)
color_ez = "#6c7a89"               # muted gray/teal for Euro-Zone
ribbon_pos = "#7FB77E"             # greenish when Spain > EZ
ribbon_neg = "#E88B8B"             # reddish when Spain < EZ
zero_line_color = "#666666"        # neutral gray

# Plot setup
fig, ax = plt.subplots(figsize=(11, 5.5))

# Difference ribbon (only when absolute diff >= 0.3, per spec skip very small differences)
min_ribbon_threshold = 0.3
mask_pos = (spain > ez) & (np.abs(diff) >= min_ribbon_threshold)
mask_neg = (spain < ez) & (np.abs(diff) >= min_ribbon_threshold)

# fill_between with where to color only segments meeting criteria; interpolate=True smooths edges at boundaries
ax.fill_between(years, spain, ez, where=mask_pos, interpolate=True, color=ribbon_pos, alpha=0.22, linewidth=0)
ax.fill_between(years, spain, ez, where=mask_neg, interpolate=True, color=ribbon_neg, alpha=0.22, linewidth=0)

# Plot lines
ax.plot(years, ez, color=color_ez, linewidth=1.8, zorder=2)                     # euro-zone average (muted)
ax.plot(years, spain, color=color_spain, linewidth=2.8, zorder=3)               # spain (bolder)

# Markers only on labeled points
marker_indices = np.where(label_mask)[0]
ax.scatter(years[marker_indices], spain[marker_indices], s=36, color=color_spain, edgecolor='white', linewidth=0.6, zorder=4)

# Selective numeric labels near Spain points for labeled years
for idx in marker_indices:
    x = years[idx]
    y = spain[idx]
    d = diff[idx]
    # Format difference as signed one-decimal
    diff_text = f"{d:+.1f} pp"
    # Compose label text: Spain value and difference vs EZ
    label_text = f"Spain {y:.1f} ({d:+.1f} pp vs EZ)"
    # Position label slightly above or below depending on sign to avoid overlap
    offset_y = 0.6 if y >= 0 else -0.9
    # For extremely negative values, place label below further
    if y < -8:
        offset_y = -1.3
    ax.text(x, y + offset_y, label_text, fontsize=9, color=color_spain, ha='center',
            va='bottom' if offset_y>0 else 'top',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color_spain, lw=0.6, alpha=0.9), zorder=6)

# Annotations / callouts with arrows
# 2006: Spain surplus +2.4 vs EZ +1.1 (Spain ahead).
i2006 = int(np.where(years == 2006)[0][0])
ax.annotate("2006: Spain ahead\n2.4% vs 1.1%", xy=(2006, spain[i2006]), xytext=(2006+0.6, spain[i2006]+2.1),
            fontsize=9, color=color_spain, weight='bold',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color_spain, lw=0.8),
            arrowprops=dict(arrowstyle="->", color=color_spain, linewidth=0.9), zorder=7)

# 2009: crisis gap (prominent)
i2009 = int(np.where(years == 2009)[0][0])
ax.annotate("2009 crisis gap\nSpain −11.2% vs EZ −6.3%", xy=(2009, spain[i2009]), xytext=(2009-3.0, spain[i2009]-1.4),
            fontsize=9, color=color_spain, weight='bold',
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=ribbon_neg, lw=0.9),
            arrowprops=dict(arrowstyle="->", color=ribbon_neg, linewidth=0.9), zorder=8)

# 2014: return to smaller deficit (compact)
i2014 = int(np.where(years == 2014)[0][0])
ax.annotate("2014: Return to smaller\ndeficits (−2.5% vs −2.0%)", xy=(2014, spain[i2014]), xytext=(2014-2.6, spain[i2014]+1.6),
            fontsize=9, color=color_spain,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color_spain, lw=0.6),
            arrowprops=dict(arrowstyle="->", color=color_spain, linewidth=0.9), zorder=7)

# End-of-line inline labels (no boxed legend)
# Place labels just to the right of the final datapoint (2014); Spain label emphasized (bolder)
x_last = years[-1]
# Slight horizontal offset for placing labels outside the plotting area slightly
x_offset = 0.45
ax.text(x_last + x_offset, spain[-1], "Spain", color=color_spain, fontsize=11, fontweight='bold', va='center', zorder=10, clip_on=False)
ax.text(x_last + x_offset, ez[-1], "Euro‑Zone Avg", color=color_ez, fontsize=10, va='center', zorder=10, clip_on=False)

# Optionally add a small numeric difference in parentheses next to Spain label if space permits
overall_diff = spain[-1] - ez[-1]
diff_label = f"({overall_diff:+.1f} pp)"
ax.text(x_last + x_offset + 0.85, spain[-1], diff_label, color=color_spain, fontsize=9, va='center', clip_on=False)

# Axes and grid styling
ax.set_xlim(years[0]-0.5, years[-1]+1.6)  # give room for inline labels
ymin = -12.5
ymax = 3.5
ax.set_ylim(ymin, ymax)

# Thin horizontal gridlines only at multiples of 5: -10, -5, 0, 5
ax.set_yticks([-10, -5, 0, 5])
ax.yaxis.grid(True, which='major', linestyle='-', linewidth=0.6, color='#e7e7e7')
ax.xaxis.grid(False)

# Thin zero reference line (slightly emphasized)
ax.axhline(0, color=zero_line_color, linewidth=1.0, zorder=1)

# Axis labels (concise) with small unobtrusive font
ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("% of GDP", fontsize=10)

# Title & short subtitle (single-line title emphasized; short clarifier)
ax.set_title("Spain vs Euro‑Zone Average: Budget Balance, 1999–2014", fontsize=14, fontweight='bold', pad=12)
# Short subtitle (kept brief per spec)
fig.text(0.01, 0.935, "Differences highlighted", fontsize=10, color="#444444")

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Reduce tick label size and remove minor ticks
ax.tick_params(axis='both', which='major', labelsize=9)
ax.minorticks_off()

# Source note at bottom-right, small font
plt.annotate("Source: Provided dataset (1999–2014)", xy=(1.0, 0.01), xycoords='figure fraction',
             fontsize=8, ha='right', color='#555555')

# Tight layout and show
plt.tight_layout()
plt.savefig("generated/spain_factor4_design.png", dpi=300, bbox_inches="tight")

# Optionally save to file (uncomment to save)
# fig.savefig("spain_vs_eurozone_budget_1999_2014.png", dpi=300, bbox_inches='tight')