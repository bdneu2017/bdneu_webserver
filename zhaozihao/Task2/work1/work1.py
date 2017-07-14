# -*- coding: utf-8 -*-  
import web,os,threading,GetInformation

urls=(
	'/','index',
    '/info','getinformation',
)
render=web.template.render('templates/')

class index:
	def GET(self):
		return render.index()

class getinformation:
	def GET(self):
		list=GetInformation.GetSystemInformation()
		return render.getinformation(list)

if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()