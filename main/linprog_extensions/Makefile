proto_server:
	python3 -m grpc_tools.protoc \
	    -I ./ --python_out=. --grpc_python_out=. \
	    ./operations_research/*.proto

# proto_client:
# 	python3 -m grpc_tools.protoc \
# 	    -I . --python_out=../client/operations_research --grpc_python_out=../client/operations_research \
# 	    ./*.proto


better_proto_server:
	mkdir -p ./server/linprog_structs
	python -m grpc_tools.protoc -I . --python_betterproto_out=./server/linprog_structs ./operations_research/linear_solver.proto ./operations_research/linear_extension.proto

