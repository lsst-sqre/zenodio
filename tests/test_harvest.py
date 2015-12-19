import pkg_resources
import pytest

from zenodio.harvest import Datacite3Collection, zenodo_harvest_url


@pytest.fixture
def lisa7_posters_xml():
    resource_args = (__name__, '../data/lisa7-posters_oai_datacite3.xml')
    assert pkg_resources.resource_exists(*resource_args)
    xml_data = pkg_resources.resource_string(*resource_args)
    return xml_data


def test_read_lisa7(lisa7_posters_xml):
    collection = Datacite3Collection.from_collection_xml(lisa7_posters_xml)
    records = [r for r in collection.records()]
    assert len(records) > 0


def test_zenodo_harvest_url():
    community_id = 'lsst-dm'
    url = zenodo_harvest_url(community_id)
    expected = 'http://zenodo.org/oai2d?verb=ListRecords&' \
               'metadataPrefix=oai_datacite3&set=user-lsst-dm'
    assert url == expected
