from abc import ABC, abstractmethod


class AbstractScreen(ABC):
    switching_to = False
    last_event_time = None
    registered_events = {}

    def switch_to(self, img, draw):
        self.switching_to = True
        self.render(img, draw)

    @abstractmethod
    def render(self, img, draw):
        pass

    def handle_touch(self, row, column):
        action = self.registered_events.get((row, column), None)
        if action:
            action()

    def register_touch_event(self, coordinate_tuple, function_reference):
        previous_event = self.registered_events.get(coordinate_tuple, None)
        self.registered_events[coordinate_tuple] = function_reference
        return previous_event
