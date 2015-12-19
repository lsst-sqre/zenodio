"""
Module for harvesting metadata for Community's collection from Zenodo.

Our goal is to transform XML accessible at a URL into a series of Python
objects with metadata attributes.
"""

import datetime

import requests
import xmltodict


def harvest_collection(community_name):
    """Harvest a Zenodo community into a set of Python objects.

    Parameters
    ----------
    community_name : str
        Name of the community.
    """
    url = zenodo_harvest_url(community_name)
    r = requests.get(url)
    r.status_code
    xml_content = r.content

    return Datacite3Collection.from_collection_xml(xml_content)


def zenodo_harvest_url(community_name, format='oai_datacite3'):
    """Build a URL for the Zenodo Community's metadata.

    Parameters
    ----------
    community_name : str
        Name of the community.
    format : str
        OAI-PMH metadata specification name. See https://zenodo.org/dev.

    Returns
    -------
    url : str
        OAI-PMH metadata URL.
    """
    template = 'http://zenodo.org/oai2d?verb=ListRecords&' \
               'metadataPrefix={metadata_format}&set=user-{community}'
    return template.format(metadata_format=format,
                           community=community_name)


class Datacite3Collection(object):
    """Zenodo metadata for a Community collection derived from Datacite v3
    metadata.
    """
    def __init__(self, xml_records):
        super().__init__()
        self._xml_records = xml_records

    @classmethod
    def from_collection_xml(cls, xml_content):
        xml_dataset = xmltodict.parse(xml_content, process_namespaces=False)
        # Unwrap the record list when harvesting a collection's datacite 3
        print(xml_dataset['OAI-PMH'].keys())
        print(xml_dataset['OAI-PMH']['request'].keys())
        xml_records = xml_dataset['OAI-PMH']['ListRecords']['record']  # NOQA
        return cls(xml_records)

    def records(self):
        for record in self._xml_records:
            yield Datacite3Record(record)


class Datacite3Record(object):
    """Zenodo metadata for a single record"""
    def __init__(self, xml_dict):
        super().__init__()
        # Unwrap the record; may want to add extra robustness to this in case
        # you can get a record's XML
        self._r = xml_dict['metadata']['oai_datacite']['payload']['resource']

    @property
    def authors(self):
        """List of authors.

        These are `dict`\ s with keys:

        - 'name'
        - 'affiliation'
        """
        return [{'name': a['creatorName'],
                 'affiliation': a['affiliation']}
                for a in self._r['creators']['creator']]

    @property
    def doi(self):
        return self._r['identifier']['#text']

    @property
    def title(self):
        return self._r['titles']['title']

    @property
    def abstract_html(self):
        return self._r['descriptions']['description']['#text']

    @property
    def date(self):
        return datetime.datetime.strptime(
            self._r['dates']['date']['#text'], '%Y-%m-%d')
