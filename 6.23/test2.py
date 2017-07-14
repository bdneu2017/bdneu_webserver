#-*- coding:utf-8 -*-
import sys,os,psutil,time,MySQLdb,re,logging,threading,msvcrt
from test2_2 import GetSystemInformation
ConfigOption={'cpu':0,'memory':0,'disk':0,'network':0}
SystemState={'time':0,'cpu':0,'memory':0,'disk':0,'network':0,'flag':"Normal"}
startflag=0
endflag=0

    
def PrintSystemState():#收集各个系统数据并显示在屏幕上
    global endflag,startflag
    funcGetSysInfo=GetSystemInformation()
    while True:
        if endflag==1:
            break
        SystemState['time']=funcGetSysInfo.OutputInformation('time')
        SystemState['cpu']=funcGetSysInfo.OutputInformation('cpu')
        SystemState['memory']=funcGetSysInfo.OutputInformation('memory')
        SystemState['disk']=funcGetSysInfo.OutputInformation('disk')
        SystemState['network']=funcGetSysInfo.OutputInformation('network')
        print '\n'
        startflag=1
        time.sleep(1)
    print "PrintSystemState Exit"

def ReadConfig():#读取Config文件里设置的各数据阈值
    global endflag
    while True:
        if endflag==1:
            break
        count=0
        fp=open("config.txt","r")
        if fp:
            optionpat=re.compile(r"\d+")
            for line in open("config.txt"):
                line=fp.readline()
                str=re.search(optionpat,line)
                if str:
                    ConfigOption[count]=str.group()
                    count+=1
            fp.close()
        else:
            print "Config.txt is not exist"
            SystemState['flag']="Normal"
        time.sleep(1)
    print "ReadConfig Exit"


def CompareWarning():#比较设置的阈值和当前系统数据并报警
    global startflag,endflag
    while True:
        if endflag==1:
            break
        else:
            if startflag==0:
                continue
            else:
                if float(ConfigOption[0])<float(SystemState['cpu']):
                    SystemState['flag']="Cpu warning"
                elif float(ConfigOption[1])<float(SystemState['memory']):
                    ystemState['flag']="Memory warning"
                elif float(ConfigOption[2])<float(SystemState['disk']):
                    ystemState['flag']="Disk warning"
                elif float(ConfigOption[3])<float(SystemState['network']):
                    SystemState['flag']="Network warning"
                else:
                    SystemState['flag']="Normal"
                if cmp(SystemState['flag'],"Normal")!=0:
                    #logWarning(SystemState['flag'])
                    logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='pythontest.log',filemode='w')
                    logging.warning('System resource Warning:%s' %SystemState['flag'])
                    print("WARNING:System resource Warning:%s\a" %SystemState['flag'])
                    time.sleep(1)
                    time.sleep(1)
    print "CompareWarning Exit"

def UseDatabase(Host,Port,User,Passwd):#连接数据库，创建并将数据写入MySQL数据库
    global startflag
    global endflag
    conn=MySQLdb.connect(host='localhost',port=3306,user='root',passwd='root')
    cur=conn.cursor()
    cur.execute('select * from information_schema.SCHEMATA where SCHEMA_NAME="python"')
    if cur.fetchone()==None:
        cur.execute('create database if not exists python')
        conn.select_db('python')
    else:
        conn.select_db('python')
    cur.execute('select * from information_schema.TABLES where TABLE_NAME="Record"')
    if cur.fetchone()==None:
        cur.execute('create table if not exists Record(time varchar(25),cpu varchar(20),memory varchar(20),disk varchar(20),net_rate varchar(20),flag varchar(20))')
    while True:
        if endflag==1:
            break
        else:
            if startflag==0:
                continue
            else:
                value=[SystemState['time'],SystemState['cpu'],SystemState['memory'],SystemState['disk'],'{0:.2f} kb'.format(SystemState['network']),SystemState['flag']]
                cur.execute('insert into Record values(%s,%s,%s,%s,%s,%s)',value)
                conn.commit()
                time.sleep(2)
    cur.close()
    conn.close()
    print "UseDatabase Exit"

def ControlProgram():#结束程序，按d或D结束程序
    global endflag
    while True:
        if ord(msvcrt.getch()) in [68,100]:
            endflag=1
            break
        else:
            continue
    print "ControlProgram Exit\n"
    
    
def main():#主函数，调用执行所有功能
    print "Program Starting...(Please Wait 2s)"
    print "Please Input 'd' or 'D' exit all function"
    time.sleep(2)
    threads=[]
    GetS=threading.Thread(target=PrintSystemState)#创建PrintSystemState()线程
    threads.append(GetS)
    ReadC=threading.Thread(target=ReadConfig)#创建ReadConfig()线程
    threads.append(ReadC)
    CompareW=threading.Thread(target=CompareWarning)#创建CompareWarning()线程
    threads.append(CompareW)
    UseD=threading.Thread(target=UseDatabase,args=('localhost',3306,'root','root',))#创建UseDatabase()线程
    threads.append(UseD)
    ControlP=threading.Thread(target=ControlProgram)
    threads.append(ControlP)
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()
    print "Main Exit" 

if __name__=="__main__":
    main()