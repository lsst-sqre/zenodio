#######
Zenodio
#######

Input and Output for Zenodo
===========================

Zenodio is a simple Python interface getting data into and out of Zenodo_, the digital archive developed by CERN.
Zenodo_ is an awesome tool for modern scientists to archive the products of research, including datasets, codes, and documents.
Zenodio adds a layer of mechanization to Zenodo_, allowing you to grab metadata about records in a Zenodo_ collection, or upload new artifacts to Zenodo_ with smart, templated metadata specification.

We're still designing the upload API, but metadata harvesting is ready to go.

Zenodio is built by SQuaRE for the Large Synoptic Survey Telescope.
`The code's on GitHub <https://github.com/lsst-sqre/zenodio>`_.

Install Zenodio
===============

Zenodio is built for Python 3.4+.
You can install the latest release via:

.. code-block:: bash

   pip install zenodio

Or you can get the latest version from GitHub:

.. code-block:: bash

   pip install git+git://github.com/lsst-sqre/zenodio.git

Developers will want to read the :ref:`developer guide <dev>`.

User Guide
==========

.. toctree::
   :maxdepth: 2

   harvest

.. _dev:

Developer Guide
===============

Zenodio is built for Python 3.4+.
Have fun.

Development Environment
-----------------------

Fork the Zenodio repository, and clone:

.. code-block:: bash

   git clone https://github.com/<username>/zenodio.git
   cd zenodio
   git remote add upstream https://github.com/lsst-sqre/zenodio.git

Setup a virtual environment, and install a development version of the code

.. code-block:: bash

   pip install -r requirements.txt
   python setup.py develop

Style Guide
-----------

Our code style is unadulterated PEP8 (*not* the LSST DM Python code style).
Use a `Flake8 <https://flake8.readthedocs.org/en/latest/>`_ to make sure your code is up to snuff.

Testing
-------

For testing we use `pytest <http://pytest.org/latest/>`_.
Don't use ``unittest2``.

Run tests via:

.. code-block:: bash

   py.test

You can find tests in the :file:`tests/` directory.
If you need to include a sample dataset, put that data in the :file:`data/` directory.
Use setuptools's `pkg_resources` to read that data.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Zenodo: http://wwww.zenodo.org
