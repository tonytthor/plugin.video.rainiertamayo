import os
import sys

from xbmcswift2 import Plugin
import xbmcaddon

__addonname__ = 'plugin.video.rainiertamayo'
__addonpath__ = xbmcaddon.Addon(id=__addonname__).getAddonInfo('path')

# append lib directory
sys.path.append(os.path.join(__addonpath__, 'resources', 'lib'))
from rainiertamayo import RainierTamayo


plugin = Plugin()
rainiertamayo = RainierTamayo()

# TODO : Factor function get_<item>
# for item in ITEMS = ['newests', 'categories', 'series']


@plugin.route('/')
def index():
    """Display plugin's main menu."""
    entries = {'Newest Videos': 'get_newests',
               'Movies': 'get_movies',
               'Categories': 'get_categories',
               'TV Series': 'get_series'}
    items = [{'label': entry,
              'path': plugin.url_for(entries[entry])
              } for entry in entries]
    return plugin.finish(items)


@plugin.cached_route('/newests')
def get_newests():
    """Display newests videos."""
    videos = rainiertamayo.get_newests()
    items = [{'label': video['label'],
              'path': plugin.url_for('get_video',
                                     url=video['path']),
              'thumbnail': video['thumbnail']
              } for video in videos]
    return plugin.finish(items)


@plugin.cached_route('/movies', TTL=30)
def get_movies():
    pass


@plugin.cached_route('/categories')
def get_categories():
    """Display all available categories."""
    categories = rainiertamayo.get_categories()
    items = [{'label': category['label'],
              'path': plugin.url_for('get_category',
                                     category=category['label'],
                                     page='1')
              } for category in categories]
    return plugin.finish(items)


@plugin.cached_route('/series', TTL=90)
def get_series():
    """Display all available series."""
    series = rainiertamayo.get_series()
    print(series)
    items = [{'label': serie['label'],
              'path': plugin.url_for('get_serie',
                                     serie=serie['label'],
                                     season='1',
                                     page='1')
              } for serie in series]
    return plugin.finish(items)


@plugin.route('/categories/<category>/<page>')
def get_category(category, page='1'):
    """Display videos for the provided category.

    :param category: category to display.
    :param page:     category page to display."""
    videos, next_page = rainiertamayo.get_category(category, page)

    items = [{'label': video['label'],
              'path': plugin.url_for('get_video',
                                     url=video['path']),
              'thumbnail': video['thumbnail']
              } for video in videos]
    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('get_category',
                                                category=category,
                                                page=int(page)+1)
                         })

    if int(page) > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('get_category',
                                                category=category,
                                                page=int(page)-1)
                         })
    return plugin.finish(items)


@plugin.route('/series/<serie>/<season>/<page>')
def get_serie(serie, season='1', page='1'):
    """Display videos for the provided serie.

    :param serie:  serie to display.
    :param season: season to display.
    :param season: page to display."""
    videos, next_page = rainiertamayo.get_serie(serie, season, page)

    items = [{'label': video['label'],
              'path': plugin.url_for('get_video',
                                     url=video['path'])
              } for video in videos]
    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('get_serie',
                                                season=season,
                                                page=int(page)+1)
                         })

    if page > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('get_serie',
                                                season=season,
                                                page=int(page)-1)
                         })
    return plugin.finish(items)


@plugin.route('/videos/<page>')
def get_videos(page='1'):
    """Display videos for the provided page.

    :param page: page to display."""
    videos, next_page = get_videos(page)
    items = [make_item(video) for video in videos]

    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('show_videos', page=int(page)+1)
                         })

    if page > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('show_videos', page=int(page)-1)
                         })
    return plugin.finish(items)


@plugin.route('/video/<url>')
def get_video(url):
    """Display the provided video.

    :param video: video to display."""
    media_url = rainiertamayo.get_video(url)
    plugin.log.info('Playing url: %s' % media_url)
    plugin.set_resolved_url(media_url)


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception, e:
        plugin.log.error(e)
