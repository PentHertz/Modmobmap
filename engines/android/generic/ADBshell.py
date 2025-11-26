# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <sebastien.dudek(<@T>)penthertz.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return FlUxIuS ;)
# ----------------------------------------------------------------------------

from __future__ import print_function
import subprocess
import threading
import os.path
import sys
import re
if sys.version_info >= (3,0):
    from queue import Queue
else:
    from Queue import Queue

default_android_sdk_path = "/opt/android/android-sdk-linux"

class ADBError(Exception):
    def __init__(self, value):
        if value == 'platform':
            self.value = "The plateform is not supported for the moment."
        elif value == 'dev':
            self.value = "libRIL use an unsupported argument."
        else:
            self.value = "Unknown error: " + value
    def __str__(self):
        return repr(self.value)

class AsynchronousFileReader(threading.Thread):
    '''
    ref: http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading/
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue
        self._stop = threading.Event()

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

class ADBshell(object):
    androidsdkpath = None
    def __init__(self, androidsdkpath=None):
        self.androidsdkpath = androidsdkpath

    def _buildcommand(self, command):
        adbpath = None
        if self.androidsdkpath is not None:
            if 'linux' in sys.platform.lower():
                adbpath = self.androidsdkpath + '/platform-tools/adb'
        if adbpath is None:
            raise ADBError('platform')
        commandstring = [adbpath, 'shell']
        commandstring.extend(command.split(' '))
        return commandstring

    def run_adbcmdshell(self, command):
        commandstring = self._buildcommand(command)
        return subprocess.Popen(commandstring, stdout=subprocess.PIPE)

    def getDevfile(self):
        '''
            Get RILd devicename
            out: string devicename
        '''
        process = self.run_adbcmdshell('getprop rild.libargs')
        devfile = process.stdout.readline().split(b'/dev/')
        if len(devfile) >= 2:
            m = re.match(rb'([\d\w]+)', devfile[1])
            if m is not None:
                devfile = b'/dev/' + devfile[1].replace(b'\r\n', b'')
            else:
                raise ADBError('bad dev string')
        else:
            raise ADBError('dev')
        return devfile.decode("utf-8")

    def _parseCOPS(self, string):
        '''
            Parse AT+COPS=? information
            in(1): string cops returned string
            out: dict infos
        '''
        dict_ = {}
        rstr = string.replace(b'+COPS: ', b'')
        for x in rstr.split(b'),'):
            ysp = x.split(b',')
            if len(ysp) == 5:
                mccmnc = ysp[3].decode("utf-8").replace('"','')
                netname = ysp[1].decode("utf-8").replace('"','')
                if mccmnc not in dict_:
                    dict_[mccmnc] = netname
        return dict_

    def getCOPSfromRIL(self):
        '''
            Grab PLMN information
            return: dict PLMN infos
        '''
        devfile = self.getDevfile()
        process = self.run_adbcmdshell("su -c 'echo -e \"AT\r\n\" > %s'" % devfile)
        process = self.run_adbcmdshell("su -c 'echo -e \"AT+COPS=?\r\n\" > %s && cat %s'" % (devfile,devfile))
        #process = self.run_adbcmdshell("su -c 'cat %s'" % devfile)
        stdout_queue = Queue()
        stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
        stdout_reader.daemon=True
        stdout_reader.start()
        stop = False
        copsList = None
        countBL = 0
        while not stdout_reader.eof() and stop is False:
            while not stdout_queue.empty() and stop is False:
                try:
                    line = stdout_queue.get()
                    if b'+COPS: ' in line:
                        copsList = self._parseCOPS(line)
                        if len(copsList) > 0:
                            stop = True
                            stdout_reader.stop()
                            process = None
                            return copsList
                    else:
                        if len(line) == 0:
                            countBL += 1
                        if countBL == 10:
                            stop = True
                except KeyboardInterrupt:
                    stop = True
        stdout_reader.stop()
        process.stdout.close()
        return copsList

    def changePLMN(self, MCCMNC, automode=False):
        '''
            Change PLMN using AT commands
            in(1): string MCCMNC
            in(2): Bool automode
            out: process resurl
        '''
        mode = 1
        devfile = self.getDevfile()
        if automode is True:
            mode = 0
        process = self.run_adbcmdshell("su -c 'echo -e \"AT+COPS=%i,2,%s\r\n\" > %s'" % (mode, MCCMNC, devfile))
        return process

    def changeNetworkTypeGBox(self, type_=1):
        '''
            Change Networktype mode using GravityBox
            in(1): int Networktype mode.
            out: process result
        '''
        process = self.run_adbcmdshell("su -c 'am broadcast -a gravitybox.intent.action.CHANGE_NETWORK_TYPE --ez networkType %i'" % type_)
        return process

    def changeNetworkType(self, type_=2):
        '''
            Change Networktype mode using AT commands
            in(1): int Networktype mode.
                2 for Autoselect, 13 for GSM only and 14 for 3G only.
            out: process result
        '''
        devfile = self.getDevfile()
        process = self.run_adbcmdshell("su -c 'echo -e \"AT^SYSCONFIG=%i,1,1,2\r\n\" > %s'" % (type_, devfile))
        return process

    def deregister(self):
        '''
            Unregister UE from current PLMN
            out: process result
        '''
        devfile = self.getDevfile()
        process = self.run_adbcmdshell("su -c 'echo -e \"AT+COPS=2\r\n\" > %s'" % devfile)
        return process

    def airplanemode(self, mode=0):
        '''
            UE airplane mode switch
            in(1): int mode - 1 = ON, 0 = OFF
            out: process result
        '''
        self.run_adbcmdshell("su -c 'settings put global airplane_mode_on %i'" % int(mode))
        process = self.run_adbcmdshell("su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE'")
        return process

    def pushsecretcode(self, secretcode):
        '''
            Call Android secret codes
            in(1): String secretcode to call
            out: process result
        '''
        process = self.run_adbcmdshell("su -c 'am broadcast -a android.provider.Telephony.SECRET_CODE -d android_secret_code://%s'" % secretcode)
        return process
