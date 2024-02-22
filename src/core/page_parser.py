import html
import json
import re

from src.models.village_model import VillageData


class PageParser:
    @staticmethod
    def get_villages_from_overview(response):
        results = re.findall(
            r'php\?village=(\d+)&amp;screen=overview"><span class="icon header village"></span>([^<]*)</a>',
            response.text)

        return list(set([(int(village_id), html.unescape(village_name)) for village_id, village_name in results]))

    @staticmethod
    def get_village_data(response):
        result = re.search(r'TribalWars\.updateGameData\((.+?)\);', response.text)
        if result:
            json_data = json.loads(result.group(1), strict=False)
            return VillageData.from_json(json_data['village'])
