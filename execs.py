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