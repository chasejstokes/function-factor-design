import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np
from matplotlib import rcParams

# Set global typography and style
rcParams['font.family'] = 'DejaVu Sans'
rcParams['font.size'] = 12

# Data setup
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.4, -1.0, -0.6, -0.2, -0.3, -0.1, 1.3, 2.4, 1.9, -4.5, -11.2, -9.3, -8.9, -6.3, -4.5, -2.8])
# Use None for missing euro-zone data
euro_zone = np.array([-1.4, 0.0, -1.8, -2.5, -3.1, -2.9, -2.4, -1.3, -0.7, -2.1, -6.3, -6.2, -4.1, None, None, None], dtype=object)

# Colors and styling
color_spain = "#A51C30"    # deep red
color_ez = "#1F4E79"       # deep blue/steel
grid_color = "#e6e6e6"
target_hatch = "////"      # diagonal hatch
target_alpha = 0.6

# Figure: portrait orientation 3:4 or taller
fig, ax = plt.subplots(figsize=(9, 12))
plt.subplots_adjust(top=0.88, bottom=0.12, left=0.12, right=0.95)

x = np.arange(len(years))
bar_width = 0.36

# Determine which years are targets (2012-2014)
target_years_mask = (years >= 2012)
actual_years_mask = ~target_years_mask

# Plot Euro-Zone bars for years with data only
ez_vals = np.array([v if v is not None else np.nan for v in euro_zone], dtype=float)
# Spain bars: differentiate targets
spain_positions = x - bar_width/2
ez_positions = x + bar_width/2

# Plot EZ bars where available
for xi, ez_val in zip(ez_positions, ez_vals):
    if not np.isnan(ez_val):
        ax.bar(xi, ez_val, width=bar_width, color=color_ez, label='_nolegend_', zorder=2)

# Plot Spain bars: actual and target styling
for xi, sval, is_target in zip(spain_positions, spain, target_years_mask):
    if is_target:
        ax.bar(xi, sval, width=bar_width, color=color_spain, alpha=target_alpha,
               hatch=target_hatch, edgecolor=color_spain, linewidth=1.0, label='_nolegend_', zorder=3)
    else:
        ax.bar(xi, sval, width=bar_width, color=color_spain, label='_nolegend_', zorder=4)

# X axis ticks and labels
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=12)
ax.set_xlabel("Year", fontsize=20, labelpad=12)
ax.xaxis.set_tick_params(rotation=0)

# Y axis labeling and grid
ax.set_ylabel("Budget balance (% of GDP)", fontsize=20, labelpad=12)
# Compute y limits with margin
all_vals = np.concatenate([spain, np.array([v for v in ez_vals if not np.isnan(v)])])
ymin = min(all_vals.min(), -12.5)
ymax = max(all_vals.max(), 3)
yrange = ymax - ymin
ax.set_ylim(ymin - 0.12*yrange, ymax + 0.12*yrange)
# Horizontal gridlines
ax.yaxis.grid(True, color=grid_color, linewidth=1)
ax.set_axisbelow(True)

# Y ticks at sensible increments (every 2)
yticks = np.arange(np.floor((ymin-1)/2)*2, np.ceil((ymax+1)/2)*2 + 1, 2)
ax.set_yticks(yticks)
ax.tick_params(axis='y', labelsize=14)
ax.tick_params(axis='x', labelsize=12)

# Title and subtitle
title_text = "Spain vs Euro‑Zone: Budget balance (% of GDP), 1999–2014"
subtitle_text = "Final three years are Spain’s official targets (2012–2014)."
ax.set_title(title_text, fontsize=30, fontweight='bold', pad=18)
ax.text(0.12, 0.945, subtitle_text, transform=fig.transFigure, fontsize=14, va='center')

# Legend (top-right, compact)
# Create custom legend handles
handle_spain = mpatches.Patch(color=color_spain, label="Spain")
handle_ez = mpatches.Patch(color=color_ez, label="Euro‑Zone average")
handle_spain_target = mpatches.Patch(facecolor=color_spain, hatch=target_hatch, alpha=target_alpha,
                                     edgecolor=color_spain, label="Spain — target")
legend = ax.legend(handles=[handle_spain, handle_ez, handle_spain_target],
                   loc='upper right', bbox_to_anchor=(0.98, 0.98), fontsize=12, frameon=False)

# Value labels: Spain above every Spain bar
for xi, sval in zip(spain_positions, spain):
    ax.text(xi, sval + (0.02*yrange if sval >= 0 else -0.03*yrange), f"{sval:.1f}",
            ha='center', va='bottom' if sval >= 0 else 'top',
            fontsize=12, fontweight='bold', color='black')

# Euro-zone value labels only where difference > 1.5 percentage points
for xi, ez_val, sval in zip(ez_positions, ez_vals, spain):
    if not np.isnan(ez_val) and abs(sval - ez_val) > 1.5:
        ax.text(xi, ez_val + (0.02*yrange if ez_val >= 0 else -0.03*yrange),
                f"{ez_val:.1f}", ha='center',
                va='bottom' if ez_val >= 0 else 'top',
                fontsize=11, color='black', alpha=0.9)

# "Target" tag above Spain target bars
for xi, sval, is_target in zip(spain_positions, spain, target_years_mask):
    if is_target:
        ax.text(xi, sval + 0.04*yrange, "TARGET", ha='center', va='bottom',
                fontsize=9, color='black', fontweight='semibold')

# Missing Euro-Zone markers for 2012-2014: small light-gray circle-with-slash icon and "N/A"
y_na = 0.6  # place slightly above x-axis (as requested)
for xi, ez_val, yr in zip(ez_positions, ez_vals, years):
    if np.isnan(ez_val):
        # Draw circle
        circ = mpatches.Circle((xi, y_na), 0.22, edgecolor='#bdbdbd', facecolor='none', linewidth=1.2, zorder=5)
        ax.add_patch(circ)
        # Draw slash
        slash = mlines.Line2D([xi-0.16, xi+0.16], [y_na-0.16, y_na+0.16], color='#bdbdbd', linewidth=1.5, zorder=6)
        ax.add_line(slash)
        # N/A label
        ax.text(xi, y_na + 0.30, "N/A", ha='center', va='bottom', fontsize=9, color='#6e6e6e', fontweight='bold')

# Annotations & callouts
# 1) 2006 cluster annotation
def add_callout(year, text, arrow_symbol, y_offset_text=1.8):
    idx = int(np.where(years == year)[0][0])
    x_bar = spain_positions[idx]
    y_bar = spain[idx]
    # circular highlight around Spain bar
    circle_radius = 0.6
    circ = mpatches.Circle((x_bar, y_bar), circle_radius, fill=False, edgecolor='#666666',
                           linewidth=1.6, zorder=7)
    ax.add_patch(circ)
    # connecting line (annotation)
    text_x = x_bar + 1.0
    text_y = y_bar + y_offset_text
    ax.annotate(f"{arrow_symbol} {text}", xy=(x_bar, y_bar + circle_radius*0.6), xytext=(text_x, text_y),
                fontsize=11, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color='#666666', lw=0.8), zorder=8, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8))
# Add 2006 annotation
add_callout(2006, "Spain +2.4 vs EZ -1.3 → ~3.7 pp advantage.", "▲", y_offset_text=1.8)
# 2) 2009 cluster annotation
add_callout(2009, "2009: Spain -11.2 vs EZ -6.3 → ~4.9 pp deeper.", "▼", y_offset_text=-3.2)

# 3) 2012–2014 annotation above Spain target bars
# place centered above those three bars
idx_start = list(years).index(2012)
x_center_targets = np.mean(spain_positions[idx_start:idx_start+3])
y_top_targets = max(spain[idx_start:idx_start+3])  # highest (least negative) among targets
annot_text = "Targets (not actuals). Euro‑Zone averages not available."
ax.annotate(annot_text, xy=(x_center_targets, spain[idx_start+1]), xytext=(x_center_targets + 0.9, y_top_targets + 2.0),
            fontsize=11, ha='left', va='bottom',
            arrowprops=dict(arrowstyle='-', color='#666666', lw=0.8), zorder=8,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9))

# Summary box (bottom-right inset)
summary_text = ("Key points:\n"
                "• Mid‑2000s: Spain in surplus while EZ averaged deficits.\n"
                "• 2009: Spain deficit (-11.2) far deeper than EZ avg (-6.3).\n"
                "• 2012–2014: Spain targets, EZ data N/A.")
ax.text(0.98, 0.08, summary_text, transform=fig.transFigure,
        ha='right', va='bottom', fontsize=11, bbox=dict(boxstyle="round,pad=0.6", fc="white", ec="#d9d9d9", alpha=0.95))

# Source line & small government logo (bottom-left)
# Draw a simple emblem as placeholder logo using an inset axes
logo_ax = fig.add_axes([0.12, 0.03, 0.06, 0.06], anchor='W')
logo_ax.add_patch(mpatches.Circle((0.22, 0.5), 0.25, color=color_spain))
logo_ax.add_patch(mpatches.Rectangle((0.42, 0.3), 0.45, 0.4, color=color_ez))
logo_ax.axis('off')

source_text = ("Source: [Government Agency], fiscal balance series. "
               "Note: values are % of GDP; last actual year = 2011; 2012–2014 = Government targets.")
fig.text(0.20, 0.045, source_text, fontsize=10, ha='left', va='center')

# Tighten layout and render
plt.tight_layout(rect=[0, 0.02, 1, 0.96])
plt.savefig("generated/spain_factor3_bar4/spain_factor3_bar4_design.png", dpi=300, bbox_inches="tight")