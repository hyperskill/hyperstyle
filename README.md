# hyperstyle

A tool for running a set of pre-configured linters and evaluating code quality.
It is used on the [Hyperskill](https://hyperskill.org/) platform 
to check the quality of learners' code.

[Read more detail about the project at Hyperskill Help Center](https://support.hyperskill.org/hc/en-us/articles/360049582712-Code-style-Code-quality)

[The dockerized version](https://hub.docker.com/r/stepik/hyperstyle/tags)

## What it does:
* runs linters for several programming languages and parses their output
* prints the result using a unified JSON-based format
* evaluates the code quality value (**EXCELLENT**, **GOOD**, **MODERATE**, or **BAD**) 
based on the linters' output and some heuristics


## License and 3rd party software

The source code of **hyperstyle** is distributed under the Apache 2.0 License.

The 3rd party software we use in this project has its own licenses.

* Checkstyle [GNU LGPL v2.1]
    * [Site and docs](https://checkstyle.sourceforge.io/)
    * [Repository](https://github.com/checkstyle/checkstyle)

* Detekt [Apache 2.0]
    * [Site and docs](https://detekt.github.io/detekt/)
    * [Repository](https://github.com/detekt/detekt)

* ESlint [MIT]
    * [Site and docs](https://eslint.org/)
    * [Repository](https://github.com/eslint/eslint)
    
* flake8 [MIT]
    * [Site and docs](https://flake8.pycqa.org/en/latest/)
    * [Repository](https://github.com/PyCQA/flake8)

* PMD [BSD]
    * [Site and docs](https://pmd.github.io/)
    * [Repository](https://github.com/pmd/pmd)

* Pylint [GNU LGPL v2]
    * [Site and docs](https://www.pylint.org/)
    * [Repository](https://github.com/PyCQA/pylint)

* SpotBugs [GNU LGPL v2.1]
    * [Site and docs](https://spotbugs.github.io/)
    * [Repository](https://github.com/spotbugs/spotbugs)

* SpringLint
    * [Repository](https://github.com/mauricioaniche/springlint)
  
---

## Installation

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r requirements-test.txt`

---

## Tests running

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.

Use `pytest test` from the root directory to run __ALL__ tests.
