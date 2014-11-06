from xbmcswift2 import Plugin
from resources.lib.rainiertamayo import RainierTamayo


plugin = Plugin()
rainiertamayo = RainierTamayo()

# TODO : Factor function get_<item>
# for item in ITEMS = ['newest', 'categories', 'series']

@plugin.route('/')
def index():
    """Display plugin's main menu."""
    entries = {'Newest Videos': 'get_newest',
               'Movies': 'get_categories',
               'TV Series': 'get_series'}
    items = [{'label': entry,
              'path': plugin.url_for(entries[entry])
    } for entry in entries]
    return items


@plugin.route('/newest')
def get_newest():
    """Display newest videos."""
    videos = rainiertamayo.get_newest()
    items = [{'label': video,
              'path': plugin.url_for('get_video',
                                     video=videos[video])
    } for video in videos]
    return items


@plugin.route('/categories')
def get_categories():
    """Display all available categories."""
    categories = rainiertamayo.get_categories()
    items = [{'label': category,
              'path': plugin.url_for('get_category',
                                     category=categories[category])
    } for category in categories]
    return items


@plugin.route('/series')
def get_series():
    """Display all available series."""
    series = rainiertamayo.get_series()
    items = [{'label': serie,
              'path': plugin.url_for('get_serie',
                                     serie=series[serie])
    } for serie in series]
    return items

@plugin.route('/categories/<category>/<page>')
def get_category(category, page='1'):
    """Display videos for the provided category.
    
    :param category: category to display.
    :param page:     category page to display."""
    videos, next_page = rainiertamayo.get_category(category, page)

    items = [{'label': video,
              'path': plugin.url_for('get_video',
                                     video=videos[video])
    } for video in videos]
    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('get_category', page=str(page + 1))
        })
    
    if page > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('get_category', page=str(page - 1))
        })
    return items

@plugin.route('/series/<serie>/<season>/<page>')
def get_serie(serie, season='1', page='1'):
    """Display videos for the provided serie.
    
    :param serie:  serie to display.
    :param season: season to display.
    :param season: page to display."""
    videos, next_page = rainiertamayo.get_serie(serie, season, page)

    items = [{'label': video,
              'path': plugin.url_for('get_video',
                                     video=videos[video])
    } for video in videos]
    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('get_serie',
                                                season=season,
                                                page=str(page + 1))
        })
    
    if page > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('get_serie',
                                                season=season,
                                                page=str(page - 1))
        })
    return items


@plugin.route('/videos/<page>')
def get_videos(page='1'):
    """Display videos for the provided page.
    
    :param page: page to display."""
    page = int(page)
    videos, next_page = get_videos(page)
    items = [make_item(video) for video in videos]

    if next_page:
        items.insert(0, {'label': 'Next >>',
                         'path': plugin.url_for('show_videos', page=str(page + 1))
        })
    
    if page > 1:
        items.insert(0, {'label': '<< Previous',
                         'path': plugin.url_for('show_videos', page=str(page - 1))
        })
    return items
    

@plugin.route('/video/<video>')
def get_video(video):
    """Display the provided video.

    :param video: video to display."""
    items = get_video_items(category)
    return []

def play_video(video):
    """Play the video.

    :param video: video to play."""
    lecture = Lecture.from_url(url)
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % lecture.youtube_id
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)

if __name__ == '__main__':
    try:
        plugin.run()
    except Exception:
        plugin.log.error(e)
