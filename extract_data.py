import json
import os
import requests

from tkinter import *


from models import (
    Circuit,
    Driver,
)

URL_BASE: str = "http://ergast.com/api/f1"
DATA_PATH: str = "data"

def import_season(year: int) -> None:
    print("Teste")
    check, drivers = import_drivers(year)
    
    print(drivers)
    


def import_circuits(year: int) -> tuple[bool, dict]:
    try:
        circuits: dict[str, dict] = {}
        response: dict = {}
        file_path: str = DATA_PATH + "circuits/circuits_" + str(year) + ".json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())
        response_data: dict = response["MRData"]
        
        for circuit_data in response_data["CircuitTable"]["Circuits"]:
            circuit: Circuit = Circuit.from_dict(circuit_data)
            circuits[circuit.id] = circuit
        return True, circuits
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return False, {}

def import_drivers(year: int) -> tuple[bool, dict]:
    try:
        drivers: dict[str, dict] = {}
        response: dict = {}
        file_path: str = DATA_PATH + "drivers/drivers_" + str(year) + ".json"
        print(file_path)
        print(os.path.isfile(file_path))
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())
        response_data: dict = response["MRData"]
        
        for driver_data in response_data["DriverTable"]["Drivers"]:
            driver: Driver = Driver.from_dict(driver_data)
            drivers[driver.id] = driver
        return True, drivers
    except Exception:
        return False, {}
    

def _create_file(year: int, entity: str) -> bool:
    try:
        url: str = f"{URL_BASE}/{year}/{entity}s.json"
        path: str = f"{DATA_PATH}/{year}/{entity}s_" + str(year) + ".json"
        response: requests.Response = requests.get(url)
        data: str = json.dumps(response.json())
        if not os.path.isfile(path):
            with open(path, "w") as file:
                file.write(data)
        return True
    except Exception:
        return False


def create_races_files(year: int, rounds: int) -> bool:
    print("0" * 50)
    print(year)
    print(rounds)
    print("0" * 50)
    for round in range(1, rounds + 1):
        create_race_file(year, round)

def create_season_file(year: int) -> bool:
    try:
        folder_path: str = f"data/{year}"
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

            url: str = f"{URL_BASE}/{year}.json"
            path: str = f"{DATA_PATH}/{year}/{year}.json"
            response: requests.Response = requests.get(url)
            data: str = response.json()
            total: int = int(data["MRData"]["total"])
            if not os.path.isfile(path):
               with open(path, "w") as file:
                    file.write(json.dumps(data))

            create_races_files(year, total)
            create_circuit_file(year)
            create_driver_file(year)
            create_constructor_file(year)
            
        return True
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return False
    

def create_race_file(year: int, round: int) -> bool:
    try:
        url: str = f"{URL_BASE}/{year}/{round}/results.json"
        print(url)
        path: str = f"{DATA_PATH}/{year}/{year}_{round}.json"
        response: requests.Response = requests.get(url)
        data: str = json.dumps(response.json())
        if not os.path.isfile(path):
            with open(path, "w") as file:
                file.write(data)
        return True
    except Exception:
        return False

def create_circuit_file(year: int) -> bool:
    _create_file(year, "circuit")

def create_driver_file(year: int) -> bool:
    _create_file(year, "driver")

def create_constructor_file(year: int) -> bool:
    _create_file(year, "constructor")
    

years: list[int] = [2016]
for year in years:
    print(create_season_file(year))
    # os.makedirs("formula_1/data/2009")
    # create_season_file(year)
    # create_races_files(2008, 18)
    # create_driver_file(year)
    # create_circuit_file(year)
    # create_constructor_file(year)
    # print(import_drivers(year))
    # print(import_circuits(year))