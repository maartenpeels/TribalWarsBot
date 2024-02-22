import html
import json
import re

from src.models.village import VillageData


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
