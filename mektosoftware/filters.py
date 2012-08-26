#-*- coding: utf-8 -*-
from urlparse import urlparse

import misaka
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from . import app


class PygmentsRenderer(misaka.HtmlRenderer, misaka.SmartyPants):
    def block_code(self, text, lang):
        try:
          lexer = get_lexer_by_name(lang, stripall=True)
        except:
          lexer = get_lexer_by_name('text')
        formatter = HtmlFormatter(cssclass='highlight {0}'.format(lexer.name.lower()))
        return highlight(text, lexer, formatter)

md = misaka.Markdown(PygmentsRenderer(), extensions=misaka.EXT_FENCED_CODE | misaka.EXT_NO_INTRA_EMPHASIS)


@app.template_filter('markdown')
def markdown_filter(s):
    return md.render(s)

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
