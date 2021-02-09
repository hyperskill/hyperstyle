from src.python.review.common.subprocess_runner import run_in_subprocess
from src.python.review.inspectors.flake8.flake8 import Flake8Inspector
from src.python.review.inspectors.issue import IssueType


class Cohesion:

    @staticmethod
    def run_flake8(path):
        inspector = Flake8Inspector()

        issues = inspector.inspect(path, {})

        return list(filter(
            lambda x: x.type == IssueType.COHESION,
            issues
        ))

    @staticmethod
    def run_origin(path):
        command = [
            'cohesion',
            '-f',
            path,
            '--verbose'
        ]
        return run_in_subprocess(command)


if __name__ == '__main__':
    path = input()

    print('FLAKE8')
    for issue in Cohesion.run_flake8(path):
        print(f'File: {issue.file_path}')
        print(f'  {issue.origin_class}: {issue.description}')
    print()

    print('COHESION')
    print(Cohesion.run_origin(path))
    print()
