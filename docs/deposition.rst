#####################################################
Zenodo Depositions
#####################################################

Zenodio's :mod:`zenodio.deposition` module provides a Pythonic interface to upload and load Zenodo depositions.

Quick Start
===========

.. code-block:: py

    import urllib
    from zenodio.deposition import Deposition
    
    book_path = 'WealthOfNations.pdf'
    urllib.request.urlretrieve(
        "http://www.ibiblio.org/ml/libri/s/SmithA_WealthNations_p.pdf",
        book_path)
    
    book_metadata = {"metadata": {
        "title": "An Inquiry into the Nature and Causes of the Wealth of Nations",
        "upload_type": "publication",
        "publication_type": "book",
        "publication_date": "1776-03-09",
        "description": "A description of what builds nations' wealth.",
        "creators": [{"name": "Smith, Adam",
                      "affiliation": "University of Glasgow"}]
        }}

    # NOTE: Smith's ACCESS_TOKEN is not specified here. He would have to follow
    # these steps: https://zenodo.org/dev#restapi-auth to obtain a value.
    d = Deposition(ACCESS_TOKEN, use_sandbox=True)
    d.append_file(book_path)
    d.metadata = book_metadata
    d.publish()

API Reference
=============

Classes
----------------

.. autoclass:: zenodio.deposition.Deposition
   :members:
