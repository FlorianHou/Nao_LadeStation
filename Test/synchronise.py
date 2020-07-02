import qi
import time
import functools


def doSomeWorks(p):
    # do your work here instead os sleeping
    time.sleep(10)
    p.setValue(42)

p = qi.Promise()
f = p.future()
qi.async(functools.partial(doSomeWorks, p))
print "result", f.value()