import html
import json
import math
import re
import time

from src.model.village import VillageData


class PageParser:
    """Class for parsing the response from the server."""

    @staticmethod
    def get_villages_from_overview(response):
        """Get the villages from the overview page."""
        results = re.findall(
            r'php\?village=(\d+)&amp;screen=overview"><span class="icon header village"></span>([^<]*)</a>',
            response.text)

        return list(set([(int(village_id), html.unescape(village_name)) for village_id, village_name in results]))

    @staticmethod
    def get_village_data_from_village_overview(response):
        """Get the village data from the overview_village response."""
        result = re.search(r'TribalWars\.updateGameData\((.+?)\);', response.text)
        if result:
            json_data = json.loads(result.group(1), strict=False)
            return VillageData.from_json(json_data['village'])

        return None

    @staticmethod
    def get_game_state(response):
        """Get the main page."""
        result = re.search(r'TribalWars\.updateGameData\((.+?)\);', response.text)
        if result:
            return json.loads(result.group(1), strict=False)

        return None

    @staticmethod
    def get_building_queue(response):
        """Get the building queue from the building page."""
        result = re.search(r'(?s)<table id="build_queue"(.+?)</table>', response.text)
        if not result:
            return []

        tasks = re.findall(r'class="lit-item">\s*<img src=".*/(\w+).png[^>]+>\s*\w+<br />\s+Level (\d+)([^=]+=[^=]+=['
                           r'^=]+="(\d+))*', result.group(1))
        if not tasks:
            return []

        queue = []
        for task in tasks:
            building = ''.join([i for i in task[0] if not i.isdigit()])
            level = int(task[1])
            unix = math.floor(time.time() + 3600)  # 1 hour
            # Check if the task has a finish time
            if len(task) == 4 and task[3] != '':
                unix = int(task[3])

            queue.append((building, level, unix))

        return queue

    @staticmethod
    def get_building_data(response):
        result = re.search(r'(?s)BuildingMain.buildings = (\{.+?});', response.text)
        if result:
            return json.loads(result.group(1), strict=False)

        return None

    @staticmethod
    def get_finish_early_id(response):
        result = re.search(r'(?s)(\d+),\s*\'BuildInstantFree.+?data-available-from="(\d+)"', response.text)
        if result:
            return result.group(1), int(result.group(2))

        return None
