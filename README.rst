============
Auto Suggest
============


.. image:: https://img.shields.io/pypi/v/autosuggest.svg
        :target: https://pypi.python.org/pypi/autosuggest

.. image:: https://img.shields.io/travis/armandgiraud/autosuggest.svg
        :target: https://travis-ci.org/armandgiraud/autosuggest

.. image:: https://readthedocs.org/projects/autosuggest/badge/?version=latest
        :target: https://autosuggest.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




suggest requests from prefix for code du travail numérique


* Free software: GNU General Public License v3


Install
--------
```pip install .```
``pip install git+https://github.com/ArmandGiraud/autosuggest.git``

Features
--------

* Basic usage:

.. code-block:: python

   from autosuggest import AutoSuggestor

    auto = autoSuggestor(build_precount = False) # use precount = False for fast instanciation
    auto.auto_suggest_fast("co")

Test
----

python -m unittest discover tests

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
