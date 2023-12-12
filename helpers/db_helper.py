import threading
import time

import pymysql
from threading import Thread, get_ident
from dbutils.pooled_db import PooledDB
from config.config import DB_Config

# 数据库连接池，多线程同时注意线程之间隔离和安全

class Local:
    def __init__(self):
        # self.stack = []   # 此处不能这样写，会先调用setattr陷入循环调用,用父类方法创建super(类名，实例对象）
        super(Local, self).__setattr__('stack', [])

    def __setattr__(self, key, value):
        tid = get_ident()

    def __getattr__(self, item):
        tid = get_ident()
        return self.stack[tid][item]


class SqlHelper:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=30,  # 最多打开多少连接
            mincached=2,  # 默认最少打开多少连接
            blocking=True,     # 没有可用连接后是否阻塞等待，默认True， False不等待就返回报错
            ping=0,    # 是否定时测试连接可用性
            host=DB_Config.host,
            port=int(DB_Config.port),
            user=DB_Config.user,
            password=DB_Config.password,
            database=DB_Config.database,
            # charset='utf-8'
        )
        # self.local = threading.local   #  这里在在class内部了，因此，这个local对象只有一个，属于main-thread里的实例对象
        self.local = threading.local()
        # print(id(self.local))

    def open(self):
        conn = self.pool.connection()
        cur = conn.cursor()
        return conn, cur

    def close(self, conn, cur):
        conn.close()
        cur.close()

    def fetchone(self, sql, *args):
        conn, cur = self.open()
        cur.execute(sql, *args)
        res = cur.fetchone()
        self.close(conn, cur)
        return res

    def fetchall(self, sql, *args):
        conn, cur = self.open()
        cur.execute(sql, *args)
        res = cur.fetchall()
        self.close(conn, cur)
        return res

    def __enter__(self):
        conn, cursor = self.open()
        rv = getattr(self.local, 'stack', None)    # getattr(对象名，属性名，如果属性不存在的默认返回值) 如果属性存在就返回属性值
        if not rv:              # false 代表self.local对象无stack属性，那就创建这个属性，给它分配一个list，放入线程刚刚取到的con,cur组成的tuple
            self.local.stack = [(conn, cursor)]
            # print('local id %s'%id(self.local))
            # print('stack id %s'%id(self.local.stack))

        else:
            rv.append((conn, cursor))   # 如果嵌套了,需要append，一个线程打开多个db连接
            self.local.stack = rv
        return cursor    #  enter打开时只需要返回cursor就行

    def __exit__(self, exc_type, exc_val, exc_tb):  # 单例模式下多线程，应该根据不同的线程关闭对应的conn和cursor
        rv = getattr(self.local, 'stack', None)
        if not rv:
            # del self.local.stack
            return
        # print(' poping %s' %repr(self.local.stack))
        conn, cursor = self.local.stack.pop()   # 删除此次会话所对应的元组
        cursor.close()
        conn.close()


db = SqlHelper()


# def task(num):
#         with db as cur:
#             cur.execute('select * from f1.f1')
#             res = cur.fetchall()
#             # time.sleep(3)\
#             print(res)
#
# #
# for i in range(5):
#     t = Thread(target=task, args=(i,))
#     t.start()
#

# 解析，单例模式下多线程变量隔离
# 本例子中，local对象是个公共资源，只在db对象里创建了一份，但是stack对象每个线程copy一份，互不干扰，可以用id()来确认
# 另一种线程局部变量隔离方法是创建一个自定义local类，里面配置setattr,getattr，然后用一个dict来存放所有线程的变量，local.storage={thread-1:{'name':'jack-1'},thread-2:{'name':'jack-2'}}

# 退出时判断本线程的stack列表里是否还有元素，没有的话就return了，不用再关了；有的话就取出最后一个元组,其实也只有一个元组，也就是子线程刚刚放进去哪个，然后关闭这个conn+cur，堆栈规则LIFO
# enter时候打开一个conn,cur, 然后执行sql,代码段结束马上exit,关闭刚刚放进去那一对
#  pop()是删除并返回元素值(元组自动拆开给2个变量)

# None、空列表[]、空字典{}、空元组()、0等一系列代表空和无的对象会被转换成False。’’’
# 多线程之间共享全局变量，所以不隔离的时候线程拿到的结果不一定是自己修改后的内容


