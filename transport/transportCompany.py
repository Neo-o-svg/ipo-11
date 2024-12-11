from .vehicle import Vehicle
from .client import Client
from .airplane import Airplane
from .van import Van
from typing import List


class TransportCompany():

    def __init__(self, name):
        self.name = name
        self.vehicles: List[Vehicle] = []
        self.clients: List[Client] = []

    def list_vehicles(self):
        return self.vehicles

    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("client должен быть экземляром класса Client")
        self.clients.append(client)

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, (Airplane, Van)):
            raise TypeError(f"""Неверное значение! {
                            vehicle} не является экземляром класса!""")
        self.vehicles.append(vehicle)

    def optimize_cargo_distribution(self):

        self.clients.sort(key=lambda client: client.is_vip, reverse=True)

        available_vehicles = sorted(
            self.vehicles, key=lambda vehicle: vehicle.capacity, reverse=True)
        # available_vehicles = self.vehicles.copy()  # Создаем копию, чтобы не изменять оригинал
        assigned_clients = []

        for client in self.clients:
            assigned = False
            for vehicle in available_vehicles:
                if vehicle.current_load + (client.cargo_weight / 1000) <= vehicle.capacity:
                    vehicle.load_cargo(client)
                    assigned_clients.append(client)
                    assigned = True
                    break  # Переходим к следующему клиенту, если нашли транспорт
            if not assigned:
                print(f"Груз клиента {client.name} не удалось разместить.")

        return assigned_clients
