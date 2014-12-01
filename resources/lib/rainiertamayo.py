import re
import os

import dryscrape
from BeautifulSoup import BeautifulSoup
from urllib import unquote

MAIN_URL = 'http://www.rainiertamayo.com'


class NetworkError(Exception):
    pass

 
class RainierTamayo:
    """RainierTamayo API class.

    Provides funtions to scrap videos from www.rainiertamayo.com 
    """

    def __init__(self):
        """Constuctor."""
        self.session = dryscrape.Session(base_url=MAIN_URL)
        """session"""

    def get_newests(self):
        """Return all the newests videos.

        :returns: a dictionary {<label>: <url>}
        """
        videos = get_videos()

        return videos

    def get_movies(self):
        """Return all the movies videos.

        :returns: a dictionary {<label>: <url>}
        """
        videos = get_videos('movie')

        nav_elem = html_tree.find('a', {'class': 'nextpostslink'})

        return videos, nav_elem

    def get_categories(self):
        """Return all the video categories.

        :returns: a dictionary {<label>: <url>}
        """
        html_tree = self.get_html_tree()

        categories = []

        # start parsing
        main_elem = html_tree.find('div', {'class': 'tagcloud'})
        for cat_elem in main_elem.findAll('a'):
            name = cat_elem.getText()
            url = cat_elem.get('href')

            categories.append({'label': name, 
                               'path': url})
        return categories


    def get_series(self):
        """Return all the TV series.

        :returns: a dictionary {<label>: <url>}
        """
        html_tree = self.get_html_tree()

        series = []

        # start parsing
        series_elem = html_tree.find('ul', {'class': 'sub-menu'})
        for serie_elem in series_elem.findAll('li', recursive=False):
            link_elem = serie_elem.find('a')

            name = link_elem.getText()
            url = link_elem.get('href')

            series.append({'label': name,
                           'path': url})
        print(series)
        return series

    def get_category(self, category, page='1'):
        """Return all the videos for a given category.

        :param category: category's video
        :param page:     category page
        :returns: a dictionary {<label>: <url>} and next_page
        """
        url = os.path.join('genre', category, 'page', page)

        videos = get_videos(url)

        nav_elem = html_tree.find('a', {'class': 'nextpostslink'})

        return videos, nav_elem

    def get_serie(self, serie, season='1', page='1'):
        """Return all the videos for a given serie.

        :param category: category's video
        :param page:     category page
        :returns: a dictionary {<label>: <url>} and next_page
        """
        url = os.path.join('page', page, '?s="%s:+Season+%s"' % (serie, season))

        videos = get_videos(url)

        nav_elem = html_tree.find('a', {'class': 'nextpostslink'})

        return videos, nav_elem

    def get_videos(self, url='/'):
        """Return all the videos for a given url.

        :param url: URL

        :returns: the list of label/path/thumbnail for each video
        """

        videos = []
        html_tree = self.get_html_tree(url)

        # start parsing
        main_elem = html_tree.find('div', {'id': 'main'} )
        for clip_elem in main_elem.findAll('a', {'class': 'clip-link'}):
            title = clip_elem.get('title')
            url = clip_elem.get('href')
            img = clip_elem.find('img').get('src')

            videos.append({'label': title, 
                           'path': url,
                           'thumbnail': img})

        return videos

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
            media_url = media_url.split('|')[-1]

        return media_url

    def get_html_tree(self, url='/'):
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
