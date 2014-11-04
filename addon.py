from xbmcswift2 import Plugin
import resources.lib.rainiertamayo as rainiertamayo


plugin = Plugin()
rntm = rainiertamayo.RainierTamayo()


@plugin.route('/')
def index():
    entries = {'newest': {'label' : 'Newest videos', 
                          'path' : 'index'},
               'movie': {'label': 'Movies',
                         'path': 'index'},
               'tv': {'label': 'TV Series',
                      'path': 'show_series'}}
    items = [{'label': entries[entry]['label'],
              'path': plugin.url_for(entries[entry]['path'])
             } for entry in entries.keys()]
    return items

@plugin.route('/genre')
def show_categories():
    categories = rntm.get_categories()
    items = [{'label': categories.get(category),
              'path': plugin.url_for('show_category',
                                     category = category,
                                     page = '1')
             } for category in categories]
    return plugin.finish(items, update_listing=True)

@plugin.cached()
@plugin.route('/genre/<category>/page/<page>')
def show_category(category, page):
    category, has_next = rntm.get_category(category, page)
    items = [{'label': categories.get(category),
              'path': plugin.url_for('show_category',
                                     category = category,
                                     page = '1')
             } for category in categories ]
    return plugin.finish(item, update_listing=True)


@plugin.route('/series/')
def show_series():
    series = rntm.get_series()
    items = [{'label': categories.get(category),
              'path': plugin.url_for('show_category',
                                     category = category,
                                     page = '1')
             } for category in categories ]
    return plugin.finish(item, update_listing=True)

@plugin.route('/movie/<video>')
def show_video(video):
    page = int(page)
    videos, next_page = get_videos(page)
    items = [make_item(video) for video in videos]

    if next_page:
        items.insert(0, {
            'label': 'Next >>',
            'path': plugin.url_for('show_videos', page=str(page + 1))
        })

    if page > 1:
        items.insert(0, {
            'label': '<< Previous',
            'path': plugin.url_for('show_videos', page=str(page - 1))
        })

    return plugin.finish(items, update_listing=True)

@plugin.route('/play/<video>')
def play_video(video):
    playback_url = rntm.get_video_url(video)
    return plugin.set_resolved_url(playback_url)

def get_metadata(refresh=False):
    metadata = rntm.get_metadata(refresh)
    return metadata

if __name__ == '__main__':
    try:
        plugin.run()
    except NetworkError, e:
        plugin.log.error(e)
