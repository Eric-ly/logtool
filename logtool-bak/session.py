#!python
import glob
import os.path
import support
import path_conf
import cherrypy
from cherrypy.lib.static import serve_file
from subprocess import Popen, PIPE

class Time:
	@cherrypy.expose
	def index(self, pid, **kw):
		command = "ps -ef | grep " + pid
		t = Popen(command, shell=True, stdout=PIPE, stderr=PIPE,
							close_fds=True, preexec_fn=os.setsid)
		t_beginning = time.time()
		seconds_passed = 0
		timeout = 4