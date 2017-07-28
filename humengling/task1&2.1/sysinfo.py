#!/usr/bin/env python
# coding:utf-8
import psutil
import time
import MySQLdb as mydb
import logging
import threading
import Queue
class Info(object):#得到资源信息并放到队列q中
	def __init__(self,queue):
		self.q=queue
	def cpu_urate(self):
		cpu=psutil.cpu_percent(interval=1)
		#return cpu
		self.q.put(['cpu',cpu])
	def memory_urate(self):
		mem=psutil.virtual_memory().percent
		#return mem
		self.q.put(['mem',mem])
	def disk_urate(self):
		all_disk=psutil.disk_partitions()
		all_mount=[]
		all_type=[]#fstype
		for i in range(len(all_disk)):
			all_mount.append(all_disk[i][1])
			all_type.append(all_disk[i][2])
		total_disk=0
		used_disk=0
		for i in range(len(all_mount)):
			if all_type[i]!='': #ensure it is a file system
				total_disk+=psutil.disk_usage(all_mount[i])[0]
				used_disk+=psutil.disk_usage(all_mount[i])[1]
		disk=used_disk*1.0/total_disk*100
		#return disk
		self.q.put(['dis',disk])
	def netp_rate(self):#the send&recv bytes change in 1 second
		all_io=psutil.net_io_counters()
		bytes_sent=all_io[0]
		bytes_recv=all_io[1]
		time.sleep(1)
		all_io1=psutil.net_io_counters()
		bytes_sent1=all_io1[0]
		bytes_recv1=all_io1[1]
		sent_rate=(bytes_sent1-bytes_sent)/1
		recv_rate=(bytes_recv1-bytes_recv)/1
		net_rate=[sent_rate,recv_rate]
		#return net_rate
		self.q.put(['net',net_rate])
	def now_time(self):
		timer=str(time.strftime('%Y-%m-%d %H:%M:%S'))
		#return timer
		self.q.put(['tim',timer])
#database operation
class DataBase():
	def __init__(self,user,password,database,ip,t_list):
		self.user=user#连接数据库的用户名
		self.password=password#连接数据库的密码
		self.database=database#要连接的数据库名
		self.ip=ip#要连接数据库的ip地址
		self.t_list=t_list#存储数据的表的列表
	def db_con(self):##建立与数据库的连接，若不存在表data或alert则创建表，返回cur
		con = mydb.connect(self.ip,self.user,self.password,self.database);
		cur = con.cursor()
		#def exist_table(table_name):#if there is table table_name
		cur.execute('show tables')
		tables=cur.fetchall()
		for table_name in self.t_list:
			table_namel="('"+table_name+"',)"#make the format same to compare
			if table_namel in str(tables):#存在表
				pass
			elif table_name=='data':
				cur.execute('create table data(r_time varchar(20),cpu_rate varchar(5),mem_rate varchar(5),dis_rate varchar(20),nes_rate varchar(20),ner_rate varchar(20))')			
			elif table_name=='alert':
				cur.execute('create table alert(r_time varchar(20),alert_name varchar(20),alert_data varchar(20))')	
		return [con,cur]
#alert info
class Alert(object):
	def __init__(self):
		pass		
	def def_log(self):
		logger=logging.getLogger('my_warning_logger')#create a logger
		logger.setLevel(logging.DEBUG)#can print all 
		fh=logging.FileHandler('test.log')#handler for writing to log file
		ch=logging.StreamHandler()#handler for printing to console
		formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')#define print formatter
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		logger.addHandler(fh)
		logger.addHandler(ch)
		return logger	
	def alert(self,logger,result,cur):#打印警告信息并将信息存入数据库
		tim=result[0]
		cpu=result[1]
		mem=result[2]
		dis=result[3]
		nes=result[4]
		ner=result[5]
		if cpu>cpu_ts:
			logger.warning(tim+"  cup_use  "+str(cpu))
			cur.execute('insert into alert values (%s,%s,%s)',[tim,"cup_use",cpu])
		if mem>mem_ts:
			logger.warning(tim+"  mem_use  "+str(mem))
			cur.execute('insert into alert values(%s,%s,%s)',[tim,"mem_use",mem])
		if dis>dis_ts:
			logger.warning(tim+"  dis_use  "+str(dis))
			cur.execute('insert into alert values(%s,%s,%s)',[tim,"dis_use",dis])
		if nes>net_ts:
			logger.warning(tim+"  net_send_rate  "+str(nes))
			cur.execute('insert into alert values(%s,%s,%s)',[tim,"net_send_rate",nes])
		if ner>net_ts:
			logger.warning(tim+"  net_recv_rate  "+str(ner))
			cur.execute('insert into alert values(%s,%s,%s)',[tim,"net_recv_rate",ner])
#thread 
class GetResultByThread(object):#传入函数的列表，使用多线程得到函数返回值
	def __init__(self,f_list,q):
		#self.num=num
		self.f_list=f_list#函数列表
		self.q=q
	def thread(self):
		r_list=[]
		t_list=[]
		for func in self.f_list:
			t=threading.Thread(target=func)
			t_list.append(t)
			t.setDaemon(True)
		for t in t_list:
			t.start()
		for t in t_list:
			t.join()
		while not self.q.empty():
			r_list.append(self.q.get())
		for v in r_list:
			if v[0]=='cpu':
				cpu=v[1]
			elif v[0]=='mem':
				mem=v[1]
			elif v[0]=='dis':
				dis=v[1]
			elif v[0]=='net':
				net=v[1]
			elif v[0]=='tim':
				tim=v[1]
		result=[tim,cpu,mem,dis,net[0],net[1]]
		return result
if __name__=='__main__':
	cpu_ts=10.0#设定阈值
	mem_ts=66.0
	dis_ts=65
	net_ts=5000.0
	print '|  time(y-m-d h:m:s)  | cpu utilization rate (%)| memory utilization rate (%)| disk utilization rate (%)| net sent rate & net recv rate (B/s)|'
	db=DataBase('root','hml','test','127.0.0.1',['data','alert'])
	[con,cur]=db.db_con()
	q=Queue.Queue()
	info=Info(q)
	alert=Alert()
	logger=alert.def_log()
	f_list=[info.cpu_urate,info.memory_urate,info.disk_urate,info.netp_rate,info.now_time]
	try:
		while True:
			thread=GetResultByThread(f_list,q)
			result=thread.thread()		
			print '%-22s %-25s %-29s %-26s %-15s %-20s' %(result[0],result[1],result[2],result[3],result[4],result[5])#real-time printing in format and write all data to database and alert 
			cur.execute('insert into data values (%s,%s,%s,%s,%s,%s)',result)
			alert.alert(logger,result,cur)
			time.sleep(3)
	except KeyboardInterrupt,e:
		pass
	finally:
		if cur:
			cur.close()
		if con:
			con.close()
		print 'closing the database...we are going to exit'			



