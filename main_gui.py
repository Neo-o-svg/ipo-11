import dearpygui.dearpygui as dpg
from transport import *
import json
import time

# ---------- Глобальные рабочие переменные----------

company = TransportCompany("CTK Logistic")
transport_list = ["Самолет", "Грузовик"]

client_row_count = 1
transport_row_count = 1

# ---------- Настройки интерфейса ----------

window_width, window_height = 1000, 800
popup_window_width, popup_window_height = 800, 400
state_button_width = 100
height_of_small_spacer = 10
height_of_medium_spacer = 30
height_of_big_spacer = 45
width_of_small_spacer = 15


# ---------- Функции очистки полей ----------
def clear_client_fields():
    dpg.set_value("name_input", "")
    dpg.set_value("cargo_weight_input", "")
    dpg.set_value("vip_checkbox", False)


def clear_transport_fields():
    dpg.set_value("transport_type", "")
    dpg.set_value("capacity_input", "")


# ---------- Функции для сохранения в файл ----------
def to_dict_client(client_ex):
    return {
        "Имя клиента": client_ex.name,
        "Вес груза": client_ex.cargo_weight,
        "VIP статус": client_ex.is_vip
    }


def to_dict_transport(transport_ex):
    if isinstance(transport_ex, Airplane):
        return {
            "Тип": "Самолет",
            "Грузоподъемность": transport_ex.capacity,
            "Текущая загрузка": transport_ex.current_load,
            "Максимальная высота полета": transport_ex.max_altitude
        }
    else:
        return {
            "Тип": "Грузовик",
            "Грузоподъемность": transport_ex.capacity,
            "Текущая загрузка": transport_ex.current_load,
            "Холодильник": transport_ex.is_refrigerated
        }


def save_data():
    data = {
        "Название компании": company.name,
        "Клиенты компании": [to_dict_client(client) for client in company.clients],
        "Транспорт компании": [to_dict_transport(vehicle) for vehicle in company.vehicles]
    }

    try:
        with open('company_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        dpg.set_value(
            "status_bar", "Данные успешно сохранены в файл: company_data.json")
    except Exception as e:
        dpg.set_value("status_bar", f"Ошибка при сохранении данных: {e}")


# ---------- Функция показа предупреждающего окна ----------
def show_warning_modal(message):
    """Отображает модальное окно с текстом предупреждения или ошибки."""
    time.sleep(0.1)  # Небольшая задержка перед показом окна
    if not dpg.does_item_exist("warning_modal"):
        with dpg.window(tag="warning_modal", label="Предупреждение", modal=True, width=popup_window_width, height=popup_window_height, show=False, no_resize=True):
            dpg.add_text(tag="warning_message")
            dpg.add_spacer(height=height_of_small_spacer)
            dpg.add_button(label="Закрыть", callback=lambda: dpg.configure_item(
                "warning_modal", show=True))

    dpg.set_value("warning_message", message)
    dpg.configure_item("warning_modal", show=False)


# ---------- Функции для таблиц ----------

def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    dpg.add_table_column(label="Выбор", parent="clients_table")
    dpg.add_table_column(label="Имя клиента", parent="clients_table")
    dpg.add_table_column(label="Вес груза (кг)", parent="clients_table")
    dpg.add_table_column(label="VIP статус", parent="clients_table")

    for idx, client in enumerate(company.clients):
        with dpg.table_row(parent="clients_table"):
            dpg.add_checkbox(tag=f"client_checkbox_{idx}")
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.is_vip else "Нет")


def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    dpg.add_table_column(label="Выбор", parent="vehicles_table")
    dpg.add_table_column(label="ID", parent="vehicles_table")
    dpg.add_table_column(label="Тип", parent="vehicles_table")
    dpg.add_table_column(label="Грузоподъемность (тонны)",
                         parent="vehicles_table")
    dpg.add_table_column(label="Текущая загрузка (тонны)",
                         parent="vehicles_table")

    for vehicle in company.vehicles:
        with dpg.table_row(parent="vehicles_table"):
            # Привязываем уникальный чекбокс для каждого транспортного средства по его ID
            checkbox_tag = f"vehicle_checkbox_{vehicle.vehicle_id}"
            # Чекбокс для каждого транспорта
            dpg.add_checkbox(tag=checkbox_tag)
            dpg.add_text(str(vehicle.vehicle_id))
            dpg.add_text("Самолет" if isinstance(
                vehicle, Airplane) else "Грузовик")
            dpg.add_text(str(vehicle.capacity))
            dpg.add_text(str(vehicle.current_load))


def update_distribution_table():
    existing_clients = set()  # Для отслеживания добавленных клиентов

    dpg.delete_item("distribution_table", children_only=True)

    dpg.add_table_column(label="Имя клиента", parent="distribution_table")
    dpg.add_table_column(label="Вес груза (кг)", parent="distribution_table")
    dpg.add_table_column(label="VIP статус", parent="distribution_table")
    dpg.add_table_column(label="Транспорт ID", parent="distribution_table")
    dpg.add_table_column(label="Тип транспорта", parent="distribution_table")

    for vehicle in company.vehicles:
        for client in vehicle.clients_list:
            # Создаем уникальный ключ клиента на основе имени и веса груза
            client_key = (client.name, client.cargo_weight)

            if client_key in existing_clients:
                continue

            existing_clients.add(client_key)

            with dpg.table_row(parent="distribution_table"):
                dpg.add_text(client.name)
                dpg.add_text(str(client.cargo_weight))
                dpg.add_text("Да" if client.is_vip else "Нет")
                dpg.add_text(vehicle.vehicle_id)
                dpg.add_text("Самолет" if isinstance(
                    vehicle, Airplane) else "Грузовик")

    update_vehicles_table()
    dpg.set_value("status_bar", "Таблица распределения успешно обновлена!")


def delete_selected_client_object(table_tag, data_list, checkbox_prefix):
    """Удаляет выбранные объекты на основе состояния чекбоксов."""
    items_to_delete = []

    for idx in range(len(data_list)):
        checkbox_tag = f"{checkbox_prefix}_{idx}"
        if dpg.does_item_exist(checkbox_tag) and dpg.get_value(checkbox_tag):
            items_to_delete.append(idx)

    if not items_to_delete:
        dpg.set_value("status_bar", "Выберите объект для удаления.")
        return

    for idx in sorted(items_to_delete, reverse=True):
        del data_list[idx]

    if table_tag == "clients_table":
        update_clients_table()

    dpg.set_value("status_bar", "Объект(ы) успешно удалены!")


def delete_selected_transport_object(table_tag, data_list, checkbox_prefix):
    """Удаляет выбранные объекты на основе состояния чекбоксов."""
    items_to_delete = []

    for idx in range(len(data_list)):
        checkbox_tag = f"{checkbox_prefix}_{data_list[idx].vehicle_id}"
        if dpg.does_item_exist(checkbox_tag) and dpg.get_value(checkbox_tag):
            items_to_delete.append(idx)

    if not items_to_delete:
        dpg.set_value("status_bar", "Выберите объект для удаления.")
        return

    for idx in sorted(items_to_delete, reverse=True):
        if table_tag == "vehicles_table":
            vehicle = data_list[idx]
            print(f"Удаление транспорта: {vehicle}")
            # Удаляем транспортное средство из списка компании
            del data_list[idx]
            update_vehicles_table()

    dpg.set_value("status_bar", "Объект(ы) успешно удалены!")


# ---------- Функции клиента----------

def create_new_client(sender, app_data):
    client_name = dpg.get_value("name_input")
    cargo_weight = dpg.get_value("cargo_weight_input")
    is_vip = dpg.get_value("vip_checkbox")

    if not client_name.strip() or not cargo_weight.strip():
        show_warning_modal("Ошибка: Все поля должны быть заполнены.")
        return False, "Ошибка добавления клиента: все поля должны быть заполнены."

    try:
        cargo_weight = float(cargo_weight)
    except ValueError:
        show_warning_modal("Ошибка: Вес груза должен быть числом.")
        dpg.set_value("cargo_weight_input", "")  # Очищаем поле ввода
        return False, "Ошибка добавления клиента: вес груза должен быть числом."

    if not (client_name.isalpha() and len(client_name) >= 2):
        show_warning_modal(
            "Ошибка: Имя клиента должно содержать только буквы и быть длиной от 2 символов.")
        dpg.set_value("name_input", "")  # Очищаем поле ввода
        return False, "Ошибка добавления клиента: Имя клиента должно содержать только буквы и быть длиной от 2 символов."

    if not (0 < cargo_weight <= 10000):
        show_warning_modal(
            "Ошибка: Вес груза должен быть положительным числом и не более 10000 кг.")
        dpg.set_value("cargo_weight_input", "")  # Очищаем поле ввода
        return False, "Ошибка добавления клиента: Вес груза должен быть положительным числом и не более 10000 кг."

    company.add_client(Client(client_name, cargo_weight, is_vip))
    update_clients_table()
    dpg.set_value("status_bar", "Клиент успешно добавлен!")
    dpg.configure_item("add_client_window", show=False)
    clear_client_fields()

# ---------- Функции транспорта ----------


def add_new_transport(sender, app_data):
    transport_mode = dpg.get_value("transport_type")
    capacity = dpg.get_value("capacity_input")

    if not transport_mode.strip() or not capacity.strip():
        show_warning_modal("Ошибка: Все поля должны быть заполнены.")
        return

    try:
        capacity = float(capacity)
    except ValueError:
        show_warning_modal("Ошибка: Грузоподъемность должна быть числом.")
        dpg.set_value("capacity_input", "")  # Очищаем поле ввода
        return

    if capacity <= 0:
        show_warning_modal(
            "Ошибка: Грузоподъемность должна быть положительным числом.")
        dpg.set_value("capacity_input", "")  # Очищаем поле ввода
        return

    if transport_mode == "Самолет":
        company.add_vehicle(Airplane(0))
    else:
        company.add_vehicle(Van(False))

    company.vehicles[-1].capacity = capacity
    update_vehicles_table()
    dpg.set_value("status_bar", "Транспортное средство успешно добавлено!")
    dpg.configure_item("add_transport_window", show=False)
    clear_transport_fields()

# ---------- Функция распределения веса ----------


def distribute_cargo():
    if not company.clients:
        dpg.set_value(
            "status_bar", "Ошибка: В компании отсутствуют клиенты. Распределение невозможно.")
        return

    if not company.vehicles:
        dpg.set_value(
            "status_bar", "Ошибка: В компании отсутствуют транспортные средства. Распределение невозможно.")
        return
    company.optimize_cargo_distribution()
    update_distribution_table()
    dpg.set_value("status_bar", "Распределение грузов завершено успешно!")


# ---------- Начало программы----------
dpg.create_context()

#  ---------- Подключение шрифта + киррилицы ----------

big_let_start = 0x00C0  # Capital "A" in cyrillic alphabet
big_let_end = 0x00DF  # Capital "Я" in cyrillic alphabet
small_let_end = 0x00FF  # small "я" in cyrillic alphabet
remap_big_let = 0x0410  # Starting number for remapped cyrillic alphabet
# adds the shift from big letters to small
alph_len = big_let_end - big_let_start + 1
# adds the shift from remapped to non-remapped
alph_shift = remap_big_let - big_let_start
with dpg.font_registry():
    with dpg.font("fonts/RobotoMono-VariableFont_wght.ttf", 20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        biglet = remap_big_let  # Starting number for remapped cyrillic alphabet
        # Cycle through big letters in cyrillic alphabet
        for i1 in range(big_let_start, big_let_end + 1):
            dpg.add_char_remap(i1, biglet)  # Remap the big cyrillic letter
            # Remap the small cyrillic letter
            dpg.add_char_remap(i1 + alph_len, biglet + alph_len)
            biglet += 1  # choose next letter
        dpg.bind_font(default_font)


# ---------- Создание главного окна программы ----------
with dpg.window(tag="Main Window", label="CTK Logistic Company",  width=window_width, height=window_height):

    # ---------- Меню бар ----------
    with dpg.menu_bar():
        with dpg.menu(label="Файл"):
            dpg.add_menu_item(label="Экспорт результата", callback=save_data)

        dpg.add_spacer(width=width_of_small_spacer)

        with dpg.menu(label="Помощь"):
            dpg.add_menu_item(label="О программе", callback=lambda: dpg.configure_item(
                "about_window", show=True))

    dpg.add_spacer(height=height_of_big_spacer)

    # ---------- Зона добавления обьекта ----------
    with dpg.group(horizontal=True):
        dpg.add_button(label="Добавить клиента", callback=lambda: dpg.configure_item(
            "add_client_window", show=True))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Добавить транспорт", callback=lambda: dpg.configure_item(
            "add_transport_window", show=True))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Распределить грузы", callback=distribute_cargo)

    dpg.add_spacer(height=height_of_big_spacer)

    # ---------- Зона создания таблиц ----------
    with dpg.table(header_row=True, tag="clients_table"):
        dpg.add_table_column(label="Имя клиента")
        dpg.add_table_column(label="Вес груза (кг)")
        dpg.add_table_column(label="VIP статус")

    dpg.add_spacer(height=height_of_medium_spacer)

    with dpg.table(header_row=True, tag="vehicles_table"):
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Тип")
        dpg.add_table_column(label="Грузоподъемность (тонны)")
        dpg.add_table_column(label="Текущая загрузка (тонны)")

    dpg.add_spacer(height=height_of_medium_spacer)

    # ---------- Таблица для распределенных грузов ----------
    with dpg.table(header_row=True, tag="distribution_table"):
        dpg.add_table_column(label="Имя клиента")
        dpg.add_table_column(label="Вес груза (кг)")
        dpg.add_table_column(label="VIP статус")
        dpg.add_table_column(label="Транспорт ID")
        dpg.add_table_column(label="Тип транспорта")

    dpg.add_spacer(height=height_of_medium_spacer)

    # ---------- Зона удаления обьекта ----------
    with dpg.group(horizontal=True):
        dpg.add_button(label="Удалить клиента", callback=lambda: delete_selected_client_object(
            "clients_table", company.clients, "client_checkbox"))
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Удалить транспорт", callback=lambda: delete_selected_transport_object(
            "vehicles_table", company.vehicles, "vehicle_checkbox"))

    # ---------- Статусная строка ----------
    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_text("Статусная строка:")
    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_text("", tag="status_bar")

# ----------Модальное окно "О программе" ----------
with dpg.window(tag="about_window", label="О программе", modal=True, show=False, no_resize=True, width=popup_window_width, height=popup_window_height):
    dpg.add_text("Номер ЛР: 12")
    dpg.add_text("Вариант: 4")
    dpg.add_text("ФИО: Кучерина Стефания Андреевна")
    dpg.add_spacer(height=height_of_medium_spacer)
    dpg.add_button(label="Закрыть", callback=lambda: dpg.configure_item(
        "about_window", show=False))

# ----------Модальное окно "Добавления клиента" ----------
with dpg.window(tag="add_client_window", label="Добавить клиента", modal=True, show=False, no_resize=True,  width=popup_window_width, height=popup_window_height):
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Имя клиента", tag="name_input")
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Вес груза", tag="cargo_weight_input")
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_checkbox(label="VIP статус", tag="vip_checkbox")
    dpg.add_spacer(height=height_of_medium_spacer)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=create_new_client)
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Отмена", callback=lambda: dpg.configure_item(
            "add_client_window", show=False))

# ----------Модальное окно "Добавления транспорта" ----------
with dpg.window(tag="add_transport_window", label="Добавить транспорт", modal=True, show=False, no_resize=True, width=popup_window_width, height=popup_window_height):
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_combo(label="Тип транспорта",
                  items=transport_list, tag="transport_type")
    dpg.add_spacer(height=height_of_small_spacer)
    dpg.add_input_text(label="Грузоподъемность (тонны)", tag="capacity_input")
    dpg.add_spacer(height=height_of_small_spacer)

    with dpg.group(horizontal=True):
        dpg.add_button(label="Сохранить", callback=add_new_transport)
        dpg.add_spacer(width=width_of_small_spacer)
        dpg.add_button(label="Отмена", callback=lambda: dpg.configure_item(
            "add_transport_window", show=False))

# ---------- Конец ----------
dpg.create_viewport(title="CTK Logistic Company",
                    width=window_width, height=window_height)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
