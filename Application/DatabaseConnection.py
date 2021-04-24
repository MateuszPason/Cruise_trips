import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'..\..\..\instantclient_19_10')
connection = cx_Oracle.connect(user='ADMIN', password='Shipsproject01', dsn='ships_high')
cursor = connection.cursor()
