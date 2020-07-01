import pymysql
import cx_Oracle



def get_connection():
    conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="password", db='yours', charset='utf8')
    return conn


def free(conn, cursor):
    cursor.close()
    conn.close()


def get_connection_oracle():
    conn = cx_Oracle.connect('userID/pwd@localhost/ORCL')
    return conn