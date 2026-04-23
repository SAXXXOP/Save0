SIZE = 16
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


def maze_substance_needed():
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level <= 0:
		return 0
	return get_world_size() * 2 ** (maze_level - 1)


def ensure_bush_at_origin():
	go_to(0, 0)

	t = get_entity_type()
	if t != None and t != Entities.Bush:
		harvest()

	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)


def grow_maze_once(run_no):
	go_to(0, 0)

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


def abs_val(v):
	if v < 0:
		return -v
	return v


def next_pos(x, y, d):
	if d == North:
		return [x, y + 1]
	if d == South:
		return [x, y - 1]
	if d == East:
		return [x + 1, y]
	return [x - 1, y]


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


def target_score(nx, ny, tx, ty):
	return abs_val(tx - nx) + abs_val(ty - ny)


def dir_index(d):
	if d == North:
		return 0
	if d == East:
		return 1
	if d == South:
		return 2
	return 3


def ordered_dirs_toward_target(tx, ty):
	x = get_pos_x()
	y = get_pos_y()

	base = [North, East, South, West]
	best = []

	i = 0
	while i < len(base):
		d = base[i]
		if can_move(d):
			p = next_pos(x, y, d)
			nx = p[0]
			ny = p[1]
			best.append([d, target_score(nx, ny, tx, ty), dir_index(d)])
		i = i + 1

	i = 0
	while i < len(best):
		j = i + 1
		while j < len(best):
			if best[j][1] < best[i][1]:
				tmp = best[i]
				best[i] = best[j]
				best[j] = tmp
			elif best[j][1] == best[i][1]:
				if best[j][2] < best[i][2]:
					tmp = best[i]
					best[i] = best[j]
					best[j] = tmp
			j = j + 1
		i = i + 1

	out = []
	i = 0
	while i < len(best):
		out.append(best[i][0])
		i = i + 1

	return out


def choose_unvisited_dir(tx, ty, visited):
	x = get_pos_x()
	y = get_pos_y()

	order = ordered_dirs_toward_target(tx, ty)

	i = 0
	while i < len(order):
		d = order[i]
		p = next_pos(x, y, d)
		nx = p[0]
		ny = p[1]
		k = pos_key(nx, ny)

		if not (k in visited):
			return d

		i = i + 1

	return None


def solve_maze_parent_walk(run_no):
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
	k = pos_key(x, y)

	visited[k] = 1
	parent[k] = None

	steps = 0
	limit = SIZE * SIZE * 30
	backtracks = 0

	while steps < limit:
		if get_entity_type() == Entities.Treasure:
			quick_print("run=" + str(run_no) + " backtracks=" + str(backtracks))
			return steps

		d = choose_unvisited_dir(tx, ty, visited)

		if d != None:
			cur_x = get_pos_x()
			cur_y = get_pos_y()

			p = next_pos(cur_x, cur_y, d)
			nx = p[0]
			ny = p[1]
			nk = pos_key(nx, ny)

			move(d)
			visited[nk] = 1
			parent[nk] = [cur_x, cur_y]
			steps = steps + 1
			continue

		cur_x = get_pos_x()
		cur_y = get_pos_y()
		cur_k = pos_key(cur_x, cur_y)

		prev = parent[cur_k]
		if prev == None:
			break

		back = dir_between(cur_x, cur_y, prev[0], prev[1])
		if back == None:
			quick_print("run=" + str(run_no) + " back dir none")
			return -1

		move(back)
		steps = steps + 1
		backtracks = backtracks + 1

	quick_print("run=" + str(run_no) + " backtracks=" + str(backtracks))
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
	go_to(0, 0)

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
	steps = solve_maze_parent_walk(run_no)
	d = work_end(s)
	stat_add(run_no, "solve_parent_walk", d[0], d[1], [steps])

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