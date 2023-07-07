
import logging
from concurrent.futures import ThreadPoolExecutor
import grpc

#from auth_pb2_grpc import add_authServicer_to_server, authServicer
#from auth_pb2 import auth_pb2.loginRequest, auth_pb2.registerRequest, auth_pb2.validationResponce
from . import auth_pb2_grpc
from . import auth_pb2
from . import main

#from . import auth_pb2.loginRequest, auth_pb2.registerRequest, auth_pb2.validationResponce, authServicer, add_authServicer_to_server, auth_pb2_grpc, main

class Auth(auth_pb2_grpc.authServicer):

    def login(self, request: auth_pb2.loginRequest, context) -> auth_pb2.validationResponce:
        print("Serving login:")

        if main.accountManagment.login(request.customer_name, request.customer_password) == "no_customer":
            print("bad login")
            return auth_pb2.validationResponce(valid="false")

        return auth_pb2.validationResponce(valid="true")
    
    def register(self, request: auth_pb2.registerRequest, context) -> auth_pb2.validationResponce:
        print("Serving register:")

        if main.accountManagment.register(request.customer_name, request.customer_password):
            print("registered")
            return auth_pb2.validationResponce(valid="true")
        
        return auth_pb2.validationResponce(valid="false")



def serve() -> None:
    port = '50051'
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    #server = grpc.grpc.server()

    auth_pb2_grpc.add_authServicer_to_server(Auth(), server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()