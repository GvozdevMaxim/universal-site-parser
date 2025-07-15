import os
import mysql.connector
from mysql.connector import errorcode


class DbConnection:

    def __init__(self, database, user, password, host):
        self.__database = database
        self.__user = user
        self.__password = password
        self.__host = host

    def db_try_to_connect(self):
        try:
            return mysql.connector.connect(database=self.__database, user=self.__user, password=self.__password,
                                           host=self.__host)

        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    @staticmethod
    def execute_site_links_from_table(db_name, cell):
        with conn.cursor() as curs:
            try:
                curs.execute(f'SELECT {cell} FROM {db_name}')
                return curs.fetchall()

            except mysql.connector.ProgrammingError as err:
                if errorcode.ER_NO_SUCH_TABLE == err.errno:
                    print("No table exists")
                else:
                    print("Table exists")
                    print(err)

            except mysql.connector.Error as err:
                print("Some other error")
                print(err)

    @staticmethod
    def execute_from_table(db_name, cell, filter_var, where):
        with conn.cursor() as curs:
            try:
                curs.execute(f'SELECT {cell} FROM {db_name} WHERE {where}=%s', (filter_var,))
                return curs.fetchone()[0]


            except mysql.connector.ProgrammingError as err:
                if errorcode.ER_NO_SUCH_TABLE == err.errno:
                    print("No table exists")
                else:
                    print("Table exists")
                    print(err)

            except mysql.connector.Error as err:
                print("Some other error")
                print(err)

    @staticmethod
    def insert_into_table(db_name, collection):
        query = f"INSERT INTO {db_name} (res_id, link, title, content, nd_date, s_date, not_date) VALUES (%s, %s, %s, %s, %s ,%s, %s)"
        with conn.cursor() as curs:
            try:
                match len(collection):
                    case 1:
                        curs.execute(query, collection[0])
                    case _:
                        curs.executemany(query, collection)

                conn.commit()
                print(f"{len(collection)} записей успешно вставлены")
            except (mysql.connector.IntegrityError, mysql.connector.DataError) as err:
                print("DataError or IntegrityError")
                print(err)

            except mysql.connector.ProgrammingError as err:
                print("Programming Error")
                print(err)

            except mysql.connector.Error as err:
                print(err)


dbconnection = DbConnection(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host='db'
)
conn = dbconnection.db_try_to_connect()







