
'''Decorator Pattern with Python Code
'''

from abc import abstractmethod, ABCMeta


# 创建一个形状接口
class Shape(metaclass=ABCMeta):
    @abstractmethod 
    def draw(self):
        pass


# 创建圆形实体类
class Circle(Shape):
    def draw(self): 
        print("Shape: Circle")


# 创建矩形实体类
class Rectangle(Shape):
    def draw(self):
        print("Shape: Rectangle")


# 创建实现了 Shape 接口的抽象装饰类
class ShapeDecorator(Shape):
    decoratedShape = None
 
    def __init__(self, decoratedShape):
        self.decoratedShape = decoratedShape
    
    def draw(self):
       self.decoratedShape.draw()


# 创建扩展了 ShapeDecorator 类的实体装饰类
class RedShapeDecorator(ShapeDecorator):
    def __init__(self, decoratedShape):
       ShapeDecorator.__init__(self, decoratedShape)   
 
    def draw(self):
       self.decoratedShape.draw()   
       self.setRedBorder(self.decoratedShape)

    def setRedBorder(self, decoratedShape):
        print("Border Color: Red")


class Client(object):
    def main(self):
        circle = Circle()
        redCircle = RedShapeDecorator(Circle())
        redRectangle = RedShapeDecorator(Rectangle())

        print("Circle with normal border")
        circle.draw()

        print("\nCircle of red border")
        redCircle.draw()

        print("\nRectangle of red border")
        redRectangle.draw()
   

if __name__ == '__main__':
    Client().main()