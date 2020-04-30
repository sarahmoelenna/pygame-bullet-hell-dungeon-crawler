from typing import Dict, List, Tuple
from level.tileset_loader import TileTypeEnum, DecoratorEnum
from level.tileset_loader import TileSet, DecoratorType
from random import randrange, shuffle
from enum import Enum
from itertools import combinations
from uuid import uuid4
from registries.collision_registry import Collidable, CollisionObject
from copy import copy

class DirectionEnum(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Decoration(Collidable):
	
	def __init__(self, x_pos: int, y_pos: int, type: DecoratorType, out_of_bounds: bool = False):
		self.id = str(uuid4())
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.type = type
		self.out_of_bounds = out_of_bounds

	def is_adjacent_to_position(self, x_pos_in: int, y_pos_in: int) -> bool:
		if self.x_pos - 1 == x_pos_in and self.y_pos == y_pos_in:
			return True
		if self.x_pos + 1 == x_pos_in and self.y_pos == y_pos_in:
			return True
		if self.x_pos + 1 == x_pos_in and self.y_pos + 1 == y_pos_in:
			return True
		if self.x_pos + 1 == x_pos_in and self.y_pos - 1 == y_pos_in:
			return True
		if self.x_pos - 1 == x_pos_in and self.y_pos + 1 == y_pos_in:
			return True
		if self.x_pos - 1 == x_pos_in and self.y_pos - 1 == y_pos_in:
			return True
		if self.x_pos == x_pos_in and self.y_pos + 1 == y_pos_in:
			return True
		if self.x_pos == x_pos_in and self.y_pos - 1 == y_pos_in:
			return True
		return False

	def render(self, x_pos: int, y_pos: int, zoom_level: int, surface):

		self.type.render(self.x_pos * zoom_level - x_pos, self.y_pos * zoom_level - y_pos, zoom_level, surface)

	def get_collision_objects(self) -> CollisionObject:
		collision_objects = self.type.get_collision_objects()
		adjusted_collison_objects = []
		for collision_object in collision_objects:
			collision_object = copy(collision_object)
			collision_object.x_pos = collision_object.x_pos + self.x_pos
			collision_object.y_pos = collision_object.y_pos + self.y_pos
			adjusted_collison_objects.append(collision_object)
		return adjusted_collison_objects

class GridRegion():

	def __init__(self, tile_positions: List[Dict], tile_type: TileTypeEnum):
		self.tile_positions = tile_positions
		self.tile_type = tile_type
		self.size = len(tile_positions)

	
	def replace_tiles(self, grid: Dict, replacement_tile_type: TileTypeEnum):
		for item in self.tile_positions:
			grid[item["x"]][item["y"]] = GridGenerator.tileset.get_tile_for_type(replacement_tile_type)

	def add_to_collision_grid(collision_grid: Dict):
		for item in self.tile_positions:
			collision_grid[item["x"]][item["y"]] = 1

	def is_region_touching_edge(self, grid: Dict):
		lowest_x = 0
		lowest_y = 0
		highest_x = grid["width"] - 1
		highest_y = grid["height"] - 1

		for item in self.tile_positions:
			if item["x"] == lowest_x or item["x"] == highest_x:
				return True
			if item["y"] == lowest_y or item["y"] == highest_y:
				return True
		
		return False

class GridGenerator():

	def __init__(self, width: int, height: int, tileset: TileSet):

		GridGenerator.tileset = tileset
		self.decorations = []

		self.grid = {}
		self.grid['width'] = width
		self.grid['height'] = height
		for x in range(0, width):
			self.grid[x] = {}
			for y in range(0, height):
				self.grid[x][y] = GridGenerator.tileset.get_tile_for_type(TileTypeEnum.BLANK)

		self.collision_grid = {}
		self.collision_grid['width'] = width
		self.collision_grid['height'] = height
		for x in range(0, width):
			self.collision_grid[x] = {}
			for y in range(0, height):
				self.collision_grid[x][y] = 0

	def generate_grid(self) -> Tuple[Dict, Dict, List[Decoration]]:
		raise NotImplementedError("generate_grid must be implemented")

	tileset = None

class MazeGenerator(GridGenerator):
	def __init__(self, width: int, height: int, tileset: TileSet):

		super().__init__(int(width/2), int(height/2), tileset)

	def generate_grid(self)-> Tuple[Dict, Dict, List[Decoration]]:

		line_grid_edge(self.grid, TileTypeEnum.BlueTile, 5)
		generate_maze(self.grid, TileTypeEnum.BLANK, TileTypeEnum.STONE_TILES, 5)
		replace_type(self.grid, TileTypeEnum.BlueTile, TileTypeEnum.BLANK)
		bridge_gaps(self.grid, TileTypeEnum.BLANK, TileTypeEnum.STONE_TILES, TileTypeEnum.STONE_TILES, 5, 0.5)
		trim_edges(self.grid, TileTypeEnum.STONE_TILES, TileTypeEnum.BLANK, 1, 50)
		self.grid, self.collision_grid = scale_grid_up(self.grid, self.collision_grid, 2)

		regions: List[Region] = get_grid_regions(self.grid, TileTypeEnum.BLANK)
		regions_to_fill = get_regions_grid_percentage(self.grid, regions, 20, True)

		for item in regions_to_fill:
			item.replace_tiles(self.grid, TileTypeEnum.NEON_TILE)

		add_rim_to_tile_type(self.grid, TileTypeEnum.STONE_TILES, TileTypeEnum.WALL_TILE, TileTypeEnum.BLANK)

		add_rim_to_tile_type(self.grid, TileTypeEnum.WALL_TILE, TileTypeEnum.STONE_FLOOR, TileTypeEnum.BLANK)
		add_rim_to_tile_type(self.grid, TileTypeEnum.STONE_FLOOR, TileTypeEnum.STONE_FLOOR, TileTypeEnum.BLANK)
		add_rim_to_tile_type(self.grid, TileTypeEnum.STONE_FLOOR, TileTypeEnum.STONE_FLOOR, TileTypeEnum.BLANK)

		replace_type(self.grid, TileTypeEnum.BLANK, TileTypeEnum.SNOW_FLOOR)

		snow_regions = get_grid_regions(self.grid, TileTypeEnum.SNOW_FLOOR)
		exterior_snow_regions, interior_snow_regions = split_by_exterior_and_interior_regions(self.grid, snow_regions)
		for snow_region in exterior_snow_regions:
			self.decorations.extend(
				decorate_region_with_decoration_at_sparsity_percentage(snow_region, DecoratorEnum.TREE, 25, True, False)
			)

		for snow_region in interior_snow_regions:
			self.decorations.extend(
				decorate_region_with_decoration_at_sparsity_percentage(snow_region, DecoratorEnum.TREE, 5, True, False)
			)

		GridGenerator.tileset = None

		add_tile_types_to_collision_grid(self.grid, self.collision_grid, [TileTypeEnum.WALL_TILE, TileTypeEnum.STONE_FLOOR])

		return self.grid, self.collision_grid, self.decorations


def add_tile_types_to_collision_grid(grid: Dict, collision_grid: Dict, tile_types: List[TileTypeEnum]):
	for x in range(grid["width"]):
		for y in range(grid["height"]):
			if grid[x][y].tile_type in tile_types:
				collision_grid[x][y] = 1


def decorate_region_with_decoration_at_sparsity_percentage(region: GridRegion, decoration_type: DecoratorEnum, sparsity_percentage: float, out_of_counds_decorations: bool = False, leave_space: bool = False) -> List[Decoration]:
	if sparsity_percentage < 0 or sparsity_percentage > 100:
		raise ValueError("sparsity_percentage must be between 0 and 100. provided: " + str(sparsity_percentage))

	decorations: List[Decoration] = []
	potential_placements = region.tile_positions

	size_goal = len(region.tile_positions) * sparsity_percentage / 100
	decoration_completed = False
	while decoration_completed is False:
		positions_to_remove = []

		for tile_position in potential_placements:
			chance = randrange(0, 100000) / 1000
			if chance <= 0.5:
				can_place = True
				if leave_space == True:
					for decoration in decorations:
						if decoration.is_adjacent_to_position(tile_position["x"], tile_position["y"]):
							can_place = False
							break
				if can_place:
					decorations.append(
						Decoration(
							tile_position["x"],
							tile_position["y"],
							GridGenerator.tileset.get_decorator_for_type(decoration_type),
							out_of_counds_decorations
						)
					)
				positions_to_remove.append(tile_position)

		for position_to_remove in positions_to_remove:
			potential_placements.remove(position_to_remove)

		if len(potential_placements) == 0 or len(decorations) > size_goal:
			decoration_completed = True

	return decorations


def add_rim_to_tile_type(grid: Dict, tile_type_to_rim: TileTypeEnum, rim_tile_type: TileTypeEnum, tile_type_to_replace: TileTypeEnum):
	tiles_to_rim = []

	for x in range(0, grid["width"]):
		for y in range(0, grid["height"]):
			if grid[x][y].tile_type == tile_type_to_rim:

				if x - 1 >= 0:
					if tile_type_to_replace is None or grid[x - 1][y].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x - 1, "y": y})

				if x - 1 >= 0 and y - 1 >= 0:
					if tile_type_to_replace is None or grid[x - 1][y - 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x - 1, "y": y - 1})

				if y - 1 >= 0:
					if tile_type_to_replace is None or grid[x][y - 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x, "y": y - 1})

				if x + 1 < grid["width"]:
					if tile_type_to_replace is None or grid[x + 1][y].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x + 1, "y": y})

				if x + 1 < grid["width"] and y + 1 < grid["height"]:
					if tile_type_to_replace is None or grid[x + 1][y + 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x + 1, "y": y + 1})

				if y + 1 < grid["height"]:
					if tile_type_to_replace is None or grid[x][y + 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x, "y": y + 1})

				if x + 1 < grid["width"] and y - 1 >= 0:
					if tile_type_to_replace is None or grid[x + 1][y - 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x + 1, "y": y - 1})

				if x - 1 >= 0 and y + 1 < grid["height"]:
					if tile_type_to_replace is None or grid[x - 1][y + 1].tile_type == tile_type_to_replace:
						tiles_to_rim.append({"x": x - 1, "y": y + 1})

	for tile in tiles_to_rim:
		grid[tile["x"]][tile["y"]] = GridGenerator.tileset.get_tile_for_type(rim_tile_type)


def get_grid_regions(grid: Dict, tile_type: TileTypeEnum) -> List[GridRegion]:

	flood_data = {}
	for x in range(0, grid["width"]):
		flood_data[x] = {}
		for y in range(0, grid["height"]):
			flood_data[x][y] = {}

	region_data = {}

	region_identification_complete = False
	region_count = 0

	for x in range(0, grid["width"]):
		for y in range(0, grid["height"]):
			if grid[x][y].tile_type == tile_type:
				if "id" not in flood_data[x][y].keys():
					region_count = region_count + 1
					flood_data[x][y]["id"] = region_count

					region_data[region_count] = [{"x": x, "y": y}]
					flooding_queue = [{"x": x, "y": y}]

					count = 0
					while count < len(flooding_queue):
						check_x = flooding_queue[count]["x"]
						check_y = flooding_queue[count]["y"]

						if check_x - 1 >= 0:
							if grid[check_x - 1][check_y].tile_type == tile_type and "id" not in flood_data[check_x - 1][check_y].keys():
								flooding_queue.append({"x": check_x - 1, "y": check_y})
								region_data[region_count].append({"x": check_x - 1, "y": check_y})
								flood_data[check_x - 1][check_y]["id"] = region_count

						if check_x + 1 < grid["width"]:
							if grid[check_x + 1][check_y].tile_type == tile_type and "id" not in flood_data[check_x + 1][check_y].keys():
								flooding_queue.append({"x": check_x + 1, "y": check_y})
								region_data[region_count].append({"x": check_x + 1, "y": check_y})
								flood_data[check_x + 1][check_y]["id"] = region_count

						if check_y - 1 >= 0:
							if grid[check_x][check_y - 1].tile_type == tile_type and "id" not in flood_data[check_x][check_y - 1].keys():
								flooding_queue.append({"x": check_x, "y": check_y - 1})
								region_data[region_count].append({"x": check_x, "y": check_y - 1})
								flood_data[check_x][check_y - 1]["id"] = region_count

						if check_y + 1 < grid["height"]:
							if grid[check_x][check_y + 1].tile_type == tile_type and "id" not in flood_data[check_x][check_y + 1].keys():
								flooding_queue.append({"x": check_x, "y": check_y + 1})
								region_data[region_count].append({"x": check_x, "y": check_y + 1})
								flood_data[check_x][check_y + 1]["id"] = region_count

						count = count + 1
						
	regions = []

	for value in region_data.values():
		regions.append(
			GridRegion(value, tile_type)
		)

	return regions


def get_regions_grid_percentage(grid: Dict, regions: List[GridRegion], percentage_of_grid: int, exclude_edge_regions: bool = False) -> List[GridRegion]:
	ordered_regions = order_regions_by_size_descending(grid, regions, exclude_edge_regions)

	if percentage_of_grid < 0 or percentage_of_grid > 100:
		raise ValueError("percentage_of_grid must be between 0 and 100. provided: " + str(percentage_of_grid))

	size_goal = int((grid["width"] * grid["height"]) * percentage_of_grid / 100)

	size_list = []
	for region in ordered_regions:
		size_list.append(region.size)

	closest = []
	closet_size_combo = None
	pefect_match_found = False
	max_depth = len(ordered_regions) + 1
	if max_depth > 6:
		max_depth = 6
	for depth in range(2,max_depth):
		if pefect_match_found == False:
			for i in combinations(size_list, depth):
				if sum(i) == size_goal:
					pefect_match_found = True
					closet_size_combo = i
				else:
					closest.append((abs(sum(i) - size_goal), i))
	if closet_size_combo is None:
		closet_size_combo = min(closest)[1]

	identified_regions = []
	for size in closet_size_combo:
		found = False
		for region in ordered_regions:
			if found == False:
				if region.size == size:
					identified_regions.append(region)
					found = True
					break

	return identified_regions


def order_regions_by_size_descending(grid: Dict, regions: List[GridRegion], exclude_edge_regions: bool = False) -> List[GridRegion]:
	if not exclude_edge_regions:
		applicable_regions = regions
	else:
		applicable_regions = []
		for region in regions:
			if not region.is_region_touching_edge(grid):
				applicable_regions.append(region)

	ordered_regions = []

	is_ordered = False
	while is_ordered is False:

		if len(applicable_regions) > 0:
			largest_region = None 

			for region in applicable_regions:
				if largest_region is None:
					largest_region = region
				else:
					if region.size > largest_region.size:
						largest_region = region

			ordered_regions.append(largest_region)

			applicable_regions.remove(largest_region)
		else:
			is_ordered = True
	
	return ordered_regions	


def split_by_exterior_and_interior_regions(grid: Dict, regions: List[GridRegion]) -> Tuple[List[GridRegion], List[GridRegion]]:
	exterior_reions = []
	interior_regions = []

	for region in regions:
		if region.is_region_touching_edge(grid):
			exterior_reions.append(region)
		else:
			interior_regions.append(region)

	return exterior_reions, interior_regions


def line_grid_edge(grid: Dict, new_tile_type: TileTypeEnum, thickness: int):
		for x in range(0, grid['width']):
			for y in range(0, grid['height']):
				if x < thickness or grid['width'] - x <= thickness or y < thickness or grid['height'] - y <= thickness:
					grid[x][y] = GridGenerator.tileset.get_tile_for_type(new_tile_type)


def replace_type(grid: Dict, old_tile_type: TileTypeEnum, new_tile_type: TileTypeEnum):
	for x in range(0, grid['width']):
		for y in range(0, grid['height']):
			if grid[x][y].tile_type == old_tile_type:
				grid[x][y] = GridGenerator.tileset.get_tile_for_type(new_tile_type)


def scale_grid_up(grid: Dict, collision_grid: Dict, scale_multiple: int):
	if scale_multiple < 1:
		raise ValueError("scale_multiple must be a whole number more than 1. Provided: " + str(scale_multiple))

	new_grid = {}
	new_grid["width"] = grid["width"] * scale_multiple
	new_grid["height"] = grid["height"] * scale_multiple
	for x in range(0, grid["width"] * scale_multiple):
		new_grid[x] = {}
		for y in range(0, grid["height"] * scale_multiple):
			new_grid[x][y] = grid[int(x/scale_multiple)][int(y/scale_multiple)]

	new_collision_grid = {}
	new_collision_grid["width"] = grid["width"] * scale_multiple
	new_collision_grid["height"] = grid["height"] * scale_multiple
	for x in range(0, collision_grid["width"] * scale_multiple):
		new_collision_grid[x] = {}
		for y in range(0, collision_grid["height"] * scale_multiple):
			new_collision_grid[x][y] = collision_grid[int(x/scale_multiple)][int(y/scale_multiple)]

	return new_grid, new_collision_grid


def trim_edges(grid: Dict, edge_tile_type: TileTypeEnum, replacement_tile_type: TileTypeEnum, minimum_edges: int, pass_through_count: int):

	for i in range(0, pass_through_count):

		edges_found = []

		for x in range(0, grid['width']):
			for y in range(0, grid['height']):
				edge_count = 0

				if not x - 1 < 0:
					if grid[x - 1][y].tile_type == edge_tile_type:
						edge_count = edge_count + 1

				if not x + 1 > grid["width"] - 1:
					if grid[x + 1][y].tile_type == edge_tile_type:
						edge_count = edge_count + 1

				if not y - 1 < 0:
					if grid[x][y - 1].tile_type == edge_tile_type:
						edge_count = edge_count + 1

				if not y + 1 > grid["height"] - 1:
					if grid[x][y + 1].tile_type == edge_tile_type:
						edge_count = edge_count + 1

				if edge_count <= minimum_edges:
					edges_found.append({"x": x, "y": y})
		
		for edge_found in edges_found:
			grid[edge_found["x"]][edge_found["y"]] = GridGenerator.tileset.get_tile_for_type(replacement_tile_type)


def bridge_gaps(grid: Dict, gap_tile_type: TileTypeEnum, edge_tile_type: TileTypeEnum, bridge_tile_type: TileTypeEnum, max_bridge_length: int, fill_chance: float):
	bridges_found = []

	for x in range(0, grid["width"]):
		for y in range(0, grid["height"]):
			if grid[x][y].tile_type == gap_tile_type:

				invalid_horizontal_edge = False
				invalid_vertical_edge = False

				horizontal_bridge = [{"x": x, "y": y}]
				vertical_bridge = [{"x": x, "y": y}]

				right_horizontal_edge_found = False
				left_horizontal_edge_found = False

				top_vertical_edge_found = False
				bottom_vertical_edge_found = False
				if x - max_bridge_length > 0 and x + max_bridge_length < grid["width"] - 1 and y > 1 and y < grid["height"] - 1:
					for i in range(1, max_bridge_length + 2):
						if grid[x + i][y].tile_type == gap_tile_type:
							if not right_horizontal_edge_found:
								horizontal_bridge.append({"x": x + i, "y": y})
						if grid[x - i][y].tile_type == gap_tile_type:
							if not left_horizontal_edge_found:
								horizontal_bridge.append({"x": x - i, "y": y})
						
						if grid[x + i][y].tile_type == edge_tile_type:
							right_horizontal_edge_found = True
						if grid[x - i][y].tile_type == edge_tile_type:
							left_horizontal_edge_found = True


						if grid[x + i][y].tile_type != gap_tile_type and grid[x + i][y].tile_type != edge_tile_type:
							if not right_horizontal_edge_found:
								invalid_horizontal_edge = True
						if grid[x + i][y + 1].tile_type != gap_tile_type:
							if not right_horizontal_edge_found:
								invalid_horizontal_edge = True
						if grid[x + i][y - 1].tile_type != gap_tile_type:
							if not right_horizontal_edge_found:
								invalid_horizontal_edge = True
						if grid[x - i][y].tile_type != gap_tile_type and grid[x - i][y].tile_type != edge_tile_type:
							if not left_horizontal_edge_found:
								invalid_horizontal_edge = True
						if grid[x - i][y + 1].tile_type != gap_tile_type:
							if not left_horizontal_edge_found:
								invalid_horizontal_edge = True
						if grid[x - i][y - 1].tile_type != gap_tile_type:
							if not left_horizontal_edge_found:
								invalid_horizontal_edge = True
				else:
					invalid_horizontal_edge = True

				if y - max_bridge_length > 0 and y + max_bridge_length < grid["height"] - 1 and x > 1 and x < grid["width"] - 1:
					for i in range(1, max_bridge_length + 2):
						if grid[x][y + i].tile_type == gap_tile_type:
							if not bottom_vertical_edge_found:
								vertical_bridge.append({"x": x, "y": y + i})
						if grid[x][y - i].tile_type == gap_tile_type:
							if not top_vertical_edge_found:
								vertical_bridge.append({"x": x, "y": y - i})

						if grid[x][y + i].tile_type == edge_tile_type:
							bottom_vertical_edge_found = True
						if grid[x][y - i].tile_type == edge_tile_type:
							top_vertical_edge_found = True

						if grid[x][y + i].tile_type != gap_tile_type and grid[x][y + i].tile_type != edge_tile_type:
							if not bottom_vertical_edge_found:
								invalid_vertical_edge = True
						if grid[x + 1][y + i].tile_type != gap_tile_type:
							if not bottom_vertical_edge_found:
								invalid_vertical_edge = True
						if grid[x - 1][y + i].tile_type != gap_tile_type:
							if not bottom_vertical_edge_found:
								invalid_vertical_edge = True
						if grid[x][y - i].tile_type != gap_tile_type and grid[x][y - i].tile_type != edge_tile_type:
							if not top_vertical_edge_found:
								invalid_vertical_edge = True
						if grid[x + 1][y - i].tile_type != gap_tile_type:
							if not top_vertical_edge_found:
								invalid_vertical_edge = True
						if grid[x - 1][y - i].tile_type != gap_tile_type:
							if not top_vertical_edge_found:
								invalid_vertical_edge = True
				else:
					invalid_vertical_edge = True
				
				valid_horizontal = len(horizontal_bridge) <= max_bridge_length and not invalid_horizontal_edge and left_horizontal_edge_found and right_horizontal_edge_found
				valid_vertical = len(vertical_bridge) <= max_bridge_length and not invalid_vertical_edge

				if not valid_horizontal and not valid_vertical:
					continue

				bridge_options = []
				if valid_horizontal:
					bridge_options.append(horizontal_bridge)
				if valid_vertical:
					bridge_options.append(vertical_bridge)

				bridge_choice = randrange(0, len(bridge_options))
				bridges_found.append(bridge_options[bridge_choice])
	
	for bridge in bridges_found:
		chance = randrange(0, 100000)/ 1000
		if chance <= fill_chance:
			for bridge_position in bridge:
				grid[bridge_position["x"]][bridge_position["y"]] = GridGenerator.tileset.get_tile_for_type(bridge_tile_type)
				

def generate_maze(grid: Dict, base_tile_type: TileTypeEnum, new_tile_type: TileTypeEnum, maze_path_distance: int):

	starting_x = None
	starting_y = None

	start_location_select = False

	parent_grid = {}
	for x in range(grid['width']):
		parent_grid[x] = {}
		for y in range(grid['height']):
			parent_grid[x][y] = {"x": None, "y": None}

	while start_location_select is False:

		starting_x = randrange(1, grid['width'])
		starting_y = randrange(1, grid['height'])

		if grid[starting_x][starting_y].tile_type == base_tile_type:
			start_location_select = True
			grid[starting_x][starting_y] = GridGenerator.tileset.get_tile_for_type(new_tile_type)
			parent_grid[starting_x][starting_y] = {"x": None, "y": None}

	current_x, current_y = build_path_from_position(grid, parent_grid, starting_x, starting_y, base_tile_type, new_tile_type, maze_path_distance)

	maze_done = False
	while maze_done is False:
		current_x, current_y = build_path_from_position(grid, parent_grid, current_x, current_y, base_tile_type, new_tile_type, maze_path_distance)
		current_parents = parent_grid[current_x][current_y]
		current_x = current_parents["x"]
		current_y = current_parents["y"]

		if not current_x and not current_y:
			maze_done = True

def build_path_from_position(grid: Dict, parent_grid: Dict, current_x: int, current_y: int, base_tile_type: TileTypeEnum, new_tile_type: TileTypeEnum, movement_distance: int):

	path_done = False

	while path_done is False:
		direction = get_random_valid_direction_for_placement(grid, current_x, current_y, movement_distance, base_tile_type)

		if direction == DirectionEnum.RIGHT: # Positive X
			for i in range(1, movement_distance + 1):
				grid[current_x + i][current_y] = GridGenerator.tileset.get_tile_for_type(new_tile_type)
			parent_grid[current_x + movement_distance][current_y] = {"x": current_x, "y": current_y}
			current_x = current_x + movement_distance

		elif direction == DirectionEnum.LEFT: # Negative X
			for i in range(1, movement_distance + 1):
				grid[current_x - i][current_y] = GridGenerator.tileset.get_tile_for_type(new_tile_type)
			parent_grid[current_x - movement_distance][current_y] = {"x": current_x, "y": current_y}
			current_x = current_x - movement_distance

		elif direction == DirectionEnum.DOWN: # Positive Y
			for i in range(1, movement_distance + 1):
				grid[current_x][current_y + i] = GridGenerator.tileset.get_tile_for_type(new_tile_type)
			parent_grid[current_x][current_y + movement_distance] = {"x": current_x, "y": current_y}
			current_y = current_y + movement_distance

		elif direction == DirectionEnum.UP: # negative X
			for i in range(1, movement_distance + 1):
				grid[current_x][current_y - i] = GridGenerator.tileset.get_tile_for_type(new_tile_type)
			parent_grid[current_x][current_y - movement_distance] = {"x": current_x, "y": current_y}
			current_y = current_y - movement_distance

		elif direction is None:
			path_done = True

	return current_x, current_y

def get_random_valid_direction_for_placement(grid: Dict, x: int, y: int, placement_length: int, valid_placement_type: TileTypeEnum) -> DirectionEnum:
	direction_list = [1,2,3,4]
	shuffle(direction_list)
	for direction in direction_list:
		

		if direction == DirectionEnum.RIGHT.value: # Positive X
			if grid[x + placement_length][y].tile_type == valid_placement_type:
				return DirectionEnum.RIGHT
			
		if direction == DirectionEnum.DOWN.value: # Positive Y
			if grid[x][y + placement_length].tile_type == valid_placement_type:
				return DirectionEnum.DOWN

		if direction == DirectionEnum.LEFT.value: # Negative X
			if grid[x - placement_length][y].tile_type == valid_placement_type:
				return DirectionEnum.LEFT
			
		if direction == DirectionEnum.UP.value: # Negative Y
			if grid[x][y - placement_length].tile_type == valid_placement_type:
				return DirectionEnum.UP
	
	return None
