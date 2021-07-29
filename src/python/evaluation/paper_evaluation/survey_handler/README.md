# Surveys handlers

These scripts allow handling surveys results for the SIGCSE paper. 
We have two surveys (for Python and for Java) where participants should choose a fragments 
that has better formatting.
Each question in the surveys have randomly orders for fragments. 
The left fragment can have good formatting, but at the same time, it can have bad formatting.
To handle these cases we created JSON configs with this information and another one with the results. 
These scripts allow processing these config files.

## Usage

Run the [survey_statistics_gathering.py](survey_statistics_gathering.py) with the arguments from command line.

Required arguments:

`questions_json_path` — path to the JSON with labelled questions;
`results_json_path` — path to the JSON with survey results.

An example of `questions_json` file:
```json
{
  "questions": [
    {
      "number": 1,
      "left_fragment": "before_formatting",
      "right_fragment": "after_formatting"
    },
    {
      "number": 2,
      "left_fragment": "after_formatting",
      "right_fragment": "before_formatting"
    }
  ]
}
```

An example of `results_json` file:

```json
{
  "questions": [
    {
      "number": 1,
      "left_fragment": 0,
      "right_fragment": 11,
      "both": 0
    },
    {
      "number": 2,
      "left_fragment": 10,
      "right_fragment": 0,
      "both": 1
    }
  ]
}
```

An example of the statistics:
```text
total participants=11
------before----after----any----
1.		0		11		  0
2.		1		10		  0
3.		0		11		  0
4.		0		11		  0
5.		0		11		  0
6.		1		10		  0
7.		0		11		  0
8.		1		8		  2
9.		0		11		  0
10.		0		8		  3
```
