#Welcome to Neko
[![Version][version-badge]][version-link] ![Supported-python-version][python27-badge] [![Build Status][travis-badge]][travis-link]  [![Coverage][coverage-badge]][coverage-link] ![Star][stars] ![Fork][forks] [![MIT License][license-badge]](LICENSE.md)

##Introduction
pyFneko is a pure Python library designed to making magic to code for Neko.
You can use pyFneko to making magic beautiful.
In [/scripts](https://github.com/sudaning/Fneko/tree/master/scripts) , there are some scripts written by me for daily use.

##Installation
1. Via **pip**  
```pip install pyFneko```  
2. Via **easy_install**  
```easy_install pyFneko```  
3. From **source**(recommend)  
```cd third-party && tar zxf swig-3.0.12.tar.gz && cd swig-3.0.12 && ./configure && make && make install```  
```python setup.py install```  

##upgrading
1. Via **pip**  
```pip install --upgrade pyFneko```

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
**Welcome to use pyFneko (●'◡'●)ﾉ♥**  
If you find any bug, please report it to me by opening a issue.
pyFneko needs to be improved, your contribution will be welcomed.


[version-badge]:   https://img.shields.io/pypi/v/pyFneko.svg?label=pypi
[version-link]:    https://pypi.python.org/pypi/pyFneko/
[python27-badge]:  https://img.shields.io/badge/python-2.7-green.svg
[stars]:           https://img.shields.io/github/stars/sudaning/Fneko.svg
[forks]:           https://img.shields.io/github/forks/sudaning/Fneko.svg
[travis-badge]:    https://img.shields.io/travis/sudaning/Fneko.svg
[travis-link]:     https://travis-ci.org/sudaning/Fneko
[coverage-badge]:  https://img.shields.io/coveralls/sudaning/Fneko.svg
[coverage-link]:   https://coveralls.io/github/sudaning/Fneko
[license-badge]:   https://img.shields.io/badge/license-MIT-007EC7.svg
