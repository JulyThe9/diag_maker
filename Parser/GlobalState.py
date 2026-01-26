class GlobalState:
    def __init__(self):
        # communicating entity name -> drawable idx in Control.drawables
        self.comm_entities = {}