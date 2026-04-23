def log(msg):
	quick_print(msg)

def go_to(tx, ty):
	x = get_pos_x()
	y = get_pos_y()

	while x < tx:
		move(East)
		x = x + 1

	while x > tx:
		move(West)
		x = x - 1

	while y < ty:
		move(North)
		y = y + 1

	while y > ty:
		move(South)
		y = y - 1


def run_rect(x0, y0, w, h, cb):
	go_to(x0, y0)
	ry = 0

	while ry < h:
		if ry % 2 == 0:
			rx = 0
			while rx < w:
				cb(x0 + rx, y0 + ry)
				if rx < w - 1:
					move(East)
				rx = rx + 1
		else:
			rx = w - 1
			while rx >= 0:
				cb(x0 + rx, y0 + ry)
				if rx > 0:
					move(West)
				rx = rx - 1

		if ry < h - 1:
			move(North)
		ry = ry + 1
		