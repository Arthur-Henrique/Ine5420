from app import model, view


model.init()
view.init()

clipping = model.CLIPPING
coordenates = [(750, 500), (800, 800)]

result = clipping.apply(coordenates)
print(result)