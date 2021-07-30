# Comparison with other tools evaluation

This module allows getting statistic about using of several code quality tools.
In our work we compare the Hyperstyle tool with the [Tutor](https://www.hkeuning.nl/rpt/) tool.
Other tools (FrenchPress, WebTA, and AutoStyle) does not have open sources.

To get statistics we use students solutions for six programming tasks, 
but the main script can gather this statistics for any tasks.

The tasks from the out dataset:
- **countEven**. The `countEven` method returns the number of even integers in the values-array.
- **sumValues**. The `sumValues` method adds up all numbers from the values-array, 
  or only the positive numbers if the `positivesOnly` boolean parameter is set 
  to `true`.
- **oddSum**. The method `oddSum` returns the sum of all numbers at an odd index 
  in the array parameter, until the number -1 is seen at an odd index.
- **calculateScore**. The `calculateScore` method calculates the score for a train trip. 
  The highest score is 10. The score is based on the number of changes and the day of 
  the week (Monday is 1, Sunday is 7).
- **hasDoubled**. Write a program that calculates in how many years your savings 
  have doubled with the given interest.
- **haveThree**. Given an array of ints, return true if the value 3 appears in the 
  array exactly  3 times, and no 3's are next to each other.
  
The dataset has several columns:
- Student id (student_id);
- Task key (task_key);
- Code fragment (solution);
- Tutor error, if it is existed (tutor_error);
- Tutor issues keys (tutor_issues);
- Hyperstyle issues keys (hyperstyle_issues);
- Hyperstyle INFO issues keys (hyperstyle_info_issues);
- Code style issues count (code_style_issues_count).

The dataset stores in the `csv` format.

## Usage

Run the [statistics_gathering.py](statistics_gathering.py) with the arguments from command line.

Required arguments:

`solutions_file_path` — path to csv-file with code samples.

The statistics will be printed in the terminal. The statistics includes:
- Unique users count;
- Code snippets count;
- Tasks statistics: for each task count code snippets and count snippets with the Tutor errors;
- Count code fragments has Tutor errors;
- Count of unique errors was found in Tutor;
- Error statistics: for each error get the error text and frequency;
- Issues statistics:
    - Count of unique issues in total;
    - Common issues statistics: for all common issues for Hyperstyle and Tutor count frequency of this issue;
    - Tutor unique issues statistics: for all Tutor issues (that were not found by Hyperstyle) count frequency of this issue;
    - Hyperstyle unique issues statistics: for all Hyperstyle issues (that were not found by Tutor) count frequency of this issue;
    - Count code style issues and count fragments with these issues.

