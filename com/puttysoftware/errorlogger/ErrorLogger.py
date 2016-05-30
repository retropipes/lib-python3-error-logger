'''
Created on Feb 11, 2015

@author: ericahnell
'''

# Imports
import traceback
import datetime
import platform
import os
import sys

def log_errors(mainfunc):
    try:
        mainfunc()
    except SystemExit:
        # Don't handle SystemExit
        raise
    except StopIteration:
        # Don't handle StopIteration
        raise
    except KeyboardInterrupt:
        # Don't handle KeyboardInterrupt
        raise
    except GeneratorExit:
        # Don't handle GeneratorExit
        raise
    except:
        try:
            with open(_get_log_filename(mainfunc), "w") as logfile:
                traceback.print_exc(file=logfile)
        except:
            traceback.print_exc()
        sys.exit(1)
            
def _get_log_filename(mainfunc):
    stamp = datetime.datetime.now().isoformat()
    progname = str(mainfunc)
    osname = platform.system()
    logfile = progname + '_' + stamp
    ext = ''
    if osname == 'Darwin':
        ext = '.crash'
    elif osname == 'Windows':
        ext = '.log'
    else:
        ext = '.log'
    logfile = logfile + ext
    # Make sure the path exists before trying to use it
    logdir = _get_log_directory()
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    return os.path.join(logdir, logfile)

def _get_log_directory():
    osname = platform.system()
    logdir = ''
    envs = os.environ
    if osname == 'Darwin':
        logdir = os.path.join(envs['HOME'], 'Library', 'Logs', 'CrashReporter')
    elif osname == 'Windows':
        logdir = os.path.join(envs['USERPROFILE'], 'Crash')
    else:
        logdir = os.path.join(envs['HOME'], '.crash')
    return logdir