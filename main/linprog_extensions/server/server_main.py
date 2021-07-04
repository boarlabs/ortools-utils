from concurrent.futures import ThreadPoolExecutor
import logging

import grpc

from context import operations_research

from operations_research.python.linprog_service_pb2_grpc import(
    add_LinProgServiceServicer_to_server
)

from linprog_server import LinProgServer


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)



def main():
    server = grpc.server(ThreadPoolExecutor(max_workers=200), maximum_concurrent_rpcs=100)
    
    add_LinProgServiceServicer_to_server(LinProgServer(), server)
    port = 50051
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info('MILP solver server ready on port %r', port)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
