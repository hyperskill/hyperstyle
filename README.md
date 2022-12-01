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

Python language (all versions can be found in the [requirements.txt](requirements.txt) file):

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

- [x]  PMD [BSD] (Version: 6.37.0)
    * [Site and docs](https://pmd.github.io/)
    * [Repository](https://github.com/pmd/pmd)
  
- [x]  Checkstyle [GNU LGPL v2.1] (Version: 8.44)
    * [Site and docs](https://checkstyle.sourceforge.io/)
    * [Repository](https://github.com/checkstyle/checkstyle)



Kotlin language:

- [x]  Detekt [Apache 2.0] (Version: 1.14.2)
    * [Site and docs](https://detekt.github.io/detekt/)
    * [Repository](https://github.com/detekt/detekt)



JavaScript language:

- [x]  ESlint [MIT] (Version: 7.5.0)
    * [Site and docs](https://eslint.org/)
    * [Repository](https://github.com/eslint/eslint)
  


Go language:

- [x] golangci-lint [GNU GPL v3.0] (Version: 1.49.0)
    * [Site and docs](https://golangci-lint.run/)
    * [Repository](https://github.com/golangci/golangci-lint)
---

## Installation

You have to create set of environment variables:
- `CHECKSTYLE_VERSION` (the value of the variable must be the same with its value in [Dockerfile](Dockerfile))
- `CHECKSTYLE_DIRECTORY` (the directory with `CHECKSTYLE` linter sources)
- `DETEKT_VERSION` (the value of the variable must be the same with its value in [Dockerfile](Dockerfile))
- `DETEKT_DIRECTORY` (the directory with `DETEKT` linter sources)
- `PMD_VERSION` (the value of the variable must be the same with its value in [Dockerfile](Dockerfile))
- `PMD_DIRECTORY` (the directory with `PMD` linter sources)
- `GOLANG_LINT_VERSION` (the value of the variable must be the same with its value in [Dockerfile](Dockerfile))
- `GOLANG_LINT_DIRECTORY` (the directory with `GOLANG_LINT` linter sources)

### Using script

Just run the following command:
```bash
./setup_environment.sh
```
and install everything the script suggests. 

**Note**: You can also use this script to update linters. To do this, just update the corresponding 
linter version variables, run the script, and reinstall only the necessary linters. 

### Manually

If you don't want to use the script, you can install the environment manually.

Simply clone the repository and run the following commands:

1. `pip install -r requirements.txt`
2. `pip install -r requirements-test.txt` for tests
3. `npm install eslint@7.5.0 -g && eslint --init`

You can download all linters sources manually or by the following commands:
- `CHECKSTYLE`: 
```bash
curl -L https://github.com/checkstyle/checkstyle/releases/download/checkstyle-${CHECKSTYLE_VERSION}/checkstyle-${CHECKSTYLE_VERSION}-all.jar > ${CHECKSTYLE_DIRECTORY}/checkstyle-${CHECKSTYLE_VERSION}-all.jar
```
- `DETEKT`: 
```bash
curl -sSLO https://github.com/detekt/detekt/releases/download/v${DETEKT_VERSION}/detekt-cli-${DETEKT_VERSION}.zip \
&& unzip detekt-cli-${DETEKT_VERSION}.zip -d ${DETEKT_DIRECTORY} \
&&  curl -H "Accept: application/zip" https://repo.maven.apache.org/maven2/io/gitlab/arturbosch/detekt/detekt-formatting/${DETEKT_VERSION}/detekt-formatting-${DETEKT_VERSION}.jar -o ${DETEKT_DIRECTORY}/detekt-formatting-${DETEKT_VERSION}.jar
```
- `PMD`: 
```bash
curl -sSLO https://github.com/pmd/pmd/releases/download/pmd_releases/${PMD_VERSION}/pmd-bin-${PMD_VERSION}.zip \
&& unzip pmd-bin-${PMD_VERSION}.zip -d ${PMD_DIRECTORY}
```
- `GOLANG_LINT`:
```bash
curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b ${GOLANG_LINT_DIRECTORY} v${GOLANG_LINT_VERSION}
```

### Using docker

Alternatively, you can build a docker image by [Dockerfile](Dockerfile) and run the tool inside this image.
Or use the public docker image, that we use in the [build.yml](.github/workflows/build.yml) file.

## Usage

Run the [run_tool.py](hyperstyle/src/python/review/run_tool.py) with the arguments.

A simple configuration: `python run_tool.py <path>`.

**Required arguments:**
1. **path** — path to file or directory to inspect.

Optional arguments:

Argument | Description
--- | ---
**&#8209;h**, **&#8209;&#8209;help**      |  show the help message and exit.
**&#8209;v**, **&#8209;&#8209;verbosity** |  choose logging level according [this](https://docs.python.org/3/library/logging.html#levels) list: `1` - **ERROR**; `2` - **INFO**; `3` - **DEBUG**; `0` - disable logging (**CRITICAL** value); default value is `0` (**CRITICAL**).
**&#8209;d**, **&#8209;&#8209;disable**   |  disable inspectors. Available values: for **Python** language: `pylint` for [Pylint](https://github.com/PyCQA/pylint), `flake8` for [flake8](https://flake8.pycqa.org/en/latest/), `radon` for [Radon](https://radon.readthedocs.io/en/latest/), `python_ast` to check different measures providing by AST; for **Java** language: `checkstyle` for the [Checkstyle](https://checkstyle.sourceforge.io/), `pmd` for [PMD](https://pmd.github.io/); for `Kotlin` language: detekt for [Detekt](https://detekt.github.io/detekt/); for **JavaScript** language: `eslint` for [ESlint](https://eslint.org/); for **Go** language: `golang_lint` for [golangci-lint](https://golangci-lint.run/). Example: `-d pylint,flake8`.
**&#8209;&#8209;allow-duplicates**        |  allow duplicate issues found by different linters. By default, duplicates are skipped.
**&#8209;&#8209;language-version**, **&#8209;&#8209;language_version**  |  specify the language version for JAVA inspectors. Available values: `java7`, `java8`, `java9`, `java11`, `java15`, `java17`. **Note**: **&#8209;&#8209;language_version** is deprecated and will be deleted in the future.
**&#8209;&#8209;n-cpu**, **&#8209;&#8209;n_cpu**  |  specify number of _cpu_ that can be used to run inspectors. **Note**: **&#8209;&#8209;n_cpu** is deprecated. Will be deleted in the future.
**&#8209;f**, **&#8209;&#8209;format**    |  the output format. Available values: `json`, `text`. Default value is `json`.
**&#8209;s**, **&#8209;&#8209;start-line**|  the first line to be analyzed. By default it starts from `1`.
**&#8209;e**, **&#8209;&#8209;end-line**  |  the end line to be analyzed. The default value is `None`, which meant to handle file by the end.
**&#8209;&#8209;new-format**              |  the argument determines whether the tool should use the _new format_. _New format_ means separating the result by the files to allow getting quality and observed issues for each file separately. The default value is `False`.
**&#8209;&#8209;history**                 |  JSON string with a list of issues for each language. For each issue its class and quantity are specified. Example: `--history "{\"python\": [{\"origin_class\": \"SC200\", \"number\": 20}, {\"origin_class\": \"WPS314\", \"number\": 3}]}"`
**&#8209;&#8209;with&#8209;all&#8209;categories** | Without this flag, all issues will be categorized into 5 main categories: `CODE_STYLE`, `BEST_PRACTICES`, `ERROR_PRONE`, `COMPLEXITY`, `INFO`.
**&#8209;&#8209;group&#8209;by&#8209;difficulty** | With this flag, the final grade and influence on penalty will be grouped by the issue difficulty.

The output examples:

(_New format_ means separating the result by the files to allow getting quality and observed issues for each file separately)

1. Json `old format` (without **&#8209;&#8209;new-format** argument):

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
      "category": "FUNC_LEN",
      "difficulty": "EASY",
      "influence_on_penalty": 0 
    },
    ...
  ]
}
```

2. Json `new format` (with **&#8209;&#8209;new-format** argument):

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
          "category": "BEST_PRACTICES", 
          "difficulty": "MEDIUM",
          "influence_on_penalty": 0 
        },
        ...
      ]
    }
  ]
}
```

3. Json `old format` (with **&#8209;&#8209;group&#8209;by&#8209;difficulty** argument):

```json
{
  "quality": {
    "EASY": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    },
    "MEDIUM": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    },
    "HARD": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    }
  },
  "issues": [
    {
      "code": "C002",
      "text": "Too long function. Try to split it into smaller functions / methods.It will make your code easy to understand and less error prone.",
      "line": "<the code line>",
      "line_number": 54,
      "column_number": 0,
      "category": "FUNC_LEN",
      "difficulty": "EASY",
      "influence_on_penalty": {
        "EASY": 0,
        "MEDIUM": 0,
        "HARD": 0
      }
    },
    ...
  ]
}
```

4. Json `new format` (with **&#8209;&#8209;group&#8209;by&#8209;difficulty** argument)

```json
{
  "quality": {
    "EASY": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    },
    "MEDIUM": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    },
    "HARD": {
      "code": "BAD",
      "text": "Code quality (beta): BAD"
    }
  },
  "file_review_results": [
    {
      "file_name": "<your file>",
      "quality": {
        "EASY": {
          "code": "BAD",
          "text": "Code quality (beta): BAD"
        },
        "MEDIUM": {
          "code": "BAD",
          "text": "Code quality (beta): BAD"
        },
        "HARD": {
          "code": "BAD",
          "text": "Code quality (beta): BAD"
        }
      },
      "issues": [
        {
          "code": "W0703",
          "text": "Catching too general exception Exception",
          "line": "<the code line>",
          "line_number": 174,
          "column_number": 12,
          "category": "BEST_PRACTICES",
          "difficulty": "MEDIUM",
          "influence_on_penalty": {
            "EASY": 0,
            "MEDIUM": 0,
            "HARD": 0
          }
        },
        ...
      ]
    }
  ]
}
```

5. Text format:

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
the [Dockerfile](Dockerfile) file.

Use `pytest` from the root directory to run __ALL__ tests.

