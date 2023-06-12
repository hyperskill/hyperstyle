import os
from pathlib import Path
from typing import List

import grpc_tools.protoc
from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel

current_dir = Path(__file__).parent.absolute()
proto_path = current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors' / 'ij_python' / 'proto'


def get_long_description() -> str:
    with open(current_dir / 'README.md', encoding='utf-8') as f:
        return f.read()


def get_version() -> str:
    with open(current_dir / 'VERSION.md') as version_file:
        return version_file.read().replace('\n', '')


def get_proto_paths() -> List[str]:
    result = []
    for root, _, files in os.walk(proto_path):
        for file in files:
            if 'pb2' in file:
                result.append(str(Path(root) / file))
    return result


def generate_proto():
    grpc_tools.protoc.main(
        ['grpc_tools.protoc',
         f'--proto_path={current_dir}',
         f'--python_out={current_dir}',
         f'--pyi_out={current_dir}',
         f'--grpc_python_out={current_dir}',
         str(proto_path / 'model.proto'),
         ],
    )


class BuildPyCommand(build_py):
    """
    Generate proto code before building the package.
    """

    def run(self):
        generate_proto()
        build_py.run(self)


class BDistWheelCommand(bdist_wheel):
    """
    Generate proto code before building a wheel.
    """

    def run(self):
        generate_proto()
        bdist_wheel.run(self)


def get_inspectors_additional_files() -> List[str]:
    inspectors_path = current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors'
    configs = ['xml', 'yml', 'eslintrc', 'flake8', 'txt', 'pylintrc']
    result = get_proto_paths()
    for root, _, files in os.walk(inspectors_path):
        for file in files:
            if not file.endswith('.py') and file.split('.')[-1] in configs:
                result.append(str(Path(root) / file))
    return result


def get_requires() -> List[str]:
    with open(current_dir / 'requirements.txt') as requirements_file:
        return requirements_file.read().split('\n')


setup(
    name='hyperstyle',
    version=get_version(),
    description='A tool for running a set of pre-configured linters and evaluating code quality.',
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
    install_requires=get_requires(),
    include_package_data=True,
    packages=find_packages(exclude=[
        '*.unit_tests',
        '*.unit_tests.*',
        'unit_tests.*',
        'unit_tests',
        '*.functional_tests',
        '*.functional_tests.*',
        'functional_tests.*',
        'functional_tests',
    ]),
    zip_safe=False,
    package_data={
        '': get_inspectors_additional_files(),
    },
    entry_points={
        'console_scripts': [
            'review=hyperstyle.src.python.review.run_tool:main',
        ],
    },
    cmdclass={
        'build_py': BuildPyCommand,
        'bdist_wheel': BDistWheelCommand,
    },
)
