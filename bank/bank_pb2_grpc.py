# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import bank_pb2 as bank__pb2


class bankStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.deposit = channel.unary_unary(
                '/com.zxc.grpc.bank/deposit',
                request_serializer=bank__pb2.depositRequest.SerializeToString,
                response_deserializer=bank__pb2.validationResponce.FromString,
                )
        self.withdraw = channel.unary_unary(
                '/com.zxc.grpc.bank/withdraw',
                request_serializer=bank__pb2.withdrawRequest.SerializeToString,
                response_deserializer=bank__pb2.validationResponce.FromString,
                )
        self.send = channel.unary_unary(
                '/com.zxc.grpc.bank/send',
                request_serializer=bank__pb2.sendRequest.SerializeToString,
                response_deserializer=bank__pb2.validationResponce.FromString,
                )


class bankServicer(object):
    """Missing associated documentation comment in .proto file."""

    def deposit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def withdraw(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def send(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_bankServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'deposit': grpc.unary_unary_rpc_method_handler(
                    servicer.deposit,
                    request_deserializer=bank__pb2.depositRequest.FromString,
                    response_serializer=bank__pb2.validationResponce.SerializeToString,
            ),
            'withdraw': grpc.unary_unary_rpc_method_handler(
                    servicer.withdraw,
                    request_deserializer=bank__pb2.withdrawRequest.FromString,
                    response_serializer=bank__pb2.validationResponce.SerializeToString,
            ),
            'send': grpc.unary_unary_rpc_method_handler(
                    servicer.send,
                    request_deserializer=bank__pb2.sendRequest.FromString,
                    response_serializer=bank__pb2.validationResponce.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.zxc.grpc.bank', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class bank(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def deposit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.zxc.grpc.bank/deposit',
            bank__pb2.depositRequest.SerializeToString,
            bank__pb2.validationResponce.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def withdraw(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.zxc.grpc.bank/withdraw',
            bank__pb2.withdrawRequest.SerializeToString,
            bank__pb2.validationResponce.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def send(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.zxc.grpc.bank/send',
            bank__pb2.sendRequest.SerializeToString,
            bank__pb2.validationResponce.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
