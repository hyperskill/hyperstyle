from hyperstyle.src.python.review.inspectors.issue_configs import IssueConfig

ISSUE_CONFIGS = [
    IssueConfig(
        origin_class='W1404',
        new_description='Found implicit string concatenation. If you want to concatenate strings, use "+".',
    ),
    IssueConfig(
        origin_class='R1721',
        new_description=(
            'Unnecessary use of a comprehension. Instead of using an identity comprehension, '
            'consider using the list, dict or set constructor. It is faster and simpler. '
            'For example, instead of {{key: value for key, value in list_of_tuples}} use dict(list_of_tuples).'
        ),
    ),
]
