import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List

def apply_style(color: str, is_visible: bool = True) -> None:

    ax = plt.gca()

    ax.tick_params(axis = 'x', colors = color)
    ax.tick_params(axis = 'y', colors = color)

    if is_visible:
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
    else:
        for spine in ax.spines.values():
            spine.set_visible(is_visible)

def score_histogram(score_set: List[float], number_of_intervals: int, path: str, color: str = "#2CA6F1", font_size: int = 18) -> None:

    apply_style(color = color)
    plt.xlabel("Quantity", fontdict = {"family": "monospace", "size": font_size, "color": color})
    plt.ylabel("Score", fontdict = {"family": "monospace", "size": font_size, "color": color})
    plt.xlim(-1, 11)
    plt.hist(score_set, bins = number_of_intervals, color = color)
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf() #Important if we want the figures to be independent of each other

def year_bar(base: List[int], response: List[int], path: str, color: str = "#2CA6F1", font_size: int = 18):

    apply_style(color = color)
    plt.xlabel("Year", fontdict = {"family": "monospace", "size": font_size, "color": color})
    plt.ylabel("Average score", fontdict = {"family": "monospace", "size": font_size, "color": color})
    plt.bar(base, response, color = color)
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf()