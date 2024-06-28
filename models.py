from abc import ABC
from dataclasses import dataclass
from functools import reduce

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
    races: list["Race"]

    def __init__(self) -> None:
        self.races = []

    def driver_classification(self, drivers: dict) -> dict:
        classification: list = []
        for driver in drivers.keys():
            driver_id: str = drivers[driver].code
            positions: list["RacePosition"] = self.driver_races(driver_id)
            classification.append(
                {
                    "driver": driver_id,
                    "points": reduce(
                        lambda points, position: points + position.points,
                        positions,
                        0
                    ),
                    "positions": self.grid_positions(driver_id),
                }
            )
        return sorted(classification, key=lambda driver: driver["points"], reverse=True)
    
    def constructor_classification(self, constructors: dict) -> dict:
        classification: list = []
        for constructor in constructors.keys():
            constructor: str = constructors[constructor].id
            positions: list["RacePosition"] = self.constructor_races(constructor)
            classification.append(
                {
                    "constructor": constructor,
                    "points": reduce(
                        lambda points, position: points + position.points,
                        positions,
                        0
                    ),
                }
            )
        return sorted(classification, key=lambda driver: driver["points"], reverse=True)

    def driver_races(self, driver_id: str) -> list["RacePosition"]:
        races_by_driver: list = []
        for race in self.races:
            races_by_driver.extend(
                race.driver_races(driver_id)
            )
        return races_by_driver
    
    def constructor_races(self, constructor_id: str) -> list["RacePosition"]:
        races_by_constructor: list = []
        for race in self.races:
            races_by_constructor.extend(
                race.constructor_races(constructor_id)
            )
        return races_by_constructor
    
    def grid_positions(self, driver_id: str) -> list[int]:
        positions: list[int] = []
        for race in self.driver_races(driver_id):
            positions.append(race.position)
        return positions


@dataclass
class Race:
    circuit: Circuit
    date: str
    round: str
    positions: list["RacePosition"]

    def __init__(self) -> None:
        self.positions = []

    def classification(self) -> list["RacePosition"]:
        table: list = []
        for race_position in self.positions:
            table.append(
                race_position
            )
        return sorted(table, key=lambda driver: driver.position)

    def driver_races(self, driver_id: str) -> list["RacePosition"]:
        return list(
            filter(
                lambda race_position: race_position.driver.code == driver_id,
                self.positions
            )
        )
    
    def constructor_races(self, constructor_id: str) -> list["RacePosition"]:
        return list(
            filter(
                lambda race_position: race_position.constructor.id == constructor_id,
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
    time_in_ms: float
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
        self.time_in_ms = self._time_in_ms(data)
        self.status = data.get("status", None)

    def _time(self, data: dict) -> None:
        try:
            return data["Time"]["time"]
        except Exception:
            return ""
        
    def _time_in_ms(self, data: dict) -> None:
        try:
            return float(data["Time"]["millis"])
        except Exception:
            return float("inf")
        
    def __str__(self) -> str:
        return f"{self.driver} - {self.position} - {self.time} ({self.status})"

    
