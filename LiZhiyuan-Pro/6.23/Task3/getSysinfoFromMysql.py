# encoding:utf-8
#-*-coding:utf-8-*-
'''
Created on 2017��6��22��

@author: David
'''

import pymysql
import json

def getinfofromMysql():
    conn=pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='lzy958',
                         db='systeminfo',
                         )
    cursor=conn.cursor()
    sql='select * from info'
    cursor.execute(sql)
    
    row_1=cursor.fetchone()
    print(row_1)
    j_disk=row_1[4]
    disk=json.loads(j_disk)
    print('The disk_use_percent is',str(disk))
    j_net=row_1[5]
    net=json.loads(j_net)
    print('The net info is\n',net)
    conn.commit()
    cursor.close()
    conn.close()
    
def main():
    getinfofromMysql()
    
if __name__ == '__main__':
    #pass
    main()