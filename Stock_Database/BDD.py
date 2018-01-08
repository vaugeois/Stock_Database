# -*- coding: utf-8 -*-
"""
@author: Antoine Vaugeois
"""

import sqlite3
import pandas as pd
import numpy as np
from API_Request import asset_data

class BDD:
    
    """
    This class is representing a database. All the following functions
    allows to create a database, insert datas into it, and get datas as
    different datatypes.
    """
    
    def __init__(self,BDD):
        
        """
        Just defining the name of the databas in order to retrieve it later.
        """
        
        self.Name_BDD=BDD
            
    def create_table(self, Name_Table):
        
        """
        Allows the user to create a database with a specified name.
        If a table with a similar name already exists, an error message
        will be displayed.
        """
        
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS"""+'"'+Name_Table+'"'+"""(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            date DATE,
            open REAL,
            close REAL,
            high REAL,
            low REAL,
            volume REAL
            )        
            """)
            conn.commit()
        except sqlite3.OperationalError:
            print('Error : the table already exists')
        except Exception as e:
            print("Error")
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def insert_data(self, data, Name_Table):
        
        """
        Insert specific datas in a specific database.
        Datas must be list of lists like this following :
                [(Date, Open, Close, High, Low, Volume), ...]
        """
        
        conn=sqlite3.connect(self.Name_BDD)
        cursor=conn.cursor()
        cursor.executemany("""
        INSERT OR REPLACE INTO """+'"'+Name_Table+'"'+"""
        (date, open,close,high,low,volume) VALUES(?, ?, ?, ?, ?, ?)""", data)
        cursor.execute("""DELETE FROM """+'"'+Name_Table+'"'+""" WHERE rowid NOT IN (SELECT min(rowid) FROM """+Name_Table+""" GROUP BY date, open, close, high, low, volume);""")
        conn.commit()
        
    def get_data_bdd_as_array(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            req="SELECT date, open, high, low, volume FROM "+Name_Table+" ORDER BY date"
            cursor.execute(req)
        except Exception as e:
            print("Error")
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

    def get_data_bdd_as_df(self,Name_Table):
        try:
            conn=sqlite3.connect(self.Name_BDD)
            df=pd.read_sql_query("SELECT date, open, close, high, low, volume FROM "+Name_Table+" ORDER BY date",conn)
        except Exception as e:
            print("Erreur")
            raise e
        return df

    def add_column_bdd(self,Name_Table,Name_Column,df):
        """
        Add a new column in the database for example to add an indicator
        and add datas to the new column
        """
        try:
            conn=sqlite3.connect(self.Name_BDD)
            cursor=conn.cursor()
            req="ALTER TABLE "+Name_Table+" ADD COLUMN "+Name_Column+" INTEGER"
            cursor.execute(req)
        except:
            print("Column already exist")
            pass
        conn=sqlite3.connect(self.Name_BDD)
        cursor=conn.cursor()
        for index, row in df.iterrows():
        	req="UPDATE "+Name_Table+" SET "+Name_Column+"="+str(row[Name_Column])+" WHERE DATE="+"'"+str(index)[0:10]+"'"
        	cursor.execute(req)
        conn.commit()
     

 