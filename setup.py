import os
from typing import List

from setuptools import find_packages, setup

current_dir = __file__.parent.absolute()


def get_long_description() -> str:
    with open(current_dir / 'README.md', encoding='utf-8') as f:
        return f.read()


def get_version() -> str:
    with open(current_dir / 'VERSION.md') as version_file:
        return version_file.read().replace('\n', '')


def get_inspectors_additional_files() -> List[str]:
    inspectors_path = current_dir / 'src' / 'python' / 'review' / 'inspectors'

    result = []
    for root, _, files in os.walk(inspectors_path):
        for file in files:
            file_path = root / file
            if not file_path.name.endswith('.py'):
                result.append(str(file_path))

    return result


setup(
    name='review',
    version=get_version(),
    description='review',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/hyperskill/hyperstyle',
    author='Stepik.org',
    author_email='ivan.magda@stepik.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='code review',
    python_requires='>=3.8, <4',
    install_requires=['upsourceapi'],
    packages=find_packages(exclude=[
        '*.unit_tests', '*.unit_tests.*', 'unit_tests.*', 'unit_tests',
        '*.functional_tests', '*.functional_tests.*', 'functional_tests.*', 'functional_tests',
    ]),
    zip_safe=False,
    package_data={
        '': get_inspectors_additional_files(),
    },
    entry_points={
        'console_scripts': [
            'review=src.python.review.run_tool:main',
        ],
    },
)
