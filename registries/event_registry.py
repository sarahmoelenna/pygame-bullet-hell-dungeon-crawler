from enum import Enum
from typing import Dict

class EventTypeEnum(Enum):
    TILE_ANIMATION_UPDATE = "TILE_ANIMATION_UPDATE"

    def get_enum_for_value(value_in: str):
        for enum in EventTypeEnum:
            if enum.value == value_in:
                return enum
        raise ValueError("Unrecognised Event Type Enum Value: " + value_in)

class Event():
    def __init__(self, type: EventTypeEnum, data: Dict):
        self.type = type
        self.data = data

class EventSubscriber():

    def process_event(self, delta: float, event_type: EventTypeEnum, event: Event):
        raise NotImplementedError("process_event must be implemented")

class EventRegistry():

    previous_events = {}
    events = {}
    subscriptions = {}

    @staticmethod
    def process_subscriptions(delta: float):
        EventRegistry.previous_events = EventRegistry.events
        EventRegistry.events = {}

        for event_type, subscribers in EventRegistry.subscriptions.items():
            if event_type in EventRegistry.previous_events.keys():
                events = EventRegistry.previous_events[event_type]
                for subcriber in subscribers:
                    for event in events:
                        subcriber.process_event(delta, event.type, event)

    @staticmethod
    def post_event(event: Event):
        if event.type not in EventRegistry.events.keys():
            EventRegistry.events[event.type] = []
        EventRegistry.events[event.type].append(event)

    @staticmethod
    def subscribe_to_event_type(subscriber: EventSubscriber, event_type: EventTypeEnum):
        if not isinstance(subscriber, EventSubscriber):
            raise Exception("Must inherit EventSubscriber to subscribe to events")

        if event_type not in EventRegistry.subscriptions.keys():
            EventRegistry.subscriptions[event_type] = []
        EventRegistry.subscriptions[event_type].append(subscriber)

    @staticmethod
    def purge_events():
        EventRegistry.previous_events = {}