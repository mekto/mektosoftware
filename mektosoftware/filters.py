#-*- coding: utf-8 -*-
from markdown import markdown
from urlparse import urlparse

from . import app


@app.template_filter('markdown')
def markdown_filter(s):
    return markdown(s, extensions=['codehilite(guess_lang=False)'])

@app.template_filter('parse_video_url')
def parse_video_url_filter(url):
    rv = dict(service=None, video_id=None)
    url_data = urlparse(url)
    if url_data.netloc.endswith('vimeo.com'):
        rv['service'] = 'vimeo.com'
        rv['video_id'] = url_data.path[1:]
    return rv

@app.template_filter('format_date')
def format_date_filter(date):
    months = [u'stycznia', u'lutego', u'marca', u'kwietnia', u'maja', u'czerwca', u'lipca', u'sierpnia', u'września', u'października', u'listopada', u'grudnia']
    return '{0} {1} {2}'.format(date.day, months[date.month-1], date.year)
