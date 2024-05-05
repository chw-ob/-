import tkinter as tk

def get_entry_value():
    value = entry.get()
    result_label.config(text="输入的值是：" + value)

root = tk.Tk()
root.title("获取Entry控件输入的值")

entry = tk.Entry(root)
entry.pack(padx=10, pady=10)

get_value_button = tk.Button(root, text="获取值", command=get_entry_value)
get_value_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()