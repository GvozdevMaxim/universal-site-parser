import psycopg2


class DbConnection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        DbConnection.__instance = None

    def __init__(self, dbname, user, password, host, port):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    def db_try_to_connect(self):
        try:
            return psycopg2.connect(dbname=self.__dbname, user=self.__user, password=self.__password, host=self.__host,
                                    port=self.__port)
        except:
            print('Can`t establish connection to database')

    def execute_from_table(self, db_name, cell, filter_var, where):
        with conn.cursor() as curs:
            try:
                curs.execute(f'SELECT {cell} FROM {db_name} WHERE {where}=%s', (filter_var,))
                return curs.fetchone()[0]
            except:
                print('The record was not taken from the table')

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
            except:
                print('Records were not inserted')


dbconnection = DbConnection(dbname='parcer_db', user='gastinha', password='Gastinh@', host='localhost', port='5432')
conn = dbconnection.db_try_to_connect()

