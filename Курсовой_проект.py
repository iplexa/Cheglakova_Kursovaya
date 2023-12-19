import tkinter as tk
from tkinter import messagebox, filedialog
import io
import sqlite3
import pandas as pd
from PIL import Image, ImageTk
from tkinter.ttk import Treeview
import os


class PhoneBookApp:
    def __init__(self, master):
        self.master = master
        master.title("Телефонная книга")

        background_image = Image.open("фон_тел_книга.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(master, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Создание и размещение меток и полей ввода
        self.label_name = tk.Label(master, text="Имя:", bg="sky blue")
        self.label_name.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_name = tk.Entry(master, bg="sky blue")
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_surname = tk.Label(master, text="Фамилия:", bg="sky blue")
        self.label_surname.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_surname = tk.Entry(master, bg="sky blue")
        self.entry_surname.grid(row=1, column=1, padx=10, pady=10)

        self.label_dob = tk.Label(master, text="Дата рождения:", bg="sky blue")
        self.label_dob.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_dob = tk.Entry(master, bg="sky blue")
        self.entry_dob.grid(row=2, column=1, padx=10, pady=10)

        self.label_country = tk.Label(master, text="Страна:", bg="sky blue")
        self.label_country.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_country = tk.Entry(master, bg="sky blue")
        self.entry_country.grid(row=3, column=1, padx=10, pady=10)

        self.label_number = tk.Label(master, text="Телефон:", bg="sky blue")
        self.label_number.grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.entry_number = tk.Entry(master, bg="sky blue")
        self.entry_number.grid(row=4, column=1, padx=10, pady=10)

        # Создание и размещение кнопок
        self.button_browse_photo = tk.Button(master, text="Добавить фото", command=self.browse_photo, width=30, bg="sky blue",)
        self.button_browse_photo.grid(row=5, column=0, padx=10, pady=10, columnspan=2)

        self.button_add = tk.Button(master, text="Добавить контакт", command=self.add_contact, width=20)
        self.button_add.grid(row=6, column=0, padx=10, pady=10)
        self.button_add.config(bg="pale green")

        self.button_delete = tk.Button(master, text="Удалить контакт", command=self.delete_contact, width=20)
        self.button_delete.grid(row=6, column=1, padx=10, pady=10)
        self.button_delete.config(bg="pink")

        self.button_show_all = tk.Button(master, text="Показать все контакты", command=self.show_all_contacts, width=20, bg="sky blue")
        self.button_show_all.grid(row=8, column=0, padx=10, pady=10)

        self.button_search = tk.Button(master, text="Поиск контактов", command=self.search_contacts, width=20, bg="sky blue")
        self.button_search.grid(row=7, column=0, padx=10, pady=10)

        self.button_export_excel = tk.Button(master, text="Вывести в Excel", command=self.export_to_excel, width=20, bg="sky blue")
        self.button_export_excel.grid(row=8, column=1, padx=10, pady=10)

        self.button_show_contact = tk.Button(master, text="Просмотреть контакт", command=self.show_contact, width=20, bg="sky blue")
        self.button_show_contact.grid(row=7, column=1, padx=10, pady=10)

        # Создание и подключение к базе данных
        self.connection = sqlite3.connect("phone_book.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                surname TEXT,
                dob TEXT,
                country TEXT,
                number TEXT,
                photo BLOB DEFAULT NULL
            )
        """)
        self.connection.commit()

    def browse_photo(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.photo_path = filepath
            messagebox.showinfo("Фото", "Файл фотографии выбран успешно.")
        else:
            messagebox.showinfo("Фото", "Файл фотографии не выбран.")

    def add_contact(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        dob = self.entry_dob.get()
        country = self.entry_country.get()
        number = self.entry_number.get()

        if name and number and hasattr(self, "photo_path"):
            # Чтение фото из файла
            with open(self.photo_path, "rb") as file:
                photo_data = file.read()

            # Добавление контакта в таблицу contacts
            self.cursor.execute("INSERT INTO contacts (name, surname, dob, country, number, photo) "
                                "VALUES (?, ?, ?, ?, ?, ?)",
                                (name, surname, dob, country, number, photo_data))
            self.connection.commit()
            messagebox.showinfo("Добавление", "Контакт успешно добавлен!")
            self.clear_entries()
            delattr(self, "photo_path")
        else:
            messagebox.showwarning("Добавление", "Заполните все данные!")

    def search_contacts(self):
        criteria = self.entry_name.get()

        if criteria:
            # Поиск контактов по критерию имени
            self.cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + criteria + '%',))
            matching_contacts = self.cursor.fetchall()

            if matching_contacts:
                result = "Результаты поиска:\n"
                for contact in matching_contacts:
                    result += f'Имя: {contact[1]}, Фамилия: {contact[2]}, Дата рождения: {contact[3]}, Страна: {contact[4]}, Телефон: {contact[5]}\n'
                messagebox.showinfo("Поиск", result)
                self.clear_entries()
            else:
                messagebox.showinfo("Поиск", "Нет результатов поиска.")
                self.clear_entries()
        else:
            messagebox.showwarning("Поиск", "Введите критерии поиска!")

    def delete_contact(self):
        name = self.entry_name.get()

        if name:
            # Поиск контакта по имени
            self.cursor.execute("SELECT * FROM contacts WHERE name=?", (name,))
            contact = self.cursor.fetchone()

            if contact:
                # Удаление контакта из таблицы contacts
                self.cursor.execute("DELETE FROM contacts WHERE name=?", (name,))
                self.connection.commit()
                messagebox.showinfo("Удаление", "Контакт успешно удален!")
                self.clear_entries()
            else:
                messagebox.showwarning("Удаление", "Абонент не найден!")
        else:
            messagebox.showwarning("Удаление", "Введите имя абонента для удаления!")

    def show_all_contacts(self):
        # Создание нового окна и настройка его свойств
        window = tk.Toplevel()
        window.title("Все контакты")
        window.geometry("1000x250")

        background_image = Image.open("фон_тел_книга.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(window, image=background_photo)
        background_label.image = background_photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Создание и настройка виджета Treeview
        tree = Treeview(window)
        tree["columns"] = ("Name", "Surname", "Date of Birth", "Country", "Phone")
        tree.column("#0", width=0, stretch="no")
        tree.column("Name", anchor="w")
        tree.column("Surname", anchor="w")
        tree.column("Date of Birth", anchor="w")
        tree.column("Country", anchor="w")
        tree.column("Phone", anchor="w")

        # Установка заголовков столбцов
        tree.heading("Name", text="Имя")
        tree.heading("Surname", text="Фамилия")
        tree.heading("Date of Birth", text="Дата рождения")
        tree.heading("Country", text="Страна")
        tree.heading("Phone", text="Телефон")

        # Получение всех контактов из таблицы contacts
        self.cursor.execute("SELECT * FROM contacts")
        contacts = self.cursor.fetchall()

        if contacts:
            for contact in contacts:
                # Добавление контакта в виджет Treeview
                tree.insert("", "end", text="", values=(contact[1], contact[2], contact[3], contact[4], contact[5]))

            tree.pack(padx=10, pady=10)
        else:
            messagebox.showinfo("Все контакты", "Телефонная книга пуста.")

    def export_to_excel(self):
        # Получение всех контактов из таблицы contacts
        self.cursor.execute("SELECT * FROM contacts")
        contacts = self.cursor.fetchall()

        if contacts:
            df = pd.DataFrame(contacts, columns=["id", "Имя", "Фамилия", "Дата рождения", "Страна", "Телефон", "Фото"])
            df = df.drop(columns=["id", "Фото"])
            df.to_excel("phone_book.xlsx", index=False, sheet_name="Телефонная книга")
            messagebox.showinfo("Экспорт в Excel", "Данные успешно экспортированы в файл phone_book.xlsx!")

            # Открытие файла
            try:
                os.startfile("phone_book.xlsx")
            except OSError:
                messagebox.showinfo("Открытие файла", "Не удалось открыть файл.")
        else:
            messagebox.showinfo("Экспорт в Excel", "Телефонная книга пуста.")

    def show_contact(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        if name and surname:
            self.cursor.execute("SELECT * FROM contacts WHERE name=? AND surname=?", (name, surname))
            contact = self.cursor.fetchone()

            if contact:
                # Создание нового окна и настройка его свойств
                contact_window = tk.Toplevel()
                contact_window.title("Контакт")
                contact_window.geometry("270x240")

                background_image = Image.open("фон_тел_книга.jpg")
                background_photo = ImageTk.PhotoImage(background_image)
                background_label = tk.Label(contact_window, image=background_photo)
                background_label.image = background_photo
                background_label.place(x=0, y=0, relwidth=1, relheight=1)

                # Разбор информации о контакте
                contact_id, name, surname, dob, country, number, photo = contact

                # Отображение фотографии
                if photo:
                    pil_image = Image.open(io.BytesIO(photo))
                    pil_image.thumbnail((100, 100))  # Изменение размеров до миниатюры
                    photo = ImageTk.PhotoImage(pil_image)
                    photo_label = tk.Label(contact_window, image=photo)
                    photo_label.image = photo
                    photo_label.pack(pady=10)

                # Отображение информации о контакте
                tk.Label(contact_window, text=f"Имя: {name}", bg="sky blue").pack()
                tk.Label(contact_window, text=f"Фамилия: {surname}", bg="sky blue").pack()
                tk.Label(contact_window, text=f"Дата рождения: {dob}", bg="sky blue").pack()
                tk.Label(contact_window, text=f"Страна: {country}", bg="sky blue").pack()
                tk.Label(contact_window, text=f"Телефон: {number}", bg="sky blue").pack()

            else:
                messagebox.showwarning("Просмотр контакта", "Контакт не найден.")

        else:
            messagebox.showwarning("Просмотр контакта", "Введите имя контакта.")

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_surname.delete(0, tk.END)
        self.entry_dob.delete(0, tk.END)
        self.entry_country.delete(0, tk.END)
        self.entry_number.delete(0, tk.END)

    def __del__(self):
        # Закрытие подключения к базе данных при закрытии приложения
        self.connection.close()


root = tk.Tk()
root.geometry("340x390")

phone_book_app = PhoneBookApp(root)

root.mainloop()