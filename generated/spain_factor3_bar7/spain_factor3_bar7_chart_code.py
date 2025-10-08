import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, Circle
import matplotlib.lines as mlines
import numpy as np

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Derived stats
diff = spain - ez
mean_diff = diff.mean()  # expected around -0.09
years_spain_gt = int((spain > ez).sum())
years_spain_lt = int((spain < ez).sum())
largest_gap_idx = np.argmax(np.abs(diff))
largest_gap_year = years[largest_gap_idx]
largest_gap_value = diff[largest_gap_idx]
largest_gap_spain = spain[largest_gap_idx]
largest_gap_ez = ez[largest_gap_idx]
# For positive max where Spain advantage highest
pos_gap_idx = np.argmax(diff)
pos_gap_year = years[pos_gap_idx]
pos_gap_value = diff[pos_gap_idx]
pos_gap_spain = spain[pos_gap_idx]
pos_gap_ez = ez[pos_gap_idx]

# Small inline markers requested for 2005 and 2010
inline_idx_2005 = np.where(years == 2005)[0][0]
inline_idx_2010 = np.where(years == 2010)[0][0]

# Plot styling & layout
plt.style.use('default')
fig, ax = plt.subplots(figsize=(9, 12), dpi=100)  # 900x1200 px canvas
fig.patch.set_facecolor('#f7f7f7')  # off-white background
ax.set_facecolor('#f7f7f7')

# Colors
spain_color = '#C8102E'   # deep Spanish red
ez_color = '#0B3D91'      # deep navy blue
neutral_gray = '#666666'

# X positions for pairs
x = np.arange(len(years))
bar_width = 0.35
offset = bar_width / 2.0

# Draw bars as rounded rectangles using FancyBboxPatch for polish
for xi, s_val, e_val in zip(x, spain, ez):
    # Spain bar
    if s_val >= 0:
        y0_sp = 0
        h_sp = s_val
    else:
        y0_sp = s_val
        h_sp = -s_val
    sp_patch = FancyBboxPatch((xi - offset - 0.02, y0_sp),
                              bar_width, h_sp,
                              boxstyle="round,pad=0,rounding_size=3",
                              linewidth=0, facecolor=spain_color, alpha=0.98, zorder=3)
    # subtle shadow behind
    shadow_sp = FancyBboxPatch((xi - offset - 0.02 + 0.01, y0_sp - 0.12),
                               bar_width, h_sp,
                               boxstyle="round,pad=0,rounding_size=3",
                               linewidth=0, facecolor='k', alpha=0.04, zorder=2)
    ax.add_patch(shadow_sp)
    ax.add_patch(sp_patch)

    # EZ bar
    if e_val >= 0:
        y0_ez = 0
        h_ez = e_val
    else:
        y0_ez = e_val
        h_ez = -e_val
    ez_patch = FancyBboxPatch((xi + offset - 0.02, y0_ez),
                              bar_width, h_ez,
                              boxstyle="round,pad=0,rounding_size=3",
                              linewidth=0, facecolor=ez_color, alpha=0.98, zorder=3)
    shadow_ez = FancyBboxPatch((xi + offset - 0.02 + 0.01, y0_ez - 0.12),
                               bar_width, h_ez,
                               boxstyle="round,pad=0,rounding_size=3",
                               linewidth=0, facecolor='k', alpha=0.04, zorder=2)
    ax.add_patch(shadow_ez)
    ax.add_patch(ez_patch)

# Set axis limits
ax.set_xlim(-0.8, len(years)-0.2)
ymin = -12
ymax = 3
ax.set_ylim(ymin, ymax)

# Zero baseline emphasized
ax.axhline(0, color='black', linewidth=2.2, zorder=4)

# X axis
ax.set_xticks(x)
ax.set_xticklabels(years.astype(str), fontsize=18)
ax.tick_params(axis='x', which='major', pad=8)

# Y axis
ax.set_ylabel('% of GDP', fontsize=22, labelpad=10)
ax.set_yticks(np.arange(-12, 4, 2))
ax.set_yticklabels([f"{t:g}" for t in np.arange(-12, 4, 2)], fontsize=20)
ax.tick_params(axis='y', which='major', pad=8)

# Title and subtitle (title left-aligned inside top-left area)
title_text = "Spain vs Euro‑Zone average: Budget balance (% of GDP), 1999–2014"
subtitle_text = "Annual budget balance, % of GDP"
# Place title left of center to allow legend on top-right
ax.text(0.01, 1.02, title_text, transform=ax.transAxes,
        fontsize=42, fontweight='bold', va='bottom', ha='left')
ax.text(0.01, 0.98, subtitle_text, transform=ax.transAxes,
        fontsize=20, va='top', ha='left', color=neutral_gray)

# Manual legend top-right with small flag/icon graphics
legend_x = 0.85
legend_y = 1.02
# Spain flag mini (three horizontal bands: red, yellow, red)
flag_w = 0.03
flag_h = 0.03
# Create small inset axes for better control of mini-icons placement
ax_flag = fig.add_axes([0.84, 0.95, 0.06, 0.06], frameon=False)
ax_flag.set_axis_off()
# draw Spain flag as three horizontal rectangles
ax_flag.add_patch(Rectangle((0.05, 0.55), 0.9, 0.35, facecolor=spain_color, transform=ax_flag.transAxes))
ax_flag.add_patch(Rectangle((0.05, 0.25), 0.9, 0.3, facecolor='#FFD100', transform=ax_flag.transAxes))
ax_flag.add_patch(Rectangle((0.05, 0.02), 0.9, 0.23, facecolor=spain_color, transform=ax_flag.transAxes))
ax_flag.text(1.05, 0.55, "Spain", transform=ax_flag.transAxes, fontsize=20, va='center', ha='left')

# Euro symbol / EU flag style - simple circle with euro sign
ax_euro = fig.add_axes([0.84, 0.88, 0.06, 0.055], frameon=False)
ax_euro.set_axis_off()
# blue circle background and euro symbol
ax_euro.add_patch(Circle((0.12, 0.5), 0.35, facecolor=ez_color, transform=ax_euro.transAxes))
ax_euro.text(0.18, 0.48, "€", transform=ax_euro.transAxes, color='white', fontsize=18, fontweight='bold')
ax_euro.text(1.05, 0.5, "Euro‑Zone avg.", transform=ax_euro.transAxes, fontsize=20, va='center', ha='left')

# Summary box under legend (top-right)
summary_x = 0.60
summary_y = 0.86
summary_text = [
    f"Mean Spain − Euro‑Zone (1999–2014): {mean_diff:.2f} pp (essentially similar)",
    f"Years Spain > EZ: {years_spain_gt} | Years Spain < EZ: {years_spain_lt}",
    f"Largest gap: {int(largest_gap_year)} (Spain {largest_gap_spain:+.1f} vs EZ {largest_gap_ez:+.1f}; gap {largest_gap_value:+.1f} pp)"
]
summary_str = "\n".join(summary_text)
ax.text(0.60, 0.85, summary_str, transform=ax.transAxes, fontsize=22,
        va='top', ha='left', bbox=dict(boxstyle="round,pad=0.6", facecolor='white', edgecolor=neutral_gray, alpha=0.95))

# Annotations with halos for 2009 (largest negative divergence) and 2004 (largest Spain advantage)
def add_halo_and_callout(year_val, sp_val, ez_val, text, text_xy, text_align='left', color=spain_color, icon='🇪🇸'):
    idx = np.where(years == year_val)[0][0]
    xi = x[idx]
    # center and radii in data coords
    center_x = xi
    center_y = (sp_val + ez_val) / 2.0
    vert_span = abs(sp_val - ez_val)
    radius_x = 0.9
    radius_y = max(1.2, vert_span/2.0 + 1.2)
    halo = Ellipse((center_x, center_y), width=radius_x*2, height=radius_y*2,
                   edgecolor=color, facecolor='none', linewidth=2.0, alpha=0.35, zorder=2)
    ax.add_patch(halo)
    # connector line from halo to annotation box
    # choose connection point on halo boundary: from top-right edge of ellipse
    conn_x = center_x + radius_x*0.6
    conn_y = center_y + radius_y*0.4
    # Add line
    ax.plot([conn_x, text_xy[0]], [conn_y, text_xy[1]], linestyle='-', color=neutral_gray, linewidth=1.2, zorder=5)
    # Annotation box
    bboxprops = dict(boxstyle="round,pad=0.6", fc='white', ec=neutral_gray, lw=1.0)
    ax.text(text_xy[0], text_xy[1], text, fontsize=20, va='center', ha=text_align, bbox=bboxprops, zorder=6)

# 2009 callout on right mid
callout_2009_text = f"2009 — Spain: {spain[years==2009][0]:+.1f}% vs EZ: {ez[years==2009][0]:+.1f}% → gap: {diff[years==2009][0]:+.1f} pp"
add_halo_and_callout(2009, spain[years==2009][0], ez[years==2009][0], callout_2009_text, text_xy=(len(years)*0.62, -2.5), text_align='left', color=spain_color)

# 2004 callout below 2009
callout_2004_text = f"2004 — Spain: {spain[years==2004][0]:+.1f}% vs EZ: {ez[years==2004][0]:+.1f}% → gap: {diff[years==2004][0]:+.1f} pp"
add_halo_and_callout(2004, spain[years==2004][0], ez[years==2004][0], callout_2004_text, text_xy=(len(years)*0.62, -6.0), text_align='left', color=spain_color)

# Small inline difference markers for 2005 and 2010
def add_inline_diff_marker(index, xpos, ypos_offset=0.4):
    xi = x[index]
    txt = f"{diff[index]:+.1f} pp"
    # find top of the pair to place text slightly above
    top_val = max(spain[index], ez[index])
    ax.text(xi, top_val + ypos_offset, txt, fontsize=18, ha='center', va='bottom', color=neutral_gray, zorder=7)

add_inline_diff_marker(inline_idx_2005, x[inline_idx_2005], ypos_offset=0.6)
add_inline_diff_marker(inline_idx_2010, x[inline_idx_2010], ypos_offset=0.6)

# Small markers/labels near highlighted bars optionally show tiny icons inside callout boxes - using text icons
# Note: emoji glyphs may or may not render depending on environment; we add small 'ES' to indicate Spain inside callout near 2009
ax.text(len(years)*0.61, -2.5, " 🇪🇸", fontsize=18, va='center', ha='left')
ax.text(len(years)*0.61, -6.0, " 🇪🇸", fontsize=18, va='center', ha='left')

# Metadata and small government logo bottom-left
# Logo placeholder: simple small emblem block
logo_ax = fig.add_axes([0.02, 0.02, 0.12, 0.08], frameon=False)
logo_ax.set_axis_off()
# draw emblem: circle with small crown-like rects
logo_ax.add_patch(Circle((0.12, 0.5), 0.28, facecolor='#00539F', transform=logo_ax.transAxes))
logo_ax.text(0.12, 0.5, "GOV", transform=logo_ax.transAxes, color='white', fontsize=16, fontweight='bold', ha='center', va='center')
# Metadata text
meta_text = ("Source: Ministry of Finance / Eurostat (official data).\n"
             "Chart prepared by [agency]. Data: budget balance as % of GDP.\n"
             "Method: Annual reported values.")
ax.text(0.18, 0.06, meta_text, transform=ax.transAxes, fontsize=14, va='bottom', ha='left', color=neutral_gray)

# Legend note (also add simple line legend to clarify colors)
legend_patches = [
    mpatches.Patch(color=spain_color, label='Spain'),
    mpatches.Patch(color=ez_color, label='Euro‑Zone average')
]
# Place a small traditional legend (no frame) at coords to ensure readers can match colors to labels
leg = ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(0.58, 1.02), fontsize=20, frameon=False)
for text in leg.get_texts():
    text.set_fontsize(20)

# Clean up gridlines and spines for presentation look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(neutral_gray)
ax.spines['bottom'].set_color(neutral_gray)
ax.tick_params(axis='x', colors=neutral_gray)
ax.tick_params(axis='y', colors=neutral_gray)

# Ensure layout is tight and title/legend don't overlap
plt.subplots_adjust(top=0.93, left=0.08, right=0.96, bottom=0.12)

# Show plot
plt.savefig("generated/spain_factor3_bar7/spain_factor3_bar7_design.png", dpi=300, bbox_inches="tight")