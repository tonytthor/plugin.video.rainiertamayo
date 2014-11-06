import re

MAIN_URL = 'http://www.rainiertamayo.com'


class RainierTamayo:
    """RainierTamayo API class.

    Provides funtions to scrap videos from www.rainiertamayo.com 
    """

    def __init__(self):
        """Constuctor."""
        pass

    def get_newest(self):
        """Return all the newest videos.

        :returns: a dictionary {<label>: <url>}
        """
        newest = {}
        return newest

    def get_categories(self):
        """Return all the video categories.

        :returns: a dictionary {<label>: <url>}
        """
        categories = {}
        return categories

    def get_series(self):
        """Return all the TV series.

        :returns: a dictionary {<label>: <url>}
        """
        series = {}
        return series

    def get_category(self, category, page='1'):
        """Return all the videos for a given category.

        :param category: category's video
        :param page:     category page
        :returns: a dictionary {<label>: <url>} and next_page
        """
        videos = {}
        return video, None

    def get_serie(self, serie, season='1', page='1'):
        """Return all the videos for a given serie.

        :param category: category's video
        :param page:     category page
        :returns: a dictionary {<label>: <url>} and next_page
        """
        videos = {}
        return videos, None
