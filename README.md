#Welcome to Neko
![](https://travis-ci.org/sudaning/PytLab-Neko.svg?branch=master)
![](https://img.shields.io/pypi/v/pyNeko.svg)
![](https://img.shields.io/badge/python-3.5-green.svg)
![](https://img.shields.io/badge/python-2.7-green.svg)
![](https://img.shields.io/badge/docs-stable-brightgreen.svg?style=flat)
![](https://img.shields.io/github/stars/sudaning/PytLab-Neko.svg)
![](https://img.shields.io/github/forks/sudaning/PytLab-Neko.svg)

##Introduction
pyNeko is a pure Python library designed to making magic to code for Neko.
You can use pyNeko to making magic beautiful.
In [/scripts](https://github.com/sudaning/PytLab-Neko/tree/master/scripts) , there are some scripts written by me for daily use.

##Installation
1. Via **pip**  
```pip install pyNeko```  
2. Via **easy_install**  
```easy_install pyNeko```  
3. From **source**  
```python setup.py install```  

##upgrading
1. Via **pip**  
```pip install --upgrade pyNeko```

##Examples

* ProcBar
```python
import time  
from neko import ProcBar, color_str  
p = ProcBar(mod='details')  
total = 56  
p.set_details(total, widget_type="percent").start("Dance up...")  
for i in range(0, total + 1):  
    if p.move():  
    time.sleep(0.1)  
p.stop(color_str("ending", "sky_blue"))
```

* Ssh
```python
import sys
from neko import Ssh
s = Ssh('10.9.0.115', username = 'root', password = 'root')
stdin, stdout, stderr = s.exec_command('ls') 
for l in stdout.readlines():
    sys.stdout.write(l)
```

* tcpdump
```python
from neko import tcpdump
t = tcpdump(eth='eth0', w='test.pcap', port=10002)
if t.run():
    t.terminate(5)
```

* redisCluterBee
```python
from neko import redisCluterBee
r = redisCluterBee('10.9.0.115:7000,10.9.0.115:7001')
print(r.set('123',456))
print(r.get('123'))
print(r.set('789','aaa'))
print(r.get('sf'))
print(r.get('789'))
print(r.get('1234'))
print(r.incr('total', 100))
print(r.incr('total', 200))
print(r.decr('total', 50))
print(r.hset('city', 'cq', '023'))
print(r.hset('city', 'bj', '010'))
print(r.hget('city', 'sz'))
print(r.hget('city', 'cq'))
print(r.hgetall('city'))
```

* esl
```python
from neko import ESLEvent
class MyEvent(ESLEvent):
    # overwrite function channel_event
    def channel_event(self, event):
        event_name = event.getHeader("Event-Name")
        event_sub_name = event.getHeader("Event-Subclass")

        if event_name in ['CHANNEL_CREATE']:
            uuid = event.getHeader("unique-id")
            session_id = event.getHeader("variable_session_id")
            call_dir = event.getHeader("Caller-Direction")
            sip_call_id = event.getHeader("variable_sip_call_id")
            print("FREESWIRCH calling... uuid:%s session_id:%s direction:%s call-id:%s" % (uuid, session_id, call_dir, sip_call_id))
        pass

	event = MyEvent('10.9.0.115', 8021, 'ClueCon')
    timeout = 60
    # running 60 seconds on block and then exit. It will never exit if timeout is 0, to return "end" in function channel_event can be stopped
	event.run(timeout)
```

##From the author
**Welcome to use pyNeko (●'◡'●)ﾉ♥**  
If you find any bug, please report it to me by opening a issue.
pyNeko needs to be improved, your contribution will be welcomed.
