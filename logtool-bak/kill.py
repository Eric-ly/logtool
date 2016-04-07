import os, signal
import cherrypy
import support
import glob
import os.path
import sys
import path_conf
import time
reload(sys)
sys.setdefaultencoding("utf-8")

from os import path
from cherrypy.lib.static import serve_file
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
from string import Template   # string.Template requires Python 2.4+
from cherrypy.lib.static import serve_file
from download import Downloadlist,Download
class Kill:
    @cherrypy.expose
    def index(self, **kw):
        """Kill the process associated with the pid in our session."""
        pid = cherrypy.session.get('pid')
        if not pid:
            #return "No active process to kill"
            html = """<html><body><h2>No active process to kill</h2><br /> <input type="button" name="Submit" onclick="javascript:history.back(-1);" value="return">"""
            html += """</body></html>"""
            return html
        # Without SIGINT we don't get the final summary from the tail command
        # ...it emulates control-C (SIGKILL or SIGTERM would just end the process with no summary)
        
        #os.kill(pid, signal.SIGINT)
        #command1 = "kill -9 " + pid
        #process1 = Popen(command1,shell=True,stdout=PIPE,stderr=PIPE,close_fds=True,preexec_fn=os.setsid)
        else:
        	pidnum = pid
        	os.kill(pidnum, signal.SIGKILL)
        	cherrypy.session['pid'] = None
        	cherrypy.session.save()
        	html = """<html><body><h2>click the botten return the login page</h2><br /> <input type="button" name="Submit" onclick="javascript:history.back(-1);" value="return">"""
        	html += """</body></html>"""
        
        	return html
        
        #print pid
        #return "<strong>Success:</strong> The tail log process was killed successfully."
	
