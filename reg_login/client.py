import grpc
#from . import auth_pb2_grpc, auth_pb2 
from . import auth_pb2
from . import auth_pb2_grpc

def runlogin(cn, cp) -> str:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.authStub(channel)
        # Read from an generator

        response = stub.login(auth_pb2.loginRequest(customer_name=cn, customer_password=cp))
    print(f"Validation: {response.valid}")
    return response.valid

def runregister(cn, cp) -> str:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.authStub(channel)
        # Read from an generator

        response = stub.register(auth_pb2.registerRequest(customer_name=cn, customer_password=cp))
    print(f"Validation: {response.valid}")
    return response.valid
