import json
from .Drawables import ShapeType


class Style:
    # -------------------------
    # CONFIG
    # -------------------------
    DEFAULT_STYLE = "colorful_style"

    STYLE_MAP = {}
    _current_style = None

    def __init__(self, shape_color_map):
        self.shape_color_map = shape_color_map

    def get_color(self, shape_type):
        return self.shape_color_map.get(shape_type, (0, 0, 0))

    # -------------------------
    # REGISTRY
    # -------------------------
    @classmethod
    def register_style(cls, name: str, style: "Style"):
        cls.STYLE_MAP[name] = style

    @classmethod
    def get_style_by_name(cls, name: str):
        return cls.STYLE_MAP.get(name, cls.STYLE_MAP.get(cls.DEFAULT_STYLE))

    # -------------------------
    # CURRENT STYLE
    # -------------------------
    @classmethod
    def set_current_style(cls, name: str):
        cls._current_style = cls.get_style_by_name(name)

    @classmethod
    def current(cls):
        return cls._current_style or cls.get_style_by_name(cls.DEFAULT_STYLE)

    # -------------------------
    # JSON LOADER
    # -------------------------
    @classmethod
    def load_from_json(cls, style_data: dict):
        styles_raw = style_data.get("Styles", {})

        for style_name, mapping in styles_raw.items():
            converted_map = {}

            for shape_name, rgb in mapping.items():
                shape_type = ShapeType[shape_name]
                converted_map[shape_type] = tuple(rgb)

            cls.register_style(style_name, Style(converted_map))

        # -------------------------
        # INITIAL STYLE SELECTION
        # -------------------------
        requested = style_data.get("CurrentStyle")

        if requested in cls.STYLE_MAP:
            cls.set_current_style(requested)
        else:
            cls.set_current_style(cls.DEFAULT_STYLE)


# -------------------------
# BUILT-IN STYLES
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