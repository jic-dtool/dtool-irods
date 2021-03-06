"""Test the IrodsStorageBroker.list_dataset_uris class method."""

from . import tmp_irods_base_uri_fixture  # NOQA


def test_list_dataset_uris(tmp_irods_base_uri_fixture):  # NOQA

    import dtoolcore
    from dtool_irods.storagebroker import IrodsStorageBroker

    assert [] == IrodsStorageBroker.list_dataset_uris(
        base_uri=tmp_irods_base_uri_fixture,
        config_path=None
    )

    # Create two datasets to be copied.
    expected_uris = []
    for name in ["test_ds_1", "test_ds_2"]:
        admin_metadata = dtoolcore.generate_admin_metadata(name)
        proto_dataset = dtoolcore.generate_proto_dataset(
            admin_metadata=admin_metadata,
            base_uri=tmp_irods_base_uri_fixture
        )
        proto_dataset.create()
        expected_uris.append(proto_dataset.uri)

    actual_uris = IrodsStorageBroker.list_dataset_uris(
        base_uri=tmp_irods_base_uri_fixture,
        config_path=None
    )

    assert set(expected_uris) == set(actual_uris)
