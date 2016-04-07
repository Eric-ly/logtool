#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

from cherrypy.lib.sessions import Session
from cherrypy.lib.sessions import RamSession

class Mysessions(Session): 
	@cherrypy.expose
	def __init__(self,id=None, **kwargs):
		#Session.__init__(self, id=None, **kwargs)
		abc = "abc"
		f=open('out.txt','w')
		print >> f,abc
		f.close()
	@cherrypy.expose
	def delete():
		Session.delete()
		print >> f,"luck!"
	@cherrypy.expose
	def generate_id(self):
		f=open('out.txt','w')
		ramabc = "ramabc"
		print >> f,ramabc
		f.close()
		self.generate_id()
		
class MyRamsession(RamSession):
	@cherrypy.expose
	def _delete(self):
		f=open('out.txt','w')
		ramabc = "ramabc"
		print >> f,ramabc
		f.close()
    

        