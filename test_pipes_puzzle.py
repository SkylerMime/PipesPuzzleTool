import pipes_puzzle
from pipes_puzzle import *
import pytest


def test_pipe_tile_invalid_start():
    my_tile = PipeTile([{1, 4}], TilePosition.TOP_LEFT)
    with pytest.raises(KeyError):
        my_tile.get_end(3)


def test_get_end_gets_other_num():
    my_tile = PipeTile([{0, 2}, {3, 7}], TilePosition.TOP_RIGHT)
    assert my_tile.get_end(0) == 2
    assert my_tile.get_end(2) == 0


def test_get_next_gets_other_tile():
    top_tile = PipeTile([{7, 5}], TilePosition.TOP_LEFT)
    bottom_tile = PipeTile([{0, 2}], TilePosition.BOTTOM_LEFT)
    assert get_next_position(top_tile, 7) == (TilePosition.BOTTOM_LEFT, 0)


def test_get_next_gets_other_left():
    right_tile = PipeTile([{1, 6}], TilePosition.BOTTOM_RIGHT)
    left_tile = PipeTile([{3, 0}], TilePosition.BOTTOM_LEFT)
    assert get_next_position(right_tile, 1) == (TilePosition.BOTTOM_LEFT, 3)


def test_basic_configuration(monkeypatch):
    monkeypatch.setattr(pipes_puzzle, "INITIAL_TOP_LEFT_START", 7)
    assert does_first_configuration_work() == True


def test_basic_rotation():
    my_tile = PipeTile([{0, 2}, {5, 7}], TilePosition.TOP_RIGHT)
    my_tile.rotate_once()
    assert {2, 4} in my_tile.connections and {7, 1} in my_tile.connections


def test_total_rotation():
    my_tile = PipeTile([{0, 2}, {5, 7}], TilePosition.TOP_RIGHT)
    my_tile.rotate_from_start(4)
    assert {0, 2} in my_tile.connections and {5, 7} in my_tile.connections


def test_saved_rotation():
    my_tile = PipeTile([{0, 2}, {5, 7}], TilePosition.TOP_RIGHT)
    my_tile.rotate_from_start(1)
    my_tile.rotate_from_start(2)
    my_tile.rotate_from_start(0)
    assert {0, 2} in my_tile.connections and {5, 7} in my_tile.connections


class MockPipeTile(PipeTile):
    def __init__(self, designation: int) -> None:
        self.designation = designation
        self.position: TilePosition | None = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.designation}"


def test_orderings_generates_all_permutations(monkeypatch):
    mock_tiles_list = [MockPipeTile(i) for i in range(4)]
    monkeypatch.setattr(
        pipes_puzzle,
        "get_valid_configurations_for_permutation",
        lambda _: [mock_tiles_list],
    )
    valid_configurations = get_valid_configurations(mock_tiles_list)
    assert len(valid_configurations) == 24
    for configuration in valid_configurations:
        for designation in range(4):
            assert designation in [tile.designation for tile in configuration]


def test_deepcopy_mocks():
    mock_tiles_list = [MockPipeTile(i) for i in range(4)]
    mock_tiles_list[0].position = TilePosition.TOP_LEFT
    new_mock_tiles_list = deepcopy(mock_tiles_list)
    new_mock_tiles_list[0].position = TilePosition.TOP_RIGHT
    assert mock_tiles_list[0].position != TilePosition.TOP_RIGHT
