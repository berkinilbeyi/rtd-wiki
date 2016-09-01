from recommonmark.parser import CommonMarkParser

# Berkin: This allows using markdown files using sphinx (see
# http://docs.readthedocs.io/en/latest/getting_started.html#in-markdown)
source_parsers = {
  '.md': CommonMarkParser,
}

source_suffix = ['.md']

master_doc = 'README'

def setup(app):
  app.add_config_value('recommonmark_config', {
      'enable_auto_doc_ref': True}, True)
  app.add_transform(AutoStructify)
