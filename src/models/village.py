from dataclasses import dataclass


@dataclass
class BuildingData:
    main: int
    barracks: int
    stable: int
    garage: int
    watchtower: int
    snob: int
    smith: int
    place: int
    statue: int
    market: int
    wood: int
    stone: int
    iron: int
    farm: int
    storage: int
    wall: int


@dataclass
class VillageData:
    id: int
    name: str
    display_name: str
    wood: int
    wood_prod: float
    wood_float: int
    stone: int
    stone_prod: float
    stone_float: float
    iron: int
    iron_prod: float
    iron_float: int
    pop: int
    pop_max: int
    x: int
    y: int
    trader_away: int
    storage_max: int
    bonus_id: object
    bonus: object
    buildings: BuildingData
    player_id: int
    modifications: int
    points: int
    last_res_tick: int
    coord: str
    is_farm_upgradable: bool

    @staticmethod
    def from_json(data):
        json_data = data.copy()

        # Convert strings to ints for building values
        json_data['buildings'] = {key: int(value) for key, value in json_data['buildings'].items()}

        return VillageData(**json_data)
