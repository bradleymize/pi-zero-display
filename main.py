from stats import get_wifi_strength_icon, get_wifi_strength
from PIL import Image
import layout
import icons
import logging
import datetime
import sys
###################
# DISPLAY IMPORTS #
###################
from library import epd2in9_V2, icnt86
import threading
import time
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

SHOW_GRIDLINES = True

##################################################################

# img.show()
# img.save("screen.png")

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

    epd = epd2in9_V2.EPD_2IN9_V2()
    touch_panel = icnt86.INCT86()
    touch_event_current = icnt86.ICNT_Development()
    touch_event_old = icnt86.ICNT_Development()

    logging.info("init and Clear")
    epd.init()
    touch_panel.ICNT_Init()
    epd.Clear(0xFF)

    t1 = threading.Thread(target=pthread_irq)
    t1.daemon = True
    t1.start()

    ####################################################
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
    layout.fill_row(draw, 3, fill="black")

    layout.draw_text(draw, 0, 0, "Title", fill="white")
    layout.draw_text(draw, 1, 0, "Title")
    layout.draw_text(draw, 2, 0, "Title", font=layout.TEXT_FONT_16)
    layout.draw_text(draw, 3, 0, "Title", fill="white", font=layout.TEXT_FONT_16, additional_y_offset=2, additional_x_offset=2)

    img = img.transpose(Image.ROTATE_180)

    if SHOW_GRIDLINES:
        layout.show_gridlines(draw)
    ####################################################

    epd.display_Base(epd.getbuffer(img))

    i = j = k = ReFlag = SelfFlag = Page = Photo_L = Photo_S = 0
    font24 = font15 = None


    def Draw_Time(*args):
        pass


    Read_BMP = Show_Photo_Small = Show_Photo_Large = Draw_Time
    PagePath = []

    while True:
        if i > 20 or ReFlag == 1:
            if Page == 0:
                pass
                # print("*** Time Refresh ***\r\n")

            epd.display_Partial_Wait(epd.getbuffer(img))
            # print("*** Touch Refresh ***\r\n")
            i = 0
            k = 0
            j += 1
            ReFlag = 0
        elif k > 50000 and i > 0 and Page == 1:
            epd.display_Partial_Wait(epd.getbuffer(img))
            i = 0
            k = 0
            j += 1
            # print("*** Overtime Refresh ***\r\n")
        elif j > 50 or SelfFlag:
            SelfFlag = 0
            j = 0
            epd.init()
            epd.display_Base(epd.getbuffer(img))
            # print("--- Self Refresh ---\r\n")
        else:
            k += 1

        if Page == 0 and k > 5000000:
            ReFlag = 1

        touch_panel.ICNT_Scan(touch_event_current, touch_event_old)
        if touch_event_old.X[0] == touch_event_current.X[0] and touch_event_old.Y[0] == touch_event_current.Y[0]:
            continue

        if touch_event_current.TouchCount:
            touch_event_current.TouchCount = 0
            i += 1
            row, col = layout.get_touch_cell(touch_event_current.X[0], touch_event_current.Y[0])
            if Page == 0 and ReFlag == 0:     # main menu
                if touch_event_current.X[0] > 119 and touch_event_current.X[0] < 152 and touch_event_current.Y[0] > 31 and touch_event_current.Y[0] < 96:
                    # print("Touched Photo ...\r\n")
                    # Page = 2
                    # Read_BMP(PagePath[Page], 0, 0)
                    # Show_Photo_Small(img, Photo_S)
                    ReFlag = 1
                elif touch_event_current.X[0] > 39 and touch_event_current.X[0] < 80 and touch_event_current.Y[0] > 31 and touch_event_current.Y[0] < 96:
                    # print("Touched Weather ...\r\n")
                    # Page = 1
                    # Read_BMP(PagePath[Page], 0, 0)
                    ReFlag = 1

            # if Page == 1 and ReFlag == 0:   # weather
            #     if touch_event_current.X[0] > 136 and touch_event_current.X[0] < 159 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Home ...\r\n")
            #         Page = 0
            #         Read_BMP(PagePath[Page], 0, 0)
            #         ReFlag = 1
            #     elif touch_event_current.X[0] > 5 and touch_event_current.X[0] < 27 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Refresh ...\r\n")
            #         SelfFlag = 1
            #         ReFlag = 1
            #
            # if Page == 2  and ReFlag == 0:  # photo menu
            #     if touch_event_current.X[0] > 135 and touch_event_current.X[0] < 160 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Home ...\r\n")
            #         Page = 0
            #         Read_BMP(PagePath[Page], 0, 0)
            #         ReFlag = 1
            #     elif touch_event_current.X[0] > 203 and touch_event_current.X[0] < 224 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Next page ...\r\n")
            #         Photo_S += 1
            #         if Photo_S > 2:  # 9 photos is a maximum of three pages
            #             Photo_S = 0
            #         ReFlag = 2
            #     elif touch_event_current.X[0] > 71 and touch_event_current.X[0] < 92 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Last page ...\r\n")
            #         if Photo_S == 0:
            #             print("Top page ...\r\n")
            #         else:
            #             Photo_S -= 1
            #             ReFlag = 2
            #     elif touch_event_current.X[0] > 5 and touch_event_current.X[0] < 27 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Refresh ...\r\n")
            #         SelfFlag = 1
            #         ReFlag = 1
            #     elif touch_event_current.X[0] > 2 and touch_event_current.X[0] < 293 and touch_event_current.Y[0] > 2 and touch_event_current.Y[0] < 96 and ReFlag == 0:
            #         print("Select photo ...\r\n")
            #         Page = 3
            #         Read_BMP(PagePath[Page], 0, 0)
            #         Photo_L = touch_event_current.X[0] // 96 + touch_event_current.Y[0] // 48 * 3 + Photo_S * 3 + 1
            #         Show_Photo_Large(img, Photo_L)
            #         ReFlag = 1
            #     if ReFlag == 2:  # Refresh small photo
            #         ReFlag = 1
            #         Read_BMP(PagePath[Page], 0, 0)
            #         Show_Photo_Small(img, Photo_S)   # show small photo
            #
            # if Page == 3  and ReFlag == 0:  # view the photo
            #     if touch_event_current.X[0] > 268 and touch_event_current.X[0] < 289 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Photo menu ...\r\n")
            #         Page = 2
            #         Read_BMP(PagePath[Page], 0, 0)
            #         Show_Photo_Small(img, Photo_S)
            #         ReFlag = 1
            #     elif touch_event_current.X[0] > 203 and touch_event_current.X[0] < 224 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Next photo ...\r\n")
            #         Photo_L += 1
            #         if Photo_L > 9:
            #             Photo_L = 1
            #         ReFlag = 2
            #     elif touch_event_current.X[0] > 135 and touch_event_current.X[0] < 160 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Home ...\r\n")
            #         Page = 0
            #         Read_BMP(PagePath[Page], 0, 0)
            #         ReFlag = 1
            #     elif touch_event_current.X[0] > 71 and touch_event_current.X[0] < 92 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Last page ...\r\n")
            #         if Photo_L == 1:
            #             print("Top photo ...\r\n")
            #         else:
            #             Photo_L -= 1
            #             ReFlag = 2
            #     elif touch_event_current.X[0] > 5 and touch_event_current.X[0] < 27 and touch_event_current.Y[0] > 101 and touch_event_current.Y[0] < 124:
            #         print("Refresh photo ...\r\n")
            #         SelfFlag = 1
            #         ReFlag = 1
            #     if ReFlag == 2:    # Refresh large photo
            #         ReFlag = 1
            #         Show_Photo_Large(img, Photo_L)


except IOError as e:
    log.info(e)
except KeyboardInterrupt:
    log.info("ctrl + c")
    flag_t = 0
    epd.sleep()
    time.sleep(2)
    t1.join()
    epd.Dev_exit()
    exit()
