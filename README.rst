##################################
CLion Pytest Run Configuration Bug
##################################

This is a demonstration of a bug that effects `_CLion pytest run configurations`.
CLion builds a local index of header files used by a project for use with its
various code assistance features. These files can be seen in the *Header Search Paths*
section of the `Project window content pane`_.

The problem is that all of these paths are being injected into the Python
environment used to run pytest configurations (and presumably all Python run
configurations). Consider a project that uses a Docker toolchain for C++
development and a local Python virtualenv environment for various project
management tasks, such as integration tests written using pytest. The local
Python environment should be completely isolated from the Docker toolchain
environment.

In the real-world project where this bug was discovered, importing `urllib3`
in a pytest module was failing when the module was run from CLion. This same
module runs successfully from the command line using the local Python virtualenv.
The ``urllib3.response`` module optionally uses the ``brotli`` module if it is
available in the Python environment. The local pytest environment does not
have the ``brotli`` Python library installed, but the Docker image used as the
C++ toolchain does have the ``brotli`` C library headers installed. CLion
includes this path (``/urs/include/brotli``) when it runs pytest, and Python
interprets this is as a namespace package. Thus, ``urllib3`` thinks ``brotli``
is installed and fails when trying to use it.


******************
Steps to Reproduce
******************

Create the local development environment, including a Docker image to use as a
CLion C++ toolchain (Docker Engine must be running locally):

.. code-block::

    $ make dev

Execute pytest from the command line. All tests should pass.

.. code-block::

    $ make test


Open the project in CLion. Set up a C++ toolchain using the `clion-pytest-bug:latest`
Docker image. Once CLion has finished indexing the project, verify that ``brotli``
is listed as one of the *Header Search Paths* in the Project tool window.

Set the local Python virtualenv (``.venv/``) as the CLion Python interpreter.
Create a *pytest* run configuration to execute ``test_pytest.py`` using this
interpreter. Run the configuration; the test suite will fail. Use the debugger
to see that the value of ``brotli.__path__`` is the cached include path from
the C++ toolchain.


To reproduce the original bug in the real-world project where this was
discovered, install ``urlib3`` into the local virtualenv and attempt to import
it in ``test_pytest.py``.


.. _CLion pytest run configurations: https://www.jetbrains.com/help/clion/run-debug-configuration-py-test.html
.. _Project window content pane: https://www.jetbrains.com/help/clion/project-tool-window.html#content_pane