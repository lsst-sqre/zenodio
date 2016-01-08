"""
Interface for uploading records to Zenodo through its RESTful API.
"""

import os
import json

import requests


class Deposition(object):
    """A Zenodo deposition, consisting of files and metadata.

    Parameters
    ----------
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
            self._create_deposition()
        else:
            self._get_deposition(deposition_id)

    @property
    def id(self):
        """ID for deposition on Zenodo (str)."""
        return self._deposition_cache['id']

    def _create_deposition(self, data=None):
        """Create a deposition in Zenodo (that does not need to be complete).
        """
        if data is None:
            data = dict()

        json_data = json.dumps(data)

        headers = {"Content-Type": "application/json"}
        endpoint = '{root}/api/deposit/depositions?access_token={token}'
        r = requests.post(endpoint.format(root=self._api_root,
                                          token=self._token),
                          data=json_data,
                          headers=headers)
        print('_create_deposition', r.status_code)  # FIXME
        self._deposition_cache.update(r.json())

    def _get_deposition(self, deposition_id):
        """Get metadata for an *existing* deposition and upload the local
        metadata cache.
        """
        self._deposition_cache = {}  # FIXME implement GET


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
