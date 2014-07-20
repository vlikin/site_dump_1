__author__ = 'viktor'

from lib import Exporter
import os

data_path = os.path.join(os.path.dirname(__file__), 'data')
project_path = '/var/www/shelepen/drupal/sites/default/files'
exporter = Exporter('root', '', 'shelepen', project_path, data_path)
exporter.prepare_files()
exporter.prepare_articles()
