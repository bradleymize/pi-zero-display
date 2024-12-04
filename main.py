import layout
import logging
import datetime
import sys
###################
# DISPLAY IMPORTS #
###################
from library import epd2in9_V2, icnt86
import threading
import time
import math
from screen import set_display, get_display, SCREENS, set_current_page, get_current_page
###################


def setup_logger():
    logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)7s][%(name)15s]  %(message)s',
        stream=sys.stdout
    )


setup_logger()
log = logging.getLogger(__name__)
layout.FLIPPED = True
layout.SHOW_GRIDLINES = False

flag_t = 1


def pthread_irq():
    log.info("pthread irq running")
    while flag_t == 1:
        read_value = touch_panel.digital_read(touch_panel.INT)
        if read_value == 0:
            touch_event_current.Touch = 1
        else :
            touch_event_current.Touch = 0
        time.sleep(0.01)
    log.info("thread irq: exit")


try:
    log.info("epd2in9_V2 Touch Demo")

    set_display(epd2in9_V2.EPD_2IN9_V2())
    display = get_display()
    touch_panel = icnt86.INCT86()
    touch_event_current = icnt86.ICNT_Development()
    touch_event_old = icnt86.ICNT_Development()

    logging.info("init and Clear")
    display.init()
    touch_panel.ICNT_Init()
    display.Clear(0xFF)

    t1 = threading.Thread(target=pthread_irq)
    t1.daemon = True
    t1.start()

    log.info("Rendering initial main screen")
    img = SCREENS['MainScreen'].render_img()
    display.display_Base(display.getbuffer(img))

    touch_count = j = k = refresh_flag = SelfFlag = Page = Photo_L = Photo_S = 0
    font24 = font15 = None


    def Draw_Time(*args):
        pass


    Read_BMP = Show_Photo_Small = Show_Photo_Large = Draw_Time

    #############################################################
    # My better-named properties/flags to replace previous ones #
    set_current_page('MainScreen')
    should_draw = False
    #############################################################

    while True:
        if should_draw:
            SCREENS[get_current_page()].render("None", "None")
            should_draw = False
            touch_count = 0
            k = 0
            j += 1

        # if touch_count > 20 or refresh_flag == 1:
        #     if get_current_page() == 'MainScreen':
        #         # Must request a new image prior to updating a drawing (can't edit once epd has been updated?)
        #         SCREENS['MainScreen'].render("None", "None")
        #         # print("*** Time Refresh ***\r\n")
        #
        #     # display.display_Partial_Wait(display.getbuffer(img))
        #     # print("*** Touch Refresh ***\r\n")
        #     touch_count = 0
        #     k = 0
        #     j += 1
        #     refresh_flag = 0
        # elif k > 50000 and touch_count > 0 and Page == 1:
        #     display.display_Partial_Wait(display.getbuffer(img))
        #     touch_count = 0
        #     k = 0
        #     j += 1
        #     # print("*** Overtime Refresh ***\r\n")
        # elif j > 50 or SelfFlag:
        #     SelfFlag = 0
        #     j = 0
        #     display.init()
        #     display.display_Base(display.getbuffer(img))
        #     # print("--- Self Refresh ---\r\n")
        # else:
        #     k += 1

        # if main screen
        # and current time is n-second-interval (e.g. % 60 = every 60 seconds, % 20 = every 20 seconds)
        current_timestamp = time.time()
        current_timestamp_seconds = math.floor(current_timestamp)
        last_timestamp_seconds = None
        if (get_current_page() == 'MainScreen'
                and current_timestamp_seconds % 60 == 0
                and not current_timestamp_seconds == last_timestamp_seconds
        ):
            last_timestamp_seconds = current_timestamp_seconds
            log.debug("Time refresh")
            should_draw = True

        touch_panel.ICNT_Scan(touch_event_current, touch_event_old)
        if touch_event_old.X[0] == touch_event_current.X[0] and touch_event_old.Y[0] == touch_event_current.Y[0]:
            continue

        if touch_event_current.TouchCount:
            touch_event_current.TouchCount = 0
            touch_count += 1
            col, row = layout.get_touch_cell(touch_event_current.X[0], touch_event_current.Y[0])
            the_screen = SCREENS[get_current_page()]
            the_screen.handle_touch(row, col)
            should_draw = True


except IOError as e:
    log.info(e)
except KeyboardInterrupt:
    log.info("ctrl + c")
    flag_t = 0
    display.sleep()
    time.sleep(2)
    t1.join()
    display.Dev_exit()
    exit()
