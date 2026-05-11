from .Drawables import ShapeType

class Style:
    STYLE_MAP = {}
    _current_style = None 

    def __init__(self, shape_color_map):
        self.shape_color_map = shape_color_map

    def get_color(self, shape_type):
        return self.shape_color_map.get(shape_type, (0, 0, 0))

    # -------------------------
    # STYLE REGISTRY
    # -------------------------
    @classmethod
    def register_style(cls, name: str, style: "Style"):
        cls.STYLE_MAP[name] = style

    @classmethod
    def get_style_by_name(cls, name: str):
        return cls.STYLE_MAP.get(name, cls.STYLE_MAP.get("colorful"))

    # -------------------------
    # CURRENT STYLE (CACHE)
    # -------------------------
    @classmethod
    def set_current_style(cls, name: str):
        cls._current_style = cls.get_style_by_name(name)

    @classmethod
    def current(cls):
        return cls._current_style or cls.get_style_by_name("colorful")

# -------------------------
# JSON LOADER
# -------------------------
def load_styles(style_data):
    styles_raw = style_data["Styles"]

    for style_name, mapping in styles_raw.items():
        converted_map = {}

        for shape_name, rgb in mapping.items():
            shape_type = ShapeType[shape_name]
            converted_map[shape_type] = tuple(rgb)

        Style.register_style(style_name, Style(converted_map))


# -------------------------
# BUILT-IN DEFAULT STYLES
# -------------------------
Style.register_style(
    "classic_style",
    Style({
        ShapeType.BLOCK: (220, 220, 220),
        ShapeType.ARROW: (0, 0, 0),
        ShapeType.VERTBAR: (0, 0, 0),
    })
)

Style.register_style(
    "colorful_style",
    Style({
        ShapeType.BLOCK: (255, 200, 200),
        ShapeType.ARROW: (0, 100, 255),
        ShapeType.VERTBAR: (0, 100, 255),
    })
)