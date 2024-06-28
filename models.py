from abc import ABC
from dataclasses import dataclass

@dataclass
class Constructor:
    id: str
    name: str
    country: str
    url: str

    @staticmethod
    def from_dict(adict: dict) -> "Constructor":
        return Constructor(
            adict.get("constructorId", None),
            adict.get("name", None),
            adict.get("nationality", None),
            adict.get("url", None)
        )
    
    def __repr__(self) -> str:
        return self.id


@dataclass
class Circuit:
    id: str
    name: str
    city: str
    country: str
    url: str

    @staticmethod
    def from_dict(adict: dict) -> "Circuit":
        return Circuit(
            adict.get("circuitId", None),
            adict.get("circuitName", None),
            adict["Location"].get("locality", None),
            adict["Location"].get("country", None),
            adict.get("url", None)
        )
    
    def __repr__(self) -> str:
        return self.id

@dataclass
class Driver:
    id: str
    code: str
    first_name: str
    last_name: str
    birth_data: str
    nationality: str
    url_page: str
    
    @staticmethod
    def from_dict(adict: dict) -> "Driver":
        return Driver(
            adict.get("driverId", None),
            adict.get("code", None),
            adict.get("givenName", None),
            adict.get("familyName", None),
            adict.get("dateOfBirth", None),
            adict.get("nationality", None),
            adict.get("url", None)
        ) 
        
    def __repr__(self) -> str:
        return self.code

@dataclass
class Season:
    year: str
    rounds: int
    races: list

    def __init__(self) -> None:
        self.races = []

    def classification(self, drivers: dict) -> dict:
        table: list = []
        for driver in drivers.keys():
            driver_id: str = drivers[driver].code
            table.append(
                {
                    "driver": driver_id,
                    "points": self.total_points(driver_id),
                }
            )

        return sorted(table, key=lambda driver: driver["points"], reverse=True)

    def get_races(self, driver_id: str) -> list:
        races_by_driver: list = []
        for race in self.races:
            races_by_driver.extend(
                race.races(driver_id)
            )
        return races_by_driver
    

    def total_points(self, driver_id: str) -> int:
        total: int = 0
        for race in self.get_races(driver_id):
            total += race.points
        return total


@dataclass
class Race:
    circuit: Circuit
    date: str
    round: str
    positions: list

    def __init__(self) -> None:
        self.positions = []

    def classification(self) -> dict:
        table: list = []
        for race_position in self.positions:
            table.append(
                {
                    "driver": race_position.driver.code,
                    "position": race_position.position,
                    "time": race_position.time,
                }
            )
        return sorted(table, key=lambda driver: driver["position"])

    def races(self, driver_id: str) -> list:
        return list(
            filter(
                lambda race_position: race_position.driver.code == driver_id,
                self.positions
            )
        )
    
    def __repr__(self) -> str:
        return self.circuit.name + " - " + self.date

@dataclass
class RacePosition:
    driver: Driver
    constructor: Constructor
    position: int
    grid: int
    points: float
    time: str
    status: str

    def __init__(
            self, 
            driver: Driver,
            constructor: Constructor,
            data: dict,
        ) -> None:
        self.driver = driver
        self.constructor = constructor
        self.position = int(data.get("position", 0))
        self.grid = int(data.get("grid", 0))
        self.points = float(data.get("points", 0))
        self.time = self._time(data)
        self.status = data.get("status", None)
        print()

    def _time(self, data: dict) -> None:
        try:
            return data["Time"]["time"]
        except Exception:
            return ""

    
