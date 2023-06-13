import grpc

import hyperstyle.src.python.review.inspectors.ij_python.proto.model_pb2 as model_pb2
import hyperstyle.src.python.review.inspectors.ij_python.proto.model_pb2_grpc as model_pb2_grpc


class IJClient(object):
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

        # bind the client and the server
        try:
            grpc.channel_ready_future(self.channel).result(timeout=60)
        except grpc.FutureTimeoutError:
            raise Exception("Failed to connect to ij code server")
        else:
            self.stub = model_pb2_grpc.CodeInspectionServiceStub(self.channel)

    def inspect(self, code: model_pb2.Code) -> model_pb2.InspectionResult:
        return self.stub.inspect(code, timeout=60)

    def init(self, service: model_pb2.Service) -> model_pb2.InitResult:
        return self.stub.init(service, timeout=60)
