#!python
import cherrypy

class Kill-pid:
    def kill_proc(self, **kw):
"""Kill the process associated with the pid in our session."""
        pid = cherrypy.session.get('pid')
        #if not pid:
        #    return "No active process to kill"
        # Without SIGINT we don't get the final summary from the tail command
        # ...it emulates control-C (SIGKILL or SIGTERM would just end the process with no summary)
        os.killpg(pid, signal.SIGINT)
        #return "<strong>Success:</strong> The tail log process was killed successfully."
