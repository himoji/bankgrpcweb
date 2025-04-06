import grpc
#from . import bank_pb2_grpc, bank_pb2 
from . import bank_pb2
from . import bank_pb2_grpc
from ..main import accountManagment, atm, investment

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

# Investment gRPC client methods
def runbuyStockClient(customer_name, stock_symbol, amount) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.buyStock(customer_name, stock_symbol, amount)
    return result

def runsellStockClient(customer_name, stock_symbol, amount) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.sellStock(customer_name, stock_symbol, amount)
    return result

def runbuyBondClient(customer_name, bond_id, amount) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.buyBond(customer_name, bond_id, amount)
    return result

def runsellBondClient(customer_name, bond_id, amount) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.sellBond(customer_name, bond_id, amount)
    return result

def runtradeFuturesClient(customer_name, futures_symbol, amount, position_type) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.tradeFutures(customer_name, futures_symbol, amount, position_type)
    return result

def runcloseFuturesPositionClient(customer_name, position_id) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.closeFuturesPosition(customer_name, position_id)
    return result

def rungetPortfolioClient(customer_name) -> None:
    # Direct call to the investment module since gRPC for investments is not set up yet
    result = investment.getPortfolio(customer_name)
    return result