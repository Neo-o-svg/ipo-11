from .client import Client
import uuid


class Vehicle:
    unique_id = uuid.uuid4()

    def __init__(self):

        self.vehicle_id = Vehicle.unique_id
        self.capacity = 0
        self.current_load = 0
        self.clients_list = []

    def load_cargo(self, client):
        if (self.current_load + client.cargo_weight) > self.capacity:
            print("Превышение грузоподъемности транспорта.")
        else:
            self.current_load += client.cargo_weight
            self.clients_list.append(client)

    def __str__(self):
        return (
            f"""\nID транспорта: {self.vehicle_id},
            \nГрузоподъемность (в тоннах): {self.capacity},
            \nТекущая загрузка: {self.current_load}"""
        )
