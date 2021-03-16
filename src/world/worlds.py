class World:
    def __init__(self, camera_cls, renderer_cls, width=None, height=None):
        self._camera = camera_cls(self)
        self._renderer = renderer_cls(self)
        self._width = width
        self._height = height
        self._models = []

    @property
    def camera(self):
    	return self._camera

    @property
    def models(self):
    	return self._models
    

    def add_model(self, model):
        self._models.append(model)

    def clear(self):
        return self._renderer.clear()

    def update(self):
        for model in self._models:
            model.update()

    def render(self):
        self._renderer.render()

    def show(self):
        self._renderer.show()
    