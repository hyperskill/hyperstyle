from pathlib import Path

from src.python.review.inspectors.inspector_type import InspectorType
from src.python.review.inspectors.spotbugs.spotbugs import SpotbugsInspector


def test_parse_single_line_when_lines_range():
    line = ('M B HE: Person defines equals and uses Object.hashCode()  '
            'At test_when_only_equals_overridden.java:[lines 15-27]')

    issue = SpotbugsInspector._parse_single_line(
        line, {
            'test_when_only_equals_overridden.java':
                Path('test_when_only_equals_overridden.java')})

    assert issue.origin_class == 'M B HE'
    assert issue.file_path == Path('test_when_only_equals_overridden.java')
    assert issue.description == 'Person defines equals and uses Object.hashCode()'
    assert issue.line_no == 15
    assert issue.inspector_type == InspectorType.SPOTBUGS

    print(issue)


def test_parse_single_line_when_single_line():
    line = ('M C UwF: Unwritten field: Person.firstName  '
            'At test_when_only_equals_overridden.java:[line 27]')

    issue = SpotbugsInspector._parse_single_line(
        line, {
            'test_when_only_equals_overridden.java':
                Path('test_when_only_equals_overridden.java')})

    assert issue.origin_class == 'M C UwF'
    assert issue.file_path == Path('test_when_only_equals_overridden.java')
    assert issue.description == 'Unwritten field: Person.firstName'
    assert issue.line_no == 27
    assert issue.inspector_type == InspectorType.SPOTBUGS

    print(issue)


def test_parse_single_line_when_no_line():
    line = ('M P UuF: Unused field: Person.testField  '
            'At test_when_only_equals_overridden.java')

    issue = SpotbugsInspector._parse_single_line(
        line, {
            'test_when_only_equals_overridden.java':
                Path('test_when_only_equals_overridden.java')})

    assert issue.origin_class == 'M P UuF'
    assert issue.file_path == Path('test_when_only_equals_overridden.java')
    assert issue.description == 'Unused field: Person.testField'
    assert issue.line_no == 0
    assert issue.inspector_type == InspectorType.SPOTBUGS

    print(issue)


def test():
    line = ('M C NP: Read of unwritten field entity in CommandPickItem.execute()  '
            'At hyperskill39939.java:[line 46]')

    issue = SpotbugsInspector._parse_single_line(
        line, {'hyperskill39939.java': Path('hyperskill39939.java')})

    assert issue.origin_class == 'M C NP'
    assert issue.file_path == Path('hyperskill39939.java')
    assert issue.description == 'Read of unwritten field entity in CommandPickItem.execute()'
    assert issue.line_no == 46
    assert issue.inspector_type == InspectorType.SPOTBUGS

    print(issue)


def test_parse_with_filename_in_message():
    line = ('M P UuF: Public class Main should be declared in Main.java  '
            'In test_when_only_equals_overridden.java')

    issue = SpotbugsInspector._parse_single_line(
        line, {
            'test_when_only_equals_overridden.java':
                Path('test_when_only_equals_overridden.java')})

    assert issue.origin_class == 'M P UuF'
    assert issue.file_path == Path('test_when_only_equals_overridden.java')
    assert issue.description == 'Public class Main should be declared in Main.java'
    assert issue.line_no == 0
    assert issue.inspector_type == InspectorType.SPOTBUGS

    print(issue)
