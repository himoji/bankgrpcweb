
import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

from . import bank_pb2_grpc
from . import bank_pb2
from . import main

"""class Greeter(GreetingService_pb2_grpc.GreetingServiceServicer):
    def greeting(self, request, context):
        print(f"req: {request}")

        for i in range(10):
            yield GreetingService_pb2.HelloResponce(greeting=f"hello responce, {request.name}")
            time.sleep(0.1)

def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    GreetingService_pb2_grpc.add_GreetingServiceServicer_to_server(Greeter(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()"""


class Servicer(bank_pb2_grpc.bankServicer):

    def deposit(self, request, context) -> bank_pb2.validationResponce:
        print("Serving deposit:")

        if main.atm.deposit(request.customer_id, request.cash_amount):
            print("OK")
            return bank_pb2.validationResponce(valid="true")
        return bank_pb2.validationResponce(valid="false")
        
    
    def withdraw(self, request: bank_pb2.withdrawRequest,
                       context) -> bank_pb2.validationResponce:
        print(f"Serving withdraw: {request}")

        if main.atm.withdraw(request.customer_id, request.cash_amount):
            print("OK")
            return bank_pb2.validationResponce(valid="true")
        return bank_pb2.validationResponce(valid="false")

    def send(self, request: bank_pb2.sendRequest,
                       context) -> bank_pb2.validationResponce:
        print(f"Serving sending: {request}")

        if main.atm.send(request.customer_id, request.cash_amount, request.taker_id):
            print("OK")
            return bank_pb2.validationResponce(valid="true")
        return bank_pb2.validationResponce(valid="false")



def serve() -> None:
    port = '50052'
    #server = grpc.grpc.server()

    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()