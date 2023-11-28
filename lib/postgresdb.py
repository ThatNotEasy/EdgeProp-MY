import configparser
import psycopg2

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

DB_HOST = config['POSTGRESQL']["DB_HOST"]
DB_DATABASE = config['POSTGRESQL']["DB_DATABASE"]
DB_USERNAME = config['POSTGRESQL']["DB_USERNAME"]
DB_PASSWORD = config['POSTGRESQL']["DB_PASSWORD"]
DB_PORT = config['POSTGRESQL']["DB_PORT"]


class POSTGRESQL:

    def __init__(self,
                 hostname=DB_HOST,
                 dbname=DB_DATABASE,
                 username=DB_USERNAME,
                 password=DB_PASSWORD,
                 port=DB_PORT
                 ):
        self.hostname = hostname
        self.dbname = dbname
        self.username = username
        self.password = password
        self.port = port
        try:
            self.conn = self.connect()
        except Exception as err:
            print("DB CLOSE")

    def connect(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host=str(self.hostname),
                database=str(self.dbname),
                user=str(self.username),
                password=str(self.password),
                port=int(self.port)
            )
            return conn
        except Exception as err:
            conn.close()
            print("DB error on SQLPOSTL:", err)
            return None

    def query(self, sql="", args=(), one=False):
        cur = self.conn.cursor()
        cur.execute(sql, args)

        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()

        return (r[0] if r else None) if one else r

    def execute(self, sql, args=()):
        cur = self.conn.cursor()
        cur.execute(sql, args)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
