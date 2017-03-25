#encoding=utf-8

import Queue
import threading
import time


threadLock = threading.Lock()

class MyThreadSync (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        global threadLock
        print "Starting " + self.name
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout 参数不填时将一直阻塞知道获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release();
        
def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

def testThreadSync():
    thread1 = MyThreadSync(1, "Thread-1", 1)
    thread2 = MyThreadSync(2, "Thread-2", 2)

    thread1.start()
    thread2.start()

    threadSyncList = []
    threadSyncList.append(thread1)
    threadSyncList.append(thread2)

    for t in threadSyncList:
        t.join()

    del threadSyncList[:]
    print "Exiting Thread Sync Test"




exitFlag = 0
queueLock = threading.Lock()
workQueue = Queue.Queue(10)

class MyThreadPriorityQueue (threading.Thread):
    def __init__(self, threadID, name, queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.queue);
        print "Exiting " + self.name
        
def process_data(threadName, queue):
    global exitFlag
    global queueLock
    global workQueue
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = queue.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)


def testThreadPriorityQueue():
    global exitFlag
    global queueLock
    global workQueue
    
    threadID = 1
    threads = []
    threadList = ["Thread-1", "Thread-2", "Thread-3"]
    nameList = ["One", "Two", "Three", "Four", "Five"]

    # 创建线程
    for tName in threadList:
        thread = MyThreadPriorityQueue(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for word in nameList:
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    print "join threads"
    # 等待所有线程完成
    for t in threads:
        t.join()

    print "Exiting Thread Async Test"




