import json
import os
from models import (
    Circuit,
    Constructor,
    Driver,
    Race,
    RacePosition,
    Season,
)

DATA_PATH: str = "data"

CIRCUITS: dict[str, Driver] = {}
CONSTRUCTORS: dict[str, Driver] = {}
DRIVERS: dict[str, Driver] = {}

def import_season(year: int) -> Season:
    try:
        file_path: str = f"{DATA_PATH}/{year}/{year}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())

        response_data: dict = response["MRData"]
        season: Season = Season()
        season.year = year
        season.rounds = int(response_data["total"])
        season.races = []
        for round in range(1, season.rounds + 1):
            season.races.append(
                import_race(year, round)
            )

        return season
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return None
    

def import_race(year: int, round: int) -> Race:
    try:
        race: Race = Race()
        file_path: str = f"{DATA_PATH}/{year}/{year}_{round}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())
        
        response_data: dict = response["MRData"]
        data: dict = response_data["RaceTable"]["Races"][0]
        race.circuit = CIRCUITS[data["Circuit"]["circuitId"]]
        race.date = data.get("date", "")
        race.round = data.get("round", "")
        results = []
        for lap_data in data["Results"]:
            results.append(
                RacePosition(
                    DRIVERS[lap_data["Driver"]["driverId"]],
                    CONSTRUCTORS[lap_data["Constructor"]["constructorId"]],
                    lap_data,
                )
            )
            race.positions = results

        return race
    except Exception:
        return race

def import_constructors(year: int) -> dict:
    try:
        constructors: dict[str, dict] = {}
        response: dict = {}
        file_path: str = f"{DATA_PATH}/{year}/constructors_{year}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())
        response_data: dict = response["MRData"]
        for data in response_data["ConstructorTable"]["Constructors"]:
            constructor: Constructor = Constructor.from_dict(data)
            constructors[constructor.id] = constructor
        return constructors
    except Exception:
        return {}

def import_circuits(year: int) -> dict:
    try:
        circuits: dict[str, dict] = {}
        response: dict = {}
        file_path: str = f"{DATA_PATH}/{year}/circuits_{year}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response = json.loads(file.read())
        response_data: dict = response["MRData"]
        
        for data in response_data["CircuitTable"]["Circuits"]:
            circuit: Circuit = Circuit.from_dict(data)
            circuits[circuit.id] = circuit
        return circuits
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return {}

def import_drivers(year: int) -> dict:
    try:
        drivers: dict[str, dict] = {}
        response: dict = {}
        file_path: str = f"{DATA_PATH}/{year}/drivers_{year}.json"
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                response: dict = json.loads(file.read())
        driver_data: dict = response["MRData"]
        for data in driver_data["DriverTable"]["Drivers"]:
            driver: Driver = Driver.from_dict(data)
            drivers[driver.id] = driver
        return drivers
    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return {}
    

years: list[int] = [2016] #, 2022, 2023]
for year in years:
    DRIVERS = import_drivers(year)
    CONSTRUCTORS = import_constructors(year)
    CIRCUITS = import_circuits(year)

    # a = import_race(year, 3)
    # race: Race = a[0]
    # print(race.positions)
    # print(
    #     race.races("HAM")
    # )
    # # print(race.positions)
    print(DRIVERS)

    season = import_season(year)
    

    # print("")

    # print(season)
    # print(season.races)
    # for race in season.races:
    #     print("")
    #     print("Race: " + race.circuit.name)
    #     for data in race.classification():
    #         print(data)

    print("0" * 50)
    print(CONSTRUCTORS)
    print("-" * 50)
    print(CIRCUITS)
    print("0" * 50)

    print("=" * 50)
    print("Classification " + str(year))
    print("=" * 50)
    # classification = season.driver_classification(DRIVERS)
    for data in season.constructor_classification(CONSTRUCTORS):
        print(data["constructor"] + " - " + str(data["points"]))

    

    # print(season.get_races("HAM"))
# print(season.total_points("HAM"))
# print(season.classification(DRIVERS))
