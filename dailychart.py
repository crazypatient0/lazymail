import os
import copy
import xlrd
import pymysql
import datetime
from xlrd import xldate_as_tuple


class ExcelData():
    # 初始化方法
    def __init__(self, data_path, sheetname):
        # 定义一个属性接收文件路径
        self.data_path = data_path
        # 定义一个属性接收工作表名称
        self.sheetname = sheetname
        # 使用xlrd模块打开excel表读取数据
        self.data = xlrd.open_workbook(self.data_path)
        # 根据工作表的名称获取工作表中的内容（方式①）
        self.table = self.data.sheet_by_name(self.sheetname)
        # 根据工作表的索引获取工作表的内容（方式②）
        # self.table = self.data.sheet_by_name(0)
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)
        # 获取工作表的有效行数
        self.rowNum = self.table.nrows
        # 获取工作表的有效列数
        self.colNum = self.table.ncols

    # 定义一个读取excel表的方法
    def readExcel(self):
        for i in range(self.rowNum):
            for j in range(self.colNum):
                # 获取单元格数据类型
                c_type = self.table.cell(i, j).ctype
                # 获取单元格数据
                c_cell = self.table.cell_value(i, j)
                if c_type == 1:
                    #抓取数据时需要定义定位点，定位点是表格中恒定不变的格子，在固定格式表格中，定位点就是数格子的起始点，
                    #数据抓取点都根据定位点来进行相对定位
                    a = c_cell.find('aaa')
                    b = c_cell.find('bbb')
                    if a != -1:
                        r1 = i
                        c = j
                    if b != -1:
                        r2 = i

        return r1, c, r2

    # 猛烈输出

    def output(self, tur):
        list1 = []
        list2 = []
        r1 = tur[0]
        c = tur[1]
        r2 = tur[2]
        dict = {}
        for k in range(r1, r2):
            dict[self.table.cell_value(k, 0)] = self.table.cell_value(k, c + 2)
            list1.append(self.table.cell_value(k, 0))
            list2.append(self.table.cell_value(k, c + 2))
        list1.reverse()
        list3 = copy.copy(list1[0:-1])
        #中间删去了我对list3的reverse处理，所以多了一次copy，请按需修改
        list4 = copy.copy(list3)
        return list4, list2


def checkdb(res, db_date):
    # print(db_date)
    # 准备exceldata,放入dict
    dict = {}
    for i in range(len(res[0])):
        dict[res[0][i]] = res[1][i]
    print('datasource:%s' % dict)

    # 查询现有字段放入resul1，然后放进list#####################################
    sql = "select COLUMN_NAME from information_schema.columns where table_name='rawin'"
    cursor.execute(sql)
    result1 = cursor.fetchall()
    # print(result1)
    list = []
    for j in range(len(result1)):
        list.append(result1[j][0])
    # print(list)
    # 查询现有行数获取id####################################################
    sql2 = 'SELECT count(*) FROM rawin'
    cursor.execute(sql2)
    id = cursor.fetchone()
    id2 = '%d' % (id[0] + 1)
    # 插入日期##############################################################
    date2 = db_date
    sql4 = ' INSERT INTO rawin (id,date) VALUES (' + id2 + ',"' + date2 + '")'
    # print(sql2)
    cursor.execute(sql4)
    conn.commit()

    for i in res[0]:
        if i in list:
            j = '%f' % dict[i]
            # print(i)
            # print(j)
            sql5 = 'UPDATE rawin SET `' + i + '` = ' + j + ' where id =' + id2 + ''
            # print(sql5)
            re = cursor.execute(sql5)
            #print(re)
            conn.commit()
        else:
            j = '%f' % dict[i]
            sql6 = 'alter table rawin add `' + i + '` float(20)'
            # print(sql6)
            cursor.execute(sql6)
            sql7 = 'UPDATE rawin SET `' + i + '` = ' + j + '  where id =' + id2 + ''
            # print(sql7)
            cursor.execute(sql7)
            re = cursor.execute(sql5)
            conn.commit()
    # 关闭光标对象
    #cursor.close()
    # 关闭数据库连接
    #conn.close()
    warn = '---------- rawin Updated !!---------'
    print(warn)


def suck(fname, date, db_date):
    get_data = ExcelData(fname, date)
    res = get_data.output(get_data.readExcel())
    # print(res)
    checkdb(res, db_date)


def fill_db(path, str):
    dir = os.listdir(path)
    for i in dir:
        path2 = path + '/' + i
        filelist = []
        for x in os.listdir(path2):
            filelist.append(x)
        a = [x for x in filelist if str in x]
        if len(a):
            fname = path2 + '/' + a[0]
            date = i.replace("-0", ".").replace("-", ".")
            db_date = i
        # 查询日期，若有日期则跳过##############################################
            sql3 = 'SELECT * FROM rawin where date ="' + db_date + '" '
            cursor.execute(sql3)
            dateexist = cursor.fetchone()
            if dateexist == None:
                # print(fname,date,db_date)
                suck(fname, date, db_date)
        else:
            print(path2+'missing'+str)

if __name__ == '__main__':
    path = r'C:\Users\Administrator\Desktop\XXX'#自定义个路径
    str = '日报表'#你要提取的文件名关键字
    db_date = ''
    # 连接db
    conn = pymysql.connect(host="？？？？", user="？？？？", password="？？？？", database="？？？？")#数据库ip,user,pwd,dbname
    cursor = conn.cursor()
    fill_db(path, str)
