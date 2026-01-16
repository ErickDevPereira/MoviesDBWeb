import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List

def apply_style(color: str,
                is_visible: bool = True,
                label_size: int = 16) -> None:

    """
    Explanation:
    This function is responsible for setting the layout of the graph.

    Parameters:
    color: color of the layout, including numbers and border
    is_visible: boolean that defines if the border will be visible or not.
    label_size: size of the numbers.
    """

    ax: plt.Axes = plt.gca()

    #Setting color and size of the numbers.
    ax.tick_params(axis = 'x', colors = color, labelsize = label_size)
    ax.tick_params(axis = 'y', colors = color, labelsize = label_size)

    if is_visible:
        for spine in ax.spines.values():
            spine.set_edgecolor(color) #Painting the borders
            spine.set_linewidth(2) #Expanding the border.
    else:
        for spine in ax.spines.values():
            spine.set_visible(is_visible)

def score_histogram(score_set: List[float],
                    number_of_intervals: int,
                    path: str,
                    color: str = "#00B894",
                    font_size: int = 18,
                    border_color: str = 'white') -> None:

    """
    Explanation:
    This function defines a histogram graph through matplotlib. It was configured
    such that the histogram will have as interval some range of score values from 0 to 10, while
    the y axis will have the quantity of movies inside some interval.
    
    Parameters:
    score_set: list of scores to be analyzed.
    number_of_intervals: number of intervals that will represent the data.
    path: relative path to the placement of that image with its oficial name.
    color: color of each column.
    font_size: size of the label.
    border_color: color of the border of the columns.
    """

    apply_style(color = border_color)
    plt.xlabel("Score", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.ylabel("Quantity", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.xlim(-1, 11) #Minimum and maximum limits for the horizontal axis.
    plt.hist(score_set, bins = number_of_intervals, color = color, edgecolor = 'black')
    plt.tight_layout() # This function will fix layout issues automatically.
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf() #Important if we want the figures to be independent of each other

def year_bar(base: List[int],
             response: List[int | float],
             path: str,
             color: str = "#00B894",
             font_size: int = 18,
             border_color: str = 'white') -> None:

    """
    Explanation:
    Generates a bar graph with each year on the x axis and the average score of movies at that year on 
    the y axis.

    Parameters:
    base: years of the movies.
    response: average year for each set of movies at a year inside base at that same position.
    color: color of the bar.
    font_size: size of the label.
    border_color: color of the border of the bar plot.
    """

    apply_style(color = border_color)
    plt.xlabel("Year", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    plt.ylabel("Average score", fontdict = {"family": "monospace", "size": font_size, "color": border_color})
    base_str: List[str] = [str(element) for element in base] #This list will present the set of years related to all movies registered by the user.
    plt.bar(base_str, response, color = color)
    plt.tight_layout()
    plt.savefig(path, dpi = 75, transparent = True)
    plt.clf()

def year_curve(base: List[int],
               response: List[int],
               path: str,
               color: str = "#00B894",
               font_size: int = 18,
               marker_size:int = 25,
               marker_color: str = "#D15555",
               border_color: str = 'white') -> None:

    """
    Explanation:
    Curve with the quantity of registered movies for each year. x axis has the years
    while y axis will have the quantities for each year. Each year with a movie in it
    will have a star.

    Parameters:
    base: list with years
    response: list with quanitty per year with same order as the base parameter.
    color: color of the curve.
    font_size: size of the label.
    marker_size: size of the star.
    marker_color: color of the star.
    border_color: color of border, labels and numbers.
    """

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