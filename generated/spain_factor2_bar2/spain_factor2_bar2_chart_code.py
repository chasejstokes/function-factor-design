# Ensure required packages are installed/importable
import importlib
import sys
import subprocess

def ensure_package(pkg_name, import_name=None):
    try:
        return importlib.import_module(import_name or pkg_name)
    except Exception:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])
        return importlib.import_module(import_name or pkg_name)

# Ensure numpy and matplotlib are available
np = ensure_package("numpy")
plt = ensure_package("matplotlib.pyplot", "matplotlib.pyplot")
from matplotlib.patches import Rectangle

# Optionally set a sensible default style, with fallbacks if a specific seaborn style isn't available
import matplotlib as mpl
try:
    plt.style.use('seaborn-whitegrid')
except Exception:
    try:
        plt.style.use('seaborn-v0_8-whitegrid')
    except Exception:
        try:
            plt.style.use('seaborn')
        except Exception:
            mpl.rcParams.update({'figure.facecolor': 'white'})

# Data setup
data = [
    {"year": 1999, "spain": -1.4, "euro": -1.4},
    {"year": 2000, "spain": -1.0, "euro": 0.0},
    {"year": 2001, "spain": -0.6, "euro": -1.8},
    {"year": 2002, "spain": -0.2, "euro": -2.5},
    {"year": 2003, "spain": -0.3, "euro": -3.1},
    {"year": 2004, "spain": -0.1, "euro": -2.9},
    {"year": 2005, "spain": 1.3, "euro": -2.4},
    {"year": 2006, "spain": 2.4, "euro": -1.3},
    {"year": 2007, "spain": 1.9, "euro": -0.7},
    {"year": 2008, "spain": -4.5, "euro": -2.1},
    {"year": 2009, "spain": -11.2, "euro": -6.3},
    {"year": 2010, "spain": -9.3, "euro": -6.2},
    {"year": 2011, "spain": -8.9, "euro": -4.1},
    {"year": 2012, "spain": -6.3, "euro": np.nan},  # targets (not outturn)
    {"year": 2013, "spain": -4.5, "euro": np.nan},  # targets
    {"year": 2014, "spain": -2.8, "euro": np.nan},  # targets
]

years = [d["year"] for d in data]
spain_vals = np.array([d["spain"] for d in data], dtype=float)
euro_vals = np.array([d["euro"] for d in data], dtype=float)

# Visual parameters
fig_w, fig_h = 9, 12  # 3:4 aspect ratio (width:height = 3:4), taller than wide
fig, ax = plt.subplots(figsize=(fig_w, fig_h))

# Colors (accessible contrast)
color_spain = "#d9534f"   # warm deep coral/cerise
color_euro = "#6d8aa3"    # desaturated slate blue / muted steel
no_data_marker_color = "#cfcfcf"

# Bar positions
x = np.arange(len(years))
bar_width = 0.35
spain_pos = x - bar_width/2
euro_pos = x + bar_width/2

# Y limits and ticks
ymin, ymax = -12, 3
ax.set_ylim(ymin, ymax)
yticks = np.arange(ymin, ymax + 0.1, 2.5)
ax.set_yticks(yticks)
# Make tick labels large for presentation
ax.set_yticklabels([f"{t:.1f}" if (abs(t % 1) > 1e-8) else f"{int(t)}" for t in yticks], fontsize=16)
ax.set_ylabel("Budget balance (% of GDP)", fontsize=22, labelpad=14)

# Zero baseline
ax.axhline(0, color='0.2', linewidth=1.6, zorder=2)

# Draw Euro zone bars only where data exists
euro_mask = ~np.isnan(euro_vals)
b_euro = ax.bar(euro_pos[euro_mask], euro_vals[euro_mask],
                width=bar_width, color=color_euro,
                edgecolor='none', zorder=3)

# Draw Spain bars; for 2012-2014 (targets) draw with hatch & lighter alpha
target_mask = np.array(years) >= 2012
spain_colors = []
spain_hatches = []
spain_alphas = []
for is_target in target_mask:
    if is_target:
        spain_colors.append(color_spain)
        spain_hatches.append('////')  # subtle diagonal hatch
        spain_alphas.append(0.60)
    else:
        spain_colors.append(color_spain)
        spain_hatches.append(None)
        spain_alphas.append(1.0)

bars_spain = []
for xi, val, col, hatch, a in zip(spain_pos, spain_vals, spain_colors, spain_hatches, spain_alphas):
    if hatch:
        b = ax.bar(xi, val, width=bar_width, color=col, alpha=a,
                   hatch=hatch, edgecolor='none', zorder=4)
    else:
        b = ax.bar(xi, val, width=bar_width, color=col, alpha=a,
                   edgecolor='none', zorder=4)
    bars_spain.append(b[0])

# "No data" markers for Euro Zone after 2011: place a light open circle at zero in euro position
no_data_years = []
for i, is_valid in enumerate(euro_mask):
    if not is_valid:
        no_data_years.append(i)
        ax.plot(euro_pos[i], 0, marker='o', markersize=8,
                markerfacecolor='none', markeredgecolor=no_data_marker_color, zorder=3)
        ax.text(euro_pos[i], 0.35, "no data", fontsize=12, color='0.3',
                ha='center', va='bottom')

# Thin connector lines between paired bars when both exist
for i in range(len(years)):
    if euro_mask[i]:
        ax.plot([spain_pos[i] + bar_width/2, euro_pos[i] - bar_width/2],
                [spain_vals[i], euro_vals[i]],
                color='0.5', linewidth=0.8, alpha=0.25, zorder=2)

# Value labels on every Spain bar (one decimal)
for i, rect in enumerate(bars_spain):
    h = rect.get_height()
    label = f"{h:.1f}"
    if h >= 0:
        ax.text(rect.get_x() + rect.get_width()/2, h - 0.15,
                label, ha='center', va='top', color='white', fontsize=14, fontweight='bold', zorder=6)
    else:
        ax.text(rect.get_x() + rect.get_width()/2, h + 0.25,
                label, ha='center', va='bottom', color='black', fontsize=14, fontweight='bold', zorder=6)

# Euro value labels for existing bars
for rect in b_euro:
    h = rect.get_height()
    label = f"{h:.1f}"
    if h >= 0:
        ax.text(rect.get_x() + rect.get_width()/2, h - 0.15,
                label, ha='center', va='top', color='white', fontsize=14, fontweight='bold', zorder=6)
    else:
        ax.text(rect.get_x() + rect.get_width()/2, h + 0.25,
                label, ha='center', va='bottom', color='black', fontsize=14, fontweight='bold', zorder=6)

# X-axis labels
ax.set_xticks(x)
ax.set_xticklabels([str(y) for y in years], fontsize=16, rotation=60, ha='right')
ax.set_xlabel("", fontsize=16)

# Title and subtitle
ax.set_title("Spain vs Euro‑Zone: Budget balance (% of GDP)",
             fontsize=32, pad=28)
fig.text(0.5, 0.93, "Paired bars show Spain (left) vs Euro‑Zone average (right); 2012–2014 are Spain targets.",
         ha='center', fontsize=16)

# Annotations (anchored boxes with arrows)
ann_style = dict(boxstyle="round,pad=0.6", fc="#f6f6f6", ec="#bdbdbd", linewidth=0.8)

# 1) 2006–2007 pre-crisis surpluses (point to 2006 Spain bar)
idx_2006 = years.index(2006)
ax.annotate(
    "Pre‑crisis surpluses — Spain recorded positive balances in 2005–2007 (peak: 2.4% in 2006).",
    xy=(spain_pos[idx_2006], spain_vals[idx_2006]),
    xytext=(spain_pos[idx_2006]-0.9, 2.6),
    fontsize=14, bbox=ann_style,
    arrowprops=dict(arrowstyle="->", color='0.45', linewidth=0.9),
    ha='left', va='bottom'
)

# 2) 2009 sharp reversal (point to 2009 Spain bar)
idx_2009 = years.index(2009)
ax.annotate(
    "Sharp reversal in 2009: Spain plunged to -11.2% amid the financial crisis.",
    xy=(spain_pos[idx_2009], spain_vals[idx_2009]),
    xytext=(spain_pos[idx_2009]-1.0, -8.5),
    fontsize=15, bbox=ann_style,
    arrowprops=dict(arrowstyle="->", color='0.45', linewidth=0.9),
    ha='left', va='bottom'
)

# 3) 2012–2014 cluster: targets and Euro‑Zone NA
idx_2013 = years.index(2013)
ax.annotate(
    "2012–2014 shown as official Spain targets (not outturns). Euro‑Zone averages unavailable after 2011.",
    xy=(spain_pos[idx_2013], spain_vals[idx_2013]),
    xytext=(spain_pos[idx_2013]+0.8, -1.0),
    fontsize=14, bbox=ann_style,
    arrowprops=dict(arrowstyle="->", color='0.45', linewidth=0.9),
    ha='left', va='center'
)

# Optional difference callout for most extreme difference (2009)
if euro_mask[idx_2009]:
    diff = abs(spain_vals[idx_2009] - euro_vals[idx_2009])
    diff_text = f"Gap: {diff:.1f} p.p. vs Euro‑Zone"
    x_left = spain_pos[idx_2009] + bar_width/2
    x_right = euro_pos[idx_2009] - bar_width/2
    mid_x = (x_left + x_right) / 2
    y_top = max(spain_vals[idx_2009], euro_vals[idx_2009]) + 0.4
    ax.plot([x_left, x_right], [y_top, y_top], color='0.4', linewidth=0.9, zorder=5)
    ax.text(mid_x, y_top + 0.15, diff_text, fontsize=12, ha='center', va='bottom', color='0.2')

# Direct in-chart identification for Spain and Euro (above first pair)
first_idx = 0
legend_x = spain_pos[first_idx] - 0.05
legend_y = ymax - 0.6
# Small color swatches using Rectangle patches
swatch_size = 0.14
ax.add_patch(Rectangle((legend_x, legend_y - 0.1), swatch_size, 0.45*swatch_size,
                       transform=ax.transData, color=color_spain, zorder=6))
ax.text(legend_x + swatch_size + 0.06, legend_y - 0.05, "Spain", fontsize=13, va='bottom')
ax.add_patch(Rectangle((legend_x + 0.9, legend_y - 0.1), swatch_size, 0.45*swatch_size,
                       transform=ax.transData, color=color_euro, zorder=6))
ax.text(legend_x + 0.9 + swatch_size + 0.06, legend_y - 0.05, "Euro‑Zone avg.", fontsize=13, va='bottom')

# Note for Euro‑Zone data unavailability under the plot (concise)
fig.text(0.02, 0.01, "Note: Euro‑Zone avg. not available after 2011.",
        transform=fig.transFigure, ha='left', fontsize=12, color='0.2')

# Source attribution bottom-left (unobtrusive)
fig.text(0.02, 0.005, "Source: national releases / Euro‑Zone aggregates",
        transform=fig.transFigure, ha='left', fontsize=11, color='0.35')

# Presenter notes (accessible caption) bottom-center in small type
presenter_note = ("Presenter note: Spain moved from small surpluses in 2005–07 to deep deficits after 2008, "
                  "peaking in 2009. 2012–2014 bars are government targets, not reported outturns.")
fig.text(0.5, 0.01, presenter_note, ha='center', fontsize=10, color='0.25')

# Clean up gridlines: only horizontal, light and subtle
ax.xaxis.grid(False)
ax.yaxis.grid(True, which='major', color='0.9', linestyle='-', linewidth=0.9)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
ax.spines['left'].set_linewidth(0.8)
ax.spines['bottom'].set_linewidth(0.8)

# Tight layout with generous margins
plt.subplots_adjust(top=0.88, left=0.12, right=0.92, bottom=0.08)

plt.savefig("generated/spain_factor2_bar2/spain_factor2_bar2_design.png", dpi=300, bbox_inches="tight")