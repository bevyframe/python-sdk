inherit = 'inherit'
NoStyle = 'none'


class Float:
    left = 'left'
    right = 'right'
    none = 'none'


class Theme:
    blank = "blank"
    red = "red"
    orange = "orange"
    yellow = "yellow"
    green = "green"
    blue = "blue"
    pink = "pink"


class Effect:
    blur = lambda x: f'blur({x}px)'
    brightness = lambda x: f'brightness({x})'
    contrast = lambda x: f'contrast({x})'
    drop_shadow = lambda x, y, blur, color: f'drop-shadow({x}px {y}px {blur}px {color})'
    grayscale = lambda x: f'grayscale({x})'
    hue_rotate = lambda x: f'hue-rotate({x}deg)'
    invert = lambda x: f'invert({x})'
    opacity = lambda x: f'opacity({x})'
    saturate = lambda x: f'saturate({x})'
    sepia = lambda x: f'sepia({x})'


class BorderLine:
    solid = 'solid'
    dashed = 'dashed'
    dotted = 'dotted'
    double = 'double'
    groove = 'groove'
    ridge = 'ridge'
    inset = 'inset'
    outset = 'outset'
    hidden = 'hidden'


def Border(width: str, style: str, color: str) -> str:
    return f"{width} {style} {color}"


class Scroll:
    smooth = 'smooth'
    auto = 'auto'
    hidden = 'hidden'


class Visibility:
    visible = 'visible'
    hidden = 'hidden'
    collapse = 'collapse'


class Align:
    center = 'center'
    left = 'left'
    right = 'right'
    baseline = 'baseline'
    sub = 'sub'
    text_top = 'text-top'


class Cursor:
    pointer = 'pointer'
    default = 'default'
    help = 'help'
    wait = 'wait'
    text = 'text'
    move = 'move'
    not_allowed = 'not-allowed'
    grab = 'grab'
    grabbing = 'grabbing'
    zoom_in = 'zoom-in'
    zoom_out = 'zoom-out'
    crosshair = 'crosshair'
    e_resize = 'e-resize'
    n_resize = 'n-resize'
    ne_resize = 'ne-resize'
    nw_resize = 'nw-resize'
    s_resize = 's-resize'
    se_resize = 'se-resize'
    sw_resize = 'sw-resize'
    w_resize = 'w-resize'
    ew_resize = 'ew-resize'
    ns_resize = 'ns-resize'
    nesw_resize = 'nesw-resize'
    nwse_resize = 'nwse-resize'
    col_resize = 'col-resize'
    row_resize = 'row-resize'


class Color:
    transparent = 'transparent'
    black = '#000000'
    white = '#ffffff'
    red = '#ff0000'
    hex = lambda x: f'#{x}'
    rgb = lambda r, g, b: f'rgb({r}, {g}, {b})'


class Size:
    max_content = 'max-content'
    fit_content = 'fit-content'
    percent = lambda x: f'{x}%'
    pixel = lambda x: f'{x}px'
    auto = 'auto'

    class Relative:
        font = lambda i: f'{i}em'
        x = lambda i: f'{i}ex'

    class Viewport:
        height = lambda x: f'{x}vh'
        width = lambda x: f'{x}vw'
        min = lambda x: f'{x}vmin'
        max = lambda x: f'{x}vmax'


class FourSided:
    def __init__(self, top=None, right=None, bottom=None, left=None) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class Coordinate:
    def __init__(self, x=None, y=None) -> None:
        self.x = x
        self.y = y


class Overflow(Coordinate):
    pass


class Margin(FourSided):
    pass


class Padding(FourSided):
    pass


class Position:

    class absolute(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None) -> None:
            self.item = 'absolute'
            super().__init__(top, right, bottom, left)

    class relative(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None) -> None:
            self.item = 'relative'
            super().__init__(top, right, bottom, left)

    class fixed(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None) -> None:
            self.item = 'fixed'
            super().__init__(top, right, bottom, left)

    class sticky(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None) -> None:
            self.item = 'sticky'
            super().__init__(top, right, bottom, left)


def add_style(p1, p2) -> str:
    return f"calc({p1} + {p2})"


def substract_style(p1, p2) -> str:
    return f"calc({p1} - {p2})"


def multiply_style(p1, p2) -> str:
    return f"calc({p1} * {p2})"


def divide_style(p1, p2) -> str:
    return f"calc({p1} / {p2})"
