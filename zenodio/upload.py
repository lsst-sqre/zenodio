"""
Interface for uploading records to Zenodo through its RESTful API.
"""

import os
import json

import requests


def list_depositions(token=None, api_root='http://sandbox.zenodo.org'):
    """List your submitted depositions.

    Note that unsubmitted depositions don't appear in this list.
    In development; currently the raw json reponse is return.

    Parameters
    ----------
    token : str, optional
        Zenodo personal API token, obtained from
        https://zenodo.org/account/settings/applications/tokens
        If not provided, the token can be obtained from the ``ZENODO_TOKEN``
        environment variable.
    """
    token = _get_api_token(token)

    url = "{root}/api/deposit/depositions?access_token={token}"
    r = requests.get(url.format(root=api_root, token=token))
    print(r.status_code)  # FIXME
    return r.json()


class Deposition(object):
    """A Zenodo deposition, consisting of files and metadata.

    Parameters
    ----------
    deposition_id : int, option
        Identifier for a deposition. A new deposition will be created if
        an existing deposition ID is not provided.
    token : str, optional
        Zenodo personal API token, obtained from
        https://zenodo.org/account/settings/applications/tokens
        If not provided, the token can be obtained from the ``ZENODO_TOKEN``
        environment variable.
    """
    def __init__(self, deposition_id=None,
                 token=None,
                 api_root="http://sandbox.zenodo.org"):
        super().__init__()
        self._token = _get_api_token(token)

        self._api_root = api_root
        self._api_root = self._api_root.lstrip('/')

        # dict derived from JSON with a local copy of the deposition
        self._deposition_cache = dict()

        if deposition_id is None:
            # create a new, empty deposition
            self._create()
        else:
            self._get_deposition(deposition_id)

    @property
    def id(self):
        """ID for deposition on Zenodo (int)."""
        return self._deposition_cache['id']

    def update_metadata(self, **kwargs):
        """Update metadata for the deposition as key-value pairs

        Uses PUT deposit/depositions/:id

        The available metadata fields is available at
        https://zenodo.org/dev#collapse-r-meta

        Parameters
        ----------
        kwargs :
            Metadata key-value pairs, see
            https://zenodo.org/dev#collapse-r-dep
        """
        json_data = json.dumps(dict(**kwargs))

        headers = {"Content-Type": "application/json"}
        endpoint = 'deposit/depositions/{dep_id:d}'
        api_url = self._build_api_url(endpoint)
        print(api_url)
        r = requests.put(api_url,
                         data=json_data,
                         headers=headers)
        print('update_metatadata', r.status_code)  # FIXME
        self._deposition_cache.update(r.json())

    def upload_file(self, filepath):
        pass

    @property
    def file_names(self):
        """Names of files in the deposition."""
        filenames = [f['filename'] for f in self._deposition_cache['files']]
        return filenames

    def _create(self, data=None):
        """Create a deposition in Zenodo (that does not need to be complete).

        Calls POST deposit/depositions to CREATE a new deposition.
        https://zenodo.org/dev#collapse-create
        """
        if data is None:
            data = dict()

        json_data = json.dumps(data)

        headers = {"Content-Type": "application/json"}
        endpoint = 'deposit/depositions'
        api_url = self._build_api_url(endpoint)
        print(api_url)
        r = requests.post(api_url,
                          data=json_data,
                          headers=headers)
        print('_create_deposition', r.status_code)  # FIXME
        self._deposition_cache.update(r.json())

    def _get_deposition(self, deposition_id):
        """Get metadata for an *existing* deposition and upload the local
        metadata cache.

        Calls GET deposit/depositions/:id
        https://zenodo.org/dev#collapse-get
        """
        endpoint = 'deposit/depositions/{dep_id:d}'.format(
            dep_id=deposition_id)
        api_url = self._build_api_url(endpoint)
        print(api_url)
        r = requests.get(api_url)
        print('_get_deposition', r.status_code)
        self._deposition_cache = r.json()

    def _build_api_url(self, endpoint):
        endpoint = endpoint.lstrip('/')
        url = '{root}/api/{endpoint}?access_token={token}'
        return url.format(endpoint=endpoint,
                          root=self._api_root,
                          token=self._token)


def _get_api_token(provided_token=None, env_var='ZENODO_TOKEN'):
    if provided_token is None:
        # attempt to get a token from an environment variable instead
        api_token = os.getenv(env_var, default=None)
    else:
        api_token = provided_token

    if api_token is None:
        msg = 'Zenodo API token not found in ${0}. Get a token at set that ' \
              'environment variable'.format(env_var)
        raise EnvironmentError(msg)

    return api_token
