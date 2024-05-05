import tkinter as tk

class Line:
    def __init__(self, canvas, item1, item2, n1, n2):
        self.item1 = item1
        self.item2 = item2
        self.wtc1 = n1
        self.wtc2 = n2
        self.canvas = canvas
        self.line1 = self.canvas.create_line(0, 0, 0, 0, width=2)
        self.line2 = self.canvas.create_line(0, 0, 0, 0, width=2)

        self.update_line()

    def get_center(self, item):
        # 获取组件的中心坐标
        if item.wtc == 1:
            x = item.point1[0]
            y = item.point1[1]
            return x, y
        if item.wtc == 2:
            x = item.point2[0]
            y = item.point2[1]
            return x, y

    def get_center1(self, item):
        # 获取组件的中心坐标
        x = item.point1[0]
        y = item.point1[1]
        return x, y

    def get_center2(self, item):
        # 获取组件的中心坐标
        x = item.point2[0]
        y = item.point2[1]
        return x, y

    def update_line(self):
        # 获取两个组件的中心坐标
        x1, y1 = self.get_center(self.item1)
        x2, y2 = self.get_center(self.item2)
        # 更新连接线的坐标
        self.canvas.coords(self.line1, x1, y1, x1, y2)
        self.canvas.coords(self.line2, x1, y2, x2, y2)

    def update_line1(self):
        # 获取两个组件的中心坐标
        x1, y1 = self.get_center1(self.item1)
        x2, y2 = 0, 0
        if self.wtc2 == 1:
            x2, y2 = self.get_center1(self.item2)
        if self.wtc2 == 2:
            x2, y2 = self.get_center2(self.item2)
        # 更新连接线的坐标
        self.canvas.coords(self.line1, x1, y1, x1, y2)
        self.canvas.coords(self.line2, x1, y2, x2, y2)

    def imupdate_line1(self):
        x1, y1 = self.get_center1(self.item2)
        x2, y2 = 0, 0
        if self.wtc1 == 1:
            x2, y2 = self.get_center1(self.item1)
        if self.wtc1 == 2:
            x2, y2 = self.get_center2(self.item1)
        # 更新连接线的坐标
        self.canvas.coords(self.line1, x1, y1, x1, y2)
        self.canvas.coords(self.line2, x1, y2, x2, y2)

    def update_line2(self):
        # 获取两个组件的中心坐标
        x1, y1 = self.get_center2(self.item1)
        x2, y2 = 0, 0
        if self.wtc2 == 2:
            x2, y2 = self.get_center2(self.item2)
        if self.wtc2 == 1:
            x2, y2 = self.get_center1(self.item2)
        # 更新连接线的坐标
        self.canvas.coords(self.line1, x1, y1, x1, y2)
        self.canvas.coords(self.line2, x1, y2, x2, y2)

    def imupdate_line2(self):
        x1, y1 = self.get_center2(self.item2)
        x2, y2 = 0, 0
        if self.wtc1 == 1:
            x2, y2 = self.get_center1(self.item1)
        if self.wtc1 == 2:
            x2, y2 = self.get_center2(self.item1)
        # 更新连接线的坐标
        self.canvas.coords(self.line1, x1, y1, x1, y2)
        self.canvas.coords(self.line2, x1, y2, x2, y2)

