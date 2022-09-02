# Contributing Guidelines

In this document you will find a detailed description of how to add new functionality to Hyperstyle.

## Contents

1. [Adding a new inspector for an existing language](#adding-a-new-inspector-for-an-existing-language).
2. [Adding a new inspector for a new language](#adding-a-new-inspector-for-a-new-language).

## Adding a new inspector for an existing language

If you want to add a new inspector for an existing language, you need to:
1. Inherit from the [`BaseInspector`](hyperstyle/src/python/review/inspectors/base_inspector.py#L9) class.
2. Define the [`inspector_type`](hyperstyle/src/python/review/inspectors/base_inspector.py#L29) property. To do this, you need to update the [`InspectorType`](hyperstyle/src/python/review/inspectors/inspector_type.py#L6) class by adding there a name of the inspector.
3. Implement the [`inspect`](hyperstyle/src/python/review/inspectors/base_inspector.py#L33) function, which should run an analysis of the language and return a list of found issues;

Usually the inspector runs a third-party linter through a command line and parses its result. In this case it will be useful to implement several auxiliary functions:
1. `create_command` – creates a command to run the linter via subprocess.
2. `parse` – parses the linter's result and returns the list of found issues. For more details about the implementation of this function, see [this](#implementation-of-the-parse-function) section.
3. `choose_issue_type` – selects an issue type by its origin class. This function usually uses the `ORIGIN_CLASS_TO_ISSUE_TYPE` dictionary, stored next to the inspector, to select the issue type. Also the `ORIGIN_CLASS_PREFIX_TO_ISSUE_TYPE` dictionary can sometimes be useful to determine the type of groups of issues.

Usually the third-party linter needs a configuration file to run. This file should be stored next to the inspector.

An example of inspectors that are implemented in such a way: [`PMDInpsector`](hyperstyle/src/python/review/inspectors/pmd), [`GolangLintInspector`](hyperstyle/src/python/review/inspectors/golang_lint), [`Flake8Inspector`](hyperstyle/src/python/review/inspectors/flake8).

If the inspector does not need the third-party linter (for example, if the inspector works with a code directly), then the above functions are not necessary. In this case, each such inspector is implemented uniquely. Currently, only one inspector of this kind is implemented in Hyperstyle: [`PythonAstInspector`](hyperstyle/src/python/review/inspectors/pyast).

After implementing all the necessary functions, you need to add the inspector instance to the [`LANGUAGE_TO_INSPECTORS`](hyperstyle/src/python/review/reviewers/common.py#L28) dictionary, and update the main [README](README.md) file with a mention of the new inspector there.

If you are implementing the inspector that uses the third-party linter, you must also update the [Dockerfile](Dockerfile) with necessary environment variables and commands to install the linter, and update the [README](README.md) file and the [`setup_environment.sh`](setup_environment.sh) script in the same way.

### Implementation of the `parse` function

Usually, the `parse` function parses the result of the third-party linter line-by-line, then creates a base issue using the [`BaseIssue`](hyperstyle/src/python/review/inspectors/issue.py#L199) dataclass, which is later converted to either [`CodeIssue`](hyperstyle/src/python/review/inspectors/issue.py#L217) or one of the measurable issues using the [`convert_base_issue`](hyperstyle/src/python/review/inspectors/common/base_issue_converter.py#L17) function and an instance of the [`IssueConigsHandler`](hyperstyle/src/python/review/inspectors/issue_configs.py#L117) class. The resulting issue is added to the general list of found issues and this list is returned from the function after the parsing is finished.

The `IssueConfigHandler` class handles custom issue descriptions and also parses metrics from their descriptions (examples of metrics are: line or function length, cyclomatic complexity, maintainability index).  It receives instances of [`IssueConfig`](hyperstyle/src/python/review/inspectors/issue_configs.py#L46) or [`MeasurableIssueConfig`](hyperstyle/src/python/review/inspectors/issue_configs.py#L85) classes as input, which should be stored in the `ISSUE_CONFIGS` list next to the inspector.

Also, if the third-party linter supports output in "Checkstyle" format, you can use the [`parse_xml_file_result`](hyperstyle/src/python/review/inspectors/common/xml_parser.py#L47) function to parse the output file.

### Checklist

A sample checklist for adding a new inspector looks like this:
- [ ] I've inherited from the `BaseInspector` class.
- [ ] I've implemented the `inspect` function and _if needed_ I've added a check for the existence of third-party linter environment variables using the [`check_set_up_env_variable`](hyperstyle/src/python/review/common/file_system.py#L124) function.
- [ ] I've added a new inspector type to the `InspectorType` class, updated the [`available_values`](hyperstyle/src/python/review/inspectors/inspector_type.py#L27) function and defined the inspector type.
- [ ] _If needed_. I've added a config to run the third-party linter.
- [ ] _If needed_. I've implemented the `create_command` function.
- [ ] _if needed_. I've implemented the `parse` function and defined the `ISSUES_CONFIGS` list in a separate file.
- [ ] _If needed_. I've implemented the `choose_issue_type` function and defined the `ORIGIN_CLASS_TO_ISSUE_TYPE` dictionary in a separate file.
- [ ] I've added an instance of the new inspector to the `LANGUAGE_TO_INSPECTORS` dictionary.
- [ ] I've updated the main README file: 
	- [ ] I've added an information about the new inspector.
	- [ ] I've updated a description of the `--disable` flag.
	- [ ] _If needed_. I've added an information about the new linter environment variables.
	- [ ] _If needed_. I've added a command to manually install the third-party linter.
- [ ] _If needed_. I've updated the Dockerfile with the new linter environment variables and commands to install the third-party linter.
- [ ] I've added tests to check the inspector:
	- [ ] _If needed_. The linter's output parsing is working correctly.
	- [ ] _If needed_. The issue categorization is working correctly.
	- [ ] The total number of issues from a source code is collected correctly.
	- [ ] The number of issues of each type from a source code is collected correctly.
	- [ ] _If needed_. Metric issues are parsed correctly.
	- [ ] _If needed_. Custom issues descriptions are added correctly.

## Adding a new inspector for a new language

Before you can add a new inspector, you must add support for a new language to Hyperstyle. To do this, you must do the following:
1. Add a new language in the [`Language`](hyperstyle/src/python/review/common/language.py#L10) class.
2. Add a version of the new language in the [`LanguageVersion`](hyperstyle/src/python/review/application_config.py#L24) class.
3. Add file extensions of the new language in the [`Extension`](hyperstyle/src/python/review/common/file_system.py#L28) class.
4. Define configurations for the new language in the [`rules`](hyperstyle/src/python/review/quality/rules/) module.
5. Add an entry for the new language in the [`language_to_reviewer`](hyperstyle/src/python/review/reviewers/perform_review.py#L31) dictionary.

Next, use the "[Adding a new inspector for an existing language](#adding-a-new-inspector-for-an-existing-language)" guideline.

### Checklist

A sample checklist for adding a new linter looks like this:
- [ ] I've added a new language to the `Language` class, updated the [`from_language_version`](hyperstyle/src/python/review/common/language.py#L18) function and the [`EXTENSION_TO_LANGUAGE`](hyperstyle/src/python/review/common/language.py#L45) dictionary.
- [ ] I've added a version of the new language to `LanguageVersion`.
- [ ] I've added new language file extensions to the `Extensions` class and updated the [`language_to_extension_dict`](#hyperstyle/src/python/review/application_config.py#L40) dictionary.
- [ ] I've defined rule configs for the new language.
- [ ] I've added functional tests for the new language.

And all the items from the "[Adding a new inspector for an existing language](#adding-a-new-inspector-for-an-existing-language)" checklist.
