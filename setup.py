import os
import subprocess
from distutils.command.build_py import build_py
from distutils.command.clean import clean
from pathlib import Path
from typing import List

from setuptools import find_packages, setup

current_dir = Path(__file__).parent.absolute()


def get_long_description() -> str:
    with open(current_dir / 'README.md', encoding='utf-8') as f:
        return f.read()


def get_version() -> str:
    with open(current_dir / 'VERSION.md') as version_file:
        return version_file.read().replace('\n', '')


def get_inspectors_additional_files() -> List[str]:
    inspectors_path = current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors'
    configs = ['xml', 'yml', 'eslintrc', 'flake8', 'txt', 'pylintrc']
    result = []
    for root, _, files in os.walk(inspectors_path):
        for file in files:
            if not file.endswith('.py') and file.split('.')[-1] in configs:
                result.append(str(Path(root) / file))
    return result


def get_requires() -> List[str]:
    with open(current_dir / 'requirements.txt') as requirements_file:
        return requirements_file.read().split('\n')


class ProtoBuild(build_py):

    @staticmethod
    def _build_proto():
        proto_path = current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors' / 'ij_python'
        protoc_command = ["python3", "-m", "grpc_tools.protoc",
                          f'--proto_path={proto_path / "proto"}',
                          f'--python_out={proto_path}',
                          f'--pyi_out={proto_path}',
                          f'--grpc_python_out={proto_path}',
                          "model.proto"]
        subprocess.call(protoc_command)

    def run(self):
        self._build_proto()
        build_py.run(self)


class ProtoClean(clean):

    @staticmethod
    def _clean_proto():
        proto_path = current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors' / 'ij_python'

        for (dir_path, dir_names, filenames) in os.walk(proto_path):
            for filename in filenames:
                print(filename)
                filepath = os.path.join(dir_path, filename)
                if "pb2" in filename:
                    os.remove(filepath)

    def run(self):
        self._clean_proto()
        clean.run(self)


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
    cmdclass={'build_py': ProtoBuild, 'clean': ProtoClean},
)
