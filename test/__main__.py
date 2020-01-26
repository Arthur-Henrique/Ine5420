
forward_differences = lambda d: [sum(d[i - 2:i]) for i in range(2, len(d)+1)]

dx = [1.503, 2.223, 3.671, 4.1212]

x, d1x, d2x, d3x = dx

j = 0
delta = 0.01

while j < 1.0:
	x = x + d1x
	d1x = d1x + d2x
	d2x = d2x + d3x

	(dx) = forward_differences(dx+[0])

	j += delta
