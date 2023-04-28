import pymysql
from pymysql import cursors

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '',
    'db': 'housingwebsiteproject',
    'charset': 'utf8mb4',
    # 資料庫內容以字典格式輸出
    'cursorclass': pymysql.cursors.DictCursor,
}


# 連接資料庫
def link_sql():
    # 連接資料庫
    db = pymysql.connect(**config)
    # cursor()方法獲取操作游標
    cursor = db.cursor()

    try:
        return db, cursor

    except ConnectionError:
        print(f"資料庫訪問失敗")
