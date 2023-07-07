import grpc
from . import bank_pb2
from . import bank_pb2_grpc

"""def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")

    with grpc.insecure_channel('localhost:50051') as channel:

        stub = GreetingService_pb2_grpc.GreetingServiceStub(channel)
        response = stub.greeting(GreetingService_pb2.HelloRequest(name=f'{__name__}', hobbies=['qwe', 'qwesssssssssqw']))

    print("Greeter client received: " + response.greeting)

def runStream() -> None:
    with grpc.insecure_channel('localhost:50051') as channel:

        stub = GreetingService_pb2_grpc.GreetingServiceStub(channel)
        for response in stub.greeting(GreetingService_pb2.HelloRequest(name=f'{__name__}', hobbies=['qwe', 'qwesssssssssqw'])):
            print("Greeter client received: " + response.greeting)
            
if __name__ == '__main__':
    
    logging.basicConfig()
    runStream()"""


def rundeposit(ci: int, ca: int) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator
        print("deposit")
        #zxc = stub.deposit()
        response = stub.deposit(bank_pb2.depositRequest(customer_id=ci, cash_amount=ca))
    print(f"Validation: {response.valid}")
    return response.valid

def runwithdraw(ci: int, ca: int) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator
        print("wd")

        response = stub.withdraw(bank_pb2.withdrawRequest(customer_id=ci, cash_amount=ca))
    print(f"Validation: {response.valid}")
    return response.valid

def runsend(ci: int, ca: int, ti: int) -> None:
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = bank_pb2_grpc.bankStub(channel)
        # Read from an generator
        print("send")

        response = stub.send(bank_pb2.sendRequest(customer_id=ci, cash_amount=ca, taker_id=ti))
    print(f"Validation: {response.valid}")
    return response.valid