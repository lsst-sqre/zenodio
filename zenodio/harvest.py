"""
Module for harvesting metadata for Community's collection from Zenodo.

Use :func:`~zenodio.harvest.harvest_collection` to download metadata for a
Zenodo Community, by identifier. Downloaded metadata for a collection is
encapsulated by a :class:`~zenodio.harvest.Datacite3Collection` object.
:meth:`~zenodio.harvest.Datacite3Collection.records` generates
:class:`~zenodio.harvest.Datacite3Record` objects for individual records in
the Zenodo community. Using :class:`~zenodio.harvest.Datecite3Record`\ 's
members you can access attributes about that record, such as authors, title,
and DOI.

Examples
--------

>>> import zenodio.harvest
>>> collection = harvest_collection('lsst-dm')
>>> for record in collection.records():
...    print(record.title)
"""

import datetime

import requests
import xmltodict


def harvest_collection(community_name):
    """Harvest a Zenodo community's record metadata.

    Examples
    --------
    You can harvest record metadata for a Zenodo community by its identifier
    name. For example, the identifier for LSST Data Management's Zenodo
    collection is ``'lsst-dm'``:

    >>> import zenodio.harvest import harvest_collection
    >>> collection = harvest_collection('lsst-dm')

    ``collection`` is a :class:`~zenodio.harvest.Datacite3Collection` instance.
    Use its :meth:`~zenodio.harvest.Datacite3Collection.records` method to
    generate :class:`~zenodio.harvest.Datacite3Record` objects for individual
    records in the Zenodo collection.

    Parameters
    ----------
    community_name : str
        Name of the community.

    Returns
    -------
    collection : :class:`zenodio.harvest.Datacite3Collection`
        The :class:`~zenodio.harvest.Datacite3Collection` instance with record
        metadata downloaded from Zenodo.
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

    Use the :meth:`~zenodio.harvest.Datacite3Collection.from_collection_xml`
    classmethod to build a :class:`~zenodio.harvest.Datacite3Collection`
    from XML obtained from the Zenodo OAI-PMH API. Most likely, users should
    use :func:`~zenodio.harvest.harvest_collection` to build
    a :class:`~zenodio.harvest.Datacite3Collection` for a Community.
    """
    def __init__(self, xml_records):
        super().__init__()
        self._xml_records = xml_records

    @classmethod
    def from_collection_xml(cls, xml_content):
        """Build a :class:`~zenodio.harvest.Datacite3Collection` from
        Datecite3-formatted XML.

        Users should use :func:`zenodio.harvest.harvest_collection` to build a
        :class:`~zenodio.harvest.Datacite3Collection` for a Community.

        Parameters
        ----------
        xml_content : str
            Datacite3-formatted XML content.

        Returns
        -------
        collection : :class:`Datacite3Collection`
            The collection parsed from Zenodo OAI-PMH XML content.
        """
        xml_dataset = xmltodict.parse(xml_content, process_namespaces=False)
        # Unwrap the record list when harvesting a collection's datacite 3
        xml_records = xml_dataset['OAI-PMH']['ListRecords']['record']  # NOQA
        return cls(xml_records)

    def records(self):
        """Yield records from the collection.

        Yields
        ------
        record : :class:`Datacite3Record`
            The :class:`Datacite3Record` for an individual resource in
            the Zenodo collection.
        """
        for record in self._xml_records:
            yield Datacite3Record(record)


class Datacite3Record(object):
    """Zenodo metadata for a single record.

    Use :class:`~zenodio.harvest.Datacite3Record`\ s to access metadata about a
    record though a convient object properties.

    Parameters
    ----------
    xml_dict : :class:`collections.OrderedDict`
        A `dict`-like object mapping XML content for a single record (i.e.,
        the contents of the ``record`` tag in OAI-PMH XML). This dict is
        typically generated from :mod:`xmltodict`.
    """
    def __init__(self, xml_dict):
        super().__init__()
        # Unwrap the record; may want to add extra robustness to this in case
        # you can get a record's XML
        self._r = xml_dict['metadata']['oai_datacite']['payload']['resource']

    @property
    def authors(self):
        """List of :class:`~zenodio.harvest.Author`\ s
        (:class:`zenodio.harvest.Author`).

        Authors correspond to `creators` in the Datacite schema.
        """
        creators = _pluralize(self._r['creators'], 'creator')
        authors = [Author.from_xmldict(c) for c in creators]
        return authors

    @property
    def doi(self):
        """Digital object identifier `str`."""
        return self._r['identifier']['#text']

    @property
    def title(self):
        """Title of resource (`str`).

        If there are multiple titles, the first title is returned.
        """
        return _pluralize(self._r['titles'], 'title')[0]

    @property
    def abstract_html(self):
        """Abstract text, marked up with HTML (`str`)."""
        descriptions = _pluralize(self._r['descriptions'], 'description')
        for desc in descriptions:
            if desc['@descriptionType'] == 'Abstract':
                return desc['#text']

    @property
    def issue_date(self):
        """Date when the DOI was issued (:class:`datetime.datetime.Datetime`).
        """
        dates = _pluralize(self._r['dates'], 'date')
        for date in dates:
            if date['@dateType'] == 'Issued':
                return datetime.datetime.strptime(date['#text'], '%Y-%m-%d')


class Author(object):
    """Metadata about an author.

    :class:`~zenodio.harvest.Author` instances are typically built by
    :meth:`Datacite3Record.authors`.

    Parameters
    ----------
    last_first : str
        Author's name, formatted as `'Last, First'`.
    orcid : str, optional
        Author's ORCiD.
    affiliation : str, optional
        Author's affiliation.

    Attributes
    ----------
    last_first : str
        Author's name, formatted as `'Last, First'`.
    orcid : str
        Author's ORCiD.
    affiliation : str
        Author's affiliation.
    """
    def __init__(self, last_first, orcid=None, affiliation=None):
        super().__init__()
        self.last_first = last_first
        self.orcid = orcid
        self.affiliation = affiliation

    @classmethod
    def from_xmldict(cls, xml_dict):
        """Create an `Author` from a datacite3 metadata converted by
        `xmltodict`.

        Parameters
        ----------
        xml_dict : :class:`collections.OrderedDict`
            A `dict`-like object mapping XML content for a single record (i.e.,
            the contents of the ``record`` tag in OAI-PMH XML). This dict is
            typically generated from :mod:`xmltodict`.
        """
        name = xml_dict['creatorName']

        kwargs = {}
        if 'affiliation' in xml_dict:
            kwargs['affiliation'] = xml_dict['affiliation']

        return cls(name, **kwargs)

    @property
    def first_name(self):
        """Author's first name (`str`)."""
        return self.last_first.split(',')[-1].strip()

    @property
    def last_name(self):
        """Author's last name (`str`)."""
        return self.last_first.split(',')[0].strip()


def _pluralize(value, item_key):
    """"Force the value of a datacite3 key to be a list.

    >>> _pluralize(xml_input['authors'], 'author')
    ['Sick, Jonathan', 'Economou, Frossie']

    Background
    ----------
    When `xmltodict` proceses metadata, it turns XML tags into new key-value
    pairs whenever possible, even if the value should semantically be treated
    as a `list`.

    For example

    .. code-block:: xml

       <authors>
         <author>Sick, Jonathan</author>
       </authors

    Would be rendered by `xmltodict` as::

       {'authors': {'author': 'Sick, Jonathan'}}

    While

    .. code-block:: xml

       <authors>
         <author>Sick, Jonathan</author>
         <author>Economou, Frossie</author>
       </authors

    is rendered by `xmltodict` as::

       {'authors': [{'author': ['Sick, Jonathan', 'Economou, Frossie']}}

    This function ensures that values are *always* lists so that they can be
    treated uniformly.

    Parameters
    ----------
    value : obj
        The value of a key from datacite metadata extracted by `xmltodict`.
        For example, `xmldict['authors']`.
    item_key : str
        Name of the tag for each item; for example, with the `'authors'` key
        the item key is `'author'`.

    Returns
    -------
    item_values : list
        List of values of all items.
    """
    v = value[item_key]
    if not isinstance(v, list):
        # Force a singular value to be a list
        return [v]
    else:
        return v
