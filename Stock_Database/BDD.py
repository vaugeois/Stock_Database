# -*- coding: utf-8 -*-
"""
@author: Antoine Vaugeois
"""

import sqlite3
from API_Request import asset_data

class BDD:
    
    def __init__(self,BDD):
            self.Name_BDD=BDD
            
    def create_table(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS"""+'"'+Name_Table+'"'+"""(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            date TEXT,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume REAL
            )        
            """)
            conn.commit()
        except sqlite3.OperationalError:
            print('Erreur la table existe déjà')
        except Exception as e:
            print("Erreur")
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def insert_data(self,data,Name_Table):
        conn=sqlite3.connect(self.Name_BDD)
        cursor=conn.cursor()
        cursor.executemany("""
        INSERT INTO """+'"'+Name_Table+'"'+"""
        (date, open,close,high,low,volume) VALUES(?, ?, ?, ?, ?, ?)""", data)
        conn.commit()
        
    def get_data_bdd(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            req="SELECT * FROM "+Name_Table+" ORDER BY date"
            cursor.execute(req)
        except Exception as e:
            print("Erreur")
            conn.rollback()
            raise e
        rows=cursor.fetchall()
        liste=[]
        append=liste.append
        for row in rows:
            tmp=[]
            for j in range(1,7):
                tmp.append(row[j])
            append(tmp)
        return liste

#CREATE THE CLASS AND INITIALIZE DB         
cla=BDD("Asset.db")
#CREATE TABLE IF NOT EXIST
cla.create_table("Microsoft")
#GET DATAS FROM API
liste=asset_data("MSFT")
#STORE DATA IN THE TABLE
cla.insert_data(liste,"Microsoft")
#GET DATA FROM TABLE AS TABLE OF TABLE
value=cla.get_data_bdd("Microsoft")