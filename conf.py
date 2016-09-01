from recommonmark.parser import CommonMarkParser

# Berkin: This allows using markdown files using sphinx (see
# http://docs.readthedocs.io/en/latest/getting_started.html#in-markdown)
source_parsers = {
  '.md': CommonMarkParser,
}

source_suffix = ['.rst', '.md']
