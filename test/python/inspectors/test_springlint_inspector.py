from test.python.inspectors import SPRING_DATA_FOLDER

from src.python.review.inspectors.issue import IssueType
from src.python.review.inspectors.springlint.springlint import SpringlintInspector


def test_controller_with_smells():
    inspector = SpringlintInspector()

    path_to_file = SPRING_DATA_FOLDER / 'case1'
    issues = inspector.inspect(path_to_file, {})

    assert len(issues) == 8

    smell_issue = next(x for x in issues if x.type == IssueType.ARCHITECTURE)
    assert smell_issue.origin_class == 'Promiscuous Controller'

    dit_issue = next(x for x in issues if x.type == IssueType.INHERITANCE_DEPTH)
    assert dit_issue.inheritance_tree_depth == 1

    noc_issue = next(x for x in issues if x.type == IssueType.CHILDREN_NUMBER)
    assert noc_issue.children_number == 0

    wmc_issue = next(x for x in issues if x.type == IssueType.WEIGHTED_METHOD)
    assert wmc_issue.weighted_method == 12

    cbo_issue = next(x for x in issues if x.type == IssueType.COUPLING)
    assert cbo_issue.class_objects_coupling == 3

    lcom_issue = next(x for x in issues if x.type == IssueType.COHESION)
    assert lcom_issue.cohesion_lack == 66

    rfc_issue = next(x for x in issues if x.type == IssueType.CLASS_RESPONSE)
    assert rfc_issue.class_response == 0

    nom_issue = next(x for x in issues if x.type == IssueType.METHOD_NUMBER)
    assert nom_issue.method_number == 12


def test_simple_class():
    inspector = SpringlintInspector()

    path_to_file = SPRING_DATA_FOLDER / 'case2'
    issues = inspector.inspect(path_to_file, {})

    assert len(issues) == 7

    dit_issue = next(x for x in issues if x.type == IssueType.INHERITANCE_DEPTH)
    assert dit_issue.inheritance_tree_depth == 1

    noc_issue = next(x for x in issues if x.type == IssueType.CHILDREN_NUMBER)
    assert noc_issue.children_number == 0

    wmc_issue = next(x for x in issues if x.type == IssueType.WEIGHTED_METHOD)
    assert wmc_issue.weighted_method == 8

    cbo_issue = next(x for x in issues if x.type == IssueType.COUPLING)
    assert cbo_issue.class_objects_coupling == 2

    lcom_issue = next(x for x in issues if x.type == IssueType.COHESION)
    assert lcom_issue.cohesion_lack == 22

    rfc_issue = next(x for x in issues if x.type == IssueType.CLASS_RESPONSE)
    assert rfc_issue.class_response == 2

    nom_issue = next(x for x in issues if x.type == IssueType.METHOD_NUMBER)
    assert nom_issue.method_number == 8
