from __future__ import annotations

import grpc

from hyperstyle.src.python.review.inspectors.common.inspector.proto import model_pb2, model_pb2_grpc

TIMEOUT = 1


class IJClient:
    stub: model_pb2_grpc.CodeInspectionServiceStub

    def __init__(self, host: str = "localhost", port: int = 8080) -> None:
        self.host = host
        self.port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        # bind the client and the server
        try:
            grpc.channel_ready_future(self.channel).result(timeout=TIMEOUT)
        except grpc.FutureTimeoutError as e:
            msg = "Failed to connect to ij code server"
            raise Exception(msg) from e
        else:
            self.stub = model_pb2_grpc.CodeInspectionServiceStub(self.channel)  # type: ignore[no-untyped-call]

    def inspect(self, code: model_pb2.Code) -> model_pb2.InspectionResult:
        return self.stub.inspect(code, timeout=TIMEOUT)

    def init(self, service: model_pb2.Service) -> model_pb2.InitResult:
        return self.stub.init(service, timeout=TIMEOUT)  # type: ignore[attr-defined]
