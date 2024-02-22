from collections import defaultdict
from enum import Enum

subscribers = defaultdict(list)


class Event(Enum):
    VILLAGE_DATA_UPDATE = 1


def subscribe_event(event: Event, callback):
    """Subscribe to an event."""
    subscribers[event].append(callback)


def publish_event(event: Event, data=None):
    """Publish an event."""
    for subscriber in subscribers[event]:
        subscriber(data)
