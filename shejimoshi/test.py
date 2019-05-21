#! --*-- coding:utf-8 --*--
class Burger():
    """
    主食类，价格名字
    """
    name=""
    price=0.0
    def getPrice(self):
        return self.price
    def setPrice(self,price):
        self.price=price
    def getName(self):
        return self.name
class cheeseBurger(Burger):
    """
    奶酪汉堡
    """
    def __init__(self):
        self.name="cheese burger"
        self.price=10.0
class spicyChickenBurger(Burger):
    """
    香辣鸡汉堡
    """
    def __init__(self):
        self.name="spicy chicken burger"
        self.price=15.0


class Snack():
    """
    小食类，价格以及名字
    """
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
    """
    炸薯条
    """
    def __init__(self):
        self.name = "chips"
        self.price = 6.0
class chickenWings(Snack):
    """
    鸡翅
    """
    def __init__(self):
        self.name = "chicken wings"
        self.price = 12.0

class Beverage():
    """
    饮料
    """
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
    """
    可乐
    """
    def __init__(self):
        self.name = "coke"
        self.price = 4.0
class milk(Beverage):
    """
    牛奶
    """
    def __init__(self):
        self.name = "milk"
        self.price = 5.0

class order():
    def __init__(self, order):
        self.burger = order.burger
        self.  





