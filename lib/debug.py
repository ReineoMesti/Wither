import os
import time
if __name__ in ('__main__', 'debug'):
    os.chdir('../log')
    log_output = open('logout.log', mode='a+')
    error_output = open('error.log', mode='a+')
else:
    print(__name__)
    log_output = open('log/logout.log', mode='a+')
    error_output = open('log/error.log', mode='a+')
start_time = time.time()
def report(source, message):
    global error_output
    running_time = int(time.time() - start_time) 
    error_output.write('[%d] %s: %s\n'%(running_time, source, message))
def log(source, message):
    global log_output
    running_time = int(time.time() - start_time) 
    log_output.write('[%d] %s: %s\n'%(running_time, source, message))
