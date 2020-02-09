import app.domain as domain
import app.view as view

# domain.create(
# 	name='p',
# 	type='Point',
# 	color=(1, 0, 0),
# 	coordinates=[(500, 500, 7)]
# )

# domain.create(
# 	name='l',
# 	type='Line',
# 	color=(0, 1, 0),
# 	coordinates=[(50, 50, 20), (60, 60, 20)]
# )

# domain.create(
# 	name='c',
# 	type='Chain',
# 	color=(0, 0, 1),
# 	coordinates=[(500, 600, 80), (900, 400, 80), (200, 200, 80)]
# )

domain.create(
	name='p',
	type='Polygon',
	color=(0, 0, 1),
	coordinates=[(100, 100, 10), (100, 400, 10), (400, 400, 10), (400, 100, 10)]
)

# domain.create(
# 	name='bzc',
# 	type='',
# 	color=(1, 0, 1),
# 	coordinates=[(100, 100), (100, 400), (400, 400), (400, 100)]
# )
#
# domain.create(
# 	name='bsc',
# 	type='Bspine_curve',
# 	color=(1, 1, 1),
# 	coordinates=[(100, 100), (100, 400), (400, 400), (400, 100)]
# )

view.run()
