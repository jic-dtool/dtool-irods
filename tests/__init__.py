"""Test fixtures."""

import os
import shutil
import tempfile
import string
import random
from contextlib import contextmanager

import pytest

from dtoolcore import generate_admin_metadata
from dtool_irods.storagebroker import (
    _mkdir,
    _rm_if_exists,
    IrodsStorageBroker,
)


_HERE = os.path.dirname(__file__)
TEST_SAMPLE_DATA = os.path.join(_HERE, "data")

TEST_ZONE = "/jic_overflow/dtool-testing"


@contextmanager
def tmp_env_var(key, value):
    os.environ[key] = value
    yield
    del os.environ[key]


@contextmanager
def tmp_directory():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)


def random_string(
    size=9,
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))


@pytest.fixture
def chdir_fixture(request):
    d = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(d)

    @request.addfinalizer
    def teardown():
        os.chdir(curdir)
        shutil.rmtree(d)


@pytest.fixture
def tmp_dir_fixture(request):
    d = tempfile.mkdtemp()

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def local_tmp_dir_fixture(request):
    d = tempfile.mkdtemp(dir=_HERE)

    @request.addfinalizer
    def teardown():
        shutil.rmtree(d)
    return d


@pytest.fixture
def tmp_uuid_and_uri(request):
    admin_metadata = generate_admin_metadata("test_dataset")
    uuid = admin_metadata["uuid"]

    base_uri = "irods:" + TEST_ZONE
    uri = IrodsStorageBroker.generate_uri("test_dataset", uuid, base_uri)

    @request.addfinalizer
    def teardown():
        _, irods_path = uri.split(":", 1)
        _rm_if_exists(irods_path)

    return (uuid, uri)


@pytest.fixture
def tmp_irods_base_uri_fixture(request):
    collection = os.path.join(TEST_ZONE, random_string())

    _mkdir(collection)

    @request.addfinalizer
    def teardown():
        _rm_if_exists(collection)

    return "irods:" + collection
