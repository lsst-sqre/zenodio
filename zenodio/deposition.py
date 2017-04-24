"""
Interface for uploading records to Zenodo through its RESTful API.

"""
import os
import requests
import json
from dateutil import parser
import hashlib


def checksum_md5(file_path):
    """Calculate md5 checksum of a file

    Works even on large files, by chunking rather than loading
    the entire file into memory.

    From https://stackoverflow.com/questions/1131220/
    """
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)

    # Match the format used by Zenodo's checksum
    return 'md5:%s' % md5.hexdigest()


class Deposition():
    """A Zenodo deposition, consisting of files and metadata.

    Methods:
    - list_all_depositions
    - upload_files
    - publish
    - delete

    Attributes (ALL EXCEPT metadata ARE READ-ONLY):
    - created
    - doi
    - doi_url
    - files
    - id
    - metadata
    - modified
    - owner
    - record_id
     (actually, while `record_url` is present in API documentation, it is
     not actually returned by the API, so we leave it out):
    - record_url
    - state
    - submitted
    - title

    """
    _headers = {"Content-Type": "application/json"}

    @staticmethod
    def list_all_depositions(access_token, use_sandbox=False):
        """
        Note that unsubmitted depositions don't appear in this list.

        Parameters
        ----------
        access_token: str
        use_sandbox: bool

        Returns
        -------
        A list of deposition ids

        """
        if use_sandbox:
            _deposit_url = "https://sandbox.zenodo.org/api/deposit/depositions"
        else:
            _deposit_url = "https://zenodo.org/api/deposit/depositions"

        _token_str = "?access_token=%s" % access_token

        r = requests.get(_deposit_url + _token_str)

        return [r['id'] for r in r.json()]

    def __init__(self, access_token, deposition_id=None, use_sandbox=False):
        """
        Parameters
        ----------

        access_token: str
            The access token
        deposition_id: int
            The deposition id to be retrieved.  If None is specified,
            a new deposition and id will be created on the server.
        use_sandbox: bool
            If True, use Zenodo's developer sandbox instead of
            the real site.
        """
        self._access_token = access_token
        self._use_sandbox = use_sandbox

        # Ensure the access token is valid before proceeding
        self._test_access_token()

        if deposition_id is None:
            # Create a new, empty deposition
            self._create()
        else:
            # Load the desired deposition
            self._retrieve(deposition_id)

    def _create(self):
        """Start a new empty Zenodo record
        """
        r = requests.post(self._deposit_url + self._token_str,
                          data="{}",
                          headers=self._headers)
        if r.status_code != 201:
            raise Exception("Error creating resource: " + str(r.json()))

        self._update_attributes(r)

    def _retrieve(self, deposition_id):
        """Load a deposition from Zenodo
        """
        r = requests.get(
            self._deposit_url +
            self._token_str +
            '/' +
            str(deposition_id) +
            self._token_str)

        self._update_attributes(r)

    def _update_attributes(self, r):
        self.created = parser.parse(r.json()['created'])
        self.files = r.json()['files']
        self.deposition_id = r.json()['id']
        self._metadata = r.json()['metadata']
        self.modified = parser.parse(r.json()['modified'])
        self.owner = r.json()['owner']
        self.state = r.json()['state']
        self.title = r.json()['title']

        if self.submitted:
            # These attributes are only present in published depositions
            self.doi = r.json()['doi']
            self.doi_url = str(r.json()['doi_url'])
            self.record_id = r.json()['record_id']
            # Although the published Zenodo API claims this is present
            # for published depositions, it appears to not be there, so
            # here we comment it out.
            # self.record_url = str(r.json()['record_url'])

    def append_file(self, file_path):
        """
        Append a file to the Zenodo deposition.

        (Called "upload" in the Zenodo API)

        Note: Files can only be changed if the deposition is not yet submitted.

        """
        if self.submitted:
            raise Exception("Files can only be added if the deposition "
                            "is not yet submitted.")

        # Ensure the file exists
        if not os.path.isfile(file_path):
            raise Exception("Error: the specified file does not exist: %s "
                            % file_path)

        data = {'filename': os.path.basename(file_path)}
        files = {'file': open(file_path, 'rb')}
        r = requests.post(
            (self._deposit_url + '/' + str(self.deposition_id) + '/files' +
             self._token_str),
            data=data, files=files)
        if r.status_code != 201:
            raise Exception("Error uploading resource %s: %s" %
                            (file_path, r.json()))

        # Every time we upload a file, the files list should expand
        self.files.append(r.json())

        # Validate the integrity of the uploaded file via its checksum
        local_md5 = checksum_md5(file_path)
        remote_md5 = r.json()['checksum']
        if local_md5 != remote_md5:
            raise Exception(
                "Error uploading file: Checksums do not match. "
                "%s is local, %s is remote" %
                (local_md5, remote_md5))

    @property
    def metadata(self):
        """JSON-serializable dict; A deposition metadata resource
        """
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        # Check that the metadata submitted is JSON-serializable
        try:
            metadata_str = json.dumps(value)
        except TypeError as err:
            print("Error: The provided metadata is not valid JSON: %s" % err)
            raise

        # Amend metadata
        r = requests.put((self._deposit_url + '/' + str(self.deposition_id) +
                          self._token_str),
                         data=metadata_str, headers=self._headers)

        if r.status_code != 200:
            raise Exception("Error amending metadata for resource: %s" %
                            r.json())

        # Now that we've updated it on the server, let's have our object
        # reflect the metadata changes
        self._update_attributes(r)

    def publish(self):
        # Publish the resource
        r = requests.post(self._deposit_url + '/' + str(self.deposition_id) +
                          '/actions/publish' + self._token_str)
        if r.status_code != 202:
            raise Exception("Error publishing resource: %s" % str(r.json()))

        self._update_attributes(r)

    def delete(self):
        """Deletes this deposition on Zenodo.
        This object should not be used afterwards.
        """
        r = requests.delete(self._deposit_url + '/' + str(self.deposition_id) +
                            self._token_str)
        if r.status_code != 204:
            raise Exception("Error deleting resource: %s" % str(r.json()))

    def _test_access_token(self):
        # Test the access token
        r = requests.get(self._deposit_url + self._token_str)
        if r.status_code != 200:
            raise Exception("Error: Access Token not accepted: " +
                            str(r.json()))

    @property
    def filenames(self):
        """ Returns a list of the file names
        """
        return [f['filename'] for f in self.files]

    @property
    def _deposit_url(self):
        if self._use_sandbox:
            return "https://sandbox.zenodo.org/api/deposit/depositions"
        else:
            return "https://zenodo.org/api/deposit/depositions"

    @property
    def _token_str(self):
        return '?access_token=%s' % self._access_token

    @property
    def submitted(self):
        """Bool; True of deposition has been published, False otherwise.
        """
        return self.state == "done"
