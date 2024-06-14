from enum import Enum, auto
from copy import deepcopy


INITIAL_TOP_LEFT_START = 6
FINAL_BOTTOM_RIGHT_END = (
    6  # 3 on the bottom-right tile, which is 6 if there were another tile after
)


class TilePosition(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()


class PipeTile:
    def __init__(
        self,
        connections: list[set[int]] = [set()],
        position: TilePosition = TilePosition.TOP_LEFT,
        designation: str = "A",
    ):
        self.connections = connections
        self.position = position
        self.starting_rotation = connections.copy()
        self.designation = designation

    def rotate_from_start(self, num_turns=1):
        self.connections = self.starting_rotation.copy()
        for i in range(num_turns):
            self.rotate_once()

    def rotate_once(self):
        new_connections = []
        for connection in self.connections:
            new_connections.append({((element + 2) % 8) for element in connection})
        self.connections = new_connections

    def get_end(self, index: int):
        for connection in self.connections:
            if index in connection:
                return (connection - set([index])).copy().pop()
        raise KeyError("Index is not found in connections")

    def get_possible_starts(self):
        all_possible_starts = set()
        for connection in self.connections:
            all_possible_starts = all_possible_starts | connection
        return all_possible_starts

    def __str__(self):
        return f"{self.designation}: {self.connections}"


def get_og_six_configuration():
    return [
        PipeTile([{1, 2}, {3, 4}, {5, 7}], TilePosition.TOP_LEFT, "A"),
        PipeTile([{1, 7}, {4, 6}], TilePosition.TOP_RIGHT, "B"),
        PipeTile([{1, 2}, {3, 0}], TilePosition.BOTTOM_LEFT, "C"),
        PipeTile([{1, 3}, {6, 7}], TilePosition.BOTTOM_RIGHT, "D"),
    ]


def get_five_solution():
    return [
        PipeTile([{1, 2}, {3, 4}, {5, 7}], TilePosition.TOP_LEFT, "A"),
        PipeTile([{1, 7}, {4, 6}], TilePosition.TOP_RIGHT, "B"),
        PipeTile([{1, 2}, {3, 0}], TilePosition.BOTTOM_LEFT, "C"),
        PipeTile([{2, 3}, {6, 5}], TilePosition.BOTTOM_RIGHT, "D"),
    ]


def get_starter_tiles():
    return [
        PipeTile([{1, 2}, {3, 4}, {5, 7}], TilePosition.TOP_LEFT, "A"),
        PipeTile([{1, 7}, {4, 6}], TilePosition.TOP_RIGHT, "B"),
        PipeTile([{1, 2}, {3, 0}], TilePosition.BOTTOM_LEFT, "C"),
        PipeTile([{2, 3}, {6, 5}], TilePosition.BOTTOM_RIGHT, "D"),
    ]


def does_first_configuration_work():
    four_tiles = get_og_six_configuration()

    return pipes_lead_to_an_end(four_tiles)


def get_valid_configurations(
    four_tiles: list[PipeTile],
):
    four_tiles_copy = deepcopy(four_tiles)
    new_four_tiles: dict[int, PipeTile] = {}
    valid_configurations: list[list[PipeTile]] = []
    for i in range(4):
        new_four_tiles[0] = four_tiles_copy[i]
        new_four_tiles[0].position = TilePosition.TOP_LEFT
        for j in range(4):
            if j != i:
                new_four_tiles[1] = four_tiles_copy[j]
                new_four_tiles[1].position = TilePosition.TOP_RIGHT
                for k in range(4):
                    if k not in (i, j):
                        new_four_tiles[2] = four_tiles_copy[k]
                        new_four_tiles[2].position = TilePosition.BOTTOM_LEFT
                        for l in range(4):
                            if l not in (i, j, k):
                                new_four_tiles[3] = four_tiles_copy[l]
                                new_four_tiles[3].position = TilePosition.BOTTOM_RIGHT
                                valid_rotations_for_permutation = (
                                    get_valid_configurations_for_permutation(
                                        list(new_four_tiles.values())
                                    )
                                )
                                valid_configurations += valid_rotations_for_permutation
    return valid_configurations


def get_valid_configurations_for_permutation(four_tiles: list[PipeTile]):
    valid_rotations: list[list[PipeTile]] = []
    for i in range(4):
        four_tiles[0].rotate_from_start(i)
        for j in range(4):
            four_tiles[1].rotate_from_start(j)
            for k in range(4):
                four_tiles[2].rotate_from_start(k)
                for l in range(4):
                    four_tiles[3].rotate_from_start(l)
                    if pipes_lead_to_an_end(four_tiles):
                        valid_rotations.append(deepcopy(four_tiles))
    return valid_rotations


def main():
    four_tiles = get_starter_tiles()
    valid_configurations = get_valid_configurations(four_tiles)
    for valid_configuration in valid_configurations:
        print("Found valid configuration:")
        for tile in valid_configuration:
            print(tile)
    print(f"Total valid configurations: {len(valid_configurations)}")


def pipes_lead_to_an_end(four_pipes: list[PipeTile]) -> bool:
    top_left_tile = four_pipes[0]
    top_right_tile = four_pipes[1]
    bottom_left_tile = four_pipes[2]
    bottom_right_tile = four_pipes[3]
    next_tile = top_left_tile
    next_start_num = INITIAL_TOP_LEFT_START
    while True:
        if next_start_num == None:
            return False
        if next_start_num not in next_tile.get_possible_starts():
            return False
        next_tile_position, next_start_num = get_next_position(
            next_tile, next_start_num
        )
        if (next_tile_position, next_start_num) == (None, FINAL_BOTTOM_RIGHT_END):
            # We made it to the end
            return True
        for tile in [
            top_left_tile,
            top_right_tile,
            bottom_left_tile,
            bottom_right_tile,
        ]:
            if tile.position == next_tile_position:
                next_tile = tile
        if (next_tile_position) is None:
            return False
        pipe_exists_in_next_tile = False
        for connection in next_tile.connections:
            if next_start_num in connection:
                pipe_exists_in_next_tile = True
        if not pipe_exists_in_next_tile:
            return False
    return True


def get_next_position(tile: PipeTile, index: int):
    end_of_tile_index = tile.get_end(index)
    next_tile = None
    next_index: int | None = None
    if tile.position == TilePosition.TOP_LEFT:
        if end_of_tile_index == 2:
            next_tile = TilePosition.TOP_RIGHT
            next_index = 7
        elif end_of_tile_index == 3:
            next_tile = TilePosition.TOP_RIGHT
            next_index = 6
        elif end_of_tile_index == 4:
            next_tile = TilePosition.BOTTOM_LEFT
            next_index = 1
        elif end_of_tile_index == 5:
            next_tile = TilePosition.BOTTOM_LEFT
            next_index = 0
    elif tile.position == TilePosition.TOP_RIGHT:
        if end_of_tile_index == 4:
            next_tile = TilePosition.BOTTOM_RIGHT
            next_index = 1
        elif end_of_tile_index == 5:
            next_tile = TilePosition.BOTTOM_RIGHT
            next_index = 0
        elif end_of_tile_index == 6:
            next_tile = TilePosition.TOP_LEFT
            next_index = 3
        elif end_of_tile_index == 7:
            next_tile = TilePosition.TOP_LEFT
            next_index = 2
    elif tile.position == TilePosition.BOTTOM_LEFT:
        if end_of_tile_index == 0:
            next_tile = TilePosition.TOP_LEFT
            next_index = 5
        elif end_of_tile_index == 1:
            next_tile = TilePosition.TOP_LEFT
            next_index = 4
        elif end_of_tile_index == 2:
            next_tile = TilePosition.BOTTOM_RIGHT
            next_index = 7
        elif end_of_tile_index == 3:
            next_tile = TilePosition.BOTTOM_RIGHT
            next_index = 6
    elif tile.position == TilePosition.BOTTOM_RIGHT:
        if end_of_tile_index == 6:
            next_tile = TilePosition.BOTTOM_LEFT
            next_index = 3
        elif end_of_tile_index == 7:
            next_tile = TilePosition.BOTTOM_LEFT
            next_index = 2
        elif end_of_tile_index == 0:
            next_tile = TilePosition.TOP_RIGHT
            next_index = 5
        elif end_of_tile_index == 1:
            next_tile = TilePosition.TOP_RIGHT
            next_index = 4
        if end_of_tile_index == 3:
            return None, 6
    return next_tile, next_index


if __name__ == "__main__":
    main()
