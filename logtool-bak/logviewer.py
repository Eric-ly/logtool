#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from auth import AuthController, require, member_of, name_is
from cherrypy.lib.static import serve_file
from download import Downloadlist,Download

__author__ = 'Ruby Yu <yanbing@sap.com>'
current_dir = path.dirname(path.abspath(__file__))
env = Environment(loader=FileSystemLoader(path.join(current_dir,'templates')))
title = "My Hybris LogViewer"
baseUrl = "/" + path.basename(current_dir)
log_path = path_conf.log_path
server_port  = 9010


config = {
 '/': {
   'tools.staticdir.root': current_dir,
  },
 '/logviewer/js': {
   'tools.staticdir.on': True,
   'tools.staticdir.dir': "js",
   },
 '/logviewer/css': {
   'tools.staticdir.on': True,
   'tools.staticdir.dir': "css",
   },
  'favicon.ico': {
    'tools.staticfile.on': True,
    #'tools.staticfile.filename':  '/logviewer/images/hybrisfavicon.ico',
    'tools.staticfile.filename': os.path.join(os.path.dirname(__file__), '/logviewer/images/favicon.ico')
   },
}


class Root(object):
    downloadlist=Downloadlist()
    download=Download()    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }

    auth = AuthController()
    download=Download()
    @cherrypy.expose
    @require(name_is("admin"))
    def index(self):
        files = support.getLogFiles()
        files.sort()
        tmpl = env.get_template("index.html")
        template_params ={
            "title"   : title,
            "files"   : files,
            "baseUrl" : baseUrl,  
            "logPath" : log_path,  

        }
        return tmpl.render( template_params )

    @cherrypy.expose
    def kill_proc(self, **kw):
        """Kill the process associated with the pid in our session."""
        pid = cherrypy.session.get('pid')
        if not pid:
            return "No active process to kill"
        # Without SIGINT we don't get the final summary from the tail command
        # ...it emulates control-C (SIGKILL or SIGTERM would just end the process with no summary)
        
        #os.kill(pid, signal.SIGINT)
        #command1 = "kill -9 " + pid
        #process1 = Popen(command1,shell=True,stdout=PIPE,stderr=PIPE,close_fds=True,preexec_fn=os.setsid)
        
        f=open('out.txt','w')
        print >> f,pid
        f.close() 
        time.sleep(5)
        pidnum = pid
        os.kill(pidnum, signal.SIGKILL)
        
        #print pid
        #return "<strong>Success:</strong> The tail log process was killed successfully."
	
	
	@cherrypy.expose
	def kill_process(self,**kw):
		print "Start : %s" % time.ctime()
		time.sleep( 5 )
		print "End : %s" % time.ctime()
		pid = cherrypy.session.get('pid')
		pidnum = pid
		os.kill(pidnum, signal.SIGKILL)
		


    @cherrypy.expose
    def tail(self, logfile, **kw):
        """Execute, 'tail -f log' and stream the output"""
        # Escape the log parameter (prevents things like "; rm -rf *")
        logfile = "'" + logfile.replace("'", "'\\''") + "'"
        command = "tail -f " + log_path + logfile
               
        # This javascript just scrolls the iframe to the bottom
        scroll_to_bottom = '<script type="text/javascript">window.scrollBy(0,50);</script>'
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE,
                        close_fds=True, preexec_fn=os.setsid)
        # Save the pid in the user's session (a thread-safe place)
        cherrypy.session['pid'] = process.pid
        cherrypy.session.save()
        def run_command():
            # The yeilds here are the key to keeping things streaming
            yield '<style>body {font-family: monospace;}</style>'
            while not process.poll(): # While the process is still running...
                out = process.stdout.read(1) # Read it's output a character at a time
                if out == '\n': # Since we're not using text/plain we need line break tags
                    out = "\n<br />%s" % scroll_to_bottom # include the iframe scroll fix
                yield out # Stream it to the browser
            # Now write out anything left in the buffer...
            out = ""
            for char in process.stdout.read():
                if char == "\n":
                    out += "\n<br />%s" % scroll_to_bottom
                else:
                    out += char
            yield out
        return run_command()

        
    # Enable streaming for the tail method.  Without this it won't work.
    tail._cp_config = {'response.stream': True}
    

cherrypy.config.update({
    'log.screen':True,
    'tools.sessions.on': True,
    'checker.on':False
})


app = cherrypy.tree.mount(Root(), "/", config)

if __name__ == '__main__':   
    cherrypy.config.update({
        'server.socket_port': server_port,
	'server.socket_host': '0.0.0.0',
    })
    cherrypy.engine.start()
    cherrypy.engine.block()


