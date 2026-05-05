import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

# Настройки окна
window = tk.Tk()
window.title("Password Gen v1.0")
window.geometry("380x450")

# Путь к базе с историей
DB_FILE = "history.json"

def generate():
    # Получаем длину из ползунка
    length = length_slider.get()
    
    # Собираем символы в зависимости от галочек
    chars = ""
    if var_digits.get():
        chars += string.digits
    if var_letters.get():
        chars += string.ascii_letters
    if var_spec.get():
        chars += string.punctuation
        
    # Проверка: если ничего не выбрано (Валидация)
    if not chars:
        messagebox.showwarning("Ошибка", "Выберите типы символов!")
        return
        
    # Сама генерация
    new_password = "".join(random.choice(chars) for i in range(length))
    
    # Вывод в таблицу
    history_tree.insert("", 0, values=(new_password,))
    
    # Сохраняем в JSON
    save_to_file(new_password)

def save_to_file(pwd):
    data = []
    # Если файл уже есть - читаем старое
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []
    
    data.append(pwd)
    
    # Записываем обновленный список
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_data():
    # Загрузка истории при старте программы
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                items = json.load(f)
                for item in items:
                    history_tree.insert("", "end", values=(item,))
            except:
                pass

# Интерфейс (виджеты)
tk.Label(window, text="Настройки пароля", font=("Arial", 12, "bold")).pack(pady=10)

# Длина
tk.Label(window, text="Выберите длину:").pack()
length_slider = tk.Scale(window, from_=4, to=30, orient="horizontal")
length_slider.set(12) # По умолчанию 12
length_slider.pack(fill="x", padx=30)

# Чекбоксы
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_spec = tk.BooleanVar()

tk.Checkbutton(window, text="Использовать цифры", variable=var_digits).pack(anchor="w", padx=50)
tk.Checkbutton(window, text="Использовать буквы", variable=var_letters).pack(anchor="w", padx=50)
tk.Checkbutton(window, text="Спецсимволы", variable=var_spec).pack(anchor="w", padx=50)

# Кнопка
btn = tk.Button(window, text="СОЗДАТЬ ПАРОЛЬ", command=generate, bg="lightgray", height=2)
btn.pack(pady=20, fill="x", padx=30)

# Таблица истории
history_tree = ttk.Treeview(window, columns=("pass"), show="headings", height=5)
history_tree.heading("pass", text="Последние пароли")
history_tree.pack(padx=10, pady=10, fill="both")

# Загружаем старые данные и запускаем
load_data()
window.mainloop()
