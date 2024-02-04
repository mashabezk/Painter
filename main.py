import os
from random import randint
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb
from tkinter.colorchooser import askcolor
from PIL import ImageGrab

class Painter:
    def __init__(self, window):
        self.root = window
        self.root.geometry("1000x600+230+60")
        self.root.title("Графический редактор")
        self.icon = PhotoImage(file="icon.png")  # устанавливаем фото
        self.root.iconphoto(False, self.icon)  # указываем, что будем использовать заданную иконку

        self.size = 3
        self.color = "black"
        self.shape = None
        self.start_x = None
        self.start_y = None
        self.shapes = ["Прямоугольник", "Круг", "Треугольник"]
        self.enabled = BooleanVar(value=1)

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side=TOP, padx=10, pady=10)
        self.label = ttk.Label(self.button_frame,text="Фигуры").grid(row=1, column=2)
        self.label2 = ttk.Label(self.button_frame,text=f"Размер {self.size}").grid(row=1, column=4)
        self.spinbox_var = StringVar(value=self.size)

        # создаем кнопки и различные box
        ttk.Button(self.button_frame, text="Карандаш", command=self.to_start_draw).grid(row=0, column=0)
        ttk.Button(self.button_frame, text="Линия", command=self.to_start_line).grid(row=0, column=1)
        self.combobox = ttk.Combobox(self.button_frame, values=self.shapes, state="readonly")
        self.combobox.grid(row=0, column=2)
        ttk.Button(self.button_frame, text="Цвет", command=self.choose_color).grid(row=0, column=3)
        ttk.Button(self.button_frame, text="Очистить холст", command=self.clear_canvas).grid(row=0, column=5)
        ttk.Button(self.button_frame, command=self.save_file, text="Сохранить").grid(row=0, column=6)
        checkbutton = ttk.Checkbutton(self.button_frame, text="Заливка фигуры", command=self.checkbuttom_change, variable=self.enabled, onvalue=1, offvalue=0)
        checkbutton.grid(row=1, column=3)
        self.spinbox = ttk.Spinbox(self.button_frame, from_=1, to=20, command=self.choose_number, textvariable=self.spinbox_var)
        self.spinbox.grid(row=0, column=4)

        # биндим выпадющий список
        self.combobox.bind("<<ComboboxSelected>>", self.box_select)

        # создаем поле для рисования
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.pack(side=TOP, padx=10, pady=10)

        self.canvas = Canvas(self.canvas_frame, width=1000, height=600, bg="white")
        self.canvas.pack(anchor=CENTER, expand=1)

    # метод для выбора размера
    def choose_number(self):
        self.label2 = ttk.Label(self.button_frame, text=f"Размер {self.spinbox.get()}").grid(row=1, column=4)
        self.size = self.spinbox.get()

    # сохранение файла
    def save_file(self):
        path = os.getcwd() + "/outputFiles"
        if os.path.exists(path):
            filename = f'image_{randint(0, 100)}.png'
            x = self.canvas.winfo_rootx() + 70
            y = self.canvas.winfo_rooty() + 40
            w = x + self.canvas.winfo_width() + 230
            h = y + self.canvas.winfo_height() + 120
            ImageGrab.grab().crop((x, y, w, h)).save(path + "/" + filename)
            self.show_info(filename, path)
        else:
            os.mkdir(path)
            self.save_file()


    # создание вылетающего окна для сохранения файла
    def show_info(self, filename, path):
        mb.showinfo("Сохранение", "Файл с именем: " + filename + " сохранен в папку: " + path)

    # выбор цвета
    def choose_color(self):
        color = askcolor(color=self.color)
        self.color = color[1]

    def check(self):
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    # запуск рисования
    def to_start_draw(self):
        self.canvas.bind('<B1-Motion>', self.draw)

    # метод для рисования
    def draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.canvas.create_oval(self.start_x - 5, self.start_y - 5, self.start_x + 5, self.start_y + 5, fill=self.color, outline=self.color)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

    def end_draw(self, event):
        self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill=self.color, outline=self.color)

    # метод для проверки поставлена ли галочка на заливку
    def checkbuttom_change(self):
        print(self.enabled.get())
        if self.enabled.get() == 0:
            self.color = None
        elif self.enabled.get() == 1:
            self.color = "black"

    # метод для запуска рисования линии
    def to_start_line(self):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind("<Button-1>", self.on_start_draw)

    # метод для начала рисования линии
    def on_start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.on_end_draw)

    # метод для завершения рисования линии
    def on_end_draw(self, event):
        self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.size)

    # метод для запуска рисования фигур по событию
    def box_select(self, event):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind("<Button-1>", self.on_start_shape)

    # метод для начала рисования фигур
    def on_start_shape(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.bind("<ButtonRelease-1>", self.on_end_shape)

    # метод для завершения рисования фигур
    def on_end_shape(self, event):
        # self.checkbuttom_change()
        selection = self.combobox.get()
        if selection == "Прямоугольник":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.size)
        elif selection == "Круг":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=self.size)
        elif selection == "Треугольник":
            # высчитываем параметры для вписания треугольника в окружность
            R = (((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2)) ** 0.5
            side = R / 0.5773502691896258
            r = R / 2
            half_side = side / 2
            coordinates = [
                [0 + self.start_x, -R + self.start_y],
                [half_side + self.start_x, r + self.start_y],
                [-half_side + self.start_x, r + self.start_y]
            ]
            self.canvas.create_polygon(coordinates[0], coordinates[1], coordinates[2], fill=(self.color if self.color else ''), outline="black", width=self.size)

    # метод для очистки холста
    def clear_canvas(self):
        self.canvas.delete("all")

# метод для закрытия окна
def finish():
    root.destroy()  # ручное закрытие окна и всего приложения

root = Tk()  # создаем корневой объект - окно
root.protocol("WM_DELETE_WINDOW", finish)  # вызов события для закрытия окна

app = Painter(root) # cоздаем экземпляр приложения

root.mainloop()
