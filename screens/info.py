from screens.interface import AbstractScreen
import layout
import icons
import logging
from screen import get_display, set_current_page
from PIL import Image

log = logging.getLogger(__name__)


class InfoScreen(AbstractScreen):
    def __init__(self):
        super().__init__()
        self.register_touch_event((5, 0), self.load_main)

    def render(self, img_old, draw_old):
        # if switching_to: refresh screen before rendering
        log.debug("Rendering info screen")

        img, draw = layout.create_new_image()
        self.draw_header(img, draw)
        self.draw_footer(img, draw)
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

    def load_main(self):
        log.info("Load Main")
        set_current_page('MainScreen')

