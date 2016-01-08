import os

from zenodio.upload import _get_api_token


def test_get_api_token():
    orig_env = os.getenv('ZENODO_TOKEN')
    if orig_env is not None:
        # Using the environment variable
        assert orig_env == _get_api_token()

    test_key = "test_api_key"

    # test using the provided key
    assert test_key == _get_api_token(provided_token=test_key)
