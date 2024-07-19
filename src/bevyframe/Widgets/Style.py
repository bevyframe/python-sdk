inherit = 'inherit'


class Align:
    center = 'center'
    left = 'left'
    right = 'right'
    baseline = 'baseline'
    sub = 'sub'


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
    def __init__(self, top=None, right=None, bottom=None, left=None):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class Margin(FourSided):
    pass


class Padding(FourSided):
    pass


class Position:
    class absolute(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None):
            self.item = 'absolute'
            super().__init__(top, right, bottom, left)

    class relative(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None):
            self.item = 'relative'
            super().__init__(top, right, bottom, left)

    class fixed(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None):
            self.item = 'fixed'
            super().__init__(top, right, bottom, left)

    class sticky(FourSided):
        def __init__(self, top=None, right=None, bottom=None, left=None):
            self.item = 'sticky'
            super().__init__(top, right, bottom, left)


def add_style(p1, p2):
    return f"calc({p1} + {p2})"


def substract_style(p1, p2):
    return f"calc({p1} - {p2})"


def multiply_style(p1, p2):
    return f"calc({p1} * {p2})"


def divide_style(p1, p2):
    return f"calc({p1} / {p2})"
