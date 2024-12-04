from PIL import Image, ImageFont, ImageDraw
import math
import logging

log = logging.getLogger(__name__)

MAX_WIDTH = 296
MAX_HEIGHT = 128
PADDING_LEFT = 8
PADDING_TOP = 4
STEP = 20
ICON_OFFSET = 3
TEXT_OFFSET = 2

MIN_COL = 0
MAX_COL = 13
MIN_ROW = 0
MAX_ROW = 5


TEXT_FONT_NAME = "Roboto-Medium.ttf"
TEXT_FONT_20 = ImageFont.truetype(TEXT_FONT_NAME, 20)
TEXT_FONT_16 = ImageFont.truetype(TEXT_FONT_NAME, 16)

ICON_FONT_NAME = "MaterialSymbolsSharp[FILL,GRAD,opsz,wght].woff2"
ICON_FONT_VARIANT = "Medium"

ICON_FONT_20_EXTRA_LIGHT = ImageFont.truetype(ICON_FONT_NAME, 20)
ICON_FONT_20_EXTRA_LIGHT.set_variation_by_name(ICON_FONT_VARIANT)

ICON_FONT_20_EXTRA_LIGHT_FILL = ImageFont.truetype(ICON_FONT_NAME, 20)
ICON_FONT_20_EXTRA_LIGHT_FILL.set_variation_by_name(ICON_FONT_VARIANT)
ICON_FONT_20_EXTRA_LIGHT_FILL.set_variation_by_axes([1])

FLIPPED = False
IMAGE_WAS_FLIPPED = False
SHOW_GRIDLINES = False

# print(f"Font variant: {ICON_FONT_VARIANT}")
# print(FONT_20.get_variation_names())
# print(FONT_20.get_variation_axes())


def get_grid_coord(row, col, is_icon=False, is_text=False, additional_x_offset=0, additional_y_offset=0):
    x = (STEP * col) + PADDING_LEFT + additional_x_offset
    y = (STEP * row) + additional_y_offset
    if is_icon or is_text:
        y = y + (ICON_OFFSET if is_icon else TEXT_OFFSET)

    return x, y


def show_gridlines(img_draw):
    # STEP * (MAX_ROW/COL * 2) --> plus 2 due to:
    #    zero based
    #    and then needing to go to the end of the last cell, not the beginning

    # Draw Horizontal lines
    for y in range(PADDING_TOP, STEP * (MAX_ROW + 2), STEP):
        # plus 1 due to zero based
        shape = [(PADDING_LEFT, y), (STEP * (MAX_COL + 1) + PADDING_LEFT, y)]
        img_draw.line(shape, fill="black", width=0)

    # Draw vertical lines
    for x in range(PADDING_LEFT, STEP * (MAX_COL + 2), STEP):
        # plus 1 due to zero based
        shape = [(x, PADDING_TOP), (x, STEP * (MAX_ROW + 1) + PADDING_TOP)]
        img_draw.line(shape, fill="black", width=0)


def create_new_image():
    global IMAGE_WAS_FLIPPED
    img = Image.new("RGB", (MAX_WIDTH, MAX_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    IMAGE_WAS_FLIPPED = False

    return img, draw


def verify_row_col_bounds(row, col):
    if row > MAX_ROW or row < MIN_ROW:
        raise Exception(f"Row must be between: {MIN_ROW} and {MAX_ROW}")
    if col > MAX_COL or col < MIN_COL:
        raise Exception(f"Column must be between: {MIN_COL} and {MAX_COL}")


def draw_text(draw, row, col, text, font=TEXT_FONT_20, fill="black", additional_x_offset=0, additional_y_offset=0, anchor="la"):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col, is_text=True, additional_x_offset=additional_x_offset, additional_y_offset=additional_y_offset)
    ), f"{text}", font=font, fill=fill, anchor=anchor)


def draw_icon(draw, row, col, text, font=ICON_FONT_20_EXTRA_LIGHT, fill="black", additional_x_offset=0, additional_y_offset=0):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col, True, additional_x_offset=additional_x_offset, additional_y_offset=additional_y_offset)
    ), f"{text}", font=font, fill=fill)


def draw_icon_inverse(draw, row, col, text, font=ICON_FONT_20_EXTRA_LIGHT_FILL, fill="black", additional_x_offset=0, additional_y_offset=0):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col, True, additional_x_offset=additional_x_offset, additional_y_offset=additional_y_offset)
    ), f"{text}", font=font, fill=fill)


def fill_cell(draw, row, col, fill="black"):
    start_x, start_y = get_grid_coord(row, col)
    start_y = start_y + PADDING_TOP
    # print(f"({start_x},{start_y})")

    end_x, end_y = get_grid_coord(row+1, col+1)
    end_x = end_x - 1
    end_y = end_y + PADDING_TOP - 1
    # print(f"({end_x},{end_y})")

    draw.rectangle([
        (start_x, start_y),
        (end_x, end_y)
    ], fill=fill)


def fill_row(draw, row, start=MIN_COL, end=MAX_COL, fill="black"):
    if start < MIN_COL:
        raise Exception(f"start must be greater than {MIN_COL}")
    if end > MAX_COL:
        raise Exception(f"END must be LESS than {MAX_COL}")
    if start >= end:
        raise Exception(f"start must be less than end")

    for i in range(start, end + 1):
        fill_cell(draw, row, i, fill)


def fill_col(draw, col, start=MIN_ROW, end=MAX_ROW, fill="black"):
    if start < MIN_ROW:
        raise Exception(f"start must be greater than {MIN_ROW}")
    if end > MAX_ROW:
        raise Exception(f"END must be LESS than {MAX_ROW}")
    if start >= end:
        raise Exception(f"start must be less than end")

    for i in range(start, end + 1):
        fill_cell(draw, i, col, fill)


def get_touch_cell(x, y):
    if FLIPPED:
        x = MAX_WIDTH - x
        y = MAX_HEIGHT - y
    col = math.floor((x - PADDING_LEFT) / STEP)
    row = math.floor((y - PADDING_TOP) / STEP)

    if col > MAX_COL:
        col = MAX_COL
    if col < MIN_COL:
        col = MIN_COL

    if row > MAX_ROW:
        row = MAX_ROW
    if row < MIN_ROW:
        row = MIN_ROW

    log.debug(f"Touched: ({x},{y}) = Column {col}, Row {row}")

    return col, row
