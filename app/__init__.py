from app import domain

p = lambda: \
	domain.create(
		name='p',
		type='Point',
		color=(1, 0, 0),
		coordinates=[(500, 500, 7)]
	)

l = lambda: \
	domain.create(
		name='l',
		type='Line',
		color=(0, 1, 0),
		coordinates=[(500, -10, 20), (800, 500, 20)]
	)

c = lambda: \
	domain.create(
		name='c',
		type='Chain',
		color=(0, 0, 1),
		coordinates=[(500, 600, 80), (900, 400, 80), (200, 200, 80)]
	)

plg = lambda: \
	domain.create(
		name='p',
		type='Polygon',
		color=(1, 1, 0),
		coordinates=[(100, 100, 10), (100, 400, 10), (400, 400, 10), (400, 100, 10)]
	)

f = lambda: \
	domain.create(
		name='f',
		type='Face',
		color=(1, 0, 1),
		coordinates=[
			(0, 0, 0), (0, 300, 40), (0, 600, 30)
		]
	)

bzc = lambda: \
	domain.create(
		name='bzc',
		type='Bezier_curve',
		color=(0, 1, 1),
		coordinates=[(100, 100, 100), (100, 400, 100), (400, 400, 100), (400, 100, 100)]
	)

bsc = lambda: \
	domain.create(
		name='bsc',
		type='BSpine_curve',
		color=(1, 1, 1),
		coordinates=[(100, 100, 0), (100, 400, 0), (400, 400, 0), (400, 100, 0)]
	)

# noinspection DuplicatedCode
bzs = lambda: \
	domain.create(
		name='bzs',
		type='Bezier_surface',
		color=(1, .5, 0),
		coordinates=[
			(0, 0, 0), (0, 30, 40), (0, 60, 30), (0, 100, 0),
			(30, 25, 20), (20, 60, 50), (30, 80, 50), (40, 0, 20),
			(60, 30, 20), (80, 60, 50), (70, 100, 45), (60, 0, 25),
			(100, 0, 0), (110, 30, 40), (110, 60, 30), (100, 90, 0)
		]
	)

# noinspection DuplicatedCode
bss = lambda: \
	domain.create(
		name='bss',
		type='BSpine_surface',
		color=(0, .5, 1),
		coordinates=[
			(0, 0, 0), (0, 30, 40), (0, 60, 30), (0, 100, 0),
			(30, 25, 20), (20, 60, 50), (30, 80, 50), (40, 0, 20),
			(60, 30, 20), (80, 60, 50), (70, 100, 45), (60, 0, 25),
			(100, 0, 0), (110, 30, 40), (110, 60, 30), (100, 90, 0)
		]
	)

