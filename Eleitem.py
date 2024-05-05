import tkinter as tk
from Line import *

class Eleitem:
    def __init__(self, canvas):
        self.num = None
        self.kind = None
        self.net = []
        self.havenet = 0
        self.property = None
        self.name = ''
        self.point_for_label = [575, 550]
        self.point_for_net1 = [0, 0]
        self.point_for_net2 = [0, 0]
        self.point1 = [0, 0]
        self.point2 = [0, 0]
        self.wtc = 1
        self.canvas = canvas
        self.coctl1 = []
        self.coctl2 = []
        self.make_label()

    def make_label(self):
        self.label = tk.Label(self.canvas, text="", height=1, width=4, bg="white", fg='blue')
        self.label.place(x=self.point_for_label[0], y=self.point_for_label[1])

    def move_label(self):
        self.label.place(x=self.point_for_label[0], y=self.point_for_label[1])

    def update_label(self):
        pass

    def delete_label(self):
        self.label.destroy()

    def delete_label_net(self):
        if self.havenet == 1:
            self.label_net1.destroy()
            self.label_net2.destroy()
            self.havenet = 0

    def show_label_net(self):
        if self.kind:
            self.label_net1 = tk.Label(self.canvas, text=f"{self.net[0]}", height=1, width=0, bg="white", fg='red')
            self.label_net2 = tk.Label(self.canvas, text=f"{self.net[1]}", height=1, width=0, bg="white", fg='red')
            self.label_net1.place(x=self.point_for_net1[0], y=self.point_for_net1[1])
            self.label_net2.place(x=self.point_for_net2[0], y=self.point_for_net2[1])
            self.havenet = 1

    def move_label_net(self):
        self.label_net1.place(x=self.point_for_net1[0], y=self.point_for_net1[1])
        self.label_net2.place(x=self.point_for_net2[0], y=self.point_for_net2[1])

    def getit(self, event):
        lst = [self.kind, self.property]
        return lst

    def getcw(self, event):
        l_s = []
        l1 = []
        l2 = []
        if self.coctl1:
            for line in self.coctl1:
                if self == line.item1:
                    l_t = []
                    l_t.append(line.item2.num)
                    l_t.append(line.wtc2)
                    l1.append(l_t)
                if self == line.item2:
                    l_t = []
                    l_t.append(line.item1.num)
                    l_t.append(line.wtc1)
                    l1.append(l_t)
        if self.coctl2:
            for line in self.coctl2:
                if self == line.item1:
                    l_t = []
                    l_t.append(line.item2.num)
                    l_t.append(line.wtc2)
                    l2.append(l_t)
                if self == line.item2:
                    l_t = []
                    l_t.append(line.item1.num)
                    l_t.append(line.wtc1)
                    l2.append(l_t)
        l_s.append(l1)
        l_s.append(l2)
        return l_s

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()

    def setp(self, entry, root0, event):
        self.property = float(entry.get())
        self.update_label()
        root0.destroy()

    def update(self):
        if self.coctl1:
            for line in self.coctl1:
                if self == line.item1:
                    line.update_line1()
                else:
                    line.imupdate_line1()
        if self.coctl2:
            for line in self.coctl2:
                if self == line.item1:
                    line.update_line2()
                else:
                    line.imupdate_line2()


class Source_v(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 1
        self.property = 5
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        self.label = tk.Label(self.canvas, text="5V", height=1, width=7, bg="white", fg='blue', font=("黑体", 11))
        self.label.place(x=575, y=550)

    def update_label(self):
        self.label.config(text=f"{self.name}"+f"{self.property}" + 'V')

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="更改属性大小(默认单位:V)", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()


class Source_i(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 2
        self.property = 10
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        self.label = tk.Label(self.canvas, text="10A", height=1, width=7, bg="white", fg='blue', font=("黑体", 11))
        self.label.place(x=575, y=550)

    def update_label(self):
        self.label.config(text=f"{self.name}"+f"{self.property}" + 'A')

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="更改属性大小(默认单位:A)", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()



class Resistor(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 3
        self.property = 10
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        self.label = tk.Label(self.canvas, text="10Ω", height=1, width=8, bg="white", fg='blue', font=("黑体", 11))
        self.label.place(x=575, y=550)

    def update_label(self):
        self.label.config(text=f"{self.name}"+f"{self.property}" + 'Ω')

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="更改属性大小(默认单位:Ω)", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()


class Capacitor(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 4
        self.property = 10
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        self.label = tk.Label(self.canvas, text="10F", height=1, width=8, bg="white", fg='blue', font=("黑体", 11))
        self.label.place(x=575, y=550)

    def update_label(self):
        self.label.config(text=f"{self.name}"+f"{self.property}" + 'F')

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="更改属性大小(默认单位:F)", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()


class Inductance(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 5
        self.property = 10
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        self.label = tk.Label(self.canvas, text="10H", height=1, width=8, bg="white", fg='blue', font=("黑体", 11))
        self.label.place(x=575, y=550)

    def update_label(self):
        self.label.config(text=f"{self.name}"+f"{self.property}" + 'H')

    def set(self, event):
        root0 = tk.Tk()
        root0.title('')
        tk.Label(root0, text="更改属性大小(默认单位:H)", bg="WhiteSmoke").pack()
        entry = tk.Entry(root0)
        entry.pack(padx=20, pady=20)
        tk.Button(root0, text='确认', command=lambda: self.setp(entry, root0, event)).pack()
        root0.mainloop()



class Ground(Eleitem):
    def __init__(self, canvas):
        super().__init__(canvas)
        self.kind = 0
        self.point1 = [0, 0]
        self.point2 = [0, 0]

    def make_label(self):
        pass

    def move_label(self):
        pass

    def update_label(self):
        pass

    def delete_label(self):
        pass

    def delete_label_net(self):
        pass


