#####################################################
Harvesting Zenodo Metadata with OAI-PMH (DataCite v3)
#####################################################

Zenodio's :mod:`zenodio.harvest` module provides a Pythonic interface to record metadata in a Zenodo community collection.
Zenodio uses the standard OAI-PMH harvesting protocol (and specifically retrieves DataCite v3-flavored XML; it's the best and latest metadata standard used by Zenodo).

Quick Start
===========

To quickly show you harvesting metadata from Zenodo works, we'll get records from from LSST Data Management's `lsst-dm <https://zenodo.org/collection/user-lsst-dm>`_ Community:
You begin by providing the community's identifier to :func:`zenodio.harvest.harvest_collection`:

.. code-block:: py

   import zenodio.harvest
   collection = harvest_collection('lsst-dm')

``collection`` is a :class:`zenodio.harvest.Datacite3Collection` instance for the Zenodo community's record collection.
Use its :meth:`~zenodio.harvest.Datacite.records` method to generate :class:`~zenodio.harvest.Datacite3Record` instances for each record stored in the Zenodo community:

.. code-block:: py

   for record in collection.records():
      print(record.title)

Or you can get a list of all records:

.. code-block:: py

   records = [r for r in collection.records()]

With these :class:`~zenodio.harvest.Datacite3Record` instances you can access information about individual artifacts on Zenodo through simple class attributes.
For example:

.. code-block:: py

   record = records[0]
   print(record.title)
   print(record.issue_date)
   print(record.doi)
   print(record.abstract_html)

For information about authors, Zenodio provides an :class:`~zenodio.harvest.Author` class.
For example:

.. code-block:: py

   authors = record.authors
   print(','.join([a.last_name for a in authors]))


API Reference
=============

Convenience Functions
---------------------

.. autofunction:: zenodio.harvest.harvest_collection

Metadata Classes
----------------

.. autoclass:: zenodio.harvest.Datacite3Collection
   :members:

.. autoclass:: zenodio.harvest.Datacite3Record
   :members:

.. autoclass:: zenodio.harvest.Author
   :members:
