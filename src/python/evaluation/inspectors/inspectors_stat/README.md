# Hyperstyle evaluation: inspectors statistics gathering

This module allows gathering statistics about inspections that are used 
during analysis for a specific language. We collect all available issues' keys, 
removed ignored ones and gather statistics for fours main categories:

- code style issues;
- best practice issues;
- error-prone issues;
- code complexity issues.

More information about these categories can be found on [this](https://support.hyperskill.org/hc/en-us/articles/360049582712-Code-style-Code-quality) page.

## Current statistics

The current statistics is:

|            | Error prone | Code style | Code complexity | Best practice |
|------------|:-----------:|:----------:|:---------------:|:-------------:|
| Python     |     162     |     146    |        35       |      254      |
| Java       |      51     |     50     |        8        |      110      |
| JavaScript |      15     |     17     |        1        |       34      |
| Kotlin     |      21     |     70     |        12       |       75      |


## Usage

Run the [statistics_gathering.py](statistics_gathering.py) with the arguments from command line.

Required arguments:

`language` — the language for which statistics will be gathering. 
Available values are: `python`, `java`, `kotlin`, `javascript`.

An example of the output is:

```text
Collected statistics for python language:
best practices: 254 times;
code style: 146 times;
complexity: 35 times;
error prone: 162 times;
undefined: 3 times;
Note: undefined means a category that is not categorized among the four main categories. Most likely it is info category
```
