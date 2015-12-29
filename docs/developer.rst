###############
Developer Guide
###############

Zenodio is built for Python 3.4+.

Development Environment
=======================

Fork the Zenodio repository, and clone:

.. code-block:: bash

   git clone https://github.com/<username>/zenodio.git
   cd zenodio
   git remote add upstream https://github.com/lsst-sqre/zenodio.git

Setup a virtual environment, and install a development version of the code:

.. code-block:: bash

   pip install -r requirements.txt
   python setup.py develop

Style Guide
===========

Our code style is unadulterated PEP8 (*not* the LSST DM Python code style).
Use a `Flake8 <https://flake8.readthedocs.org/en/latest/>`_ to make sure your code is up to snuff.

Testing
=======

For testing we use `pytest <http://pytest.org/latest/>`_.
Don't use ``unittest``.

Run tests via:

.. code-block:: bash

   py.test

You can find tests in the :file:`tests/` directory.
If you need to include a sample dataset, put that data in the :file:`data/` directory.
Use setuptools's ``pkg_resources`` to read that data.
