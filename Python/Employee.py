#coding=utf-8

from Human import Human

class Employee(Human):
    '����Ա����'
    empCount = 0

    # ����
    def __init__(self, name, salary, sex):

        Human.__init__(self, sex)
        #self.setSex(sex)
        #self._Human__sex = sex

        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print "Total Employee %d" % Employee.empCount

    def displayEmployee(self):
        print "Name : ", self.name, ", Salary : ", self.salary, ", Sex : " + self.getSex()#self._Human__sex

    def __del__(self):      # ����
        class_name = self.__class__.__name__
        print class_name, "xxx"


