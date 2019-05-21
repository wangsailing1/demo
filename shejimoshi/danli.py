#! --*-- coding:utf-8 --*--
import threading
import time
'''
# 保证某一个类只有一个实例，而且在全局只有一个访问点
优点 : 全局只有一个实例, 比较节省空间、只有一个接入点，可以更好的进行数据同步控制、可以常驻内存, 减少系统开销
缺点 : 不容易扩展、单例对象的职责太多、单例在并发协作需要优先完成、可能会导致资源瓶颈
'''
#这里使用方法__new__来实现单例模式
class Singleton(object):#抽象单例
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
#总线
class Bus(Singleton):
    lock = threading.RLock()
    def sendData(self,data):
        self.lock.acquire()
        time.sleep(3)
        print "Sending Signal Data...",data
        print '实例化id', id(self)
        self.lock.release()
#线程对象，为更加说明单例的含义，这里将Bus对象实例化写在了run里
class VisitEntity(threading.Thread):
    my_bus=""
    name=""
    def getName(self):
        return self.name
    def setName(self, name):
        self.name=name
    def run(self):
        self.my_bus=Bus()
        self.my_bus.sendData(self.name)

if  __name__=="__main__":
    for i in range(3):
        print "Entity %d begin to run..."%i
        my_entity=VisitEntity()
        my_entity.setName("Entity_"+str(i))
        my_entity.start()