from distutils.command.build import build
from pathlib import Path

from setuptools import Command, setup


class GenerateProto(Command):
    """Generates a client and classes for IJ inspectors"""

    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self):
        import grpc_tools.protoc

        current_dir = Path(__file__).parent.absolute()
        proto_path = (
            current_dir / 'hyperstyle' / 'src' / 'python' / 'review' / 'inspectors' / 'common' / 'inspector' / 'proto'
        )

        grpc_tools.protoc.main(
            [
                'grpc_tools.protoc',
                f'--proto_path={current_dir}',
                f'--python_out={current_dir}',
                f'--pyi_out={current_dir}',
                f'--grpc_python_out={current_dir}',
                str(proto_path / 'model.proto'),
            ],
        )


if __name__ == '__main__':
    # Register a new command
    build.sub_commands.insert(0, ('generate_proto', None))

    # Run the setup script
    setup(cmdclass={"generate_proto": GenerateProto})
