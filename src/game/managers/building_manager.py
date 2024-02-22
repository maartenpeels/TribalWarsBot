import logging
import time

from src.core.config import Config
from src.core.events import subscribe_event, Event
from src.core.file_manager import FileManager
from src.core.page_parser import PageParser
from src.core.web_wrapper import WebWrapper
from src.model.village import VillageData

logger = logging.getLogger("BuildingManager")


class BuildingManager:
    village_data: VillageData = None

    def __init__(self, village_id: int, village_name: str, config: Config, web: WebWrapper):
        self.village_id = village_id
        self.village_name = village_name
        self.config = config
        self.web = web

        global logger
        logger = logging.getLogger(f"BuildingManager \"{self.village_name}\"")

        subscribe_event(Event.VILLAGE_DATA_UPDATE, self._on_village_data_update)

    def _on_village_data_update(self, village_data: VillageData):
        if village_data.id != self.village_id:
            return

        logger.debug(f"Village data updated")
        self.village_data = village_data

    def run(self):
        if self.village_data is None:
            logger.warning("Village data is not available")
            return

        # Get data needed
        response = self.web.get_screen("main", params={"village": self.village_id})
        max_queue_size = self.config.get("building_manager.queue_size", 2)
        building_queue = PageParser.get_building_queue(response)
        building_data = PageParser.get_building_data(response)

        # Check if we can finish any building early to make space for new ones
        finish_enabled = self.config.get("building_manager.finish_enabled", True)
        finish_early = PageParser.get_finish_early_id(response)  # (id, finish_time)
        current_time = time.time()
        if finish_enabled and finish_early is not None and current_time > finish_early[1]:
            self.finish_early(finish_early[0])
            self.run()

        upgrade_enabled = self.config.get("building_manager.upgrade_enabled", True)
        if not upgrade_enabled:
            return

        # Check if we can start any new buildings
        if len(building_queue) >= max_queue_size:
            logger.info(f"Building queue is full, max size: {max_queue_size}")
            return

        # Find next task
        task = self.find_next_task(building_queue, building_data)
        if task is None:
            logger.info("No upgrades to do at the moment")
            return

        self.queue_upgrade(task)

    def queue_upgrade(self, task):
        data = {
            'id': task[0],
            'force': 1,
            'destroy': 0,
            'source': self.village_id,
            'h': self.web.last_h
        }

        response = self.web.ajax_post_action(self.village_id, "upgrade_building", data)
        if response.status_code != 200:
            logger.error(f"Failed to queue upgrade for building {task[0]}")
            return

        logger.info(f"Queued upgrade for building {task[0]} to level {task[1]}")

    def finish_early(self, finish_early_id):
        params = {
            'id': finish_early_id,
            'destroy': 0,
            'h': self.web.last_h
        }

        response = self.web.ajax_get_action(self.village_id, "build_order_reduce", params)
        if response.status_code != 200:
            logger.error(f"Failed to finish upgrade early")
            return False

        logger.info(f"Finished upgrade early")
        return True

    def find_next_task(self, building_queue, building_data):
        strategy = self.config.get_village(self.village_id, "strategy.building", "purple_predator")
        lines = FileManager.read_lines(f"strategy/building/{strategy}.txt")

        # Parse strategy file
        tries = 0
        for building, target_level in [line.split(":") for line in lines]:
            current_level = self.village_data.buildings.get_level(building)
            target_level = int(target_level)

            if target_level <= current_level:
                continue

            should_skip = False

            # Check if building is already in queue
            for queued_building, queued_level, _ in building_queue:
                if queued_building == building:
                    if target_level < queued_level:
                        should_skip = True
                    else:
                        current_level = queued_level

            if should_skip:
                logger.debug(f"Skipping {building} because it's already in queue")
                continue

            # Check if building is already at target level
            if current_level < target_level:
                # Calculate how many levels we need to build
                diff = target_level - current_level

                # Add tasks
                for i in range(diff):
                    logger.debug(
                        f"Building {building} level {current_level + i} -> {current_level + i + 1}")

                    if self.can_afford(building, building_data):
                        return building, current_level + i + 1
                    else:
                        logger.debug(
                            f"Can't afford building {building} level {current_level + i + 1} or it's not available")
                        tries += 1
                        should_skip = True

            if should_skip and tries < self.config.get("building_manager.lookahead", 2):
                continue
            return None
        return None

    def can_afford(self, building, building_data):
        data = building_data.get(building)
        if data is None:
            # Building is not available
            return False

        return data.get("pop") <= self.village_data.pop \
            and data.get("wood") <= self.village_data.wood \
            and data.get("stone") <= self.village_data.stone \
            and data.get("iron") <= self.village_data.iron
