import util

SIZE = 12
HALF = SIZE // 2

BURST_PASSES = 7
RUNS = 3

stats = []


def stat_add(run_no, label, ticks, secs, extra):
	stats.append([run_no, label, ticks, secs, extra])


def stat_dump():
	i = 0
	while i < len(stats):
		row = stats[i]
		quick_print(
			"run=" + str(row[0]) +
			" " + row[1] +
			" ticks=" + str(row[2]) +
			" secs=" + str(row[3]) +
			" extra=" + str(row[4])
		)
		i = i + 1


def stat_reset():
	global stats
	stats = []


def work_start():
	return [get_tick_count(), get_time()]


def work_end(start_info):
	return [
		get_tick_count() - start_info[0],
		get_time() - start_info[1]
	]


def soil_if_needed():
	if get_ground_type() != Grounds.Soil:
		till()


def seed_half(x0, y0, w, h):
	util.go_to(x0, y0)

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				t = get_entity_type()

				if t != Entities.Cactus:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Cactus)

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				t = get_entity_type()

				if t != Entities.Cactus:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Cactus)

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1


def ready_half(x0, y0, w, h):
	util.go_to(x0, y0)

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				if get_entity_type() != Entities.Cactus:
					return False
				if not can_harvest():
					return False

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				if get_entity_type() != Entities.Cactus:
					return False
				if not can_harvest():
					return False

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1

	return True


def h_sweep_once():
	util.go_to(0, 0)
	changed = 0

	y = 0
	while y < SIZE:
		if y % 2 == 0:
			x = 0
			while x < SIZE:
				a = measure()

				if x < SIZE - 1:
					b = measure(East)
					if a != None and b != None:
						if a > b:
							swap(East)
							changed = changed + 1

				if x < SIZE - 1:
					move(East)
				x = x + 1
		else:
			x = SIZE - 1
			while x >= 0:
				a = measure()

				if x > 0:
					move(West)
					b = measure()
					move(East)

					if a != None and b != None:
						if b > a:
							swap(West)
							changed = changed + 1

				if x > 0:
					move(West)
				x = x - 1

		if y < SIZE - 1:
			move(North)
		y = y + 1

	return changed


def v_sweep_once():
	changed = 0

	x = 0
	while x < SIZE:
		if x % 2 == 0:
			util.go_to(x, 0)
			y = 0

			while y < SIZE:
				a = measure()

				if y < SIZE - 1:
					b = measure(North)
					if a != None and b != None:
						if a > b:
							swap(North)
							changed = changed + 1

				if y < SIZE - 1:
					move(North)
				y = y + 1

		else:
			util.go_to(x, SIZE - 1)
			y = SIZE - 1

			while y >= 0:
				a = measure()

				if y > 0:
					move(South)
					b = measure()
					move(North)

					if a != None and b != None:
						if b > a:
							swap(South)
							changed = changed + 1

				if y > 0:
					move(South)
				y = y - 1

		x = x + 1

	return changed


def h_worker(passes):
	total = 0
	n = 0
	while n < passes:
		total = total + h_sweep_once()
		n = n + 1
	return total


def v_worker(passes):
	total = 0
	n = 0
	while n < passes:
		total = total + v_sweep_once()
		n = n + 1
	return total


def seed_worker(x0, y0, w, h):
	seed_half(x0, y0, w, h)
	return 1


def ready_worker(x0, y0, w, h):
	if ready_half(x0, y0, w, h):
		return 1
	return 0


def row_text(y):
	x = 0
	text = ""

	while x < SIZE:
		util.go_to(x, y)
		v = measure()

		if x > 0:
			text = text + " "

		if v == None:
			text = text + "N"
		else:
			text = text + str(v)

		x = x + 1

	return text


def log_rows(tag, run_no):
	quick_print("run=" + str(run_no) + " " + tag)
	quick_print("top: " + row_text(SIZE - 1))
	quick_print("mid: " + row_text(SIZE // 2))
	quick_print("bot: " + row_text(0))


def seed_parallel(run_no):
	s = work_start()

	h = spawn_drone(seed_worker, HALF, 0, SIZE - HALF, SIZE)
	left = seed_worker(0, 0, HALF, SIZE)

	right = 0
	if h != None:
		right = wait_for(h)

	d = work_end(s)
	stat_add(run_no, "seed", d[0], d[1], [left, right])

	return left + right


def ready_parallel(run_no):
	s = work_start()

	h = spawn_drone(ready_worker, HALF, 0, SIZE - HALF, SIZE)
	left = ready_worker(0, 0, HALF, SIZE)

	right = 0
	if h != None:
		right = wait_for(h)

	d = work_end(s)
	stat_add(run_no, "ready", d[0], d[1], [left, right])

	if left == 1 and right == 1:
		return True

	return False


def burst_once(run_no):
	s = work_start()

	h = spawn_drone(v_worker, BURST_PASSES)
	hc = h_worker(BURST_PASSES)

	vc = 0
	if h != None:
		vc = wait_for(h)

	d = work_end(s)
	stat_add(run_no, "burst", d[0], d[1], [hc, vc])

	if hc == 0 and vc == 0:
		return False

	return True


def try_harvest(run_no):
	s = work_start()

	before = num_items(Items.Cactus)

	util.go_to(0, 0)
	if can_harvest():
		harvest()
		after = num_items(Items.Cactus)
		d = work_end(s)
		delta = after - before
		stat_add(run_no, "harvest", d[0], d[1], [delta])
		quick_print("run=" + str(run_no) + " delta=" + str(delta))
		return delta

	d = work_end(s)
	stat_add(run_no, "harvest_try", d[0], d[1], [0])
	return 0


def do_one_run(run_no):
	quick_print("run=" + str(run_no) + " phase=seed")
	seed_parallel(run_no)

	quick_print("run=" + str(run_no) + " phase=ready")
	if not ready_parallel(run_no):
		quick_print("run=" + str(run_no) + " grow")
		return False

	log_rows("ready", run_no)

	quick_print("run=" + str(run_no) + " phase=sort")
	burst_once(run_no)

	delta = try_harvest(run_no)

	log_rows("after sort", run_no)

	if delta > 0:
		quick_print("run=" + str(run_no) + " harvest")
		return True

	quick_print("run=" + str(run_no) + " harvest failed")
	return False


def run_test():
	set_world_size(SIZE)
	clear()
	stat_reset()

	if max_drones() < 2:
		quick_print("need 2 total")
		return

	run_no = 1
	while run_no <= RUNS:
		ok = False

		while not ok:
			ok = do_one_run(run_no)

		run_no = run_no + 1

	stat_dump()


run_test()