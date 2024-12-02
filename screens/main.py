from screens.interface import AbstractScreen
import layout
import icons
import stats
from datetime import datetime
import logging
from PIL import Image
from screen import get_display, set_current_page

log = logging.getLogger(__name__)


class MainScreen(AbstractScreen):
    def __init__(self):
        super().__init__()
        self.register_touch_event((5, 0), self.load_info)
        self.register_touch_event((5, 13), self.load_settings)

    def render(self, img_old, draw_old):
        # if switching_to: refresh screen before rendering
        log.debug("Rendering main screen")
        img = self.render_img()
        display = get_display()
        display.display_Partial_Wait(display.getbuffer(img))

    def render_img(self):
        img, draw = layout.create_new_image()
        super().render(img, draw)
        self.draw_header(img, draw)
        self.draw_footer(img, draw)

        # Rotating must be the last thing that is done # TODO: Somehow do gridlines before, rotate after, automatically
        if layout.FLIPPED and not layout.IMAGE_WAS_FLIPPED:
            log.debug("Rotating image 180 degrees")
            img = img.transpose(Image.ROTATE_180)
            layout.IMAGE_WAS_FLIPPED = True

        return img

    def draw_header(self, img, draw):
        layout.fill_row(draw, 0, fill="black")
        layout.draw_text(draw, 0, 0, "Main", fill="white")
        date_time_string = self.get_date_time_string()
        log.debug(f"Updating time to: {date_time_string}")
        layout.draw_text(draw, 0, 13, date_time_string, fill="white", anchor="ra", additional_x_offset=layout.STEP-1)

    def draw_footer(self, img, draw):
        layout.draw_icon(draw, 5, 0, icons.INFO)
        layout.draw_icon(draw, 5, 11, stats.get_wifi_strength_icon(stats.get_wifi_strength()))
        layout.draw_icon(draw, 5, 13, icons.SETTINGS)

    def get_date_time_string(self):
        return datetime.now().strftime("%m/%d/%y %-I:%M %p")

    def load_settings(self):
        log.info("Load Settings")

    def load_info(self):
        log.info("Load Info")
        set_current_page('InfoScreen')
