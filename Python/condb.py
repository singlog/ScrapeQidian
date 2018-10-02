'''
Created on Oct 21, 2017

@author: zyrgz
'''
import pymysql.cursors
import json

class Connection:
    
    def __init__(self):
        with open('../config/mysql_config') as f:
            param = json.load(f)
            param['cursorclass'] = pymysql.cursors.DictCursor
            self.conn = pymysql.connect(**param)
            self.cursor = self.conn.cursor() 
        
    def saveBookInfo(self,**info):
        sql = "INSERT INTO books("
        for k in info.keys():
            sql += ( k + ", ")
        sql = sql[0:len(sql)-2]    
        sql +=  ")\nVALUES(" 
        
        for v in info.values():
            sql += ( repr(v) + ", " )
        sql = sql[0:len(sql)-2]      
        sql += ')'
        
        self.cursor.execute(sql)
        self.conn.commit()
    
    def end(self):
        self.conn.close()