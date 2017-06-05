from time import gmtime, strftime

CUSTOM_LOG = '/root/g8keepr/log/events.log'
DEBUG = True

def log(string, path):
    with open(path, 'ab') as logfile:
        now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        logfile.write(now)
        logfile.write(" -- ")
        logfile.write(string)
        logfile.write("\n")
    if DEBUG:
        print string

def cLog(string):
    log(string, CUSTOM_LOG)
