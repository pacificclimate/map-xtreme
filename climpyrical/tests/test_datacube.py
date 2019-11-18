from climpyrical.datacube import (
    check_valid_keys,
    read_data,
    check_valid_data_path,
)
import pytest
from pkg_resources import resource_filename
import xarray as xr


@pytest.mark.parametrize(
    "data_path,passed",
    [
        (resource_filename("climpyrical", "tests/data/snw.nc"), True),
        (4, False),
        (resource_filename("climpyrical", "tests/data/maskarray.npy"), False),
    ],
)
def test_check_valid_data_path(data_path, passed):
    if passed:
        assert check_valid_data_path(data_path)
    else:
        with pytest.raises((KeyError, TypeError)):
            check_valid_data_path(data_path)


@pytest.mark.parametrize(
    "actual_keys,required_keys,passed",
    [
        (
            {"rlat", "rlon", "dv", 4, "lat", "lon"},
            {"rlat", "rlon", "dv", 4},
            True,
        ),
        ({"rlat", "rlon", True, 99999}, {"rlat", "rlon", True, 99999}, True),
        (
            {"rlat", "rlon", 4.0, False},
            {"hi", "nic", "was", "here", "lon"},
            False,
        ),
    ],
)
def test_check_valid_keys(actual_keys, required_keys, passed):
    if passed:
        assert check_valid_keys(actual_keys, required_keys)
    else:
        with pytest.raises(KeyError):
            check_valid_keys(actual_keys, required_keys)


@pytest.mark.parametrize(
    "data_path,design_value_name,keys,shape",
    [
        (
            resource_filename("climpyrical", "tests/data/snw.nc"),
            "snw",
            {"rlat", "rlon", "lat", "lon"},
            (66, 130, 155),
        ),
        (
            resource_filename("climpyrical", "tests/data/hdd.nc"),
            "heating_degree_days_per_time_period",
            {"rlat", "rlon", "lat", "lon", "level"},
            (35, 130, 155),
        ),
        (
            resource_filename("climpyrical", "tests/data/example1.nc"),
            "hyai",
            {"lon", "lat"},
            (27,),
        ),
        (
            resource_filename("climpyrical", "tests/data/example2.nc"),
            "tas",
            {"lat", "lon"},
            (1, 130, 155),
        ),
        (
            resource_filename("climpyrical", "tests/data/example3.nc"),
            "tas",
            {"lat", "lon"},
            (1, 128, 256),
        ),
        (
            resource_filename("climpyrical", "tests/data/example4.nc"),
            "tos",
            {"lat", "lon"},
            (24, 170, 180),
        ),
    ],
)
def test_shape(data_path, design_value_name, keys, shape):
    # tests that the function loads a variety of test data
    # properly
    ds = read_data(data_path, design_value_name, keys)
    assert ds[design_value_name].shape == shape


@pytest.mark.parametrize(
    "a,b",
    [
        (
            read_data(
                resource_filename("climpyrical", "tests/data/snw.nc"),
                "snw",
                {"lat", "lon"},
            ),
            xr.open_dataset(
                resource_filename("climpyrical", "tests/data/snw.nc")
            ),
        ),
        (
            read_data(
                resource_filename("climpyrical", "tests/data/example4.nc"),
                "tos",
                {"lat", "lon"},
            ),
            xr.open_dataset(
                resource_filename("climpyrical", "tests/data/example4.nc")
            ),
        ),
    ],
)
def test_xarray_open_dataset(a, b):
    # tests that xr.open_dataset does the same
    # thing as read_data for a few examples
    xr.testing.assert_identical(a, b)
