import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

# Berkin: This allows using markdown files using sphinx (see
# http://docs.readthedocs.io/en/latest/getting_started.html#in-markdown)
source_parsers = {
  '.md': CommonMarkParser,
}

source_suffix = ['.md', '.rst', '.txt']

master_doc = 'README'

def setup(app):
  # Berkin: The following is to allow the links with .md extension to be
  # converted to .html when hosted on RtD. This seems to be a more recent
  # feature so had to add a dependency for 0.4.0.
  app.add_config_value('recommonmark_config', {
      'enable_auto_doc_ref': True}, True)
  app.add_transform(AutoStructify)
