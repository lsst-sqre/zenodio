"""Representations of Zenodo metadata.
"""


class Metadata(object):
    """Metadata for a Zenodo deposition.

    The metadata attributes available in this class mirror those in
    the Zenodo API's own deposition metadata schema,
    https://zenodo.org/dev#collapse-r-meta

    Parameters
    ----------
    deposition : optional
        A deposition instance that this metadata is associated to (if at all).
        If set, then metadata changes will be reflected automatically to the
        Zenodo deposition.
    **meta :
        Initalize the :class:`Metadata` with keyword arguments. Arguments
        are names and expected values math :class:`Metadata` attributes.
    """
    def __init__(self, deposition=None, **meta):
        super().__init__()

    @property
    def yaml(self, arg1):
        """YAML-formatted metadata representation (:class:`str`).

        Comments, variables and ordering are preserved if the
        :class:`Metadata` instance was produced with the :meth:`load_yaml`
        classmethod.
        """
        pass

    @property
    def json(self):
        """JSON-formatted metadata reprsentation suitable for the Zenodo
        API . (:class:`str`)

        This JSON can be used in the ``metadata`` field of the Zenodo API's
        ``deposition`` data; https://zenodo.org/dev#collapse-r-dep.
        """
        pass

    @property
    def upload_type(self):
        """Type of deposition (:class:`UploadType`)."""
        pass

    @upload_type.setter
    def upload_type(self, value):
        pass

    @property
    def publication_date(self):
        """Date of publication (:class:`datetime.date`).

        For Zenodo uploads, this defaults to the date of initial upload if
        not provided.
        """
        pass

    @publication_date.setter
    def publicaton_date(self, date):
        pass

    @property
    def creators(self):
        """A :class:`list` of :class:`Person` instances, corresponding to
        the creators/authors of the deposition.
        """
        pass

    @creators.setter
    def creators(self, persons):
        pass

    @property
    def contributors(self):
        """A :class:`list` of :class:`Person` instances, corresponding to
        the contributors for the deposition.
        """
        pass

    @contributors.setter
    def contributors(self, persons):
        pass

    @property
    def title(self):
        """Title of deposition (:class:`str`)."""
        pass

    @title.setter
    def title(self, value):
        pass

    @property
    def description_html(self):
        """Description of deposition, formatted as HTML (:class:`str`).

        Permitted HTML tags are: ``a``, ``p``, ``br``, ``blockquote``,
        ``strong``, ``b``, ``u``, ``i``, ``em``, ``ul``, ``ol``, ``li``,
        ``sub``, ``sup``, ``div``, ``strike``.
        """
        pass

    @description_html.setter
    def description_html(self, value):
        pass

    @property
    def access_right(self):
        """Access rights for deposition (:class:`str`).

        Allowed values are:

        - `'open'`: Open Access
        - `'embargoed'`: Embargoed Access
        - `'restricted'`: Restricted Access
        - `'closed'`: Closed Access
        """
        pass

    @access_right.setter
    def access_right(self, value):
        pass

    @property
    def embargo_date(self):
        """Date when embargo will be lifted by Zenodo (:class:`datetime.date`).
        """
        pass

    @embargo_date.setter
    def embargo_date(self, date):
        pass

    @property
    def license(self):
        """License idenfier (:class:`str`).

        License names match a controlled vocabulary,
        https://zenodo.org/kb/export?kbname=licenses&format=kba. The selected
        license applies to all files in this deposition, but not to the
        metadata which is licensed under `Creative Commons Zero
        <https://zenodo.org/terms>`_. Further information about licenses is
        available at `Open Definition Licenses Service
        <http://licenses.opendefinition.org/>`_.

        Defaults to `'cc-by'` for non-datasets and `'cc-zero'` for datasets.
        """
        pass

    @license.setter
    def license(self, value):
        pass

    @property
    def access_conditions_html(self):
        """Specify the conditions under which you grant users access to the
        files in your upload.

        User requesting access will be asked to justify how they fulfil the
        conditions. Based on the justification, you decide who to grant/deny
        access. You are not allowed to charge users for granting access to data
        hosted on Zenodo.

        Permitted HTML tags are: ``a``, ``p``, ``br``, ``blockquote``,
        ``strong``, ``b``, ``u``, ``i``, ``em``, ``ul``, ``ol``, ``li``,
        ``sub``, ``sup``, ``div``, ``strike``.
        """
        pass

    @access_conditions_html.setter
    def access_conditions_html(self, value):
        pass

    @property
    def doi(self):
        """Digital object identifier (:class:`str`).

        Set this attribute for new uploads if a DOI has already been reserved
        for your deposition.

        Zenodo will automatically assign a DOI for new uploads if this
        attribute isn't set.
        """
        pass

    @doi.setter
    def doi(self, value):
        pass

    @property
    def keywords(self):
        """:class:`list` of Free form keywords (:class:`str`) for this
        deposition.
        """
        pass

    @keywords.setter
    def keywords(self, value):
        pass

    @property
    def notes(self):
        """Additional notes. Plain text, no HTML. (:class:`str`)."""
        pass

    @notes.setter
    def notes(self, value):
        pass

    @property
    def related_identifiers(self):
        """:class:`list` of :class:`RelatedId` instances indicating resources
        that are related to this one in any of several ways. (:class:`list`).
        """
        pass

    @related_identifiers.setter
    def related_identifiers(self, value):
        pass

    @property
    def references(self):
        """List of references formatted as plain :class:`str`\ s
        (:class:`list`).

        E.g.::

           ['Doe J (2014). Title. Publisher. DOI',
            'Smith J (2014). Title. Publisher. DOI']
        """
        pass

    @references.setter
    def references(self, value):
        pass

    @property
    def communities(self):
        """List of Zenodo community identifiers (as :class:`str`) that this
        upload is part of (:class:`list`).
        """
        pass

    @communities.setter
    def communities(self, value):
        pass

    @property
    def grants(self):
        """List of FP7 grants (formatted as :class:`str`) that contributed to
        this upload (:class:`list`).
        """
        pass

    @grants.setter
    def grants(self, value):
        pass

    @property
    def journal_title(self):
        """Name of journal, if a publication (:class:`str`)."""
        pass

    @journal_title.setter
    def journal_title(self, value):
        pass

    @property
    def journal_volume(self):
        """Journal volume, if a publication (:class:`str`)."""
        pass

    @journal_volume.setter
    def journal_volume(self, value):
        pass

    @property
    def journal_issue(self):
        """Journal issue, if a publication (:class:`str`)."""
        pass

    @journal_issue.setter
    def journal_issue(self, value):
        pass

    @property
    def journal_pages(self):
        """Page range of publication in the journal issue (:class:`str`)."""
        pass

    @journal_pages.setter
    def journal_pages(self, value):
        pass

    @property
    def conference_title(self):
        """Name of conference, if a conference contribution (:class:`str`)."""
        pass

    @conference_title.setter
    def conference_title(self, value):
        pass

    @property
    def conference_acronym(self):
        """Common acronym identifying conference, if a conference contribution
        (:class:`str`).
        """
        pass

    @conference_acronym.setter
    def conference_acronym(self, value):
        pass

    @property
    def conference_dates(self):
        """Date range of conference, formatted as 'DD-DD Month Year'
        (:class:`str`).

        Conference title or acronym must also be specified if this field is
        specified.
        """
        pass

    @conference_dates.setter
    def conference_dates(self, value):
        pass

    @property
    def conference_place(self):
        """Place of conference in the format 'city, country'.

        Example::

            'Amsterdam, The Netherlands'

        Conference title or acronym must also be specified if this field is
        specified.
        """
        pass

    @conference_place.setter
    def conference_place(self, value):
        pass

    @property
    def conference_url(self):
        """URL of conference (:class:`str`)."""
        pass

    @conference_url.setter
    def conference_url(self, value):
        pass

    @property
    def conference_session(self):
        """Number of session within the conference (e.g. `'VI'`).
        (:class:`str`).
        """
        pass

    @conference_session.setter
    def conference_session(self, value):
        pass

    @property
    def conference_session_part(self):
        """Number of part within a session (e.g. `'1'`). (:class:`str`)."""
        pass

    @conference_session_part.setter
    def conference_session_part(self, value):
        pass

    @property
    def imprint_publisher(self):
        """Publisher of a book/report/chapter (:class:`str`)."""
        pass

    @imprint_publisher.setter
    def imprint_publisher(self, value):
        pass

    @property
    def imprint_place(self):
        """Place of publication of a book/report/chapter in the format
        `'city, country'` (:class:`str`).
        """
        pass

    @imprint_place.setter
    def imprint_place(self, value):
        pass

    @property
    def imprint_isbn(self):
        """ISBN of a book/report (:class:`str`)."""
        pass

    @imprint_isbn.setter
    def imprint_isbn(self, value):
        pass

    @property
    def partof_title(self):
        """Title of book for chapters (:class:`str`)."""
        pass

    @partof_title.setter
    def partof_title(self, value):
        pass

    @property
    def partof_pages(self):
        """Pages numbers of book (:class:`str`)."""
        pass

    @partof_pages.setter
    def partof_pages(self, value):
        pass

    @property
    def thesis_supervisors(self):
        """A :class:`list` of :class:`Person` instances, corresponding to
        the supervisors for this thesis.
        """
        pass

    @thesis_supervisors.setter
    def thesis_supervisors(self, persons):
        pass

    @property
    def thesis_university(self):
        """Awarding university of thesis (:class:`str`)."""
        pass

    @thesis_university.setter
    def thesis_university(self, value):
        pass


class UploadType(object):
    """Type of a Zenodo deposition (publication, presentation, etc.).

    Parameters
    ----------
    category : str
        The type of deposition.
        
        The category is chosen from a controlled vocabulary of

        - `'publication'`: Publication (see also :attr:`publication_type`)
        - `'poster'`: Poster
        - `'presentation'`: Presentation
        - `'dataset'`: Dataset
        - `'image'`: Image
        - `'video'`: Video/Audio
        - `'software'`: Software
    subcategory : str, optional
        If the ``category`` is `'publication'` or `'image'`, then a subcategory
        *must* also be set.

        `'publication'` subcategories

           - `'book'`: Book
           - `'section'`: Book section
           - `'conferencepaper'`: Conference paper
           - `'article'`: Journal article
           - `'patent'`: Patent
           - `'preprint'`: Preprint
           - `'report'`: Report
           - `'softwaredocumentation'`: Software documentation
           - `'thesis'`: Thesis
           - `'technicalnote'`: Technical note
           - `'workingpaper'`: Working paper
           - `'other'`: Other

        `'image'` subcategories

           - `'figure'`: Figure
           - `'plot'`: Plot
           - `'drawing'`: Drawing
           - `'diagram'`: Diagram
           - `'photo'`: Photo
           - `'other'`: Other
    """
    def __init__(self, category, subcategory=None):
        super().__init__()
        pass

    @property
    def category(self):
        pass

    @property
    def subcategory(self):
        pass

    def insert_json_data(self, json_dataset):
        """Callback method for a parent :class:`Metadata` instance to add
        this metadata to the `dict`-like JSON dataset.

        Parameters
        ----------
        json_dataset : dict
            Dict-like instance whose ``upload_type`` and ``publication_type``
            or ``image_type`` fields will be updated.
        """
        pass

    def insert_yaml_data(self, yaml_dataset):
        """Callback method for a parent :class:`Metadata` instance to add
        this metadata to the `dict`-like YAML dataset.

        Parameters
        ----------
        yaml_dataset : dict
            Dict-like instance whose ``upload_type`` field will be updated.
            The value can either be a single string with `category`, or a list
            of `category` and `subcategory` for `'publication'` and `'image'`
            uploads.
        """
        pass


class Person(object):
    """Representation of a person in Zenodo metadata.

    This class can be used as items `creators`, `contributors`
    and `'thesis_supervisors'` lists.

    Parameters
    ----------
    name : str, optional
        Person's name, formatted 'Family, First name'.
    family_name : str, optional
        Family name of person. Set this in conjunction with `given_name`
        instead of setting name.
    given_name : str, optional
        Family name of person. Set this in conjunction with `given_name`
        instead of setting name.
    role : str, optional
        If the Person is a *contributor*, this classifies the person's
        role. Values can be one of

        - `'ContactPerson'`,
        - `'DataCollector'`,
        - `'DataCurator'`,
        - `'DataManager`',
        - `'Editor`',
        - `'Researcher`',
        - `'RightsHolder`',
        - `'Sponsor`',
        - `'Other`'

        *Only set this metadata for contributors*.
    affiliation : str, optional
        Professional affiliation of the Person.
    orcid : str, optional
        ORCiD iD of this person.
    gnd : str, optional
        GND identifier of this person.
    """
    def __init__(self, name=None, family_name=None, given_name=None,
                 role=None, affiliation=None, orcid=None, gnd=None):
        super(Person, self).__init__()
        pass

    @property
    def json_data(self):
        """`dict` data for this Person for use as a :class:`list`-item for
        the `'creators'`, `'contributors'` or `'thesis_supervisors'`
        fields in Zenodo JSON schema.
        """
        pass

    @property
    def yam_data(self):
        """`dict` data for this Person for use as a :class:`list`-item for
        the `'creators'`, `'contributors'` or `'thesis_supervisors'`
        fields in Zenodio's YAML-formatted metadata.
        """
        pass

    @property
    def name(self):
        """Person's name, formatted 'Family, First name' (:class:`str`)."""
        pass

    @property
    def family_name(self):
        """Family name of person (:class:`str`)."""
        pass

    @property
    def given_name(self):
        """Given name of person (:class:`str`)."""
        pass

    @property
    def role(self):
        """If the Person is a *contributor*, this is the person's role.

        See class documentation above for vocabulary.
        """
        pass

    @property
    def affiliation(self):
        """Professional affiliation of the Person. (:class:`str`)."""
        pass

    @property
    def orcid(self):
        """ORCiD iD of this person. (:class:`str`)."""
        pass

    @property
    def gnd(self):
        """GND identifier of this person. (:class:`str`)."""
        pass


class RelatedId(object):
    """Representation of a related artifact.

    Parameters
    ----------
    identifier : str
        Identifies the related artifacts. Several identifiers are allowed:

        - DOI
        - Handle
        - ARK
        - PURL
        - ISSN
        - ISBN
        - PubMed ID
        - PubMed Central ID
        - ADS Bibliographic Code
        - arXiv
        - Life Science Identifiers (LSID)
        - EAN-13
        - ISTC
        - URN
        - URL
    relation : str
        Description of the relationship. Allowed values are:

        - isCitedBy
        - cites
        - isSupplementTo
        - isSupplementedBy
        - isNewVersionOf
        - isPreviousVersionOf
        - isPartOf,
        - hasPart
        - compiles
        - isCompiledBy
        - isIdenticalTo
        - isAlternateIdentifier
    """
    def __init__(self, identifier, relation):
        super().__init__()
        pass

    @property
    def identifier(self):
        """Identifier for related artifact (:class:`str`).

        See class documentation for more information.
        """
        pass

    @property
    def relationship(self):
        """:class:`str` from a controlled vocabulary that defineds how this
        artifact is related to the Zenodo upload.

        See class documentation for more information.
        """
        pass
