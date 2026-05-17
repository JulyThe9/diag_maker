from Drawing.Style import FontStyle


class TextStruct:
    def __init__(self, font_style: FontStyle = None, text_str="", label_x=0, label_y=0, text_rect_x=0, text_rect_y=0):
        self.text_str = text_str
        self.label_x = label_x
        self.label_y = label_y
        self.text_rect_x = text_rect_x
        self.text_rect_y = text_rect_y
        
        if font_style:
            self.font = font_style.Font
            self.size = font_style.Size
            self.bold = font_style.Bold
        else:
            self.font = "Roboto"
            self.size = 18
            self.bold = False
        