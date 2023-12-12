from helpers.db_helper import db, SqlHelper


# def task(num):
#     with db1 as cur:
#         cur.execute('select * from f1.f1')
#         print(id(cur))
#             # v1 = cur.fetchone('select * from f1.f1')
#
#

if __name__ == '__main__':
    db1 = db
    res = db1.fetchall('select * from f1.f1')
    print(res)