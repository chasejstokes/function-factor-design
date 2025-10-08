import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Data setup
years = np.array(list(range(1999, 2015)))
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
euro = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan])

# Identify target years (2012-2014)
target_mask = (years >= 2012)

# Colors (colorblind-friendly)
color_spain = "#b22222"   # deep red (Spain)
color_euro = "#1f77b4"    # mid blue (Euro-Zone)
placeholder_edge = "#bfbfbf"

# Figure: portrait orientation (900x1200 px equivalent)
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)
plt.subplots_adjust(top=0.87, bottom=0.19, left=0.1, right=0.95)

# Bar positions and width
n = len(years)
ind = np.arange(n)
group_width = 0.7
bar_width = group_width / 2.0  # two bars per group

# Plot Euro-Zone bars where data exists
euro_mask = ~np.isnan(euro)
ax.bar(ind[euro_mask] - bar_width/2, euro[euro_mask], width=bar_width,
       color=color_euro, edgecolor=color_euro, label="Euro‑Zone average", zorder=2)

# For Euro-Zone NA years, draw a faint open outline placeholder centered at zero
na_indices = ind[np.isnan(euro)]
for xi in na_indices:
    # Small neutral placeholder (thin outline centered around 0)
    rect = mpatches.Rectangle((xi - bar_width/2, -0.5), bar_width, 1.0,
                              fill=False, edgecolor=placeholder_edge, linewidth=1.0, linestyle='--', zorder=1)
    ax.add_patch(rect)

# Plot Spain bars: solid for actuals, hatched/semi-transparent for targets
# Actuals (non-target years)
actual_mask = ~target_mask
ax.bar(ind[actual_mask] + bar_width/2, spain[actual_mask], width=bar_width,
       color=color_spain, edgecolor=color_spain, label="Spain (actual)", zorder=3)

# Targets (2012-2014): hatched, semi-transparent fill
ax.bar(ind[target_mask] + bar_width/2, spain[target_mask], width=bar_width,
       color=color_spain, edgecolor=color_spain, alpha=0.6, hatch='////', label="Spain (target)", zorder=3)

# Subtle vertical shading for target period (2012-2014)
start_shade = np.where(years == 2012)[0][0] - 0.5
end_shade = np.where(years == 2014)[0][0] + 0.5
ax.axvspan(start_shade, end_shade, color='gray', alpha=0.06, zorder=0)

# Optional subtle contextual highlight for crisis years 2008-2011
start_crisis = np.where(years == 2008)[0][0] - 0.5
end_crisis = np.where(years == 2011)[0][0] + 0.5
ax.axvspan(start_crisis, end_crisis, color='gray', alpha=0.03, zorder=0)

# Zero line emphasized
ax.axhline(0, color='black', linewidth=1.2, zorder=4)

# Gridlines
ax.yaxis.grid(True, which='major', color='#dddddd', linewidth=0.8, zorder=0)
ax.set_axisbelow(True)

# X-axis ticks and labels (one per year)
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=14)
# keep x labels horizontal (0°)
for label in ax.get_xticklabels():
    label.set_rotation(0)

# Y-axis label and ticks
ax.set_ylabel("Percent of GDP", fontsize=16)
ymin, ymax = -13, 3
ax.set_ylim(ymin, ymax)
yticks = np.arange(-12.5, 3.1, 2.5)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{t:g}" for t in yticks], fontsize=14)

# Title and subtitle (top center)
title = "Spain’s Budget: Deficits and Surpluses vs. Euro‑Zone Average, 1999–2014"
subtitle = ("Annual government balance (% of GDP). Final three years (2012–2014) are Spain’s stated targets, not outturns.")
fig.suptitle(title, fontsize=34, fontweight='bold', y=0.96)
ax.set_title(subtitle, fontsize=20, pad=12)

# Legend (top-right inside plot)
# Construct legend entries manually to show hatched sample for Spain targets
legend_patches = [
    mpatches.Patch(facecolor=color_spain, edgecolor=color_spain, label="Spain (actual)"),
    mpatches.Patch(facecolor=color_spain, edgecolor=color_spain, hatch='////', label="Spain (target)", alpha=0.6),
    mpatches.Patch(facecolor=color_euro, edgecolor=color_euro, label="Euro‑Zone average")
]
legend = ax.legend(handles=legend_patches, loc='upper right', fontsize=14, frameon=False, bbox_to_anchor=(0.98, 0.95))

# Minimal on-chart numeric labels: label Spain 2009 (largest deficit) and 2010 as example
highlight_years = [2009, 2010]
for hy in highlight_years:
    idx = np.where(years == hy)[0][0]
    val = spain[idx]
    x_pos = ind[idx] + bar_width/2
    # Place label just above (for negative, slightly above the top of bar)
    y_text = val - 0.6 if val < 0 else val + 0.2
    ax.text(x_pos, y_text, f"{val:.1f}%", color='white' if val < -2 else 'black',
            fontsize=12, fontweight='bold', ha='center', va='top' if val < 0 else 'bottom', zorder=5)

# Tighten layout of plot area
ax.set_xlim(-0.6, n - 0.4)

# Caption and metadata block at bottom
caption_lines = [
    "Notes: Values are percent of GDP. Euro‑Zone average not available for 2012–2014 (NA). Positive values indicate surplus; negative indicate deficit.",
    "Variables: 'Spain' = national government balance; 'Euro‑Zone average' = aggregate average (see source).",
    "Spain’s balance plunges sharply after 2008, reflecting the economic crisis and subsequent fiscal adjustments.",
    "Peak gap: 2009 — Spain −11.2% vs Euro‑Zone −6.3%. Targets for 2012–2014 are government forecasts/targets, not outturns."
]
caption_text = "\n".join(caption_lines)
fig.text(0.1, 0.07, caption_text, ha='left', va='top', fontsize=12, wrap=True)

# PresentMetadata block (compact) bottom-left below caption
metadata = "Source: Eurostat / Spanish Ministry of Finance. Method: government balance (% GDP). Chart prepared for presentation."
fig.text(0.1, 0.03, metadata, ha='left', va='top', fontsize=12)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Show plot
plt.savefig("generated/spain_factor1_bar0/spain_factor1_bar0_design.png", dpi=300, bbox_inches="tight")