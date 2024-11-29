from stats import get_wifi_strength_icon, get_wifi_strength
import layout
import icons
import logging
import datetime
import sys


def setup_logger():
    logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)7s][%(name)15s]  %(message)s',
        stream=sys.stdout
    )


setup_logger()
log = logging.getLogger(__name__)

SHOW_GRIDLINES = False

img, draw = layout.create_new_image()

wifi_strength = get_wifi_strength()

layout.draw_icon(draw, 5, 0, get_wifi_strength_icon(wifi_strength))
layout.draw_icon(draw, 5, 1, icons.TOGGLE_OFF)
layout.draw_icon_inverse(draw, 5, 2, icons.TOGGLE_ON)
layout.draw_icon(draw, 5, 3, icons.SETTINGS)
layout.draw_icon(draw, 5, 4, icons.HOME)
layout.draw_icon(draw, 5, 5, icons.CHECKBOX)
layout.draw_icon(draw, 5, 6, icons.CHECKBOX_CHECKED)
layout.draw_icon(draw, 5, 7, icons.INFO)
layout.draw_icon(draw, 5, 8, icons.POWER_OFF)
layout.draw_icon(draw, 5, 9, icons.UP)
layout.draw_icon(draw, 5, 10, icons.DOWN)
layout.draw_icon(draw, 5, 11, icons.LEFT)
layout.draw_icon(draw, 5, 12, icons.RIGHT)
layout.draw_icon(draw, 5, 13, icons.REFRESH)

layout.fill_row(draw, 0, fill="black")
layout.draw_text(draw, 0, 0, "Title", fill="white")

if SHOW_GRIDLINES:
    layout.show_gridlines(draw)

##################################################################

# img.show()
# img.save("screen.png")
