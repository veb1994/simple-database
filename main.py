import tkinter as tk
from tkinter import ttk
import sqlite3

# Таблица "Маршруты" с панелью управления
class MainRoute(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_route()

    def init_main(self):
        # Маршруты - начало блока
        toolbar_route = tk.LabelFrame(text='Маршруты', bg='#d7d8e0', bd=2)
        toolbar_route.pack(fill=tk.X)

        btn_add_route = tk.Button(toolbar_route, text='Добавить маршрут', command=self.open_dialog_route, bg='#d7d8e0', bd=1)
        btn_add_route.pack(side=tk.LEFT)

        btn_edit_route = tk.Button(toolbar_route, text='Редактировать маршрут', command=self.open_dialog_update_route, bg='#d7d8e0', bd=1)
        btn_edit_route.pack(side=tk.LEFT)

        btn_delete_route = tk.Button(toolbar_route, text='Удалить маршрут', command=self.route_delete, bg='#d7d8e0', bd=1)
        btn_delete_route.pack(side=tk.LEFT)

        self.route_table = ttk.Treeview(self, columns=('country', 'papers', 'road', 'daycost'), height=5,
                                        show='headings')
        self.route_table.column('country', width=120, anchor=tk.CENTER)
        self.route_table.column('papers', width=180, anchor=tk.CENTER)
        self.route_table.column('road', width=200, anchor=tk.CENTER)
        self.route_table.column('daycost', width=190, anchor=tk.CENTER)
        self.route_table.heading('country', text='Страна')
        self.route_table.heading('papers', text='Оформление документов, руб.')
        self.route_table.heading('road', text='Стоимость проезда, руб.')
        self.route_table.heading('daycost', text='Стоимость дня проживания, руб.')
        self.route_table.pack()
        # Маршруты - конец блока

    def route_add(self, country, papers, road, daycost):
        self.db.insert_route(country, papers, road, daycost)
        self.view_route()  # Вызов отображения данных таблицы после изменения

    def route_update(self, country, papers, road, daycost):
        self.db.c.execute('''UPDATE route SET country=?, papers=?, road=?, daycost=? WHERE country=?''',
                          (country, papers, road, daycost, self.route_table.set(self.route_table.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_route()

    def route_delete(self):
        for selection_item in self.route_table.selection():
            self.db.c.execute('''DELETE FROM route WHERE country=?''', (self.route_table.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_route()

    def view_route(self):
        self.db.c.execute('''SELECT * FROM route ORDER BY country''')
        [self.route_table.delete(i) for i in self.route_table.get_children()]  # Очистка содержимого виджета при изменении данных для корректного отображения
        [self.route_table.insert('', 'end', values=row) for row in self.db.c.fetchall()]  # Генератор списков для отображения данных

    def open_dialog_route(self):
        Route()

    def open_dialog_update_route(self):
        RouteUpdate()

# Таблица "Клиенты" с панелью управления
class MainClient(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_client()

    def init_main(self):
        # Клиенты - начало блока
        toolbar_client = tk.LabelFrame(text='Клиенты', bg='#d7d8e0', bd=2)
        toolbar_client.pack(fill=tk.X)

        btn_add_client = tk.Button(toolbar_client, text='Добавить клиента', command=self.open_dialog_client, bg='#d7d8e0', bd=1)
        btn_add_client.pack(side=tk.LEFT)

        btn_edit_client = tk.Button(toolbar_client, text='Редактировать данные клиента', command=self.open_dialog_update_client, bg='#d7d8e0', bd=1)
        btn_edit_client.pack(side=tk.LEFT)

        btn_delete_client = tk.Button(toolbar_client, text='Удалить данные клиента', command=self.client_delete, bg='#d7d8e0', bd=1)
        btn_delete_client.pack(side=tk.LEFT)

        self.client_table = ttk.Treeview(self, columns=('name', 'passport', 'phone'), height=5, show='headings')
        self.client_table.column('name', width='200', anchor=tk.CENTER)
        self.client_table.column('passport', width='200', anchor=tk.CENTER)
        self.client_table.column('phone', width='200', anchor=tk.CENTER)
        self.client_table.heading('name', text='ФИО')
        self.client_table.heading('passport', text='Серия и номер паспорта')
        self.client_table.heading('phone', text='Телефон')
        self.client_table.pack()
        # Клиенты - конец блока

    def client_add(self, name, passport, phone):
        self.db.insert_client(name, passport, phone)
        self.view_client()  # Вызов отображения данных таблицы после изменения

    def client_update(self, name, passport, phone):
        self.db.c.execute('''UPDATE client SET name=?, passport=?, phone=? WHERE name=?''',
                          (name, passport, phone, self.client_table.set(self.client_table.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_client()

    def client_delete(self):
        for selection_item in self.client_table.selection():
            self.db.c.execute('''DELETE FROM client WHERE name=?''', (self.client_table.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_client()

    def view_client(self):
        self.db.c.execute('''SELECT * FROM client ORDER BY name''')
        [self.client_table.delete(i) for i in
         self.client_table.get_children()]  # Очистка содержимого виджета при изменении данных для корректного отображения
        [self.client_table.insert('', 'end', values=row) for row in
         self.db.c.fetchall()]  # Генератор списков для отображения данных

    def open_dialog_client(self):
        Client()

    def open_dialog_update_client(self):
        ClientUpdate()

# Таблица "Поездки" с панелью управления
class MainTrip(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_trip()

    def init_main(self):
        # Поездки - начало блока
        toolbar_trip = tk.LabelFrame(text='Поездки', bg='#d7d8e0', bd=2)
        toolbar_trip.pack(fill=tk.X)

        btn_add_trip = tk.Button(toolbar_trip, text='Добавить поездку', command=self.open_dialog_trip, bg='#d7d8e0', bd=1)
        btn_add_trip.pack(side=tk.LEFT)

        btn_edit_trip = tk.Button(toolbar_trip, text='Редактировать поездку', command=self.open_dialog_update_trip, bg='#d7d8e0', bd=1)
        btn_edit_trip.pack(side=tk.LEFT)

        btn_delete_trip = tk.Button(toolbar_trip, text='Удалить поездку', command=self.trip_delete, bg='#d7d8e0', bd=1)
        btn_delete_trip.pack(side=tk.LEFT)

        self.trip_table = ttk.Treeview(self, columns=('ID', 'name', 'passport', 'route', 'date', 'days', 'total'),
                                       height=10, show='headings')
        self.trip_table.column('ID', width='30', anchor=tk.CENTER)
        self.trip_table.column('name', width='215', anchor=tk.CENTER)
        self.trip_table.column('passport', width='200', anchor=tk.CENTER)
        self.trip_table.column('route', width='150', anchor=tk.CENTER)
        self.trip_table.column('date', width='150', anchor=tk.CENTER)
        self.trip_table.column('days', width='200', anchor=tk.CENTER)
        self.trip_table.column('total', width='150', anchor=tk.CENTER)
        self.trip_table.heading('ID', text='ID')
        self.trip_table.heading('name', text='ФИО')
        self.trip_table.heading('passport', text='Паспорт')
        self.trip_table.heading('route', text='Маршрут')
        self.trip_table.heading('date', text='Дата выезда')
        self.trip_table.heading('days', text='Продолжительность поездки, д.')
        self.trip_table.heading('total', text='Стоимость, руб.')
        self.trip_table.pack()
        # Поездки - конец блока

    def trip_add(self, name, passport, route, date, days, total):
        self.db.insert_trip(name, passport, route, date, days, total)
        self.view_trip()

    def trip_update(self, name, passport, route, date, days, total):
        self.db.c.execute('''UPDATE trip SET name=?, passport=?, route=?, date=?, days=?, total=? WHERE ID=?''',
                          (name, passport, route, date, days, total, self.trip_table.set(self.trip_table.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_trip()

    def trip_delete(self):
        for selection_item in self.trip_table.selection():
            self.db.c.execute('''DELETE FROM trip WHERE ID=?''', (self.trip_table.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_trip()


    def view_trip(self):
        self.db.c.execute('''SELECT * FROM trip''')
        [self.trip_table.delete(i) for i in
         self.trip_table.get_children()]  # Очистка содержимого виджета при изменении данных для корректного отображения
        [self.trip_table.insert('', 'end', values=row) for row in
         self.db.c.fetchall()]  # Генератор списков для отображения данных

    def open_dialog_trip(self):
        Trip()

    def open_dialog_update_trip(self):
        TripUpdate()

# Окно добавления маршрута
class Route(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_route()
        self.view = app_route

    def init_route(self):
        self.title('Добавить маршрут')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_country = tk.Label(self, text='Страна')
        label_country.place(x=10, y=50)
        label_papers = tk.Label(self, text='Оформление документов, руб.')
        label_papers.place(x=10, y=80)
        label_road = tk.Label(self, text='Стоимость проезда, руб.')
        label_road.place(x=10, y=110)
        label_daycost = tk.Label(self, text='Стоимость дня проживания, руб.')
        label_daycost.place(x=10, y=140)

        self.entry_country = ttk.Entry(self)
        self.entry_country.place(x=220, y=50, width=150)
        self.entry_papers = ttk.Entry(self)
        self.entry_papers.place(x=220, y=80, width=150)
        self.entry_road = ttk.Entry(self)
        self.entry_road.place(x=220, y=110, width=150)
        self.entry_daycost = ttk.Entry(self)
        self.entry_daycost.place(x=220, y=140, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=180)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=120, y=180)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.route_add(self.entry_country.get(),
                                                                         self.entry_papers.get(),
                                                                         self.entry_road.get(),
                                                                         self.entry_daycost.get()))

        self.grab_set()
        self.focus_set()

# Окно редактирования маршрута
class RouteUpdate(Route):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_route_update()
        self.view = app_route

    def init_route_update(self):
        self.title('Изменить маршрут')

        self.entry_country.insert(0, (self.edited_route()[0]))
        self.entry_papers.insert(0, (self.edited_route()[1]))
        self.entry_road.insert(0, (self.edited_route()[2]))
        self.entry_daycost.insert(0, (self.edited_route()[3]))

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=100, y=180)
        btn_edit.bind('<Button-1>', lambda event: self.view.route_update(self.entry_country.get(),
                                                                         self.entry_papers.get(),
                                                                         self.entry_road.get(),
                                                                         self.entry_daycost.get()))
        self.btn_ok.destroy()

    def edited_route(self):
        for selection_item in self.view.route_table.selection():
            self.db.c.execute('''SELECT * FROM route WHERE country=?''', (self.view.route_table.set(selection_item, '#1'),))
        values = []
        for row in self.db.c.fetchall():
            values.append(row[0])
            values.append(row[1])
            values.append(row[2])
            values.append(row[3])
        return values

# Окно добавления клиента
class Client(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_client()
        self.view = app_client


    def init_client(self):
        self.title('Добавить клиента')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=10, y=50)
        label_passport = tk.Label(self, text='Серия и номер паспорта')
        label_passport.place(x=10, y=80)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=10, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=220, y=50, width=150)
        self.entry_passport = ttk.Entry(self)
        self.entry_passport.place(x=220, y=80, width=150)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=220, y=110, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=180)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=120, y=180)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.client_add(self.entry_name.get(),
                                                                          self.entry_passport.get(),
                                                                          self.entry_phone.get()))

        self.grab_set()
        self.focus_set()

# Окно для изменения данных клиента
class ClientUpdate(Client):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_client_update()
        self.view = app_client

    def init_client_update(self):
        self.title('Изменить данные клиента')

        self.entry_name.insert(0, (self.edited_client()[0]))
        self.entry_passport.insert(0, (self.edited_client()[1]))
        self.entry_phone.insert(0, (self.edited_client()[2]))

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=100, y=180)
        btn_edit.bind('<Button-1>', lambda event: self.view.client_update(self.entry_name.get(),
                                                                          self.entry_passport.get(),
                                                                          self.entry_phone.get()))
        self.btn_ok.destroy()

    def edited_client(self):
        for selection_item in self.view.client_table.selection():
            self.db.c.execute('''SELECT * FROM client WHERE passport=?''', (self.view.client_table.set(selection_item, '#2'),))
        values = []
        for row in self.db.c.fetchall():
            values.append(row[0])
            values.append(row[1])
            values.append(row[2])
        return values

# Окно добавления поездки
class Trip(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.db = db
        self.init_trip()
        self.view = app_trip

    def init_trip(self):
        self.title('Добавить поездку')
        self.geometry('400x260+400+300')
        self.resizable(False, False)


        label_passport = tk.Label(self, text='Серия и номер паспорта')
        label_passport.place(x=10, y=80)
        label_route = tk.Label(self, text='Маршрут')
        label_route.place(x=10, y=110)
        label_date = tk.Label(self, text='Дата отправления')
        label_date.place(x=10, y=140)
        label_days = tk.Label(self, text='Длительность поездки (дней)')
        label_days.place(x=10, y=170)


        self.entry_passport = ttk.Entry(self)
        self.entry_passport.place(x=220, y=80, width=150)
        self.combobox_route = ttk.Combobox(self)
        self.combobox_route.place(x=220, y=110, width=150)
        self.combobox_route['values'] = self.combobox_values()
        self.entry_date = ttk.Entry(self)
        self.entry_date.place(x=220, y=140, width=150)
        self.entry_days = ttk.Entry(self)
        self.entry_days.place(x=220, y=170, width=150)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=230, y=230)

        x = 100

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=120, y=230)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.trip_add(self.client_name(),
                                                                        self.entry_passport.get(),
                                                                        self.combobox_route.get(),
                                                                        self.entry_date.get(),
                                                                        self.entry_days.get(),
                                                                        self.total()))

        self.grab_set()
        self.focus_set()

    def combobox_values(self):
        self.db.c.execute('''SELECT country FROM route''')
        data = []
        for row in self.db.c.fetchall():
            data.append(row[0])
        return data


    def client_name(self):
        passport = self.entry_passport.get()
        self.db.c.execute('''SELECT name FROM client WHERE passport=?''', (passport,))
        values = []
        for row in self.db.c.fetchall():
           values.append(row[0])
        name = values[0]
        return name

    def total(self):
        country = self.combobox_route.get()
        self.db.c.execute('''SELECT papers FROM route WHERE country=?''', (country,))
        papers_arr = []
        for row in self.db.c.fetchall():
            papers_arr.append(row[0])
        papers = papers_arr[0]

        self.db.c.execute('''SELECT road FROM route WHERE country=?''', (country,))
        road_arr = []
        for row in self.db.c.fetchall():
            road_arr.append(row[0])
        road = road_arr[0]

        self.db.c.execute('''SELECT daycost FROM route WHERE country=?''', (country,))
        daycost_arr = []
        for row in self.db.c.fetchall():
            daycost_arr.append(row[0])
        daycost = daycost_arr[0]

        days = float(self.entry_days.get())
        total = papers + road + daycost * days
        return total

# Окно изменения поездки
class TripUpdate(Trip):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_trip_update()
        self.view = app_trip
        self.view_route = app_route

    def init_trip_update(self):
        self.title('Изменить поездку')

        self.entry_passport.insert(0, (self.edited_trip()[0]))
        self.combobox_route.current(self.edited_trip_combobox()[0])
        self.entry_date.insert(0, (self.edited_trip()[2]))
        self.entry_days.insert(0, (self.edited_trip()[3]))


        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=100, y=230)
        btn_edit.bind('<Button-1>', lambda event: self.view.trip_update(self.client_name(),
                                                                        self.entry_passport.get(),
                                                                        self.combobox_route.get(),
                                                                        self.entry_date.get(),
                                                                        self.entry_days.get(),
                                                                        self.total()))
        self.btn_ok.destroy()

    def edited_trip(self):
        for selection_item in self.view.trip_table.selection():
            self.db.c.execute('''SELECT passport, route, date, days FROM trip WHERE ID=?''', (self.view.trip_table.set(selection_item, '#1'),))
        values = []
        for row in self.db.c.fetchall():
            values.append(row[0])
            values.append(row[1])
            values.append(row[2])
            values.append(row[3])
        return values

    def edited_trip_combobox(self):
        x = self.edited_trip()[1]
        self.db.c.execute('''SELECT COUNT (country) FROM route WHERE country<?''', x[0])
        values_combobox = []
        for row in self.db.c.fetchall():
            values_combobox.append(row[0])
        return  values_combobox

# Класс для работы с БД
class DB():
    def __init__(self):
        self.conn = sqlite3.connect('albatross.db')  # Подключение БД
        self.conn.execute('PRAGMA foreign_keys=ON')
        self.c = self.conn.cursor()  # Объект cursor нужен для работы с БД
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS route (country text primary key, papers real, road real, daycost real)''')
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS client (name text, passport integer primary key, phone text)''')
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS trip (id integer primary key, name text, passport integer REFERENCES client (passport), route text, date text CHECK (date LIKE '__.__.____'), days integer, total real)''')
        self.conn.commit()

    def insert_route(self, country, papers, road, daycost):
        self.c.execute('''INSERT INTO route (country, papers, road, daycost) VALUES (?, ?, ?, ?)''',
                       (country, papers, road, daycost))
        self.conn.commit()

    def insert_client(self, name, passport, phone):
        self.c.execute('''INSERT INTO client (name, passport, phone) VALUES (?, ?, ?)''', (name, passport, phone))
        self.conn.commit()

    def insert_trip(self, name, passport, route, date, days, total):
        self.c.execute('''INSERT INTO trip (name, passport, route, date, days, total) VALUES (?, ?, ?, ?, ?, ?)''',
                       (name, passport, route, date, days, total))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()  # Объект для связи таблиц с БД
    app_route = MainRoute(root)
    app_route.pack()
    app_client = MainClient(root)
    app_client.pack()
    app_trip = MainTrip(root)
    app_trip.pack()
    root.title("Туристическое агентство \"Альбатрос\"")
    root.geometry("1100x615+75+60")
    root.resizable(False, False)
    root.mainloop()
