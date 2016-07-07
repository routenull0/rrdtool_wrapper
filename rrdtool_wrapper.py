#!/usr/bin/python

import zlib
import subprocess
import sys
import time
import os

rrd = "/usr/bin/rrdtool"
process_no = 16
            
processes = []

def spawn():
        processes.append(subprocess.Popen([rrd, "-"], stdin=subprocess.PIPE))

def pipe(process, data):
        processes[process].stdin.write(data)

if len(sys.argv) > 1 and sys.argv[1] == "-":
        pno = process_no
        while pno:
                spawn()
                pno -= 1
        while True:
                line = sys.stdin.readline()
                if not line:
                        break
                args = line.lstrip().split(" ")
                
                if len(args) < 2 or args[0] != "update":
                        pipe(0, line)
                else:   
                        cmd = args[0]
                        file = args[1]
                        hash = zlib.crc32(file)
                        process = hash % process_no
                        #print "cmd: ", cmd, "file: ", file, "hash: ", hash, "process no: ", process
                        pipe(process, line)
else:   
        os.execlp(rrd, *([rrd] + sys.argv[1:]))
