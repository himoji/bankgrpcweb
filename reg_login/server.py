
import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

from auth_pb2_grpc import add_authServicer_to_server, authServicer
from auth_pb2 import loginRequest, registerRequest, validationResponce
import main

#from . import loginRequest, registerRequest, validationResponce, authServicer, add_authServicer_to_server, auth_pb2_grpc, main

class Auth(authServicer):

    def login(self, request: loginRequest, context) -> validationResponce:
        print("Serving login:")

        if main.accountManagment.login(request.customer_name, request.customer_password) == "no_customer":
            print("bad login")
            return validationResponce(valid="false")

        return validationResponce(valid="true")
    
    def register(self, request: registerRequest, context) -> validationResponce:
        print("Serving register:")

        if main.accountManagment.register(request.customer_name, request.customer_password):
            print("registered")
            return validationResponce(valid="true")
        
        return validationResponce(valid="false")



def serve() -> None:
    port = '50051'
    server = grpc.server(ThreadPoolExecutor(max_workers=10))

    add_authServicer_to_server(Auth(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()