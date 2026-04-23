import util

SIZE = 8
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


def maze_substance_needed():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level <= 0:
		return 0
	return get_world_size() * 2 ** (maze_level - 1)


def ensure_bush_at_origin():
	util.go_to(0, 0)

	t = get_entity_type()
	if t != None and t != Entities.Bush:
		harvest()

	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)


def grow_maze_once(run_no):
	util.go_to(0, 0)

	need = maze_substance_needed()
	before_ws = num_items(Items.Weird_Substance)
	before_t = get_entity_type()

	ensure_bush_at_origin()

	made = False
	if need > 0 and before_ws >= need:
		made = use_item(Items.Weird_Substance, need)

	after_ws = num_items(Items.Weird_Substance)
	after_t = get_entity_type()

	quick_print(
		"run=" + str(run_no) +
		" need=" + str(need) +
		" ws_before=" + str(before_ws) +
		" ws_after=" + str(after_ws) +
		" t_before=" + str(before_t) +
		" t_after=" + str(after_t) +
		" made=" + str(made)
	)

	return made


def read_treasure_pos():
	pos = measure()
	if pos == None:
		return None
	return pos


def pos_key(x, y):
	return str(x) + "," + str(y)


def dir_between(x1, y1, x2, y2):
	if x2 == x1 and y2 == y1 + 1:
		return North
	if x2 == x1 and y2 == y1 - 1:
		return South
	if x2 == x1 + 1 and y2 == y1:
		return East
	if x2 == x1 - 1 and y2 == y1:
		return West
	return None


def next_pos(x, y, d):
	if d == North:
		return [x, y + 1]
	if d == South:
		return [x, y - 1]
	if d == East:
		return [x + 1, y]
	return [x - 1, y]


def abs_val(v):
	if v < 0:
		return -v
	return v


def dir_priority(tx, ty):
	x = get_pos_x()
	y = get_pos_y()

	dx = tx - x
	dy = ty - y

	order = []

	if abs_val(dx) >= abs_val(dy):
		if dx > 0:
			order.append(East)
		elif dx < 0:
			order.append(West)

		if dy > 0:
			order.append(North)
		elif dy < 0:
			order.append(South)
	else:
		if dy > 0:
			order.append(North)
		elif dy < 0:
			order.append(South)

		if dx > 0:
			order.append(East)
		elif dx < 0:
			order.append(West)

	base = [North, East, South, West]

	i = 0
	while i < len(base):
		d = base[i]

		found = False
		j = 0
		while j < len(order):
			if order[j] == d:
				found = True
				break
			j = j + 1

		if not found:
			order.append(d)

		i = i + 1

	return order


def choose_next_dir(tx, ty, visited):
	x = get_pos_x()
	y = get_pos_y()

	order = dir_priority(tx, ty)

	best_dir = None
	best_score = 999999

	i = 0
	while i < len(order):
		d = order[i]

		if can_move(d):
			p = next_pos(x, y, d)
			nx = p[0]
			ny = p[1]
			k = pos_key(nx, ny)

			if not (k in visited):
				score = abs_val(tx - nx) + abs_val(ty - ny)

				if score < best_score:
					best_score = score
					best_dir = d

		i = i + 1

	return best_dir


def solve_maze_targeted_walk(run_no):
	target = read_treasure_pos()
	if target == None:
		quick_print("run=" + str(run_no) + " no target")
		return -1

	tx = target[0]
	ty = target[1]
	quick_print("run=" + str(run_no) + " target=" + str(target))

	visited = {}
	parent = {}

	x = get_pos_x()
	y = get_pos_y()

	visited[pos_key(x, y)] = 1
	parent[pos_key(x, y)] = None

	steps = 0
	limit = SIZE * SIZE * 20

	while steps < limit:
		if get_entity_type() == Entities.Treasure:
			return steps

		d = choose_next_dir(tx, ty, visited)

		if d != None:
			cur_x = get_pos_x()
			cur_y = get_pos_y()

			p = next_pos(cur_x, cur_y, d)
			nx = p[0]
			ny = p[1]

			move(d)

			parent[pos_key(nx, ny)] = [cur_x, cur_y]
			visited[pos_key(nx, ny)] = 1
			steps = steps + 1
			continue

		cur_x = get_pos_x()
		cur_y = get_pos_y()
		cur_key = pos_key(cur_x, cur_y)

		prev = parent[cur_key]
		if prev == None:
			break

		back = dir_between(cur_x, cur_y, prev[0], prev[1])
		if back == None:
			quick_print("run=" + str(run_no) + " back dir none")
			return -1

		move(back)
		steps = steps + 1

	return -1


def try_harvest_treasure(run_no):
	s = work_start()

	before = num_items(Items.Gold)

	if get_entity_type() == Entities.Treasure:
		harvest()
		after = num_items(Items.Gold)
		d = work_end(s)
		delta = after - before
		stat_add(run_no, "harvest", d[0], d[1], [delta])
		quick_print("run=" + str(run_no) + " gold_delta=" + str(delta))
		return delta

	d = work_end(s)
	stat_add(run_no, "harvest_try", d[0], d[1], [0])
	return 0


def do_one_run(run_no):
	util.go_to(0, 0)

	s = work_start()
	ok = grow_maze_once(run_no)
	d = work_end(s)
	stat_add(run_no, "grow_maze", d[0], d[1], [ok])

	if not ok:
		quick_print("run=" + str(run_no) + " maze grow failed")
		return False

	target = read_treasure_pos()
	quick_print("run=" + str(run_no) + " treasure_pos=" + str(target))

	s = work_start()
	steps = solve_maze_targeted_walk(run_no)
	d = work_end(s)
	stat_add(run_no, "solve_targeted_walk", d[0], d[1], [steps])

	quick_print("run=" + str(run_no) + " solve_steps=" + str(steps))

	if steps < 0:
		quick_print("run=" + str(run_no) + " solve failed")
		return False

	delta = try_harvest_treasure(run_no)
	if delta > 0:
		return True

	quick_print("run=" + str(run_no) + " treasure harvest failed")
	return False


def run_test():
	set_world_size(SIZE)
	clear()
	stat_reset()

	if num_unlocked(Unlocks.Mazes) <= 0:
		quick_print("need mazes unlock")
		return

	need = maze_substance_needed()
	if num_items(Items.Weird_Substance) < need:
		quick_print("need weird_substance=" + str(need))
		return

	run_no = 1
	while run_no <= RUNS:
		clear()

		ok = do_one_run(run_no)
		if ok:
			run_no = run_no + 1

	stat_dump()


run_test()