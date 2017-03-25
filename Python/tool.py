#coding=utf-8


print u'-------------------时间--------------------------'
import time
import calendar

print time.strftime("%Y-%m-%d %H:%M:%S %A %c %p", time.localtime())

cal = calendar.month(2016, 1)
print cal

from support import print_func
print_func('地方'.decode('utf-8').encode('gbk'))


print u'-------------------文件读写--------------------------'
import os

cwd = os.getcwd()
print '当前工作目录: '.decode('utf-8').encode('gbk'), os.getcwd()
if(os.path.isfile('test/test.txt')):
    os.remove('test/test.txt')

if(os.path.isdir('test')):
    os.rmdir('test')

os.mkdir('test')
os.chdir('test')    # 设置工作目录
fo = open('test.txt', 'w+')
fo.write('xxxxx\nyyyyy\n')

try:
    fo.seek(0, 2)
    endPos = fo.tell()
    print 'endpos: ', endPos
    fo.seek(0, 0)
    print fo.read(endPos)
    fo.close();
except:
    print 'except'
else:
    print 'else'
finally:
    print 'finally'

os.chdir(cwd)


print u'-------------------类测试--------------------------'
from Employee import Employee
emp1 = Employee("Zara", 2000, 'male')
emp1.displayCount();
emp1.displayEmployee();
del emp1


print "Employee.__doc__:", Employee.__doc__
print "Employee.__name__:", Employee.__name__
print "Employee.__module__:", Employee.__module__
print "Employee.__bases__:", Employee.__bases__
print "Employee.__dict__:", Employee.__dict__


print u'-------------------正则--------------------------'
import re
matchObj = re.match('([^.]+)', 'www.runoob.com')
print matchObj.group(0)

print re.search('runoob', 'www.runoob.com').span()


phone = "2004-959-559 # This is Phone Number"
num = re.sub(r'#.*$', "", phone)
print "Phone Num : ", num

#str = r"  ''  "  "
#print str

print u'-------------------xml--------------------------'
from XMLParseTest import xmlParseTest

xmlParseTest()


print u'-------------------python3 区别--------------------------'
import timeit
import platform

def test_range(n):
    for i in range(n):
        pass

def test_xrange(n):
    for i in xrange(n):
        pass

print 'Python', platform.python_version()
print(range(10))
print(xrange(10))

print bin(0o1000)
print `fo`
print repr(fo)

b = b'china'
print type(b)

#print u'-------------------输入--------------------------'
#str = raw_input("xxx: ");
#print str

#print '-------------------thread--------------------------'
#import thread
#import time

#def print_time(threadName, delay):
#    count = 0;
#    while count < 5:
#        time.sleep(delay)
#        count += 1
#        print "%s: %s" % (threadName, time.ctime(time.time()))

#try:
#    thread.start_new_thread(print_time, ("Thread-1", 2, ))
#    thread.start_new_thread(print_time, ("Thread_2", 4, ))
#except:
#    print "Error: unable to start thread"


print '-------------------threading.Thread--------------------------'

#from MyThread import testThreadSync
#testThreadSync()

from MyThread import testThreadPriorityQueue
testThreadPriorityQueue()


while 1:
    pass


