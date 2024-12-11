from transport import *


def createCompany(name):
    company = TransportCompany(name)
    return company


def showMenu():
    print("\nМеню:")
    print("1. Добавить клиента")
    print("2. Добавить транспортное средство")
    print("3. Вывести список клиентов")
    print("4. Вывести список транспортных средств")
    print("5. Оптимизировать распределение грузов")
    print("6. Выход\n")


def showAndChoose_accessible_transport():
    print("\nДоступный транспорт: самолет, грузовик")
    mode_of_transport = input("\nВыберите вид транспорта: ").strip()

    if not mode_of_transport.isalpha():
        print("\n_______________________Ошибка_______________________")
        print(f"\n{mode_of_transport} --- некорректное значение, повторите ввод.")
        return showAndChoose_accessible_transport()

    mode_of_transport = mode_of_transport.lower()

    if mode_of_transport not in ["самолет", "грузовик"]:
        print("\n_______________________Ошибка_______________________")
        print(f"{mode_of_transport} транспорт не найден, повторите ввод.")
        return showAndChoose_accessible_transport()

    return mode_of_transport


def print_client_info(client):
    if client.is_vip:
        print("\n_______VIP_______Client________")
        print(f"""\nИмя клиента: {client.name}
              \nВес груза: {client.cargo_weight}""")
        print("________________________________")

    else:
        print(f"""\nИмя клиента: {client.name}
              \nВес груза: {client.cargo_weight}""")


def print_vehicle_info(vehicle):
    if isinstance(vehicle, Airplane):
        print("\n_____________Самолет_____________")
    else:
        print("\n_____________Грузовик_____________")

    print(vehicle.__str__())
    print(f"\nСписок клиентов чьи грузы загружены:")
    if vehicle.current_load == 0:
        print("""_____________________________
              \nНа транспорт не загружен груз
              \nВыполните 5 пункт меню для загрузки
              \n_____________________________""")
    else:
        print("_____________________________")
        for client in vehicle.clients_list:
            print_client_info(client)
            print("\n_____________________________")


def output(count, actions_list, actions_count):
    # Вывод информации о завершении программы и количестве выполненных операций.
    print(f"""
        Программа завершена.
       """)

    # Вывод статистики по каждой операции
    count = 1
    print("\nКоличество выполненных операций: ")
    for act in actions_list:
        print(f"""
            {act} : {actions_count[count]}
           """)
        count += 1
    # Возвращает None, чтобы не выводить лишний None в консоль
    return None


def check_client_name(name):
    while not name:
        print("___________________________________________")
        print("Ошибка введения имени клиента.")
        print("\nИмя не должно быть пустой строкой")
        print("___________________________________________")
        name = input("\nВведите имя клиента: ").strip()
    return name


def check_cargo_weight(cargo_weight):
    while True:
        try:
            cargo_weight = float(cargo_weight)
            if cargo_weight <= 0:
                print("___________________________________________")
                print("Ошибка введения веса груза клиента.")
                print(
                    "\nВес груза должен быть положительным числом.\nВведите вес груза корректно.")
                print("___________________________________________")
                cargo_weight = input("\nВведите вес груза: ").strip()

            else:
                break

        except ValueError:
            print("___________________________________________")
            print("Ошибка введения веса груза клиента.")
            print("\nНекорректный формат веса груза. Введите число.")
            print("___________________________________________")
            cargo_weight = input("\nВведите вес груза: ").strip()
    return cargo_weight


def check_vip_status(is_vip):
    while True:
        try:
            is_vip = is_vip.lower()

            if is_vip == "да":
                is_vip = True
                break
            elif is_vip == "нет":
                is_vip = False
                break
            else:
                print("______________________________________")
                print("Ошибка введения вип-статуса клиента.")
                print(f"Некорректное значение {is_vip}!")
                print(
                    "\n Решения: \n 1. Введите 'да' если клиент имеет статус VIP\n 2. Введите нет или пропустите пункт в ином случае")
                print("______________________________________")
                is_vip = input(
                    "\nЯвляется  vip-клиентом? (да / нет): ").strip()

        except:
            print("______________________________________")
            print("Ошибка введения вип-статуса клиента.")
            print(f"Некорректное значение {is_vip}!")
            print(
                "\n Решения: \n 1. Введите 'да' если клиент имеет статус VIP\n 2. Введите нет или пропустите пункт в ином случае")
            print("______________________________________")
            is_vip = input(
                "\nЯвляется  vip-клиентом? (да / нет): ").strip()
    return is_vip


def check_capacity(capacity):
    while True:
        if not capacity:
            print("""\n__________________Ошибка__________________
                  \nЗначение грузоподъемности не должно быть пустым.
                  \nЗначение должно быть числом.
                  \nПовторите ввод корректно.\n""")
            capacity = input(
                "Введите грузоподъемность(в тоннах): ").strip()
        try:
            capacity = float(capacity)
            if capacity > 0:
                break
            else:
                print("\n__________________________________________________")
                print(
                    "Грузоподъемность должна быть положительным числом.\nПовторите ввод корректно.")
                capacity = input(
                    "\nВведите грузоподъемность(в тоннах): ").strip()
        except:
            print("______________________________________")
            print("\nПроизошла ошибка типа данных.\nПовторите ввод корректно.")
            capacity = input(
                "\nВведите грузоподъемность(в тоннах): ").strip()
    return capacity


def check_max_altitude(max_altitude):
    while True:
        try:
            max_altitude = float(max_altitude)
            if (max_altitude) <= 0:
                print("""Максимальная высота полета должен быть положительным числом.\n
                Повторите ввод корректно.""")
                max_altitude = input(
                    "Максимальная высота полета(в метрах): ").strip()
            else:
                break
        except:
            print(
                "\n__________________ Ошибка введения данных высоты __________________ ")
            print("""Максимальная высота полета должен быть положительным числом.\n
                Повторите ввод корректно.""")
            print(
                "____________________________________________________________________")
            max_altitude = input(
                "\nМаксимальная высота полета(в метрах): ").strip()
    return max_altitude


def check_is_refrigerated(is_refrigerated):
    while True:
        try:
            is_refrigerated = is_refrigerated.lower()
            if is_refrigerated == "да":
                is_refrigerated = True
                break
            elif is_refrigerated == "нет":
                is_refrigerated = False
                break
            else:
                print("\n_________________Ошибка__________________")
                print(
                    """Ответ должен быть 'да' либо 'нет'.\nПовторите ввод корректно.\n""")
                is_refrigerated = input(
                    "Есть ли в наличии холодильник (да / нет): ").strip()
        except:
            print("_________________Ошибка__________________")
            print(
                """Ответ должен быть 'да' либо 'нет'.\nПовторите ввод корректно.\n""")
            is_refrigerated = input(
                "Есть ли в наличии холодильник (да / нет): ").strip()
    return is_refrigerated


count = 0
# Список доступных действий.
actions_list = [
    "Добавить клиента",
    "Добавить транспортное средство",
    "Вывести список клиентов",
    "Вывести список транспортных средств",
    "Оптимизировать распределение грузов",
    "Выход"
]

# Словарь для подсчета количества каждой операции.
actions_count = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0
}

name_of_company = input("Введите название компании: ").strip()
company = createCompany(name_of_company)
print("Компания успешно добавлена")

while True:
    showMenu()
    # Получение номера действия от пользователя.
    num = input("\nВведите номер пункта: ")
    try:
        num = int(num)
    except:
        print("""\n_______________Ошибка________________
              \nПровторите ввод корректно (введите число)\n""")
        num = input("\nВведите номер пункта: ")

    if num == 1:
        count += 1
        actions_count[1] += 1

        name_of_client = check_client_name(
            input("\nВведите имя клиента: ").strip())
        client_cargo_weight = check_cargo_weight(
            input("Введите вес груза: ").strip())
        client_vip_status = input(
            "Является  vip-клиентом? (да / нет): ").strip()

        if not client_vip_status:
            company.add_client(
                Client(name_of_client, client_cargo_weight))
        else:
            client_vip_status = check_vip_status(client_vip_status)
            company.add_client(
                Client(name_of_client, client_cargo_weight, client_vip_status))

        print("Запись клиента успешно добавлена!")

    elif num == 2:
        count += 1
        actions_count[2] += 1
        mode_of_transport = showAndChoose_accessible_transport()

        if mode_of_transport == "самолет":
            max_altitude = check_max_altitude(input(
                "Максимальная высота полета(в метрах): ").strip())
            company.add_vehicle(Airplane(max_altitude))

        else:
            is_refrigerated = check_is_refrigerated(input(
                "Есть ли в наличии холодильник (да / нет): ").strip())
            company.add_vehicle(Van(is_refrigerated))

        vehicle_capacity = check_capacity(input(
            "Введите грузоподъемность(в тоннах): ").strip())

        company.vehicles[-1].capacity = vehicle_capacity
        print("Транспорт успешно добавлен.")

    elif num == 3:
        count += 1
        actions_count[3] += 1
        if len(company.clients) == 0:
            print(f"""У компании {
                  name_of_company} пока что нет клиентов :( Станьте первым!""")
        else:
            count_client = 1
            print(f"\nКлиенты компании {name_of_company}: ")

            for client in company.clients:
                print(
                    f"\n------------------{count_client} клиент------------------")
                print_client_info(client)
                count_client += 1
            print("\n--------------------------------------------")

    elif num == 4:
        count += 1
        actions_count[4] += 1
        if len(company.vehicles) == 0:
            print(
                f"\nКомпания {name_of_company} не имеет траспорта :(\nДобавьте транспорт.")
        else:
            for vehicle in company.vehicles:
                print_vehicle_info(vehicle)

    elif num == 5:
        count += 1
        actions_count[5] += 1
        if len(company.vehicles) == 0:
            print("\nПожалуйста добавьте транспорт.\nСписок транспорта пуст")
        elif len(company.clients) == 0:
            print("\nПожалуйста, добавьте клиентов.\nСписок клиентов пуст")
        else:
            company.optimize_cargo_distribution()
            print("Оптимизация прошла успешно.")

    elif num == 6:
        # Увеличение счетчика.
        actions_count[6] += 1
        # Вывод статистики и завершение программы.
        output(count, actions_list, actions_count)
        break

    else:
        print("Неизвестное значение пункта, повторите ввод.")
