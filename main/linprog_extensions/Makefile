proto_server:
	python3 -m grpc_tools.protoc \
	    -I ./ --python_out=. --grpc_python_out=. \
	    ./operations_research/*.proto

# proto_client:
# 	python3 -m grpc_tools.protoc \
# 	    -I . --python_out=../client/operations_research --grpc_python_out=../client/operations_research \
# 	    ./*.proto


better_proto_server:
	mkdir -p ../server/lib 
	python -m grpc_tools.protoc -I . --python_betterproto_out=../server/lib ./linear_solver.proto ./linear_extension.proto

