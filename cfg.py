GOAL_TARGETS = {
	Items.Hay: 20000,
	Items.Wood: 20000,
	Items.Carrot: 50000,
	Items.Pumpkin: 20000,
	Items.Cactus: 5000,
	Items.Bone: 20000,
}

GOAL_WEIGHTS = {
	Items.Hay: 1,
	Items.Wood: 1,
	Items.Carrot: 2,
	Items.Pumpkin: 4,
	Items.Cactus: 6,
	Items.Bone: 8,
}

BASELINE_RESERVE = {
	Items.Hay: 2000,
	Items.Wood: 2000,
	Items.Carrot: 2000,
	Items.Pumpkin: 0,
	Items.Cactus: 0,
	Items.Bone: 0,
}

ZONE_MIN_SIZE = 4
FULL_FIELD_SPECIAL_RATIO = 0.95

PUMPKIN_MIN_HAY = 2500
PUMPKIN_MIN_WOOD = 2500
PUMPKIN_MIN_CARROT = 1200
CACTUS_MIN_PUMPKIN = 5000
DINOSAUR_MIN_CACTUS = 2000

ENABLE_AUTO_UNLOCK = False
ENABLE_BONE_MODE = True

# Polyculture layer is optional. Keep disabled until rules are validated in game.
ENABLE_POLYCULTURE = False
POLYCULTURE_PRIMARY_MIN_RATIO = 0.45
POLYCULTURE_ALLOWED_CROPS = [
	"carrot",
	"pumpkin",
	"wood",
]

# Megafarm hooks are optional. Scheduler falls back to 1 drone if these APIs are absent.
ENABLE_MULTI_DRONE = False
MEGAFARM_ASSIGNMENT_MODE = "round_robin"   # round_robin | by_priority
MEGAFARM_MAX_DRONES = 16

# Ordered by practical progression. Remove or reorder freely.
UNLOCK_SEQUENCE = [
	("Speed", None),
	("Expand", None),
	("Plant", None),
	("Senses", None),
	("Grass", None),
	("Debug", None),
	("Operators", None),
	("Carrots", None),
	("Watering", None),
	("Trees", None),
	("Sunflowers", None),
	("Variables", None),
	("Functions", None),
	("Import", None),
	("Pumpkins", None),
	("Lists", None),
	("Utilities", None),
	("Timing", None),
	("Dictionaries", None),
	("Costs", None),
	("Fertilizer", None),
	("Mazes", None),
	("Polyculture", None),
	("Auto_Unlock", None),
	("Cactus", None),
	("Debug_2", None),
	("Simulation", None),
	("Megafarm", None),
	("Dinosaurs", None),
]

DEBUG = True
