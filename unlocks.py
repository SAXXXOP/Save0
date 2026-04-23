def target(inv):
	return {
		"target": None,
		"level": None,
		"cost": {},
	}


def can_do(info, inv):
	tgt = info["target"]
	if tgt == None:
		return False

	cost = info["cost"]
	for item in cost:
		if inv[item] < cost[item]:
			return False
	return True


def do_it(info):
	tgt = info["target"]
	lvl = info["level"]
	if tgt == None:
		return
	if lvl == None:
		unlock(tgt)
	else:
		unlock(tgt, lvl)
		