import os
import subprocess
import re

processname = 'python lasd1.py'
tmp = os.popen("ps -Af").read()
proccount = tmp.count(processname)

if proccount > 0:
  print(proccount, ' processes running of ', processname, 'type')
else:
  os.system(processname)