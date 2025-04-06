import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

#from bank_pb2_grpc import add_authServicer_to_server, authServicer
#from bank_pb2 import bank_pb2.loginRequest, bank_pb2.registerRequest, bank_pb2.validationResponce
from . import bank_pb2_grpc
from . import bank_pb2
from . import main

#from . import bank_pb2.loginRequest, bank_pb2.registerRequest, bank_pb2.validationResponce, authServicer, add_authServicer_to_server, bank_pb2_grpc, main

class Bank(bank_pb2_grpc.bankServicer):

    def deposit(self, request: bank_pb2.depositRequest, context) -> bank_pb2.validationResponce:
        print("Serving deposit:")

        if main.atm.rundeposit(int(request.customer_id), int(request.cash_amount)) == False:
            print("bad deposit")
            return bank_pb2.validationResponce(valid="false")
    
        return bank_pb2.validationResponce(valid="true")
    
    def withdraw(self, request: bank_pb2.withdrawRequest, context) -> bank_pb2.validationResponce:
        print("Serving withdraw:")

        if main.atm.runwithdraw(request.customer_id, request.cash_amount) == False:
            print("bad withdraw")
            return bank_pb2.validationResponce(valid="false")

        return bank_pb2.validationResponce(valid="true")
    
    def send(self, request: bank_pb2.depositRequest, context) -> bank_pb2.validationResponce:
        print("Serving send:")

        if main.atm.runsend(request.customer_id, request.cash_amount, request.taker_id) == False:
            print("bad send")
            return bank_pb2.validationResponce(valid="false")

        return bank_pb2.validationResponce(valid="true")
    
    # Investment service methods would go here if we expanded the protobuf
    # For now the investment functions are called directly,
    # but in a production system they would be gRPC services



def serve() -> None:
    port = '50052'
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    #server = grpc.grpc.server()

    bank_pb2_grpc.add_bankServicer_to_server(Bank(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()