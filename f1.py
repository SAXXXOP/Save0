# cactus_2band_try.py
# 目的:
# - 本体は「横の蛇行ソート」
# - 追加droneは「2列帯を1本の蛇行パスとしてソート」
# - 2列帯は (0,1) -> (1,2) -> (2,3) ... と1列重ねで右へ進む
#
# これはまず動きを見るための試作版です。
# 横は通常の蛇行、縦1列ソートは使わず、band だけ新設しています。

SIZE = 10
BURST_PASSES = 6
RUNS = 3

# =========================
# 基本移動
# =========================

def move_steps(d, n):
	for _ in range(n):
		move(d)

def move_to(x, y):
	cx = get_pos_x()
	cy = get_pos_y()

	if cx < x:
		move_steps(East, x - cx)
	elif cx > x:
		move_steps(West, cx - x)

	if cy < y:
		move_steps(North, y - cy)
	elif cy > y:
		move_steps(South, cy - y)

def home():
	move_to(0, 0)

# =========================
# seed / ready
# =========================

def seed_parallel():
	# 必要に応じてここは手元の成功版に差し替え
	# とりあえず全面に cactus を植えるだけの簡易版
	for y in range(SIZE):
		if y % 2 == 0:
			for x in range(SIZE):
				move_to(x, y)
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
		else:
			for x in range(SIZE - 1, -1, -1):
				move_to(x, y)
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
	home()

def ready_parallel():
	# 成熟待ちの詳細は手元の成功版があるならそちら優先
	# ここでは全マスが収穫可能になるまで待つ簡易版
	while True:
		ok = True
		for y in range(SIZE):
			for x in range(SIZE):
				move_to(x, y)
				if not can_harvest():
					ok = False
		if ok:
			break
	home()

# =========================
# 比較・交換
# =========================

def swap_if_gt(d):
	a = measure()
	swap(d)
	b = measure()

	# swap後に今マスへ来た値が b、隣へ行った値が a の想定で判定
	# 逆だったら戻す
	if b > a:
		swap(d)
		return 0
	return 1

# =========================
# 横の成功イメージに寄せた蛇行
# 「1行をならす -> 1行上がる -> 逆向きでならす」
# =========================

def h_sweep_once():
	changed = 0

	for y in range(SIZE):
		if y % 2 == 0:
			move_to(0, y)
			for x in range(SIZE - 1):
				changed += swap_if_gt(East)
				if x < SIZE - 2:
					move(East)
		else:
			move_to(SIZE - 1, y)
			for x in range(SIZE - 1):
				changed += swap_if_gt(West)
				if x < SIZE - 2:
					move(West)

	home()
	return changed

def h_worker(passes):
	total = 0
	for _ in range(passes):
		total += h_sweep_once()
	return total

# =========================
# 2列帯の蛇行パス
#
# 偶数行:
#   (x0,y)   -> (x0+1,y) -> (x0+1,y+1)
# 奇数行:
#   (x0+1,y) -> (x0,y)   -> (x0,y+1)
#
# これで
# (x0,0) -> (x0+1,0) -> (x0+1,1) -> (x0,1) -> (x0,2) -> (x0+1,2) ...
# の1本の経路になる
# =========================

def pair_band_once(x0):
	changed = 0

	for y in range(SIZE):
		if y % 2 == 0:
			# (x0,y) -> (x0+1,y)
			move_to(x0, y)
			changed += swap_if_gt(East)

			# (x0+1,y) -> (x0+1,y+1)
			if y < SIZE - 1:
				move_to(x0 + 1, y)
				changed += swap_if_gt(North)

		else:
			# (x0+1,y) -> (x0,y)
			move_to(x0 + 1, y)
			changed += swap_if_gt(West)

			# (x0,y) -> (x0,y+1)
			if y < SIZE - 1:
				move_to(x0, y)
				changed += swap_if_gt(North)

	home()
	return changed

def band_sweep_once():
	changed = 0
	for x0 in range(SIZE - 1):
		changed += pair_band_once(x0)
	return changed

def band_worker(passes):
	total = 0
	for _ in range(passes):
		total += band_sweep_once()
	return total

# =========================
# 全面 sorted 判定
# 行優先の単純判定
# まずは harvest 前の安全確認用
# =========================

def is_sorted_all():
	prev = None

	for y in range(SIZE):
		for x in range(SIZE):
			move_to(x, y)
			v = measure()

			if prev != None:
				if prev > v:
					home()
					return False

			prev = v

	home()
	return True

def try_harvest():
	if not is_sorted_all():
		return 0

	move_to(0, 0)
	if can_harvest():
		harvest()
		home()
		return 1

	home()
	return 0

# =========================
# burst
# 本体: 横
# drone: 2列帯
# =========================

def burst_once():
	if num_drones() < max_drones():
		spawn_drone(band_worker, BURST_PASSES)

	h_worker(BURST_PASSES)

	# 環境によって wait_for / has_finished の使い分けが必要ならここ調整
	wait_for(has_finished)

	return try_harvest()

# =========================
# run
# =========================

def one_run():
	seed_parallel()
	ready_parallel()

	steps = 0
	while True:
		steps += 1
		if burst_once():
			return steps

def main():
	for r in range(RUNS):
		clear()
		steps = one_run()
		quick_print("run=", r + 1, " steps=", steps)

main()