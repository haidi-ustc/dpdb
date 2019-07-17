#/usr/bin/env python
#coding:utf8
import os
import time
import uuid
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from dbconfig import DBConfig,get_database
from monty.serialization import loadfn,dumpfn
from monty.json import MSONable

class ElasticSearchDB(MSONable):
    def __init__(self, config_file=None, settings=None, index_mappings=None):
        
        '''

        :param index_name:
        :param index_type: 
        '''
        
        if settings is None:
           self.dbcfg = DBConfig(config_file=config_file)
        else:   
           self.dbcfg = DBConfig(config_dict=settings)
        self._settings=self.dbcfg.settings
  
        self._index_name =self._settings['index_name']
        self._index_type =self._settings['index_type']
        self._host= self._settings['host']
        self._index_mappings= index_mappings
        self.es = get_database(self._settings)


    def as_dict(self):
        """Returns data dict of System instance"""
        d={"@module": self.__class__.__module__,
             "@class": self.__class__.__name__,
             "settings": self._settings
          }
        return d

    @property
    def db_settings(self):
        return self._settings

    @property
    def index_name(self):
        return self._index_name

    @property
    def index_type(self):
        return self._index_type

    def create_index(self):
        '''
        :param ex: Elasticsearch obj.
        :return:
        '''
        if self.es.indices.exists(index=self._index_name) is not True:
           ret = self.es.indices.create(index=self._index_name, body=self._index_mappings)
        else:
           ret = None
        return ret
     
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        ret ="index_name:\t%s\n"%self._index_name
        ret+="index_type:\t%s"%self._index_type
        return ret

    def insert_data(self,data):
        '''
        :param data: dict obj.
        :return:
        '''
        return self.es.index(index=self._index_name, doc_type=self._index_type, body=data)

    def insert_datas(self,datas):
        '''
        insert data into es
        :return:
        '''
        ret=[]
        for data in datas:
            ret.append(InsertData)
        return ret

    def insert_bulk_datas(self,datas):
        '''
        use bulk insert batch data into es
        :return:
        '''
        ACTIONS = []
        i = 1
        for line in datas:
            action = {
                "_index": self._index_name,
                "_type": self._index_type,
                "_id": uuid.uuid4(), 
                "_source": {
                    "datas": line['datas'],
                           }
                     }
            i += 1
            ACTIONS.append(action)
        ret, _ = bulk(self.es, ACTIONS, index=self._index_name, raise_on_error=True)
        return ret

    def delete_data(self,entry_id):
        '''
        delete an entry
        :param entry_id:
        :return:
        '''
        return self.es.delete(index=self._index_name, doc_type=self._index_type, id=entry_id)

    def get_data_by_id(self,entry_id):

        return self.es.get(index=self._index_name, doc_type=self._index_type,id=entry_id)


    def get_data_by_doc(self,doc=None):
        return self.es.search(index=self._index_name, doc_type=self._index_type, body=doc)


if __name__=="__main__":
   edb =ElasticSearchDB(config_file="db.yaml")

