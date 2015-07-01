# encoding: utf-8

"""
  zh			  Chinese
  es			  Spanish
  id			  Indonesian
  nl			  Dutch
  ru			  Russian
  en			  English
  sv			  Swedish
  fr			  French
  hu			  Hungarian
  ar			  Arabic
  it			  Italian
  fi			  Finnish
  nb			  Norwegian (Bokmål)
  da			  Danish
  vi			  Vietnamese
  pt			  Portuguese
  de			  German
  ko			  Korean
  no			  Norwegian

"""

LANG_BY_DOMAINS = {
    'cn': 'zh',
    'es': 'es',
    'id': 'id',
    'nl': 'nl',
    'ru': 'ru',
    'uk': 'en',
    'us': 'en',
    'se': 'sv',
    'fr': 'fr',
    'hu': 'hu',
    'ae': 'ar',
    'it': 'it',
    'fi': 'fi',
    'no': 'no',
    'dk': 'da',
    'vn': 'vi',
    'pt': 'pt',
    'de': 'de',
    'ko': 'ko'
}


def try_to_resolve_lang_by_domain(url):
    from urlparse import urlparse
    parsed = urlparse(url)
    if parsed.netloc:
        domain = parsed.netloc.split('.')[-1]
        if domain:
            if domain in LANG_BY_DOMAINS:
                return LANG_BY_DOMAINS[domain]
    return None