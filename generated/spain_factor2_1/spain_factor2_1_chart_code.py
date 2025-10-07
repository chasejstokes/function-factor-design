import matplotlib.pyplot as plt
import numpy as np

# Data
years = np.array([1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4, 1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
ez = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1, -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Colors and style settings
color_spain = "#d64545"
color_ez = "#2b7bd3"
fill_alpha = 0.12
muted_label_color = "#333333"
connector_color = "#999999"
bg_box_alpha = 0.95
annotation_box_face = (0.98, 0.98, 0.98)  # very light gray
annotation_edge_rgba = (0.6, 0.6, 0.6, 0.25)  # 20-25% opacity grey

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
    "lines.solid_capstyle": "round",
    "lines.solid_joinstyle": "round"
})

fig, ax = plt.subplots(figsize=(9, 5))  # ~900x500 pixels

# Fill band: separate where Spain > EZ (red tint) and Spain < EZ (blue tint)
ax.fill_between(years, spain, ez, where=(spain > ez), interpolate=True,
                color=color_spain, alpha=fill_alpha, linewidth=0)
ax.fill_between(years, spain, ez, where=(spain <= ez), interpolate=True,
                color=color_ez, alpha=fill_alpha, linewidth=0)

# Plot lines and markers
ax.plot(years, ez, color=color_ez, linewidth=2.5, label="Euro-Zone average",
        marker='o', markersize=6, markerfacecolor=color_ez, markeredgecolor='white', markeredgewidth=1.2)
ax.plot(years, spain, color=color_spain, linewidth=2.5, label="Spain",
        marker='o', markersize=6, markerfacecolor=color_spain, markeredgecolor='white', markeredgewidth=1.2)

# Axes labels and ticks
ax.set_ylabel("Budget balance (% of GDP)", fontsize=10)
ax.set_xticks(years)
ax.set_xticklabels([str(int(y)) for y in years], rotation=0, fontsize=9)
ax.set_xlim(years.min() - 0.5, years.max() + 1.2)  # extra right margin for inline labels
ymin = min(spain.min(), ez.min())
ymax = max(spain.max(), ez.max())
yrange = ymax - ymin
ax.set_ylim(ymin - 0.12*yrange, ymax + 0.18*yrange)

# Subtle horizontal grid for readability
ax.yaxis.grid(True, color="#e8e8e8", linewidth=1)
ax.xaxis.grid(False)
ax.set_axisbelow(True)

# Title and subtitle (top-left)
fig.text(0.07, 0.95, "Spain vs Euro‑Zone: Budget balance", fontsize=14, fontweight='bold', va='top')
fig.text(0.07, 0.915, "Net balance, % of GDP — 1999–2014", fontsize=10, va='top', color='#444')

# Inline end-of-line labels (no legend)
last_x = years[-1] + 0.2
ax.text(last_x, spain[-1], "Spain", color=color_spain, fontsize=10, fontweight='bold',
        va='center', ha='left')
ax.text(last_x, ez[-1], "Euro‑Zone average", color=color_ez, fontsize=10, fontweight='bold',
        va='center', ha='left')

# Data point labels for every year with faint rounded background and alternating offsets
signs = np.array([1 if i % 2 == 0 else -1 for i in range(len(years))])  # alternate above/below
offset = 0.02 * yrange  # small offset relative to range

for i, x in enumerate(years):
    # Spain labels
    y_sp = spain[i]
    y_ez = ez[i]
    # Decide offset adjustment for crowding near each other: if points are close vertically, push labels apart
    vertical_gap = abs(y_sp - y_ez)
    extra = 0
    if vertical_gap < 0.6 * (yrange * 0.02):  # if very close, provide a bit more separation
        extra = 0.016 * yrange
    dy_sp = signs[i] * (offset + extra)
    dy_ez = -signs[i] * (offset + extra)  # opposite offset for the EZ label to reduce overlap

    # Styling for emphasized years
    emphasize_years = {2006, 2009, 2014}
    if x in emphasize_years:
        fontsize_point = 10
        label_color = "#111111"
        bbox_face = (1.0, 1.0, 1.0)
        bbox_alpha = 0.9
        weight = 'bold'
    else:
        fontsize_point = 9
        label_color = muted_label_color
        bbox_face = (0.97, 0.97, 0.97)
        bbox_alpha = 0.8
        weight = 'normal'

    # Spain value label
    txt_sp = f"{y_sp:+.1f}%"
    ax.text(x, y_sp + dy_sp, txt_sp, fontsize=fontsize_point, color=label_color,
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.25", facecolor=bbox_face, edgecolor=(0.6,0.6,0.6,0.2), linewidth=0.6, alpha=bbox_alpha),
            fontweight=weight)

    # EZ value label
    txt_ez = f"{y_ez:+.1f}%"
    ax.text(x, y_ez + dy_ez, txt_ez, fontsize=fontsize_point, color=muted_label_color,
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.25", facecolor=(0.99,0.99,1.0) if x in emphasize_years else bbox_face,
                      edgecolor=(0.6,0.6,0.6,0.15), linewidth=0.5, alpha=0.8))

# Annotation callouts (3): use boxes with connector lines (curved)
# 1) 2004–2007 — anchor to Spain 2006
anchor_x1, anchor_y1 = 2006, spain[years.tolist().index(2006)]
box_x1, box_y1 = 2003.8, anchor_y1 + 1.6  # position upper-left of anchor
text1 = "Pre-crisis recovery\nSpain moves into surplus (peak 2006: +2.4% vs EZ +1.1%)"
ax.annotate(text1, xy=(anchor_x1, anchor_y1), xytext=(box_x1, box_y1),
            fontsize=9, fontweight='semibold',
            va='center', ha='left',
            bbox=dict(boxstyle="round,pad=0.45", facecolor=annotation_box_face, edgecolor=annotation_edge_rgba, linewidth=0.9),
            arrowprops=dict(arrowstyle="-", color=connector_color, linewidth=0.9, connectionstyle="arc3,rad=0.25"))

# 2) 2009 — anchor to Spain 2009
anchor_x2, anchor_y2 = 2009, spain[years.tolist().index(2009)]
box_x2, box_y2 = 2007.9, anchor_y2 - 3.2  # placed lower-left to avoid overlap
text2 = "Crisis spike\nSpain hits -11.2% (much worse than EZ -6.3%)"
ax.annotate(text2, xy=(anchor_x2, anchor_y2), xytext=(box_x2, box_y2),
            fontsize=9, fontweight='semibold',
            va='center', ha='left',
            bbox=dict(boxstyle="round,pad=0.45", facecolor=annotation_box_face, edgecolor=annotation_edge_rgba, linewidth=0.9),
            arrowprops=dict(arrowstyle="-", color=connector_color, linewidth=0.9, connectionstyle="arc3,rad=-0.3"))

# 3) 2012–2014 — anchor to Spain 2014
anchor_x3, anchor_y3 = 2014, spain[years.tolist().index(2014)]
box_x3, box_y3 = 2012.1, anchor_y3 + 2.0  # above-left of anchor
text3 = "Partial convergence\nSpain and EZ draw closer by 2014"
ax.annotate(text3, xy=(anchor_x3, anchor_y3), xytext=(box_x3, box_y3),
            fontsize=9, fontweight='semibold',
            va='center', ha='left',
            bbox=dict(boxstyle="round,pad=0.45", facecolor=annotation_box_face, edgecolor=annotation_edge_rgba, linewidth=0.9),
            arrowprops=dict(arrowstyle="-", color=connector_color, linewidth=0.9, connectionstyle="arc3,rad=0.2"))

# Footer/source note (very small, muted)
fig.text(0.07, 0.02, "Source: compiled data", fontsize=8, color='#666')

# Tidy layout
plt.subplots_adjust(left=0.08, right=0.92, top=0.87, bottom=0.10)
plt.savefig("generated/spain_factor2_1_design.png", dpi=300, bbox_inches="tight")