from .Drawables import ShapeType

class Style:
    def __init__(self, shape_color_map):
        self.shape_color_map = shape_color_map  # Dict[ShapeType, (R, G, B)]

    def get_color(self, shape_type):
        return self.shape_color_map.get(shape_type, (0, 0, 0))  # default black

classic_style = Style({
    ShapeType.BLOCK: (220, 220, 220),  # light gray
    ShapeType.ARROW: (0, 0, 0),        # black
    ShapeType.VERTBAR: (0, 0, 0),        # black
})

colorful_style = Style({
    ShapeType.BLOCK: (255, 200, 200),  # light red
    ShapeType.ARROW: (0, 100, 255),    # blue
    ShapeType.VERTBAR: (0, 100, 255),  # blue
})
