import pkg_resources
import pytest
import sys
import urllib

from zenodio.deposition import Deposition


def test_upload_resource():
    book_path = 'WealthOfNations.pdf'
    urllib.request.urlretrieve(
        "http://www.ibiblio.org/ml/libri/s/SmithA_WealthNations_p.pdf",
        book_path)

    book_metadata = {"metadata": {
        "title": ("An Inquiry into the Nature and Causes of the Wealth of "
                  "Nations"),
        "upload_type": "publication",
        "publication_type": "book",
        "publication_date": "1776-03-09",
        "description": "A description of what builds nations' wealth.",
        "creators": [{"name": "Smith, Adam",
                      "affiliation": "University of Glasgow"}]
        }}

    # TODO: figure out how to test uploading without hardcoding my access token
    # perhaps by somehow getting it into an environment variable, then:
    # ACCESS_TOKEN = os.getenv('ZENODO_TOKEN', default=None)
    ACCESS_TOKEN = '____'  # insert token here

    # Currently all we can test is that it fails without a proper access token
    with pytest.raises(Exception):
        d = Deposition(ACCESS_TOKEN, sandbox=True)

    # DEBUG
    return True
    # DEBUG: the below code will only work once we have an access token

    d = Deposition(ACCESS_TOKEN, sandbox=True)
    d.upload_file(book_path)
    d.metadata = book_metadata
    d.publish()
    assert(d.title == book_metadata["metadata"]["title"])

    d2 = Deposition(ACCESS_TOKEN, sandbox=True)
    d2.load_record(d.doi)
    assert(d.title == d2.title)
    d2.publish()
    assert(d2.doi != d.doi)
