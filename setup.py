from pathlib import Path

from setuptools import setup, Command


class GenerateProto(Command):
    description = "Generates client and classes for protobuf ij inspector"
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self):
        import grpc_tools

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
    setup(cmdclass={"generate_proto": GenerateProto})
