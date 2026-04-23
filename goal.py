import cfg


def snap():
	return {
		Items.Hay: num_items(Items.Hay),
		Items.Wood: num_items(Items.Wood),
		Items.Carrot: num_items(Items.Carrot),
		Items.Pumpkin: num_items(Items.Pumpkin),
		Items.Cactus: num_items(Items.Cactus),
		Items.Bone: num_items(Items.Bone),
		Items.Power: num_items(Items.Power),
		Items.Gold: num_items(Items.Gold),
		Items.Fertilizer: num_items(Items.Fertilizer),
	}


def missing(inv):
	out = {}
	for item in cfg.GOALS:
		want = cfg.GOALS[item]
		have = inv[item]
		diff = want - have
		if diff > 0:
			out[item] = diff
	return out


def weighted(inv):
	raw = missing(inv)
	out = {}
	for item in raw:
		w = 1
		if item in cfg.WEIGHTS:
			w = cfg.WEIGHTS[item]
		out[item] = raw[item] * w
	return out


def baseline(inv):
	out = {}
	for item in cfg.BASE:
		diff = cfg.BASE[item] - inv[item]
		if diff > 0:
			out[item] = diff
	return out
	