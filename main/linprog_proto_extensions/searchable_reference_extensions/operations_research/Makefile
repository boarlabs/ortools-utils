proto_server:
	python3 -m grpc_tools.protoc \
	    -I . --python_out=../server --grpc_python_out=../server \
	    ./*.proto

proto_client:
	python3 -m grpc_tools.protoc \
	    -I . --python_out=../client --grpc_python_out=../client \
	    ./*.proto


better_proto_server:
	mkdir -p ../server/lib 
	python -m grpc_tools.protoc -I . --python_betterproto_out=../server/lib ./linear_solver.proto ./linear_extension.proto

