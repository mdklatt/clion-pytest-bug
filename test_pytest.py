""" Test a CLion pytest Run Configuration.

Attempting to reproduce an issue where a pytest Run Configuration fails due to
an import error, but running pytest via the command line works as expected, as
does running it manually using `_jb_pytest_runner.py`.

In this case, the import error is coming from the 'urllib3' library:

    .venv/lib/python3.9/site-packages/urllib3/response.py:390: in HTTPResponse
        DECODER_ERROR_CLASSES += (brotli.error,)
    E   AttributeError: module 'brotli' has no attribute 'error'

The library wil ignore 'brotli' if it's not installed for the project Python
interpreter, which should be the case here. When running pytest via CLion, an
outdated(?) version of 'brotli' is somehow being detected.

"""
import pytest


def test_true():
    assert True


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
