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
import tail
import kill_proc

from os import path
from cherrypy.lib.static import serve_file
from subprocess import Popen, PIPE
from jinja2 import Environment, FileSystemLoader
from string import Template   # string.Template requires Python 2.4+
from auth import AuthController, require, member_of, name_is
from cherrypy.lib.static import serve_file
from download import Downloadlist,Download

class Tail:
    @cherrypy.expose
    def tail(self, logfile, **kw):
        pid1 = cherrypy.session.get('pid')
        f=open('out.txt','w')
        print >> f,pid
        f.close()
        pidnum = pid1
        os.kill(pidnum, signal.SIGKILL)
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
