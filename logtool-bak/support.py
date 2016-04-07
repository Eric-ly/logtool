
import subprocess,os,re
import path_conf
logPath = path_conf.logPath


def getLogFiles(): # get all "log" files readable by me
    cmd = [ 'find', logPath, '-name', "*.log" ]
    FNULL = open('/dev/null', 'w')
    prefixlen = len(logPath)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=FNULL)
    find_files = p.communicate()[0].splitlines()
    readable_files = []
    for f in find_files:
        if os.access(f,os.R_OK):
            readable_files.append(f[prefixlen:])
    return readable_files

def getFileLines(f,expr=""): #retrieve lines from file filtered by expr
    f = open(f,"r")
    lines = f.readlines()
    pattern = re.compile(expr)
    send_lines = []
    for line in lines:
        line = line.rstrip("\n")
        if expr == "" or pattern.search(line):
            send_lines.append(line)
    return send_lines
