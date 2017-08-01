# coding:utf-8
# ...............访问localhost:5000能显示当前服务器的资源信息............
from flask import Flask, render_template
from sysinfo import Info, GetResultByThread
import Queue
app = Flask(__name__)  # 实例


@app.route('/')  # 显示资源页面
def info():
    q = Queue.Queue()
    infom = Info(q)
    f_list = [infom.cpu_urate, infom.memory_urate, infom.disk_urate,
              infom.netp_rate, infom.now_time]
    thread = GetResultByThread(f_list, q)
    result = thread.thread()
    return render_template('info.html', info=u'|**当前时间:*' + str(result[0]) +
                           u'|**利用率:*' + str(result[1]) + u'|**内存使用率:*' +
                           str(result[2]) + u'|**磁盘占用率:*' + str(result[3]) +
                           u'|**网络发送速率:*' + str(result[4]) + u'|**网络接收速率:*' +
                           str(result[5]) + '|')


if __name__ == '__main__':
    app.run()
