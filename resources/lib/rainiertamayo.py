import re

import dryscrape
from BeautifulSoup import BeautifulSoup
from urllib import unquote

MAIN_URL = 'http://www.rainiertamayo.com'


class RainierTamayo:
    """RainierTamayo API class.

    Provides funtions to scrap videos from www.rainiertamayo.com 
    """

    def __init__(self):
        """Constuctor."""
        self.session = dryscrape.Session(base_url=MAIN_URL)
        """session"""

    def get_newest(self):
        """Return all the newest videos.

        :returns: a dictionary {<label>: <url>}
        """
        html_tree = self.get_html_tree()

        newest = []

        # start parsing
        main_elem = html_tree.find('div', {'id':'main'} )
        for clip_elem in main_elem.findAll('a', {'class':'clip-link'}):
            title = clip_elem.get('title')
            url = clip_elem.get('href')
            img = clip_elem.find('img').get('src')

            newest.append({'label': title, 
                           'path': url,
                           'thumbnail': img})
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

    def get_video(self, url):
        """Return all the videos for a given serie.

        :param url: URL

        :returns: the media file's url
        """
        html_tree = self.get_html_tree(url)

        # HTML 5 <video> tag
        video_elem = html_tree.find('video')
        if video_elem:
            source_elem = video_elem.find('source')
            media_url = source_elem.get('src')
        else:
            # JavaScript <embed> tag
            embed_elem = html_tree.find('embed')
            media_url = unquote(embed_elem.get('flashvars'))

        return media_url

    def get_html_tree(self, url=MAIN_URL):
        """Return HTML tree as url is browse

        :param url: URL to browse

        :returns: an HTML tree
        """
        html = ""
        try:
            self.session.visit(url)
            html = self.session.body()
        except:
            raise NetworkError
        else:
            html_tree = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
            return html_tree
