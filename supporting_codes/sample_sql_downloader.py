import sqlalchemy
import urllib.parse
import pandas as pd
import urllib
params =urllib.parse.quote_plus('Driver={ODBC Driver 13 for SQL Server};'
                                'Server=tcp:shopifyai.database.windows.net,1433;'
                                'Database=ShopifyAI;'
                                'Uid=aiadmin;Pwd=kfk9072p!;'
                                'Encrypt=yes;'
                                'TrustServerCertificate=no;'
                                'Connection Timeout=30;')
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
pd.read_sql(f"select * from salesanalytics where cid = {client_id}",engine)
