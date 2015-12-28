import pkg_resources
import pytest
import datetime

import xmltodict

from zenodio.harvest import (Datacite3Collection, zenodo_harvest_url,
                             _pluralize, Author)


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


def test_pluralize_single_val():
    singular_input = """
       <authors>
         <author>Sick, Jonathan</author>
       </authors>
    """
    xml_dict = xmltodict.parse(singular_input)['authors']
    values = _pluralize(xml_dict, 'author')
    assert len(values) == 1
    assert isinstance(values, list) is True
    assert values[0] == 'Sick, Jonathan'


def test_pluralize_multi_val():
    multi_input = """
       <authors>
         <author>Sick, Jonathan</author>
         <author>Economou, Frossie</author>
       </authors>
    """
    xml_dict = xmltodict.parse(multi_input)['authors']
    values = _pluralize(xml_dict, 'author')
    assert len(values) == 2
    assert isinstance(values, list) is True
    assert values[0] == 'Sick, Jonathan'
    assert values[1] == 'Economou, Frossie'


def test_author():
    first_last = 'Sick, Jonathan'
    affil = 'LSST'
    orcid = '0000-0003-3001-676X'
    a = Author(first_last, affiliation=affil, orcid=orcid)
    assert a.first_name == 'Jonathan'
    assert a.last_name == 'Sick'
    assert a.orcid == orcid


def test_author_from_minimal_author():
    xml_data = """<creators>
                    <creator>
                      <creatorName>Massimino, Pietro</creatorName>
                      <affiliation>INAF</affiliation>
                    </creator>
                    <creator>
                      <creatorName>Costa, Alessandro</creatorName>
                      <affiliation>INAF</affiliation>
                    </creator>
                  </creators>"""
    xml_dict = xmltodict.parse(xml_data)
    values = _pluralize(xml_dict['creators'], 'creator')
    authors = [Author.from_xmldict(v) for v in values]
    author = authors[0]
    assert author.first_name == 'Pietro'
    assert author.last_name == 'Massimino'
    assert author.affiliation == 'INAF'
    assert author.orcid is None


def test_lisa7_first_resource_metadata(lisa7_posters_xml):
    """Test metadata retrieval for metadata in the first resource of the
    `lisa7_posters_xml`.
    """
    collection = Datacite3Collection.from_collection_xml(lisa7_posters_xml)
    record = [r for r in collection.records()][0]

    assert record.title == 'Adapting educational materials in data '\
                           'management for Astronomy graduate students'
    assert record.issue_date == datetime.datetime(2014, 5, 26)
    assert record.doi == '10.5281/zenodo.10165'
    assert record.abstract_html == \
        '<p>The aim of this poster is to explore how existing data '\
        'management training and tools can be adapted by Astronomy '\
        'Librarians for use in a library instructional session. Many '\
        'drivers have contributed to the growing '\
        'interest in data management planning, '\
        'including increase funder requirements for data '\
        'management plans with grant applications and an '\
        'increased interest in libraries and information '\
        'centers in supporting data curation services. '\
        'Instruction is one avenue for engagement and '\
        'outreach, and fits in nicely with the '\
        'established tradition of librarians providing '\
        'information literacy and bibliographic '\
        'instruction in scientific resources.</p>'

    authors = record.authors
    assert len(authors) == 1
    assert authors[0].first_name == 'Dianne'
    assert authors[0].last_name == 'Dietrich'
    assert authors[0].affiliation == 'Cornell University Library'
