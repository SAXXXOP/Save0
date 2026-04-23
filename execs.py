import util

carrot_dbg = 0
wood_dbg = 0
pump_dbg = 0
cactus_dbg = 0


def soil_if_needed():
	if get_ground_type() != Grounds.Soil:
		till()


def hay_tile(x, y):
	if can_harvest():
		harvest()


def wood_tile(x, y):
	t = get_entity_type()

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


def seed_pumpkin_zone(x0, y0, w, h):
	util.go_to(x0, y0)
	changed = False

	ry = 0
	while ry < h:
		if ry % 2 == 0:
			rx = 0
			while rx < w:
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

				if rx < w - 1:
					move(East)
				rx = rx + 1
		else:
			rx = w - 1
			while rx >= 0:
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

				if rx > 0:
					move(West)
				rx = rx - 1

		if ry < h - 1:
			move(North)
		ry = ry + 1

	return changed


def pumpkin_ready_count(x0, y0, w, h):
	ready = 0
	total = w * h

	ry = 0
	while ry < h:
		rx = 0
		while rx < w:
			x = x0 + rx
			y = y0 + ry

			util.go_to(x, y)
			t = get_entity_type()

			if t == Entities.Dead_Pumpkin:
				return -1

			if t != Entities.Pumpkin:
				return -1

			if can_harvest():
				ready = ready + 1

			rx = rx + 1
		ry = ry + 1

	if ready == total:
		return ready

	return 0


def harvest_pumpkin_zone(x0, y0, w, h):
	ry = 0
	while ry < h:
		rx = 0
		while rx < w:
			x = x0 + rx
			y = y0 + ry

			util.go_to(x, y)
			if get_entity_type() != None:
				harvest()

			rx = rx + 1
		ry = ry + 1


def run_pumpkin_zone(zone):
	x0 = zone["x"]
	y0 = zone["y"]
	w = zone["w"]
	h = zone["h"]

	if seed_pumpkin_zone(x0, y0, w, h):
		return

	state = pumpkin_ready_count(x0, y0, w, h)

	if state == -1:
		seed_pumpkin_zone(x0, y0, w, h)
		return

	if state > 0:
		harvest_pumpkin_zone(x0, y0, w, h)
		return


def seed_cactus_zone(x0, y0, w, h):
	util.go_to(x0, y0)
	changed = False

	ry = 0
	while ry < h:
		if ry % 2 == 0:
			rx = 0
			while rx < w:
				t = get_entity_type()

				if t == Entities.Cactus:
					pass
				else:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Cactus)
					changed = True

				if rx < w - 1:
					move(East)
				rx = rx + 1
		else:
			rx = w - 1
			while rx >= 0:
				t = get_entity_type()

				if t == Entities.Cactus:
					pass
				else:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Cactus)
					changed = True

				if rx > 0:
					move(West)
				rx = rx - 1

		if ry < h - 1:
			move(North)
		ry = ry + 1

	return changed


def cactus_all_ready(x0, y0, w, h):
	ry = 0
	while ry < h:
		rx = 0
		while rx < w:
			x = x0 + rx
			y = y0 + ry

			util.go_to(x, y)
			t = get_entity_type()

			if t != Entities.Cactus:
				return False

			if not can_harvest():
				return False

			rx = rx + 1
		ry = ry + 1

	return True


def cactus_path(x0, y0, w, h):
	path = []

	ry = 0
	while ry < h:
		if ry % 2 == 0:
			rx = 0
			while rx < w:
				path.append([x0 + rx, y0 + ry])
				rx = rx + 1
		else:
			rx = w - 1
			while rx >= 0:
				path.append([x0 + rx, y0 + ry])
				rx = rx - 1
		ry = ry + 1

	return path


def dir_to_next(x1, y1, x2, y2):
	if x2 == x1 + 1:
		return East
	if x2 == x1 - 1:
		return West
	if y2 == y1 + 1:
		return North
	return South


def bubble_cactus_once(path):
	changed = False
	i = 0

	while i < len(path) - 1:
		x1 = path[i][0]
		y1 = path[i][1]
		x2 = path[i + 1][0]
		y2 = path[i + 1][1]

		util.go_to(x1, y1)

		if get_entity_type() != Entities.Cactus:
			return True
		if not can_harvest():
			return True

		d = dir_to_next(x1, y1, x2, y2)

		a = measure()
		b = measure(d)

		if a == None:
			return True
		if b == None:
			return True

		if a > b:
			swap(d)
			changed = True

		i = i + 1

	return changed


def harvest_sorted_cactus(path):
	if len(path) == 0:
		return

	x = path[0][0]
	y = path[0][1]
	util.go_to(x, y)

	if can_harvest():
		harvest()


def run_cactus_zone(zone):
	x0 = zone["x"]
	y0 = zone["y"]
	w = zone["w"]
	h = zone["h"]

	if seed_cactus_zone(x0, y0, w, h):
		return

	if not cactus_all_ready(x0, y0, w, h):
		return

	path = cactus_path(x0, y0, w, h)

	if bubble_cactus_once(path):
		return

	harvest_sorted_cactus(path)


def dino_tile(x, y):
	t = get_entity_type()

	if t == Entities.Dinosaur:
		if can_harvest():
			harvest()
		return

	if t != None:
		harvest()

	plant(Entities.Dinosaur)


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

	util.run_rect(x, y, w, h, hay_tile)

def zone_each(x0, y0, w, h, cb):
	util.go_to(x0, y0)

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