import argparse
from src.python.review.reviewers.perform_review import OutputFormat


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', '--folder_path', default=None)
    parser.add_argument('--file_name', '--file_name', default='results.xlsx')
    parser.add_argument('-f', '--format', default=OutputFormat.JSON.value)
    return parser
