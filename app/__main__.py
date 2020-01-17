import app.view as view
import app.model as model
import core

model.init()
view.init()

OBJECT_MANAGER = model.OBJECT_MANAGER

# OBJECT_MANAGER.create("z", (1, 0, 1), [(-50, 200), (800, 200), (500, 500), (800, 500)])
# OBJECT_MANAGER.create("q", (1, 1, 0), [(500, 500), (500, 800), (800, 800), (800, 500), (500, 500)])

# OBJECT_MANAGER.create("l", (0, 1, 1), [(30, 50), (50, 30)])
# OBJECT_MANAGER.create("l", (0, 1, 1), [(100, 150)])

OBJECT_MANAGER.create("w", (1, 0, 1), [(-50, -50), (800, -50), (500, 500), (800, 500)])

view.run()
