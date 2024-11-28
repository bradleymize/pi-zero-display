from PIL import Image, ImageFont, ImageDraw

MAX_WIDTH = 296
MAX_HEIGHT = 128
PADDING = 4
STEP = 20
ICON_OFFSET = 3

MIN_COL = 0
MAX_COL = 13
MIN_ROW = 0
MAX_ROW = 5

FONT_20 = ImageFont.truetype("MaterialSymbolsSharp[FILL,GRAD,opsz,wght].woff2", 20)

FONT_20_EXTRA_LIGHT = ImageFont.truetype("MaterialSymbolsSharp[FILL,GRAD,opsz,wght].woff2", 20)
FONT_20_EXTRA_LIGHT.set_variation_by_name("ExtraLight")

FONT_20_EXTRA_LIGHT_FILL = ImageFont.truetype("MaterialSymbolsSharp[FILL,GRAD,opsz,wght].woff2", 20)
FONT_20_EXTRA_LIGHT_FILL.set_variation_by_name("ExtraLight")
FONT_20_EXTRA_LIGHT_FILL.set_variation_by_axes([1])
# print(FONT_20.get_variation_names())
# print(FONT_20.get_variation_axes())


def get_grid_coord(row, col, is_icon=False):
    x = (STEP * col) + PADDING
    y = (STEP * row)
    if is_icon:
        y = y + ICON_OFFSET

    return x, y


def show_gridlines(img_draw):
    # Draw Horizontal lines
    for y in range(PADDING, MAX_HEIGHT, STEP):
        shape = [(PADDING, y), (MAX_WIDTH-PADDING, y)]
        img_draw.line(shape, fill="black", width=0)

    # Draw vertical lines
    for x in range(PADDING, MAX_WIDTH, STEP):
        shape = [(x, PADDING), (x, MAX_HEIGHT-PADDING)]
        img_draw.line(shape, fill="black", width=0)


def create_new_image():
    img = Image.new("RGB", (MAX_WIDTH, MAX_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    return img, draw


def verify_row_col_bounds(row, col):
    if row > MAX_ROW or row < MIN_ROW:
        raise Exception(f"Row must be between: {MIN_ROW} and {MAX_ROW}")
    if col > MAX_COL or col < MIN_COL:
        raise Exception(f"Column must be between: {MIN_COL} and {MAX_COL}")


def draw_text(draw, row, col, text, font=FONT_20, fill="black"):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col)
    ), f"{text}", font=font, fill=fill)


def draw_icon(draw, row, col, text, font=FONT_20_EXTRA_LIGHT, fill="black"):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col, True)
    ), f"{text}", font=font, fill=fill)


def draw_icon_inverse(draw, row, col, text, font=FONT_20_EXTRA_LIGHT_FILL, fill="black"):
    verify_row_col_bounds(row, col)

    draw.text((
        get_grid_coord(row, col, True)
    ), f"{text}", font=font, fill=fill)


def fill_cell(draw, row, col, fill="black"):
    start_x, start_y = get_grid_coord(row, col)
    start_y = start_y + PADDING
    # print(f"({start_x},{start_y})")

    end_x, end_y = get_grid_coord(row+1, col+1)
    end_x = end_x - 1
    end_y = end_y + PADDING - 1
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
