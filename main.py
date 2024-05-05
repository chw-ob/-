import tkinter as tk
from tkinter import Canvas, Label, PhotoImage, messagebox
from PIL import Image, ImageTk
import matplotlib
import matplotlib.pyplot as plt
from Eleitem import *
from obj import *


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("电路元器件UI")
        
        self.lst = []
        self.wtclst = []
        self.set_of_line = []
        self.lst_of_Eitem = []
        self.result = []
        self.comp_imformation = []  # 存放画布中的所有元件信息             
        self.component_images={}
        self.scale = 100 # 缩放比例
        self.comp_id = 0 # 画布中的元件id
        self.drag_data = {"item": None, "x": 0, "y": 0}  # 存储拖动信息的字典
        self.drag_canvas = {"prew_x": None, "prew_y": None}# prew_x, prew_y用于计算鼠标拖动的距离       
        self.components = ["电压源", "电流源", "电阻", "电容", "电感", "接地"]  # 存储左侧元件栏的工具
        self.task_options = ["电路参数求解", "戴维南定理", "复频域分析", "最大功率传输定理", "方波信号暂态分析", "暂态分析"] # 储存任务
        self.task_var = tk.StringVar()
        self.task_var.set("请选择分析模式")
        
        # 左侧元件框
        self.components_frame = tk.Frame(root, width=200, bg="WhiteSmoke")
        self.components_frame.pack(side="left", fill="y")
        
        # 右侧任务框
        self.task_frame = tk.Frame(root, width=230, bg="WhiteSmoke")
        self.task_frame.pack(side="right", fill="y")
        
        # 右侧文本框
        self.text_frame = tk.Frame(self.task_frame, width=220, height=650, bg="WhiteSmoke")
        self.text_frame.place(x=5, y=40) 
        
        # 中央画布
        self.canvas = Canvas(root, bg="White")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 右下角比例显示
        self.zoom_label = Label(self.root, text="100%", bg="White")
        self.zoom_label.place(relx=0.74, rely=0.95)
        
        # 右侧选择控件
        self.dropdown_select = tk.OptionMenu(self.task_frame, self.task_var, *self.task_options, command=self.task_select)
        self.dropdown_select.config(width=11)
        self.dropdown_select.place(x=45, y=10)
        
        # 一键清除按钮
        self.clear_button = tk.Button(self.canvas, text="一键清除", highlightbackground="White", command=self.comp_clear)
        self.clear_button.place(relx=0.52, rely=0.95)
        
        # 获取数据按钮
        self.getdone_button = tk.Button(self.canvas, text="获得节点信息", highlightbackground="White")
        self.getdone_button.bind("<ButtonPress>", self.node_get)
        self.getdone_button.place(relx=0.35, rely=0.95)
        
        self.canvas.bind("<ButtonPress-3>", self.on_mouse_press)  # 绑定滚轮按下事件
        self.canvas.bind("<B3-Motion>", self.on_mouse_drag)  # 绑定滚轮移动事件
        self.canvas.bind("<ButtonRelease-3>", self.on_mouse_release)  # 绑定滚轮放开事件
        self.canvas.bind("<MouseWheel>", self.zoom)  # 绑定滚轮滑动事件

        self.load_component_images()  # 加载元件图像
        self.create_components()  # 加载左侧元件栏

    # 将元器件图片导入
    def load_component_images(self):
        for comp in self.components:
            photo_img = PhotoImage(file=f"{comp}.png")
            self.component_images[comp] = photo_img # 格式为 <PhotoImage>

    # 将元器件放在左侧栏
    def create_components(self):
        for comp in self.components:
            label = Label(self.components_frame, text=comp, image=self.component_images[comp], compound="top",
                          font=('黑体', 12),
                          bg="WhiteSmoke", cursor="hand2")
            label.image = self.component_images[comp] # 保持对图片的引用以避免被垃圾回收
            label.pack(fill=tk.X, padx=5, pady=10)  # 相隔距离
            label.bind("<Button-1>", lambda event, image=self.component_images[comp], file=Image.open(f"{comp}.png"), type=comp, angle=0 :
            self.click_components(event, image, file, type, angle)) # 绑定事件

    # 点击元件栏图标后添加元件至画布
    def click_components(self, event, comp_image, comp_file, comp_type, comp_angle):
        comp_item = self.canvas.create_image(600, 550, anchor=tk.NW, image=comp_image, tags=str(self.comp_id))
        comp_scale = None # 用于储存缩放后的图片状态
        self.comp_imformation.append([comp_file, comp_item, comp_scale, comp_type, comp_angle]) # 用于缩放函数

        # 为每个元件绑定鼠标点击事件，调用 start_drag 方法
        self.canvas.tag_bind(comp_item, "<Button-1>", lambda event, id=self.comp_id: self.start_drag(event, id))
        # 为每个元件绑定鼠标释放事件，调用 stop_drag 方法
        self.canvas.tag_bind(comp_item, "<ButtonRelease-1>", self.stop_drag)

        if comp_type=="电压源":
            c_source_v = Source_v(self.canvas)
            self.lst_of_Eitem.append(c_source_v)
            c_source_v.num = len(self.lst_of_Eitem)
            
            self.canvas.tag_bind(comp_item, "<Double-Button-1>", c_source_v.set)

            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_source_v, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_source_v))
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_source_v, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))
            self.canvas.tag_bind(comp_item, "<Control-Button-2>", lambda event, id=self.comp_id, object=c_source_v, item=comp_item:
                self.rotate_comp(event, id, object, item))
            
        if comp_type=="电流源":
            c_source_i = Source_i(self.canvas)
            self.lst_of_Eitem.append(c_source_i)
            c_source_i.num = len(self.lst_of_Eitem)
            
            self.canvas.tag_bind(comp_item, "<Double-Button-1>", c_source_i.set)

            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_source_i, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_source_i))
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_source_i, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))
            self.canvas.tag_bind(comp_item, "<Control-Button-2>", lambda event, id=self.comp_id, object=c_source_i, item=comp_item:
                self.rotate_comp(event, id, object, item))
        
        if comp_type=="电阻":
            c_resistor = Resistor(self.canvas)
            self.lst_of_Eitem.append(c_resistor)
            c_resistor.num = len(self.lst_of_Eitem)
            
            self.canvas.tag_bind(comp_item, "<Double-Button-1>", c_resistor.set)

            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_resistor, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_resistor))
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_resistor, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))
            self.canvas.tag_bind(comp_item, "<Control-Button-2>", lambda event, id=self.comp_id, object=c_resistor, item=comp_item:
                self.rotate_comp(event, id, object, item))
            
        if comp_type=="电容":
            c_capacitor = Capacitor(self.canvas)
            self.lst_of_Eitem.append(c_capacitor)
            c_capacitor.num = len(self.lst_of_Eitem)
            
            self.canvas.tag_bind(comp_item, "<Double-Button-1>", c_capacitor.set)

            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_capacitor, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_capacitor))
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_capacitor, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))
            self.canvas.tag_bind(comp_item, "<Control-Button-2>", lambda event, id=self.comp_id, object=c_capacitor, item=comp_item:
                self.rotate_comp(event, id, object, item))
            
        if comp_type=="电感": 
            c_inductance = Inductance(self.canvas)
            self.lst_of_Eitem.append(c_inductance)
            c_inductance.num = len(self.lst_of_Eitem)
            
            self.canvas.tag_bind(comp_item, "<Double-Button-1>", c_inductance.set)

            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_inductance, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_inductance))
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_inductance, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))    
            self.canvas.tag_bind(comp_item, "<Control-Button-2>", lambda event, id=self.comp_id, object=c_inductance, item=comp_item:
                self.rotate_comp(event, id, object, item))            
       
            
        if comp_type=="接地":            
            c_ground = Ground(self.canvas)
            self.lst_of_Eitem.append(c_ground)
            c_ground.num = len(self.lst_of_Eitem)
            
            # 为每个元件绑定鼠标拖动事件，调用 on_drag 方法
            self.canvas.tag_bind(comp_item, "<B1-Motion>", lambda event: self.on_drag(c_ground, event))
            # 为每个元件绑定双击删除事件，调用 delete_comp 方法      
            self.canvas.tag_bind(comp_item, "<Control-Button-1>", lambda event, item=comp_item: self.delete_comp(event, item, c_ground)) 
            # 为每个元件绑定右键连线事件，调用 ready_fo_drawline 方法   
            self.canvas.tag_bind(comp_item, "<Button-2>", lambda event, object=c_ground, id=self.comp_id, item=comp_item, type=comp_type:
                self.ready_fo_drawline(event, object, id, item, type))        
              
        self.comp_id += 1   
      
    # 节点选择和画线函数           
    def ready_fo_drawline(self, event, object, id, item, type):
        print("draw line")
        x, y = event.x, event.y
        left, top, right, bottom = self.canvas.bbox(item)
        if type != "接地":
            if self.comp_imformation[id][4] == 0:
                object.point1 = [left + 6.7, top + 34.6]
                object.point2 = [right - 6.7, top + 34.6]
                object.point_for_net1 = [left - 12, top + 38]
                object.point_for_net2 = [right + 2, top + 38]
                if x <= (left + right) / 2:
                    object.wtc = 1
                else:
                    object.wtc = 2
            if self.comp_imformation[id][4] == 90:
                object.point1 = [left + 34.6, top + 6.7]
                object.point2 = [left + 34.6, bottom - 6.7]
                object.point_for_net1 = [left + 38, top - 15]
                object.point_for_net2 = [left + 38, bottom]
                if y <= (top + bottom) / 2:
                    object.wtc = 1
                else:
                    object.wtc = 2
            if self.comp_imformation[id][4] == 180:
                object.point1 = [right - 6.7, top + 34.6]
                object.point2 = [left + 6.7, top + 34.6]
                object.point_for_net1 = [right + 2, top + 38]
                object.point_for_net2 = [left - 12, top + 38]
                if x >= (left + right) / 2:
                    object.wtc = 1
                else:
                    object.wtc = 2
            if self.comp_imformation[id][4] == 270:
                object.point1 = [left + 34.6, bottom - 6.7]
                object.point2 = [left + 34.6, top + 6.7]
                object.point_for_net1 = [left + 38, bottom]
                object.point_for_net2 = [left + 38, top - 15]
                if y >= (top + bottom) / 2:
                    object.wtc = 1
                else:
                    object.wtc = 2
        else:
            object.point1 = [left + 36, top + 25]
                       
        if len(self.lst) <= 2:
            self.lst.append(object)
            a = object.wtc
            self.wtclst.append(a)
        if len(self.lst) == 2:
            line = Line(self.canvas, self.lst[0], self.lst[1], self.wtclst[0], self.wtclst[1])
            if line.item1 == line.item2:
                self.lst.clear()
                self.wtclst.clear()
            else:
                for object in self.lst:
                    if object.wtc == 1:
                        object.coctl1.append(line)
                    if object.wtc == 2:
                        object.coctl2.append(line)
                self.set_of_line.append(line)
                self.lst.clear()
                self.wtclst.clear()
    
    # 任务选择函数
    def task_select(self, event):
        self.selected_option = self.task_var.get()
        # 清除 Frame 上的现有内容
        for widget in self.text_frame.winfo_children():
            widget.destroy()
        
        if self.selected_option == "电路参数求解":
            self.imfrom_text = tk.Text(self.text_frame, width=20, height=30, font=('黑体', 15), bg="White", wrap=tk.WORD, state=tk.DISABLED)
            self.imfrom_text.place(x=5, y=20)
            self.load_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.load_button.bind("<ButtonPress>", self.data_get)
            self.load_button.place(relx=0.37, rely=0.95)
        
        if self.selected_option == "戴维南定理":
            self.step_length = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.step_length.place(x=75, y=20)
            self.step_length_word = tk.Label(self.text_frame,text="步长", width=3, bg="WhiteSmoke").place(x=5, y=18)
            
            self.R_number = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.R_number.place(x=75, y=60)
            self.R_number_word = tk.Label(self.text_frame,text="电阻序号", width=6, bg="WhiteSmoke").place(x=5, y=58)
            
            self.R_start = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.R_start.place(x=75, y=100)
            self.R_start_word = tk.Label(self.text_frame,text="起始电阻", width=6, bg="WhiteSmoke").place(x=5, y=98)
            
            self.R_end = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.R_end.place(x=75, y=140)
            self.R_end_word = tk.Label(self.text_frame,text="终止电阻", width=6, bg="WhiteSmoke").place(x=5, y=138)
            
            self.DWN_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.DWN_button.bind("<ButtonPress>", self.DWN_get)
            self.DWN_button.place(relx=0.37, rely=0.95)
        
        if self.selected_option == "复频域分析":
            self.complex_freq = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.complex_freq.place(x=75, y=20)
            self.complex_freq_word = tk.Label(self.text_frame,text="角频率", width=6, bg="WhiteSmoke").place(x=5, y=18)
            
            self.complex_text = tk.Text(self.text_frame, width=20, height=28, font=('黑体', 15), bg="White", wrap=tk.WORD, state=tk.DISABLED)
            self.complex_text.place(x=5, y=60)
            
            self.complex_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.complex_button.bind("<ButtonPress>", self.complex_get)
            self.complex_button.place(relx=0.37, rely=0.95)
            
        if self.selected_option == "最大功率传输定理":
            self.max_freq = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.max_freq.place(x=75, y=180)
            self.max_freq_word = tk.Label(self.text_frame,text="角频率", width=6, bg="WhiteSmoke").place(x=5, y=178) 
            
            self.max_length = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.max_length.place(x=75, y=20)
            self.max_length_word = tk.Label(self.text_frame,text="步长", width=3, bg="WhiteSmoke").place(x=5, y=18)
            
            self.max_R_number = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.max_R_number.place(x=75, y=60)
            self.max_R_number_word = tk.Label(self.text_frame,text="电阻序号", width=6, bg="WhiteSmoke").place(x=5, y=58)
            
            self.max_R_start = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.max_R_start.place(x=75, y=100)
            self.max_R_start_word = tk.Label(self.text_frame,text="起始电阻", width=6, bg="WhiteSmoke").place(x=5, y=98)
            
            self.max_R_end = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.max_R_end.place(x=75, y=140)
            self.max_R_end_word = tk.Label(self.text_frame,text="终止电阻", width=6, bg="WhiteSmoke").place(x=5, y=138)
            
            self.max_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.max_button.bind("<ButtonPress>", self.max_get)
            self.max_button.place(relx=0.37, rely=0.95)
            
        
        if self.selected_option == "方波信号暂态分析":           
            self.wave_freq = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.wave_freq.place(x=75, y=20)
            self.wave_freq_word = tk.Label(self.text_frame,text="方波频率", width=6, bg="WhiteSmoke").place(x=5, y=18)
            
            self.wave_time = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.wave_time.place(x=75, y=60)
            self.wave_time_word = tk.Label(self.text_frame,text="仿真时间", width=6, bg="WhiteSmoke").place(x=5, y=58)
            
            self.wave_id = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.wave_id.place(x=75, y=100)
            self.wave_id_word = tk.Label(self.text_frame,text="方波序号", width=6, bg="WhiteSmoke").place(x=5, y=98)
            
            self.wave_comp_id = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.wave_comp_id.place(x=75, y=140)
            self.wave_comp_id_word = tk.Label(self.text_frame,text="元件序号", width=6, bg="WhiteSmoke").place(x=5, y=138)
            
            self.wave_select = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.wave_select.place(x=75, y=180)
            self.wave_select_word = tk.Label(self.text_frame,text="电压/电流", width=6, bg="WhiteSmoke").place(x=5, y=178)
            
            self.wave_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.wave_button.bind("<ButtonPress>", self.wave_get)
            self.wave_button.place(relx=0.37, rely=0.95)
            
        if self.selected_option == "暂态分析":           
            self.temp_fang_freq = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_fang_freq.place(x=75, y=20)
            self.temp_fang_freq_word = tk.Label(self.text_frame,text="方波频率", width=6, bg="WhiteSmoke").place(x=5, y=18)
            
            self.temp_sin_freq = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_sin_freq.place(x=75, y=60)
            self.temp_sin_freq_word = tk.Label(self.text_frame,text="正弦波频率", width=7, bg="WhiteSmoke").place(x=0, y=58)
            
            self.temp_time = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_time.place(x=75, y=100)
            self.temp_time_word = tk.Label(self.text_frame,text="仿真时间", width=6, bg="WhiteSmoke").place(x=5, y=98)
            
            self.temp_wave_id = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_wave_id.place(x=75, y=140)
            self.temp_wave_id_word = tk.Label(self.text_frame,text="方波序号", width=6, bg="WhiteSmoke").place(x=5, y=138)
            
            self.temp_wave_id2 = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_wave_id2.place(x=75, y=180)
            self.temp_wave_id2_word = tk.Label(self.text_frame,text="正弦波序号", width=7, bg="WhiteSmoke").place(x=0, y=178)
            
            self.temp_wave_comp_id = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_wave_comp_id.place(x=75, y=220)
            self.temp_wave_comp_id_word = tk.Label(self.text_frame,text="元件序号", width=6, bg="WhiteSmoke").place(x=5, y=218)
            
            self.temp_wave_select = tk.Entry(self.text_frame, width=14, bg="White", highlightthickness=0, bd=1)
            self.temp_wave_select.place(x=75, y=260)
            self.temp_wave_select_word = tk.Label(self.text_frame,text="电压/电流", width=6, bg="WhiteSmoke").place(x=5, y=258)
            
            self.temp_wave_button = tk.Button(self.task_frame, text="Run", highlightbackground="WhiteSmoke")
            self.temp_wave_button.bind("<ButtonPress>", self.temp_wave_get)
            self.temp_wave_button.place(relx=0.37, rely=0.95)
            
    # 电路参数求解的按钮函数       
    def data_get(self, event):
        self.getdone(event)
        self.imfrom_text.config(state=tk.NORMAL)
        self.imfrom_text.delete("1.0", tk.END)
        e=switch.switch_List(copy.deepcopy(self.result))
        data = calculator.get_linear_solution(e)
        data_text = calculator.solution_to_str(data, e)
        self.imfrom_text.insert(tk.END, data_text)
        self.imfrom_text.config(state=tk.DISABLED)
    
    # 戴维南定理求解按钮函数
    def DWN_get(self, event):
        self.getdone(event)
        step_length = float(self.step_length.get())
        R_number = int(self.R_number.get())
        R_start = float(self.R_start.get())
        R_end = float(self.R_end.get())
        e=switch.switch_List(self.result)
        apply.ana_daiweinan(e,R_number,step_length,R_start,R_end )
                   
    # 复频域分析按钮函数
    def complex_get(self, event):
        self.getdone(event)
        self.complex_text.config(state=tk.NORMAL)
        self.complex_text.delete("1.0", tk.END)
        complex_freq = float(self.complex_freq.get())
        e=switch.switch_List(self.result)
        solution=calculator.get_linear_complex_solution(e,complex_freq)
        string=switch.solution_complexstr(solution, e)
        self.complex_text.insert(tk.END, string)       
        self.complex_text.config(state=tk.DISABLED)
    
    # 最大功率传输定理按钮函数    
    def max_get(self,event):
        self.getdone(event)
        max_freq = float(self.max_freq.get())
        max_length = float(self.max_length.get())
        max_R_number = int(self.max_R_number.get())
        max_R_start = float(self.max_R_start.get())
        max_R_end = float(self.max_R_end.get())
        e=switch.switch_List(self.result)
        apply.max_power_law(e,max_R_number,max_length,max_R_start,max_R_end,max_freq)
    
    # 方波暂态分析按钮函数
    def wave_get(self, event):
        self.getdone(event)
        wave_freq = float(self.wave_freq.get())
        wave_time = float(self.wave_time.get())
        wave_id = int(self.wave_id.get())
        wave_comp_id = int(self.wave_comp_id.get())
        wave_select = str(self.wave_select.get())
        
        e=switch.switch_List(self.result)
        e[wave_id]=componnet_fang_source_v(e[wave_id].get_net(),[e[wave_id].property,wave_freq])
        calculator.cal_longe_targeted(e,[[wave_comp_id,wave_select]],wave_time)
       
    # 暂态分析按钮函数
    def temp_wave_get(self, event):
        self.getdone(event)
        if self.temp_fang_freq.get()!= '':
            temp_fang_freq = float(self.temp_fang_freq.get())
        else:
            temp_fang_freq = 1.0
                   
        if self.temp_sin_freq.get()!='':
            temp_sin_freq = float(self.temp_sin_freq.get())   
        else:
            temp_sin_freq = 1.0


        temp_wave_time = float(self.temp_time.get())
        temp_wave_id = self.temp_wave_id.get().split(',')
        if temp_wave_id!=['']:
            temp_wave_id=[int(i) for i in temp_wave_id] 
        else:
            temp_wave_id=[]
        temp_wave_id2 = self.temp_wave_id2.get().split(',')       
        if temp_wave_id2!=['']:        
            temp_wave_id2=[int(i) for i in temp_wave_id2] 
        else:
            temp_wave_id2=[]     
        temp_wave_comp_id = int(self.temp_wave_comp_id.get())
        temp_wave_select = str(self.temp_wave_select.get())
        e=switch.switch_List(self.result)
        for i in temp_wave_id:
            e[i]=componnet_fang_source_v(e[i].get_net(),[e[i].property,temp_fang_freq])
        for i in temp_wave_id2:
            e[i]=componnet_sin_source_v(e[i].get_net(),[e[i].property,temp_sin_freq])
        target_list=[]
        '''for i in range(len(temp_wave_comp_id):
            target_list.append([temp_wave_comp_id[i],]))'''
        calculator.cal_longe_targeted(e,[[temp_wave_comp_id,temp_wave_select]],temp_wave_time)
            
    # 一键清除函数                     
    def comp_clear(self):
        self.canvas.delete("all")
        for item in self.lst_of_Eitem:
            item.delete_label()
            item.delete_label_net()
        self.comp_imformation = []
        self.lst = []
        self.wtclst = []
        self.set_of_line = []
        self.lst_of_Eitem = []
        self.result = []
        self.comp_id = 0
    
    # 按住 Command + 右键 顺时针旋转元件90度
    def rotate_comp(self, event, id, object, item):
        self.comp_imformation[id][0] = self.comp_imformation[id][0].rotate(-90)
        
        if self.comp_imformation[id][4] != 270:
            self.comp_imformation[id][4] +=90 
        else:
            self.comp_imformation[id][4] =0      
              
        self.comp_imformation[id][2] = ImageTk.PhotoImage(self.comp_imformation[id][0])
        self.canvas.itemconfig(self.comp_imformation[id][1], image=self.comp_imformation[id][2])

        left, top, right, bottom = self.canvas.bbox(item)
        if self.comp_imformation[id][4] == 0:
            object.point1 = [left + 6.7, top + 34.6]
            object.point2 = [right - 6.7, top + 34.6]
            object.point_for_net1 = [left - 12, top + 38]
            object.point_for_net2 = [right + 2, top + 38]
        if self.comp_imformation[id][4] == 90:
            object.point1 = [left + 34.6, top + 6.7]
            object.point2 = [left + 34.6, bottom - 6.7]
            object.point_for_net1 = [left + 38, top - 15]
            object.point_for_net2 = [left + 38, bottom]
        if self.comp_imformation[id][4] == 180:
            object.point1 = [right - 6.7, top + 34.6]
            object.point2 = [left + 6.7, top + 34.6]
            object.point_for_net1 = [right + 2, top + 38]
            object.point_for_net2 = [left - 12, top + 38]
        if self.comp_imformation[id][4] == 270:
            object.point1 = [left + 34.6, bottom - 6.7]
            object.point2 = [left + 34.6, top + 6.7]
            object.point_for_net1 = [left + 38, bottom]
            object.point_for_net2 = [left + 38, top - 15]
        object.update()
        if object.havenet:
            object.move_label_net()
        
    # 记录拖动开始时的鼠标位置和图像ID      
    def start_drag(self, event, id):
        self.drag_data["item"] = self.comp_imformation[id][1]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    # 清除拖动数据
    def stop_drag(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        
    # 计算鼠标移动的距离
    def on_drag(self, item, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            # 移动图像
            self.canvas.move(self.drag_data["item"], dx, dy)
            # 更新鼠标位置
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            item.point1[0] += dx
            item.point1[1] += dy
            item.point2[0] += dx
            item.point2[1] += dy
            item.point_for_label[0] += dx
            item.point_for_label[1] += dy
            item.point_for_net1[0] += dx
            item.point_for_net1[1] += dy
            item.point_for_net2[0] += dx
            item.point_for_net2[1] += dy
            item.update()
            item.move_label()
            if item.havenet:
                item.move_label_net()
            
    # control + 左键 删除元件 
    def delete_comp(self, event, item, c_item):
        self.canvas.delete(item)
        c_item.delete_label()
        for i in self.lst_of_Eitem:
            i.delete_label_net()
        self.lst_of_Eitem.remove(c_item)
        for line in c_item.coctl1:
            self.canvas.delete(line.line1)
            self.canvas.delete(line.line2)
            self.set_of_line.remove(line)
            for the_other_item in self.lst_of_Eitem:
                if line in the_other_item.coctl2:
                    the_other_item.coctl2.remove(line)
                if line in the_other_item.coctl1:
                    the_other_item.coctl1.remove(line)
        for line in c_item.coctl2:
            self.canvas.delete(line.line1)
            self.canvas.delete(line.line2)
            self.set_of_line.remove(line)
            for the_other_item in self.lst_of_Eitem:
                if line in the_other_item.coctl1:
                    the_other_item.coctl1.remove(line)
        for the_other_item in self.lst_of_Eitem:
            the_other_item.name = ''
            the_other_item.update_label()
                    
    # 滚轮滑动事件       
    def zoom(self, event):
        x = self.canvas.canvasx(event.x)  # 获取鼠标坐标，并以鼠标位置为中心进行缩放
        y = self.canvas.canvasy(event.y)
        factor = 1.07 if event.delta > 0 else 1 / 1.07
        self.scale *= factor
        self.canvas.scale("all", x, y, factor, factor)
        self.zoom_label.config(text=f"{int(self.scale)}%")  # 更新缩放比例显示
        self.resize_comp()

    # png图片缩放函数
    def resize_comp(self):
        for i in range(len(self.comp_imformation)):
            self.original_width, self.original_height = self.comp_imformation[i][0].size  # 获取图片原尺寸
            new_width = int(self.original_width * self.scale / 100)  # 更新新的长和宽
            new_height = int(self.original_height * self.scale / 100)
            resized_image = self.comp_imformation[i][0].resize((new_width, new_height))
            self.comp_imformation[i][2] = ImageTk.PhotoImage(resized_image)  # 此处一定不能用临时变量
            self.canvas.itemconfig(self.comp_imformation[i][1], image=self.comp_imformation[i][2])

    # 获取按下滚轮时的鼠标位置
    def on_mouse_press(self, event):
        self.drag_canvas["prew_x"] = event.x
        self.drag_canvas["prew_y"] = event.y

    # 移动元件
    def on_mouse_drag(self, event):
        if self.drag_canvas["prew_x"] is not None and self.drag_canvas["prew_y"] is not None:
            dx = event.x - self.drag_canvas["prew_x"]
            dy = event.y - self.drag_canvas["prew_y"]
            self.canvas.move("all", dx, dy)
            self.drag_canvas["prew_x"] = event.x
            self.drag_canvas["prew_y"] = event.y

    # 松开滚轮
    def on_mouse_release(self, event):
        self.drag_canvas["prew_x"] = None
        self.drag_canvas["prew_y"] = None
        
    # 获取整个电路的信息
    def getdone(self, event):
        self.result = []
        i = 0
        for item in self.lst_of_Eitem:
            item.num = i
            name = ['', 'U', 'I', 'R', 'C', 'L']
            item.name = f"{name[item.kind]}" + f"{i}" + ':'
            item.update_label()
            i += 1
        for item in self.lst_of_Eitem:
            r_ = []
            r_.append(item.kind)
            r_.append(item.property)
            r_.append(item.getcw(event))
            self.result.append(r_)
        e=switch.switch_List(copy.deepcopy(self.result))
        apply.print_s(e)
        #for l in self.result:
        #   print(l)
        #e=switch.switch_List(copy.deepcopy(self.result))
        #print(calculator.get_linear_solution(e))
        
    # 获取整个电路的信息 如果不完整则弹出提醒信息
    def node_get(self, event):
        self.result = []
        # 先检查电路是否完整
        complete = 0
        have_ground = 0
        for item in self.lst_of_Eitem:
            if not item.kind and item.coctl1:
                have_ground = 1
            if item.kind == 1 or item.kind == 2:
                complete = 1
        for item in self.lst_of_Eitem:
            if not item.coctl1 or not item.coctl2 and item.kind:
                complete = 0
        if not complete or not have_ground:
            tk.messagebox.showinfo('获取失败', '请将电路连接完整')

        # 电路检查完整，将电路信息传出处理
        else:
            self.getdone(event)
            
            # 获得每个元件两端各节点，并在图上显示
            result_net = switch.assume_net(self.result)
            j = 0
            for item in self.lst_of_Eitem:
                item.delete_label_net()
                if item.kind:
                    item.net = result_net[j][2]
                j += 1
                item.show_label_net()
       

        

def main():
    root = tk.Tk()
    UI = GUI(root)
    root.geometry("1100x700")
    root.mainloop()

if __name__ == "__main__":
    main()
