__author__ = 'viktor'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Node, File
import os
import shutil
import json

class Exporter:
    def __init__(self, db_user, db_passwd, db, project_path, data_path):
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db = db
        self.project_path = project_path
        self.data_path = data_path

        self.file_storage_path = os.path.join(self.data_path, 'files')

        # Create an engine.
        self.engine = create_engine('mysql://%s:%s@localhost/%s' % (db_user, db_passwd, db), echo=False, encoding='latin1')

        # Create a session fabrica or static container.
        self.Session = sessionmaker(bind=self.engine)

        # Get a session.
        self.session = self.Session()

        if os.path.exists(self.data_path):
            shutil.rmtree(self.data_path)
        os.makedirs(self.data_path)
        os.makedirs(self.file_storage_path)

    def prepare_files(self):
        print 'It processes files.'
        file_list = self.session.query(File).all()
        dict_file_list = []
        for file in file_list:
            file_path = file.uri.replace('public://', self.project_path + '/')
            try:
                shutil.copyfile(file_path, '%s/%d.%s' % (self.file_storage_path, file.fid, file.filemime.split('/')[1]))
                dict_file = {
                    'uuid': file.uuid,
                    'uid': file.uid,
                    'fid': file.fid,
                    'langcode': file.langcode,
                    'status': file.status
                }
                dict_file_list.append(dict_file)
            except:
                pass
        dict_file_list = [dict_file for dict_file in dict_file_list if dict_file['status'] == True]
        with open('%s/file_list.json' % self.data_path, 'wb') as fp:
            json.dump(dict_file_list, fp)

    def prepare_articles(self):
        article_list = self.session.query(Node).filter(Node.type == 'article').all()
        dict_article_list = []
        for article in article_list:
            dict_article = {
                'uuid': article.uuid,
                'nid': article.nid
            }
            dict_article_list.append(dict_article)
        with open('%s/article_list.json' % self.data_path, 'wb') as fp:
            json.dump(dict_article_list, fp)