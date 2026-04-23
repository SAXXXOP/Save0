import cfg


def pump_ok(inv):
	if inv[Items.Hay] < cfg.P_HAY:
		return False
	if inv[Items.Wood] < cfg.P_WOOD:
		return False
	if inv[Items.Carrot] < cfg.P_CARROT:
		return False
	return True


def cactus_ok(inv):
	if inv[Items.Pumpkin] < cfg.C_PUMPKIN:
		return False
	return True


def dino_ok(inv):
	if inv[Items.Cactus] < cfg.D_CACTUS:
		return False
	return True


def score(inv, weighted_missing, baseline_gap, unlock_info):
	out = {}

	for item in weighted_missing:
		out[item] = weighted_missing[item]

	for item in baseline_gap:
		if item in out:
			out[item] = out[item] + baseline_gap[item] * 10
		else:
			out[item] = baseline_gap[item] * 10

	cost = unlock_info["cost"]
	for item in cost:
		need = cost[item] - inv[item]
		if need > 0:
			if item in out:
				out[item] = out[item] + need * 20
			else:
				out[item] = need * 20

	if not pump_ok(inv):
		out[Items.Pumpkin] = 0
	if not cactus_ok(inv):
		out[Items.Cactus] = 0
	if not dino_ok(inv):
		out[Items.Bone] = 0

	return out


def crop_of(item):
	if item == Items.Hay:
		return "hay"
	if item == Items.Wood:
		return "wood"
	if item == Items.Carrot:
		return "carrot"
	if item == Items.Pumpkin:
		return "pumpkin"
	if item == Items.Cactus:
		return "cactus"
	if item == Items.Bone:
		return "dino"
	return "hay"


def top3(score_map):
	arr = []
	for item in score_map:
		val = score_map[item]
		if val > 0:
			arr.append([item, val])

	n = len(arr)
	i = 0
	while i < n:
		j = i + 1
		while j < n:
			if arr[j][1] > arr[i][1]:
				tmp = arr[i]
				arr[i] = arr[j]
				arr[j] = tmp
			j = j + 1
		i = i + 1

	out = []
	i = 0
	while i < len(arr) and i < 3:
		out.append(arr[i])
		i = i + 1
	return out


def zones(inv, score_map):
	size = get_world_size()
	picks = top3(score_map)

	if len(picks) == 0:
		return [{"crop": "hay", "x": 0, "y": 0, "w": size, "h": size}]

	total = 0
	i = 0
	while i < len(picks):
		total = total + picks[i][1]
		i = i + 1

	out = []
	x0 = 0
	remain = size
	i = 0
	while i < len(picks):
		item = picks[i][0]
		val = picks[i][1]

		if i == len(picks) - 1:
			width = remain
		else:
			width = size * val // total
			if width < cfg.ZONE_MIN:
				width = cfg.ZONE_MIN
			if width > remain:
				width = remain

		out.append({
			"crop": crop_of(item),
			"x": x0,
			"y": 0,
			"w": width,
			"h": size,
		})
		x0 = x0 + width
		remain = remain - width
		if remain <= 0:
			break
		i = i + 1

	return out
	