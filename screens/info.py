from screens.interface import AbstractScreen
import layout
import icons
import logging
from screen import get_display, set_current_page
from PIL import Image
import stats

log = logging.getLogger(__name__)


class InfoScreen(AbstractScreen):
    def __init__(self):
        super().__init__()

        self.register_touch_event((5, 0), self.load_main)
        self.register_touch_event((1, 13), self.decrement)
        self.register_touch_event((4, 13), self.increment)

        self.display_lines_start = 0
        self.display_lines = []

    def render(self, img_old, draw_old):
        # if switching_to: refresh screen before rendering
        log.debug("Rendering info screen")

        img, draw = layout.create_new_image()
        self.draw_header(img, draw)
        self.draw_footer(img, draw)
        self.draw_main_area(img, draw)
        self.draw_sidebar(img, draw)

        # Rotating must be the last thing that is done # TODO: Somehow do gridlines before, rotate after, automatically
        if layout.FLIPPED and not layout.IMAGE_WAS_FLIPPED:
            log.debug("Rotating image 180 degrees")
            img = img.transpose(Image.ROTATE_180)
            layout.IMAGE_WAS_FLIPPED = True

        display = get_display()
        display.display_Partial_Wait(display.getbuffer(img))

    def draw_header(self, img, draw):
        layout.fill_row(draw, 0, fill="black")
        layout.draw_text(draw, 0, 0, "Info", fill="white")

    def draw_footer(self, img, draw):
        layout.draw_icon(draw, 5, 0, icons.HOME)

    def draw_sidebar(self, img, draw):
        if len(self.display_lines) > 4:
            layout.draw_icon(draw, 1, 13, icons.UP)
            layout.draw_icon(draw, 4, 13, icons.DOWN)

    def draw_main_area(self, img, draw):
        self.display_lines = self.get_display_lines()
        for i in range(min(len(self.display_lines), 4)):
            log.debug(f"i: {i}, lines index: {(i + self.display_lines_start) % len(self.display_lines)}")
            layout.draw_text(draw, i+1, 0, self.display_lines[(i + self.display_lines_start) % len(self.display_lines)])

    def get_display_lines(self):
        return [
            f"IP: {stats.get_ip_address()}",
            f"Hostname: {stats.get_hostname()}",
            f"CPU Temp: {stats.get_cpu_temperature()}",
            f"CPU Load: {stats.get_cpu_load_average()}",
            f"Wifi: {stats.get_wifi_strength()} dBm",
        ]

    def decrement(self):
        log.debug("Decrementing display_lines_start")
        self.display_lines_start -= 1

    def increment(self):
        log.debug("Incrementing display_lines_start")
        self.display_lines_start += 1

    def load_main(self):
        log.debug("Load Main")
        set_current_page('MainScreen')

