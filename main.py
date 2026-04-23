import cfg
import util
import goal
import unlocks
import planner
import execs


def tick():
	inv = goal.snap()
	info = unlocks.target(inv)

	if cfg.AUTO_UNLOCK:
		if unlocks.can_do(info, inv):
			unlocks.do_it(info)
			return

	wm = goal.weighted(inv)
	bg = goal.baseline(inv)
	sc = planner.score(inv, wm, bg, info)
	zs = planner.zones(inv, sc)

	if cfg.DEBUG:
		util.log("zones=" + str(len(zs)))

	i = 0
	while i < len(zs):
		execs.run_zone(zs[i])
		i = i + 1


while True:
	tick()
	