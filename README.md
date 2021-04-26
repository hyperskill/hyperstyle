![Python build](https://github.com/hyperskill/hyperstyle/workflows/Python%20build/badge.svg?branch=develop)

# Hyperstyle

A tool for running a set of pre-configured linters and evaluating code quality.
It is used on the [Hyperskill](https://hyperskill.org/) platform 
to check the quality of learners' code.

[Read more detail about the project at Hyperskill Help Center](https://support.hyperskill.org/hc/en-us/articles/360049582712-Code-style-Code-quality)

[The dockerized version](https://hub.docker.com/r/stepik/hyperstyle/tags)

## What it does:

* Runs linters for several programming languages and parses their output;
* Prints the result using a unified JSON-based format;
* Evaluates the code quality value (**EXCELLENT**, **GOOD**, **MODERATE**, or **BAD**) 
based on the linters' output and some heuristics.


## License and 3rd party software

The source code of **hyperstyle** is distributed under the Apache 2.0 License.

The 3rd party software we use in this project has its own licenses.

Python language:

- [x]  flake8 [MIT]
    * [Site and docs](https://flake8.pycqa.org/en/latest/)
    * [Repository](https://github.com/PyCQA/flake8)
  
- [x]  Pylint [GNU LGPL v2]
    * [Site and docs](https://www.pylint.org/)
    * [Repository](https://github.com/PyCQA/pylint)
   
- [x] Radon [MIT]
    * [Site and docs](https://radon.readthedocs.io/en/latest/)
    * [Repository](https://github.com/rubik/radon)

Java language:

- [x]  PMD [BSD]
    * [Site and docs](https://pmd.github.io/)
    * [Repository](https://github.com/pmd/pmd)
  
- [x]  Checkstyle [GNU LGPL v2.1]
    * [Site and docs](https://checkstyle.sourceforge.io/)
    * [Repository](https://github.com/checkstyle/checkstyle)
  
- [ ]  SpotBugs [GNU LGPL v2.1]
    * [Site and docs](https://spotbugs.github.io/)
    * [Repository](https://github.com/spotbugs/spotbugs)
  
- [ ]  SpringLint
    * [Repository](https://github.com/mauricioaniche/springlint)



Kotlin language:

- [x]  Detekt [Apache 2.0]
    * [Site and docs](https://detekt.github.io/detekt/)
    * [Repository](https://github.com/detekt/detekt)



JavaScript language:

- [x]  ESlint [MIT]
    * [Site and docs](https://eslint.org/)
    * [Repository](https://github.com/eslint/eslint)
  
---

## Installation

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r requirements-test.txt` for tests

## Usage

Run the [run_tool.py](./src/python/review/run_tool.py) with the arguments.

A simple configuration: `python run_tool.py <path>`.

**Required arguments:**
1. **path** — path to file or directory to inspect.

Optional arguments:

Argument | Description
--- | ---
**&#8209;h**, **&#8209;&#8209;help**      |  show the help message and exit.
**&#8209;v**, **&#8209;&#8209;verbosity** |  choose logging level according [this](https://docs.python.org/3/library/logging.html#levels) list: `1` - **ERROR**; `2` - **INFO**; `3` - **DEBUG**; `0` - disable logging (**CRITICAL** value); default value is `0` (**CRITICAL**).
**&#8209;d**, **&#8209;&#8209;disable**   |  disable inspectors. Available values: for **Python** language: `pylint` for [Pylint](https://github.com/PyCQA/pylint), `flake8` for [flake8](https://flake8.pycqa.org/en/latest/), `radon` for [Radon](https://radon.readthedocs.io/en/latest/), `python_ast` to check different measures providing by AST; for **Java** language: `checkstyle` for the [Checkstyle](https://checkstyle.sourceforge.io/), `pmd` for [PMD](https://pmd.github.io/); for `Kotlin` language: detekt for [Detekt](https://detekt.github.io/detekt/); for **JavaScript** language: `eslint` for [ESlint](https://eslint.org/). Example: `-d pylint,flake8`.
**&#8209;&#8209;allow-duplicates**        |  allow duplicate issues found by different linters. By default, duplicates are skipped.
**&#8209;&#8209;language-version**, **&#8209;&#8209;language_version** |  specify the language version for JAVA inspectors. Available values: `java7`, `java8`, `java9`, `java11`. **Note**: **&#8209;&#8209;language_version** is deprecated. Will be deleted in the future.
**&#8209;&#8209;n-cpu**, **&#8209;&#8209;n_cpu**  |  specify number of _cpu_ that can be used to run inspectors. **Note**: **&#8209;&#8209;n_cpu** is deprecated. Will be deleted in the future.
**&#8209;f**, **&#8209;&#8209;format**    |  the output format. Available values: `json`, `text`. Default value is `json`.
**&#8209;s**, **&#8209;&#8209;start-line**|  the first line to be analyzed. By default it starts from `1`.
**&#8209;e**, **&#8209;&#8209;end-line**  |  the end line to be analyzed. The default value is `None`, which meant to handle file by the end.
**&#8209;&#8209;new-format**              |  the argument determines whether the tool should use the _new format_. _New format_ means separating the result by the files to allow getting quality and observed issues for each file separately. The default value is `False`.

The output examples:

(_New format_ means separating the result by the files to allow getting quality and observed issues for each file separately)

1. Json `old format` (without **&#8209;&#8209;new_format** argument):

```json
{
  "quality": {
    "code": "BAD",
    "text": "Code quality (beta): BAD"
  },
  "issues": [
    {
      "code": "C002",
      "text": "Too long function. Try to split it into smaller functions / methods.It will make your code easy to understand and less error prone.",
      "line": "<the code line>",
      "line_number": 54,
      "column_number": 0,
      "category": "FUNC_LEN"
    },
    ...
  ]
}
```

2. Json `new format` (with **&#8209;&#8209;new_format** argument):

```json
{
  "quality": {
    "code": "BAD",
    "text": "Code quality (beta): BAD"
  },
  "file_review_results": [
    {
      "file_name": "<your file>",
      "quality": {
        "code": "BAD",
        "text": "Code quality (beta): BAD"
      },
      "issues": [
        {
          "code": "W0703",
          "text": "Catching too general exception Exception",
          "line": "<the code line>",
          "line_number": 174,
          "column_number": 12,
          "category": "BEST_PRACTICES"
        },
        ...
      ]
    }
  ]
}
```

3. Text format:

```text
Review of <path to your file or project> (N violations)
***********************************************************************************************************
File <file_name>
-----------------------------------------------------------------------------------------------------------
Line № : Column № : Type     : Inspector  : Origin : Description   : Line         : Path
54     : 0        : FUNC_LEN : PYTHON_AST : C002   : <Description> : <code line > : <path to the file>
...
-----------------------------------------------------------------------------------------------------------
Code quality (beta): BAD
Next level: EXCELLENT
Next level requirements:
FUNC_LEN: 12

***********************************************************************************************************
General quality:
Code quality (beta): BAD
Next level: EXCELLENT
Next level requirements:
FUNC_LEN: 12
```

---

## Tests running

We use [`pytest`](https://docs.pytest.org/en/latest/contents.html) library for tests.

__Note__: If you have `ModuleNotFoundError` while you try to run tests, please call `pip install -e .`
 before using the test system.

__Note__: We use [eslint](https://eslint.org/) and [open-jdk 11](https://openjdk.java.net/projects/jdk/11/)
in the tests. Please, set up the environment before running the tests. 
You can see en example of the environment configuration in 
the [build.yml](./.github/workflows/build.yml) file.

Use `pytest` from the root directory to run __ALL__ tests.

