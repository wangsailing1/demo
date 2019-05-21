#! --*-- coding:utf-8 --*--
'''
四个名词 : 抽象产品类、具体产品类、抽象工厂类、具体工厂类
定义 : 根据输入值，来返回结果，调用相同的方法，得到不同的返回值
简单工厂模式 : 不对抽象工厂类不进行实例化, 将创建食品的方法改成类方法, 
             直接使用抽象工厂类进行调用
工厂模式 : 创建一个接口函数，定义一个字典，让子类决定实例化哪一个类
抽象工厂模式 : 创建一个抽象类，通过传的参数来决定创建对象
优点 : 封装的好、可以随时进行调整
'''
class Burger():
    name=""
    price=0.0
    def getPrice(self):
        return self.price
    def setPrice(self,price):
        self.price=price
    def getName(self):
        return self.name
class cheeseBurger(Burger):
    def __init__(self):
        self.name="cheese burger"
        self.price=10.0
class spicyChickenBurger(Burger):
    def __init__(self):
        self.name="spicy chicken burger"
        self.price=15.0

class Snack():
    name = ""
    price = 0.0
    type = "SNACK"
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name


class chips(Snack):
    def __init__(self):
        self.name = "chips"
        self.price = 6.0


class chickenWings(Snack):
    def __init__(self):
        self.name = "chicken wings"
        self.price = 12.0
class Beverage():
    name = ""
    price = 0.0
    type = "BEVERAGE"
    def getPrice(self):
        return self.price
    def setPrice(self, price):
        self.price = price
    def getName(self):
        return self.name


class coke(Beverage):
    def __init__(self):
        self.name = "coke"
        self.price = 4.0


class milk(Beverage):
    def __init__(self):
        self.name = "milk"
        self.price = 5.0

class foodFactory():
    type=""
    @classmethod
    def createFood(self,foodClass):
        print self.type," factory produce a instance."
        return foodClass()
class burgerFactory(foodFactory):
    def __init__(self):
        self.type="BURGER"
class snackFactory(foodFactory):
    def __init__(self):
        self.type="SNACK"
class beverageFactory(foodFactory):
    def __init__(self):
        self.type="BEVERAGE"


class User:
    def __init__(self, name):
        self.burger_factory=burgerFactory()
        self.snack_factorry=snackFactory()
        self.beverage_factory=beverageFactory()
        self.name = name 
        self.berger = None
        self.snack = None
        self.beverage = None

    def addburger(self, foodclass):
        self.burger = self.burger_factory.createFood(foodclass)

    def addsnack(self, foodclass):
        self.snack = self.snack_factorry.createFood(foodclass)

    def addbeverage(self, foodclass):
        self.beverage = self.beverage_factory.createFood(foodclass)

if  __name__=="__main__":
    user = User("小明")
    user.addburger(cheeseBurger)
    user.addsnack(chips)
    user.addbeverage(coke)
    print '主食:', user.burger.getName(), user.burger.getPrice()
    print '小食:', user.snack.getName(), user.snack.getPrice()
    print '饮料:', user.beverage.getName(),user.beverage.getPrice()

