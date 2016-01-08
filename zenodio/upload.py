"""
Interface for uploading records to Zenodo through its RESTful API.
"""

import os


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
    def __init__(self, token=None):
        super().__init__()
        self._token = _get_api_token(token)


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
