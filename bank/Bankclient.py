import grpc
#from . import bank_pb2_grpc, bank_pb2 
from . import bank_pb2
from . import bank_pb2_grpc

def rundepositClient(ci, ca) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator
        print(type(stub.deposit(bank_pb2.depositRequest(customer_id=ci, cash_amount=ca))))
        response = stub.deposit(bank_pb2.depositRequest(customer_id=ci, cash_amount=ca))
        
    print(f"Validation: {response.valid}")
    return response.valid

def runwithdrawClient(ci, ca) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator

        response = stub.withdraw(bank_pb2.depositRequest(customer_id=ci, cash_amount=ca))
    print(f"Validation: {response.valid}")
    return response.valid

def runsendClient(ci, ca, ti) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator

        response = stub.send(bank_pb2.depositRequest(customer_id=ci, cash_amount=ca, taker_id=ti))
    print(f"Validation: {response.valid}")
    return response.valid