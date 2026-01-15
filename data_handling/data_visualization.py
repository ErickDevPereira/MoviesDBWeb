import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List

def apply_style(color: str, is_visible: bool = True, label_size: int = 16) -> None:

    ax: plt.Axes = plt.gca()

    ax.tick_params(axis = 'x', colors = color, labelsize = label_size)
    ax.tick_params(axis = 'y', colors = color, labelsize = label_size)

    if is_visible:
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
    else:
        for spine in ax.spines.values():
            spine.set_visible(is_visible)

def score_histogram(score_set: List[float], number_of_intervals: int, path: str, color: str = "#00B894", font_size: int = 18, border_color: str = 'white') -> None:

    apply_style(color = border_color)
    plt.xlabel("Score", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.ylabel("Quantity", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.xlim(-1, 11)
    plt.hist(score_set, bins = number_of_intervals, color = color, edgecolor = 'black')
    plt.tight_layout()
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf() #Important if we want the figures to be independent of each other

def year_bar(base: List[int], response: List[int | float], path: str, color: str = "#00B894", font_size: int = 18, border_color: str = 'white') -> None:

    apply_style(color = border_color)
    plt.xlabel("Year", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.ylabel("Average score", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.bar(base, response, color = color)
    plt.tight_layout()
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf()

def year_curve(base: List[int], response: List[int], path: str, color: str = "#00B894", font_size: int = 18, marker_size:int = 25, marker_color: str = "#D15555", border_color: str = 'white') -> None:

    apply_style(color = border_color)
    plt.xlabel("Year", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.ylabel("Quantity", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    min_year: int = min(base)
    max_year: int = max(base)
    plt.xlim(min_year - 1, max_year + 1)
    plt.plot(base, response, color = color, linewidth = 3, marker = '*', markersize = marker_size, markerfacecolor = marker_color, markeredgewidth = 0)
    plt.tight_layout()
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf()