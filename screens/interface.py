from abc import ABC, abstractmethod
import layout
import logging

log = logging.getLogger(__name__)


class AbstractScreen(ABC):
    def __init__(self):
        self.switching_to = False
        self.last_event_time = None
        self.registered_events = {}

    def switch_to(self, img, draw):
        self.switching_to = True
        self.render(img, draw)

    # TODO: somehow make this not require arguments (render should be isolated)
    @abstractmethod
    def render(self, img, draw):
        if layout.SHOW_GRIDLINES:
            log.info("Drawing gridlines")
            layout.show_gridlines(draw)

    def handle_touch(self, row, column):
        action = self.registered_events.get((row, column), None)
        if action:
            action()

    def register_touch_event(self, coordinate_tuple, function_reference):
        previous_event = self.registered_events.get(coordinate_tuple, None)
        self.registered_events[coordinate_tuple] = function_reference
        return previous_event
