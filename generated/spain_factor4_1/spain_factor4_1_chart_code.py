import matplotlib.pyplot as plt
import numpy as np

# Data (from the provided dataset)
years = np.array([1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006,
                  2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014])
spain = np.array([-1.2, -0.6, -0.4, -1.0, -0.8, 0.6, 1.3, 2.4,
                  1.9, -4.5, -11.2, -9.5, -7.8, -4.2, -5.0, -2.5])
euro = np.array([-0.9, -0.4, -0.8, -1.6, -2.6, -2.9, -1.8, 1.1,
                 -0.8, -3.6, -6.3, -6.0, -4.1, -4.6, -3.8, -2.0])

# Derived statistics for summary box
avg_spain = spain.mean()
avg_euro = euro.mean()
years_spain_outperformed = int((spain > euro).sum())
# Peak Spain shortfall (most negative Spain value)
idx_peak_shortfall = np.argmin(spain)
year_peak_shortfall = years[idx_peak_shortfall]
spain_peak = spain[idx_peak_shortfall]
euro_peak = euro[idx_peak_shortfall]
gap_peak = abs(spain_peak - euro_peak)

# Colors and styling (colorblind-safe pair)
color_spain = "#E69F00"   # warm/orange for Spain
color_euro = "#56B4E9"    # cool blue for Euro-zone average
color_good = "#009E73"    # green/teal for Spain better
color_bad = "#D55E00"     # red/orange-red for Spain worse

# Figure setup (wide 16:9)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
})
fig, ax = plt.subplots(figsize=(14, 7.875))  # 16:9-like ratio

# Background and grid
ax.set_facecolor("white")
ax.yaxis.grid(True, color="0.92", linewidth=0.9)  # subtle horizontal gridlines
ax.xaxis.grid(False)

# Plot the Euro-zone average (secondary, thinner dashed)
ax.plot(years, euro, label="Euro‑zone average",
        color=color_euro, linewidth=2.0, linestyle=(0, (5, 3)), zorder=3)

# Plot Spain (primary, thicker solid)
ax.plot(years, spain, label="Spain",
        color=color_spain, linewidth=2.8, linestyle='-', zorder=4)

# Fill the area between lines with sign-dependent colors
mask_spain_better = spain > euro
mask_spain_worse = spain < euro

# Spain better: fill with green/teal
ax.fill_between(years, spain, euro, where=mask_spain_better,
                interpolate=True, color=color_good, alpha=0.15, zorder=2)
# Spain worse: fill with red tint
ax.fill_between(years, spain, euro, where=mask_spain_worse,
                interpolate=True, color=color_bad, alpha=0.15, zorder=2)

# Horizontal zero line emphasized
ax.axhline(0, color="0.3", linewidth=1.4, zorder=1)

# Axes labels and ticks
ax.set_xlabel("Year", fontsize=12, labelpad=8)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=12, labelpad=10)
ax.set_xticks(years)
ax.set_xticklabels([str(int(y)) for y in years], fontsize=11)
ax.set_yticks(np.arange(-12, 4, 2))
ax.set_yticklabels([f"{y:g}" for y in np.arange(-12, 4, 2)], fontsize=11)

# Y-axis range symmetric around extremes as requested
ax.set_ylim(-12.5, 3)

# Remove top/right spines for a clean look
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
ax.spines["left"].set_linewidth(0.8)
ax.spines["bottom"].set_linewidth(0.8)

# Title and subtitle
title = "Spain vs Euro‑Zone: Budget Balance (1999–2014, % of GDP)"
subtitle = "Spain often outperformed in the mid‑2000s but suffered deeper deficits during the 2008–2011 crisis."
ax.set_title(title, fontsize=20, fontweight="bold", pad=14)
# place subtitle as a separate text just below the title
fig.text(0.5, 0.92, subtitle, ha="center", fontsize=14, fontweight=600)

# Legend (compact, top-right)
legend = ax.legend(loc="upper right", fontsize=10, frameon=False)

# Annotated years: 2004 (Spain surplus vs EZ deficit), 2006 (Spain peak surplus),
# 2009 (largest Spain deficit), and grouped 2008–2011 as crisis years.
annot_years = [2004, 2006, 2009]
annotations = {}
for y in annot_years:
    idx = np.where(years == y)[0][0]
    annotations[y] = {
        "x": years[idx],
        "spain": spain[idx],
        "euro": euro[idx],
        "gap": spain[idx] - euro[idx],
        "idx": idx
    }

# Plot markers for annotated points only
for y, info in annotations.items():
    ax.scatter(info["x"], info["spain"], s=60, color=color_spain,
               edgecolor="0.15", linewidth=0.8, zorder=6)
    ax.scatter(info["x"], info["euro"], s=42, color=color_euro,
               edgecolor="0.15", linewidth=0.8, zorder=5)

# Add numeric labels and small callouts with thin leader lines
annot_props = dict(boxstyle="round,pad=0.25", fc="white", ec="0.8", linewidth=0.6)
arrowprops = dict(arrowstyle="-", color="0.45", linewidth=0.8)
# 2004
a = annotations[2004]
text_2004 = f"2004: Spain {a['spain']:+.1f}% vs EZ {a['euro']:+.1f}%\n(gap {a['gap']:+.1f} p.p.)"
ax.annotate(text_2004,
            xy=(a["x"], a["spain"]),
            xytext=(a["x"] - 1.4, a["spain"] + 3.0),
            fontsize=10, ha="left", va="center",
            bbox=annot_props, arrowprops=arrowprops, zorder=8)

# 2006
a = annotations[2006]
text_2006 = f"2006: Spain {a['spain']:+.1f}%\npeak surplus (vs {a['euro']:+.1f}%)"
ax.annotate(text_2006,
            xy=(a["x"], a["spain"]),
            xytext=(a["x"] + 0.6, a["spain"] + 2.6),
            fontsize=10, ha="left", va="center",
            bbox=annot_props, arrowprops=arrowprops, zorder=8)

# 2009 (largest shortfall)
a = annotations[2009]
text_2009 = f"2009: Spain {a['spain']:+.1f}% vs EZ {a['euro']:+.1f}%\n(gap {abs(a['gap']):.1f} p.p.)"
ax.annotate(text_2009,
            xy=(a["x"], a["spain"]),
            xytext=(a["x"] + 0.8, a["spain"] - 5.2),
            fontsize=10, ha="left", va="top",
            bbox=annot_props, arrowprops=arrowprops, zorder=8)

# Group annotation for crisis years 2008-2011: subtle background highlight + label
x0 = 2008 - 0.4
x1 = 2011 + 0.4
ax.axvspan(x0, x1, ymin=0.02, ymax=0.98, color="0.85", alpha=0.06, zorder=1)
# text for the group, placed above the lines within the plotted area
ax.text((2008 + 2011) / 2, -1.7, "Crisis years: deeper deficits\n(2008–2011)",
        ha="center", va="center", fontsize=10, bbox=dict(boxstyle="round,pad=0.2",
                                                          fc="white", ec="0.85", linewidth=0.6),
        zorder=9)

# Summary box / caption (bottom-right)
summary_text = (
    f"Period averages (1999–2014):\n"
    f"  • Spain = {avg_spain:+.2f}% GDP; Euro‑zone = {avg_euro:+.2f}% GDP.\n"
    f"  • Spain outperformed in {years_spain_outperformed} of 16 years; peak Spain shortfall:\n"
    f"    {int(year_peak_shortfall)} ({spain_peak:+.1f}% vs {euro_peak:+.1f}%; gap {gap_peak:.1f} p.p.)."
)
# Place box in axes coordinates anchored to lower right
ax.text(0.98, 0.03, summary_text, ha="right", va="bottom",
        transform=ax.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.6",
                                                       fc="white", ec="0.85", linewidth=0.6),
        zorder=10)

# Tweak layout for hierarchy and spacing
plt.subplots_adjust(top=0.88, right=0.88, left=0.07, bottom=0.08)

# Ensure everything fits cleanly
plt.savefig("generated/spain_factor4_1_design.png", dpi=300, bbox_inches="tight")