#######
Zenodio
#######

Zenodo I/O
==========

Zenodio is a simple Python interface for getting data into and out of Zenodo_, the digital archive developed by CERN.
Zenodo_ is an awesome tool for scientists to archive the products of research, including datasets, codes, and documents.
Zenodio adds a layer of mechanization to Zenodo_, allowing you to grab metadata about records in a Zenodo_ collection, or upload new artifacts to Zenodo_ with a smart Python API.

We're still designing the upload API, but :doc:`metadata harvesting <harvest>` is ready to go.

Zenodio is built by SQuaRE for the Large Synoptic Survey Telescope.
`The code's on GitHub <https://github.com/lsst-sqre/zenodio>`_.

Install Zenodio
===============

Zenodio is runs on Python 3.4+.
You can install the latest release via:

.. code-block:: bash

   pip install zenodio

Or you can get the latest development version from GitHub:

.. code-block:: bash

   pip install git+git://github.com/lsst-sqre/zenodio.git

Developers will want to read the :doc:`Developer Guide <developer>`.

User Guide
==========

.. toctree::
   :maxdepth: 2

   metadata
   harvest
   developer

License
=======

Copyright 2015--2016 AURA/LSST

License: MIT.

.. _Zenodo: http://wwww.zenodo.org
