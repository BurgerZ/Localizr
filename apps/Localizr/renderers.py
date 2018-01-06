import re
from datetime import datetime
from rest_framework import renderers
from xml.sax.saxutils import escape


class KeyStringBaseRenderer(renderers.BaseRenderer):

  def process_key(self, key):
    raise NotImplementedError('process_key() must be implemented.')

  def process_value(self, value):
    raise NotImplementedError('process_value() must be implemented.')

  def attribution_text(self):
    return \
    "Generated by Localizr. \n" \
    "(https://github.com/michaelhenry/Localizr)\n" \
    "%s\n" % (datetime.utcnow().strftime("%Y-%m-%d %H:%M %Z"))


class KeyStringIOSRenderer(KeyStringBaseRenderer):

  media_type  = 'text/plain'
  format      = 'ios'
  charset     = 'utf-8'
  key_name    = 'key'
  value_name  = 'value'

  def process_key(self, key):
    return str(key)

  def process_value(self, value):

    v = str(value)
    v = v.replace("%s", "%@")
    
    #search for existing android sequence pattern and convert it to ios.
    sequence_pattern_regex_for_android = re.compile('([%]\d+[$]\d+[s])', re.S)
    v = sequence_pattern_regex_for_android.sub(lambda m: re.sub(r'\d+s', '@', m.group()), v)
    return v

  def render(self, data, media_type=None, renderer_context=None):

    if isinstance(data, dict):
      return '\n'.join('\"%s\" = \"%s\";' % (key, val) for (key, val) in data.items())
    elif isinstance(data, list):
      r = '/*%s*/\n\n' % self.attribution_text()
      r += '\n'.join('\"%s\" = \"%s\";' % (self.process_value(val[self.key_name]), 
        self.process_value(val[self.value_name])) for (val) in data)
      return r.encode(self.charset)


class KeyStringAndroidRenderer(KeyStringBaseRenderer):

  media_type  = 'application/xml'
  format      = 'android'
  charset     = 'utf-8'
  key_name    = 'key'
  value_name  = 'value'

  def process_key(self, key):
    pattern     =   '[^0-9a-zA-Z]+'
    
    k = str(key).lower()
    k = re.sub(pattern, '_', k).lower()
    return k

  def process_value(self, value):

    v = str(value)
    v = v.replace("%@", "%s")

    #search for existing ios sequence pattern and convert it to android.
    sequence_pattern_regex_for_ios = re.compile('([%]\d[$][@])', re.S)
    v = sequence_pattern_regex_for_ios.sub(lambda m: m.group().replace('@',"1s"), v)
    v = escape(v)
    return v

  def render(self, data, media_type=None, renderer_context=None):
      
    r = '<resources>'
    if isinstance(data, dict):
      r += '\n'.join('\t<string name=\"%s\">%s</string>' % (key, val) for (key, val) in data.items())
    elif isinstance(data, list):
      r += '\n<!--%s-->\n\n' % self.attribution_text()
      r += '\n'.join('\t<string name=\"%s\">%s</string>' % (self.process_key(val[self.key_name]), 
        self.process_value(val[self.value_name])) for (val) in data)
      r += '\n'
    r += '</resources>'
    return r.encode(self.charset)
