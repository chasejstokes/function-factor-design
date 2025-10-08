import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.ticker import FuncFormatter

# Data setup (from the provided dataset)
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Use np.nan for Euro-zone missing values
euro = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Styling constants
color_spain = "#1f77b4"        # medium-dark saturated blue
color_euro = "#6c7b7f"         # muted steel gray/teal
accent_color = "#ff8c42"       # muted orange for emphasis
bg_color = "white"

# Figure canvas (900x1200 px -> 9x12 inches at 100 dpi)
plt.rcParams.update({
    "figure.facecolor": bg_color,
    "axes.facecolor": "white",
    "font.family": "DejaVu Sans",
})
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
fig.subplots_adjust(top=0.88, left=0.18, right=0.88, bottom=0.12)

# Bar layout
n = len(years)
x = np.arange(n)
bar_width = 0.35
gap_between_groups = 0.2  # visual spacing between year groups (implicit via x spacing)

# Plot Euro bars (only where data is not NA)
valid_euro_mask = ~np.isnan(euro)
euro_positions = x[valid_euro_mask] + bar_width / 2
ax.bar(euro_positions, euro[valid_euro_mask], width=bar_width,
       color=color_euro, label="Euro‑Zone average", zorder=2)

# Plot Spain bars (actuals and targets separately)
# Determine indices for target years (final three: 2012-2014)
target_years_mask = (years >= 2012)
actual_years_mask = ~target_years_mask

spain_pos_actual = x[actual_years_mask] - bar_width / 2
spain_pos_target = x[target_years_mask] - bar_width / 2

# Actual Spain bars (solid)
ax.bar(spain_pos_actual, spain[actual_years_mask], width=bar_width,
       color=color_spain, label="Spain (actual)", zorder=3, edgecolor="none")

# Target Spain bars (render with opacity + hatch to denote planned)
# Use hatch and alpha; draw bars with edgecolor slightly darker
ax.bar(spain_pos_target, spain[target_years_mask], width=bar_width,
       color=color_spain, alpha=0.5, hatch='///', zorder=3,
       edgecolor=color_spain, linewidth=1.0, label="Spain (planned target)")

# For Euro-zone NA years: add faint vertical hatch background and small centered text
group_width = bar_width * 2 + 0.12  # span approx width of a grouped slot
for idx in np.where(np.isnan(euro))[0]:
    left = x[idx] - group_width / 2
    rect = patches.Rectangle(
        (left, -12.5), group_width, 15.5,  # cover the y-range visually (-12.5 to ~3)
        linewidth=0, facecolor="#f2f2f2", alpha=0.6, hatch='...', zorder=1
    )
    ax.add_patch(rect)
    # small note centered in the slot
    ax.text(x[idx], 0.8, "Euro‑Zone\nunavailable", ha="center", va="center",
            fontsize=10, color="#444444", zorder=6)

# Zero baseline emphasized
ax.axhline(0, color="#4d4d4d", linewidth=1.6, zorder=4)

# Horizontal gridlines (subtle)
ymin, ymax = -12, 3
ax.set_ylim(ymin, ymax)
ax.set_yticks(np.arange(-12, 4, 2.5))
ax.yaxis.grid(True, which='major', color="#e6e6e6", linestyle='-', linewidth=0.8, zorder=0)

# X-axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels(years.astype(int), fontsize=12)
ax.tick_params(axis='x', which='both', length=0)

# Y-axis label (vertical, large)
ax.set_ylabel("Government balance (% of GDP)", fontsize=16, fontweight='bold', labelpad=18)
ax.tick_params(axis='y', labelsize=13)

# Format y-tick labels to include percent sign, using one decimal only where needed
def pct_formatter(x_val, pos):
    # Show integer where possible, one decimal for values like -11.2
    if abs(x_val - round(x_val)) < 0.05:
        return f"{int(round(x_val))}%"
    else:
        return f"{x_val:.1f}%"

ax.yaxis.set_major_formatter(FuncFormatter(pct_formatter))

# Title and subtitle
title_text = "Spain vs Euro‑Zone: Budget deficit/surplus, 1999–2014"
subtitle_text = ("Paired bars show government balance as % of GDP. Final three years (2012–2014) are Spain’s planned targets; "
                 "Euro‑Zone averages unavailable for those years. Spain moved from mid‑2000s surpluses to a sharp post‑2007 deterioration.")
fig.suptitle(title_text, fontsize=30, fontweight='bold', y=0.96)
ax_title = fig.text(0.18, 0.915, subtitle_text, fontsize=18, wrap=True)

# Legend: top-right under subtitle
# Create custom legend entries to reflect styling
legend_handles = []
legend_handles.append(patches.Patch(facecolor=color_spain, edgecolor="none", label="Spain (actual)"))
legend_handles.append(patches.Patch(facecolor=color_spain, edgecolor=color_spain, hatch='///', alpha=0.5, label="Spain (planned target)"))
legend_handles.append(patches.Patch(facecolor=color_euro, label="Euro‑Zone average"))
leg = ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.0, 1.08),
                fontsize=14, frameon=False)

# Selective numeric annotations (callouts) for chosen years
def annotate_bar(xcoord, height, text, ax, offset=0.6, fontsize=13, boxprops=None):
    if boxprops is None:
        boxprops = dict(boxstyle="round,pad=0.3", fc="white", ec="#999999", lw=0.8)
    ax.text(xcoord, height + offset if height >= 0 else height - offset, text,
            ha='center', va='bottom' if height >= 0 else 'top',
            fontsize=fontsize, bbox=boxprops, zorder=10)

# 2005-2007 summary callout: place near 2006 above bars
annotate_bar(x[6] - bar_width/2, spain[6], "Spain recorded small surpluses\n(2005–07) while Euro‑Zone averaged deficits\n— notable outperformance.",
             ax, offset=1.2, fontsize=13,
             boxprops=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", lw=0.8))

# 2009 highlighted callout with accent border (largest gap)
gap_2009 = spain[10] - euro[10]  # negative gap; 2009 index = 10
callout_text_2009 = "2009: Largest measured gap\nSpain −11.2% vs EZ −6.3% → gap ≈ −4.9 pp"
ax.text(x[10] + 0.6, -5.5, callout_text_2009, fontsize=14,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=accent_color, lw=1.6),
        zorder=11, ha='left')

# 2010-2011 callout (sustained deficits)
annotate_bar(x[11] - bar_width/2, spain[11], "2010–2011: Sustained large deficits in Spain\nrelative to EZ average.",
             ax, offset=1.0, fontsize=13,
             boxprops=dict(boxstyle="round,pad=0.35", fc="white", ec="#999999", lw=0.8))

# Numeric labels for selected bars to aid accessibility and comparisons:
# Label Spain 2005, 2006, 2007, 2009, 2010, 2011 and both series for 2009
selected_spain_years = [2005, 2006, 2007, 2009, 2010, 2011]
for yr in selected_spain_years:
    idx = np.where(years == yr)[0][0]
    xpos = x[idx] - bar_width / 2
    ypos = spain[idx]
    ax.text(xpos, ypos + (0.6 if ypos >= 0 else -0.6),
            f"{ypos:.1f}%", ha='center',
            va='bottom' if ypos >= 0 else 'top',
            fontsize=12, fontweight='bold', color="#222222", zorder=12)

# Also annotate Euro and Spain numeric values in 2009 for explicit comparison
ax.text(x[10] + bar_width/2, euro[10] - 0.6, f"{euro[10]:.1f}%", ha='center', va='top',
        fontsize=12, color="#222222", zorder=12)
ax.text(x[10] - bar_width/2, spain[10] - 0.6, f"{spain[10]:.1f}%", ha='center', va='top',
        fontsize=12, color="#222222", zorder=12)

# Add small asterisk markers under x-ticks for target years and explanatory note in footnote
for idx in np.where(target_years_mask)[0]:
    ax.text(x[idx], -13.5, "*", ha='center', fontsize=14, fontweight='bold')

# Footnote / small caption (bottom-left)
footnote = ("* Euro‑Zone series unavailable (NA) 2012–2014. Spain 2012–2014 are government targets. Values are % of GDP.")
fig.text(0.02, 0.02, footnote, fontsize=11, ha='left', va='bottom')

# Small centered "synthesis" box near upper-right below subtitle
synthesis_text = ("Key takeaways —\n"
                  "Peak Spain deficit: −11.2% (2009).\n"
                  "Peak gap vs EZ: ~−4.9 pp (2009).\n"
                  "Spain had surpluses 2005–07; EU avg negative.")
fig.text(0.60, 0.83, synthesis_text, fontsize=13, ha='left', va='top',
         bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#9a9a9a", lw=1.0))

# Accessibility: ensure elements are above grid
for child in ax.get_children():
    if isinstance(child, patches.Rectangle):
        child.set_zorder(1)

# Minor visual tweaks
ax.set_axisbelow(True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Ensure layout fits and show
plt.savefig("generated/spain_factor4_bar3/spain_factor4_bar3_design.png", dpi=300, bbox_inches="tight")