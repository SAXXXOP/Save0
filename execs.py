import util

carrot_dbg = 0
wood_dbg = 0


def soil_if_needed():
	if get_ground_type() != Grounds.Soil:
		till()


def hay_tile(x, y):
	if can_harvest():
		harvest()


def wood_tile(x, y):
	t = get_entity_type()

	# 木は全面植えせずチェッカーボード配置
	if (x + y) % 2 == 0:
		if t == Entities.Tree:
			if can_harvest():
				harvest()
				plant(Entities.Tree)
			return

		if t != None:
			harvest()

		plant(Entities.Tree)
		return

	# 空けるマス
	if t != None:
		harvest()


def carrot_tile(x, y):
	t = get_entity_type()

	if t == Entities.Carrot:
		if can_harvest():
			harvest()
			soil_if_needed()
			plant(Entities.Carrot)
		return

	if t != None:
		harvest()

	soil_if_needed()
	plant(Entities.Carrot)


def cactus_seed_zone(x0, y0, w, h):
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


def cactus_all_ready(x0, y0, w, h):
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


def cactus_sweep_once(x0, y0, w, h):
	util.go_to(x0, y0)
	changed = False

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				a = measure()

				if x < w - 1:
					b = measure(East)
					if a != None and b != None:
						if a > b:
							swap(East)
							changed = True

				if y < h - 1:
					c = measure(North)
					if a != None and c != None:
						if a > c:
							swap(North)
							changed = True

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				a = measure()

				if x > 0:
					move(West)
					b = measure()
					move(East)
					if a != None and b != None:
						if b > a:
							swap(West)
							changed = True

				if y < h - 1:
					c = measure(North)
					if a != None and c != None:
						if a > c:
							swap(North)
							changed = True

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1

	return changed


def run_cactus_zone(zone):
	x0 = zone["x"]
	y0 = zone["y"]
	w = zone["w"]
	h = zone["h"]

	cactus_seed_zone(x0, y0, w, h)

	if not cactus_all_ready(x0, y0, w, h):
		return

	limit = w * h * 4
	n = 0
	while n < limit:
		if not cactus_sweep_once(x0, y0, w, h):
			break
		n = n + 1

	util.go_to(x0, y0)
	if can_harvest():
		harvest()


def pumpkin_seed_zone(x0, y0, w, h):
	util.go_to(x0, y0)
	changed = False

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				t = get_entity_type()

				if t == Entities.Pumpkin:
					pass
				elif t == Entities.Dead_Pumpkin:
					harvest()
					soil_if_needed()
					plant(Entities.Pumpkin)
					changed = True
				else:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Pumpkin)
					changed = True

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				t = get_entity_type()

				if t == Entities.Pumpkin:
					pass
				elif t == Entities.Dead_Pumpkin:
					harvest()
					soil_if_needed()
					plant(Entities.Pumpkin)
					changed = True
				else:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Pumpkin)
					changed = True

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1

	return changed


def pumpkin_ready_count(x0, y0, w, h):
	util.go_to(x0, y0)

	ready = 0
	total = w * h

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				t = get_entity_type()

				if t == Entities.Dead_Pumpkin:
					return -1
				if t != Entities.Pumpkin:
					return -1
				if can_harvest():
					ready = ready + 1

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				t = get_entity_type()

				if t == Entities.Dead_Pumpkin:
					return -1
				if t != Entities.Pumpkin:
					return -1
				if can_harvest():
					ready = ready + 1

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1

	if ready == total:
		return ready

	return 0


def harvest_pumpkin_zone(x0, y0, w, h):
	util.go_to(x0, y0)

	y = 0
	while y < h:
		if y % 2 == 0:
			x = 0
			while x < w:
				if get_entity_type() != None:
					harvest()

				if x < w - 1:
					move(East)
				x = x + 1
		else:
			x = w - 1
			while x >= 0:
				if get_entity_type() != None:
					harvest()

				if x > 0:
					move(West)
				x = x - 1

		if y < h - 1:
			move(North)
		y = y + 1


def run_pumpkin_zone(zone):
	x0 = zone["x"]
	y0 = zone["y"]
	w = zone["w"]
	h = zone["h"]

	if pumpkin_seed_zone(x0, y0, w, h):
		return

	state = pumpkin_ready_count(x0, y0, w, h)

	if state == -1:
		pumpkin_seed_zone(x0, y0, w, h)
		return

	if state > 0:
		harvest_pumpkin_zone(x0, y0, w, h)
		return


def dino_tile(x, y):
	t = get_entity_type()

	if t == Entities.Dinosaur:
		if can_harvest():
			harvest()
		return

	if t != None:
		harvest()

	plant(Entities.Dinosaur)


# =========================
# maze
# 最初は全面 maze 専用。
# zone の x,y,w,h は使わず、原点起点の full-field で回す。
# =========================

def maze_go_to(tx, ty):
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
	maze_go_to(0, 0)

	t = get_entity_type()
	if t != None and t != Entities.Bush:
		harvest()

	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)


def grow_maze_once():
	maze_go_to(0, 0)

	need = maze_substance_needed()
	if need <= 0:
		return False

	if num_items(Items.Weird_Substance) < need:
		return False

	ensure_bush_at_origin()
	return use_item(Items.Weird_Substance, need)


def read_treasure_pos():
	pos = measure()
	if pos == None:
		return None
	return pos


def maze_pos_key(x, y):
	return str(x) + "," + str(y)


def maze_abs(v):
	if v < 0:
		return -v
	return v


def maze_next_pos(x, y, d):
	if d == North:
		return [x, y + 1]
	if d == South:
		return [x, y - 1]
	if d == East:
		return [x + 1, y]
	return [x - 1, y]


def maze_dir_between(x1, y1, x2, y2):
	if x2 == x1 and y2 == y1 + 1:
		return North
	if x2 == x1 and y2 == y1 - 1:
		return South
	if x2 == x1 + 1 and y2 == y1:
		return East
	if x2 == x1 - 1 and y2 == y1:
		return West
	return None


def maze_dir_priority(tx, ty):
	x = get_pos_x()
	y = get_pos_y()

	dx = tx - x
	dy = ty - y

	order = []

	if maze_abs(dx) >= maze_abs(dy):
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


def choose_next_maze_dir(tx, ty, visited):
	x = get_pos_x()
	y = get_pos_y()

	order = maze_dir_priority(tx, ty)

	best_dir = None
	best_score = 999999

	i = 0
	while i < len(order):
		d = order[i]

		if can_move(d):
			p = maze_next_pos(x, y, d)
			nx = p[0]
			ny = p[1]
			k = maze_pos_key(nx, ny)

			if not (k in visited):
				score = maze_abs(tx - nx) + maze_abs(ty - ny)

				if score < best_score:
					best_score = score
					best_dir = d

		i = i + 1

	return best_dir


def solve_maze_targeted_walk():
	target = read_treasure_pos()
	if target == None:
		return False

	tx = target[0]
	ty = target[1]

	visited = {}
	parent = {}

	x = get_pos_x()
	y = get_pos_y()

	visited[maze_pos_key(x, y)] = 1
	parent[maze_pos_key(x, y)] = None

	limit = get_world_size() * get_world_size() * 20
	steps = 0

	while steps < limit:
		if get_entity_type() == Entities.Treasure:
			return True

		d = choose_next_maze_dir(tx, ty, visited)

		if d != None:
			cur_x = get_pos_x()
			cur_y = get_pos_y()

			p = maze_next_pos(cur_x, cur_y, d)
			nx = p[0]
			ny = p[1]

			move(d)

			parent[maze_pos_key(nx, ny)] = [cur_x, cur_y]
			visited[maze_pos_key(nx, ny)] = 1
			steps = steps + 1
			continue

		cur_x = get_pos_x()
		cur_y = get_pos_y()
		cur_key = maze_pos_key(cur_x, cur_y)

		prev = parent[cur_key]
		if prev == None:
			break

		back = maze_dir_between(cur_x, cur_y, prev[0], prev[1])
		if back == None:
			return False

		move(back)
		steps = steps + 1

	return get_entity_type() == Entities.Treasure


def run_maze_zone(zone):
	# 最初は full-field 専用
	if num_unlocked(Unlocks.Mazes) <= 0:
		return

	if not grow_maze_once():
		return

	if not solve_maze_targeted_walk():
		return

	if get_entity_type() == Entities.Treasure:
		harvest()


def run_zone(zone):
	crop = zone["crop"]
	x = zone["x"]
	y = zone["y"]
	w = zone["w"]
	h = zone["h"]

	if crop == "hay":
		util.run_rect(x, y, w, h, hay_tile)
		return
	if crop == "wood":
		util.run_rect(x, y, w, h, wood_tile)
		return
	if crop == "carrot":
		util.run_rect(x, y, w, h, carrot_tile)
		return
	if crop == "pumpkin":
		run_pumpkin_zone(zone)
		return
	if crop == "cactus":
		run_cactus_zone(zone)
		return
	if crop == "dino":
		util.run_rect(x, y, w, h, dino_tile)
		return
	if crop == "maze":
		run_maze_zone(zone)
		return

	util.run_rect(x, y, w, h, hay_tile)