from screens.interface import AbstractScreen
import layout
import icons
import stats
from datetime import datetime
from PIL import Image
import logging

log = logging.getLogger(__name__)


class MainScreen(AbstractScreen):
    def __init__(self):
        # TODO: self.register_touch_event()
        self.register_touch_event((5, 0), self.load_info)
        self.register_touch_event((5, 13), self.load_settings)
        pass

    def render(self, img, draw):
        # if switching_to: refresh screen before rendering
        log.info("Rendering main screen")
        self.draw_header(img, draw)
        self.draw_footer(img, draw)
        if layout.FLIPPED:
            log.info("Rotating image 180 degrees")
            img = img.transpose(Image.ROTATE_180)
        return img

    # def handle_touch(self, row, column):
    #     action = self.registered_events.get((row, column), None)
    #     if action:
    #         action()

    def draw_header(self, img, draw):
        layout.fill_row(draw, 0, fill="black")
        layout.draw_text(draw, 0, 0, "Main", fill="white")
        layout.draw_text(draw, 0, 13, self.get_date_time_string(), fill="white", anchor="ra", additional_x_offset=layout.STEP-1)

    def draw_footer(self, img, draw):
        layout.draw_icon(draw, 5, 0, icons.INFO)
        layout.draw_icon(draw, 5, 11, stats.get_wifi_strength_icon(stats.get_wifi_strength()))
        layout.draw_icon(draw, 5, 13, icons.SETTINGS)

    def get_date_time_string(self):
        return datetime.now().strftime("%m/%d/%y %I:%M %p")

    def load_settings(self):
        log.info("Load Settings")

    def load_info(self):
        log.info("Load Info")
