import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Data setup
years = np.array([
    1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
    2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014
])
spain = np.array([
    -1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4,
    1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8
])
# Euro-zone: last three years are NA (use np.nan)
euro = np.array([
    -1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3,
    -0.7, -2.1, -6.3, -6.2, -4.1, np.nan, np.nan, np.nan
])

# Visual parameters
color_spain = "#D84B3A"    # warm saturated
color_euro = "#4F77A6"     # muted blue/gray
bg_color = "#FAFAFB"       # very pale gray
shadow_effect = [pe.SimplePatchShadow(offset=(1.6, -1.6), shadow_rgbFace=(0,0,0), alpha=0.12),
                 pe.Normal()]

# Figure and axes: portrait orientation (9x12 inches ~ 3:4)
fig, ax = plt.subplots(figsize=(9, 12))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# X positions for grouped bars
n = len(years)
ind = np.arange(n)
bar_width = 0.38
gap_between_groups = 0.10  # implicitly via bar width and spacing

# Plot euro-zone bars (will ignore NaNs automatically)
bars_euro = ax.bar(ind - bar_width/2, euro, width=bar_width, color=color_euro,
                   label="Euro‑Zone average", zorder=3)

# Plot Spain bars with a subtle shadow effect to prioritize visually
bars_spain = ax.bar(ind + bar_width/2, spain, width=bar_width, color=color_spain,
                    label="Spain", zorder=4)
for r in bars_spain:
    r.set_path_effects(shadow_effect)

# Shade target years (2012–2014) with a subtle vertical band
# Find indices for years 2012-2014
target_years_mask = (years >= 2012) & (years <= 2014)
if target_years_mask.any():
    # Compute left and right bounds for the shaded region
    left = ind[target_years_mask][0] - bar_width
    right = ind[target_years_mask][-1] + bar_width
    ax.axvspan(left - 0.12, right + 0.12, color="#808080", alpha=0.06, zorder=1)

    # Inline label about targets / NA just above top of plot area within shaded block
    x_center = (left + right) / 2
    # Place near top (use axis transform)
    y_text = 0.92  # in axis fraction
    ax.text(x_center, y_text, "2012–2014: Spain = targets; euro‑zone avg unavailable",
            transform=ax.transAxes, fontsize=13, ha='center', va='top',
            color="#333333", alpha=0.95)

# Emphasize zero baseline
ax.axhline(0, color="#222222", linewidth=1.6, zorder=5)

# Gridlines (light, horizontal)
ax.yaxis.grid(True, color="#E6E6E6", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)

# X-axis labels: every year
ax.set_xticks(ind)
ax.set_xticklabels([str(y) for y in years], fontsize=15)
ax.tick_params(axis='x', which='major', pad=6)

# Y-axis ticks and label
# Determine y-limits with a bit of padding
ymin = min(np.nanmin(euro), np.min(spain)) if not np.isnan(np.nanmin(euro)) else np.min(spain)
ymin = min(ymin, -12.5)  # ensure space for -11.2 label
ymax = max(np.nanmax(euro), np.max(spain))
ymax = max(ymax, 3.0)
ax.set_ylim(ymin - 0.8, ymax + 1.2)
yticks = np.arange(np.floor((ymin - 1) / 2) * 2, np.ceil((ymax + 1) / 2) * 2 + 1, 2)
ax.set_yticks(yticks)
ax.set_yticklabels([f"{int(t)}" if float(t).is_integer() else f"{t}" for t in yticks], fontsize=16)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=18, labelpad=12)

# Minimal numeric labels for most extreme Spain values (2009, 2010)
def add_subtle_label(bar, text):
    # For negative bars, place label near the top of the bar (less negative)
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_y() + bar.get_height() + 0.35  # slightly above top of negative bar
    # If label would overlap beyond axis top, adjust to inside bar
    # Use white text with a thin dark halo for readability
    txt = ax.text(x, y, text, ha='center', va='bottom', fontsize=13, color='white', zorder=6)
    txt.set_path_effects([pe.Stroke(linewidth=2, foreground='black', alpha=0.45), pe.Normal()])

# Identify bars for 2009 and 2010 (years array)
for yr, val in [(2009, -11.2), (2010, -9.3)]:
    idx = np.where(years == yr)[0]
    if idx.size:
        bar = bars_spain[idx[0]]
        # Place label inside or just above the bar depending on space
        bx = bar.get_x() + bar.get_width() / 2
        by = bar.get_y() + bar.get_height()
        # For negative bars, place label slightly above the top edge (less negative)
        label_y = by + 0.35
        ax.text(bx, label_y, f"{val:.1f}", ha='center', va='bottom',
                fontsize=13, color='white', zorder=6,
                path_effects=[pe.Stroke(linewidth=2, foreground='black', alpha=0.45), pe.Normal()])

# Legend top-right of chart area with clear, large text
leg = ax.legend(fontsize=17, loc='upper right', frameon=False, bbox_to_anchor=(0.98, 0.96))

# Title, subtitle, variable descriptor
title = "Budget balance: Spain vs Euro‑Zone average (1999–2014)"
subtitle = ("Budget balance (% of GDP). Negative = deficit, positive = surplus. "
            "Last three years (2012–2014) are Spain’s government targets; euro‑zone averages unavailable for those years.")
variable_desc = "Variable shown: Budget balance as % of GDP."

# Use figure-level title for prominence
fig.suptitle(title, fontsize=34, fontweight='bold', y=0.98)

# Subtitle and variable descriptor placed beneath the title
fig.text(0.5, 0.93, subtitle, ha='center', va='top', fontsize=20, color="#222222", wrap=True)
fig.text(0.5, 0.905, variable_desc, ha='center', va='top', fontsize=14, color="#555555")

# Caption / footnote below the chart (2-3 short sentences)
caption_lines = (
    "Source: provided dataset. Note: Euro‑zone averages NA for 2012–2014; Spain’s 2012–2014 bars are targets, not observed values. "
    "Measurement: budget balance as % of GDP. Spain shows modest surpluses in the mid‑2000s but very large deficits after the 2008 crisis (2009–2011)."
)
fig.text(0.02, 0.02, caption_lines, ha='left', va='bottom', fontsize=12, color="#333333")

# Tight layout adjustments to respect subtitle/title spacing
plt.subplots_adjust(top=0.895, bottom=0.08, left=0.08, right=0.95)

# Improve layout: rotate xlabels slightly if crowded (keep horizontal if readable)
plt.setp(ax.get_xticklabels(), rotation=0)

# Show the plot
plt.savefig("generated/spain_factor1_bar3/spain_factor1_bar3_design.png", dpi=300, bbox_inches="tight")