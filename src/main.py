import app
import model
from obj import *

model.init()
app.init()

p = model.OBJECT_MANAGER.create("p", (1, 1, 1), [(40, 20)])
model.OBJECT_MANAGER.create("p2", (1, 0.5, 0.5), [(40, 25)])
l = model.OBJECT_MANAGER.create("l", (1, 0, 1), [(140, 200), (60, 90)])
model.OBJECT_MANAGER.create("l2", (0, 0, 1), [(180, 60), (160, 190)])
w = model.OBJECT_MANAGER.create("w", (1, 1, 0), [(540, 500), (560, 590), (800, 100), (700, 700)])
model.project()

app.run()
