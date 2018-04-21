import pytest

from pegboard.index_card_holder import thickened_shape, raised_shape, centered_spacing, centered_grid


def test_thickened_shape():
    shape = [1, 2, 3.0]
    thick_shape = thickened_shape(shape, 0.1)
    assert [1.1, 2.1, 3.1] == pytest.approx(thick_shape)


def test_raised_shape():
    shape = [1, 2, 3.0]
    high_shape = raised_shape(shape, 0.1)
    assert [1, 2, 3.1] == pytest.approx(high_shape)


def test_centered_spacing():
    assert [-0.5, 0.5] == pytest.approx(centered_spacing(1.8, 1.0))
    assert [-2.0, 0.0, 2.0] == pytest.approx(centered_spacing(5.1, 2.0))

def test_centered_grid():
    result = centered_grid(2.75, 1.6, 1.0)
    expected = [
        (-0.5, -1.0), (-0.5, 0.0), (-0.5, 1.0),
        (0.5, -1.0), (0.5, 0.0), (0.5, 1.0),
    ]
    assert expected == result

def test_centered_grid_with_margin():
    result = centered_grid(3.25, 2.2, 1.0, 0.5)
    expected = [
        (-0.5, -1.0), (-0.5, 0.0), (-0.5, 1.0),
        (0.5, -1.0), (0.5, 0.0), (0.5, 1.0),
    ]
    assert expected == result