""" Test pytest execution via CLion.

"""
import pytest


# Adapted from the urllib3.response module, the real-world origin of this bug.
# The 'brotli' library is not installed in the Python environment used for
# running tests, so it should set to None here.
try:
    try:
        import brotlicffi as brotli
    except ImportError:
        import brotli
except ImportError:
    brotli = None


# In some other projects, this import triggers an error when this is executed
# in CLion as pytest run configuration, but not when running pytest via the
# command line (`make pytest`) or manually running the CLion pytest runner
# script (`make pytest-jb`)
#
#    .venv/lib/python3.9/site-packages/urllib3/response.py:390: in HTTPResponse
#        DECODER_ERROR_CLASSES += (brotli.error,)
#    E   AttributeError: module 'brotli' has no attribute 'error'
#
# The urllib3 code checks if 'brotli' is installed and ignored if it's not,
# which is true here. Not sure where the outdated(?) version of 'brotli' is
# coming from when running via CLion, or why this cannot be reproduced here.


def test_brotli():
    """ Ensure that the 'brotli' library is not found.

    This will pass when tests are run via the command line, but fail when run
    in CLion as a 'pytest' run configuration. The problem is that CLion is
    injecting the header paths from the C++ toolchain into the Python
    environment used to run the tests. Python sees /usr/include/brotli in the
    project's Docker container as a namespace package, and imports it as such.

    To see this, set a breakpoint on the `assert` and run this as a debug
    configuration. The value of `brotli.__path__` will point to a CLion cache
    directory.

    """
    assert brotli is None


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
