import util

SIZE = 4
PASS_LIMIT = 32


def soil_if_needed():
	if get_ground_type() != Grounds.Soil:
		till()


def seed_zone():
	util.go_to(0, 0)

	y = 0
	while y < SIZE:
		if y % 2 == 0:
			x = 0
			while x < SIZE:
				t = get_entity_type()
				if t != Entities.Cactus:
					if t != None:
						harvest()
					soil_if_needed()
					plant(Entities.Cactus)

				if x < SIZE - 1:
					move(East)
				x = x + 1
		else:
			x = SIZE - 1
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

		if y < SIZE - 1:
			move(North)
		y = y + 1


def all_ready():
	util.go_to(0, 0)

	y = 0
	while y < SIZE:
		if y % 2 == 0:
			x = 0
			while x < SIZE:
				if get_entity_type() != Entities.Cactus:
					return False
				if not can_harvest():
					return False

				if x < SIZE - 1:
					move(East)
				x = x + 1
		else:
			x = SIZE - 1
			while x >= 0:
				if get_entity_type() != Entities.Cactus:
					return False
				if not can_harvest():
					return False

				if x > 0:
					move(West)
				x = x - 1

		if y < SIZE - 1:
			move(North)
		y = y + 1

	return True


def sweep_up_right():
	util.go_to(0, 0)
	changed = False

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
							changed = True

				if y < SIZE - 1:
					c = measure(North)
					if a != None and c != None:
						if a > c:
							swap(North)
							changed = True

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
							changed = True

				if y < SIZE - 1:
					c = measure(North)
					if a != None and c != None:
						if a > c:
							swap(North)
							changed = True

				if x > 0:
					move(West)
				x = x - 1

		if y < SIZE - 1:
			move(North)
		y = y + 1

	return changed


def harvest_once():
	before = num_items(Items.Cactus)
	util.go_to(0, 0)

	if can_harvest():
		harvest()
		after = num_items(Items.Cactus)
		quick_print("delta=" + str(after - before))
		return True

	return False


def run_test():
	set_world_size(SIZE)
	clear()

	while True:
		seed_zone()

		if not all_ready():
			continue

		n = 0
		while n < PASS_LIMIT:
			if not sweep_up_right():
				break
			n = n + 1

		harvest_once()


run_test()