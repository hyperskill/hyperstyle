# Hyperstyle evaluation: plots
This module allows you to visualize the data obtained with the [inspectors](../inspectors) module

## [diffs_plotter.py](diffs_plotter.py)
This script allows you to visualize a dataset obtained with [diffs_between_df.py](../inspectors/diffs_between_df.py). 

The script can build the following charts: 
* number of unique issues by category ([Example](#number-of-unique-issues-by-category))
* number of issues by category ([Example](#number-of-issues-by-category))
* number of unique penalty issues by category ([Example](#number-of-unique-penalty-issues-by-category))
* number of penalty issues by category ([Example](#number-of-penalty-issues-by-category))
* median penalty influence by category ([Example](#median-influence-on-penalty-by-category)) 
* distribution of penalty influence by category ([Example](#distribution-of-influence-on-penalty-by-category))

### Usage
Run the [diffs_plotter.py](diffs_plotter.py) with the arguments from command line.

**Required arguments**:
1. `diffs_file_path` — path to a file with serialized diffs that were founded by [diffs_between_df.py](../inspectors/diffs_between_df.py).
2. `save_dir` — directory where the plotted charts will be saved.
3. `config_path` — path to the yaml file containing information about the charts to be plotted. A description of the config and its example is provided in [this section](#config).


**Optional arguments**:

Argument | Description
--- | ---
**&#8209;&#8209;file&#8209;extension** | Allows you to select the extension of output files. Available extensions: `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.pdf`, `.eps`, `.json`. Default is `.svg`.

### Config
The configuration file is a dictionary in yaml format, where each chart you want to build has its parameters.

**Possible values of the charts**: 
* `unique_issues_by_category` to plot the number of unique issues by category
* `issues_by_category` to plot the number of issues by category
* `unique_penalty_issues_by_category` to plot the number of unique penalty issues by category
* `penalty_issues_by_category` to plot the number of penalty issues by category
* `median_penalty_influence_by_category` to plot the median penalty influence by category
* `penalty_influence_distribution` to plot the distribution of penalty influence by category

**Possible parameters**:
Parametr | Description
---|---
**x_axis_name** | Name of the x-axis. The default value depends on the type of chart.
**y_axis_name** | Name of the y-axis. The default value depends on the type of chart.
**limit** | A value that allows you to filter the data before displaying them. </br></br> For charts `unique_issues_by_category`, `issues_by_category`, `unique_penalty_issues_by_category` and `penalty_issues_by_category` only those categories will be shown where the number of issues is greater than or equal to the limit. </br></br> For chart `penalty_issues_by_category` only those categories will be shown where the number of median value is greater than or equal to the limit. </br></br> For chart `penalty_influence_distribution` only those categories will be shown where the number of values is greater than or equal to the limit. </br></br> The default value depends on the type of chart.
**margin** | Defines the outer margin on all four sides of the chart. The available values are specified in the Enum class `MARGIN` from [plots const file](./common/plotly_consts.py). If not specified, the default value provided by Plotly is used.
**sort_order** | Defines the sorting order of the chart. The available values are specified in the Enum class `SORT_ORDER` from [plots const file](./common/plotly_consts.py). If not specified, the default value provided by Plotly is used.
**color** | Defines the color of the chart. The available values are specified in the Enum class `COLOR` from [plots const file](./common/plotly_consts.py). If not specified, the default value provided by Plotly is used.

#### Example of config
```yaml
unique_issues_by_category:
  margin: "ZERO"
  limit: 10
  sort_order: "total descending"
  color: "RED"
unique_penalty_issues_by_category:
  limit: 30
  sort_order: "category ascending"
median_penalty_influence_by_category:
penalty_influence_distribution:
```

The result will be four graphs (`unique_issues_by_category`, `unique_penalty_issues_by_category`, `median_penalty_influence_by_category`, `penalty_influence_distribution`) with the corresponding parameters.

### Examples

#### Number of unique issues by category
<img src="./examples/unique_issues_by_category.png" width="500">

#### Number of issues by category
<img src="./examples/issues_by_category.png" width="500">

#### Number of unique penalty issues by category
<img src="./examples/unique_penalty_issues_by_category.png" width="500">

#### Number of penalty issues by category
<img src="./examples/penalty_issues_by_category.png" width="500">

#### Median influence on penalty by category
<img src="./examples/median_penalty_influence_by_category.png" width="500">

#### Distribution of influence on penalty by category
<img src="./examples/penalty_influence_distribution.png" width="500">