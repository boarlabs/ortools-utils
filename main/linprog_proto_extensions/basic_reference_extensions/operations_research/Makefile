proto_server:
	python3 -m grpc_tools.protoc \
	    -I . --python_out=../server --grpc_python_out=../server \
	    ./*.proto

proto_client:
	python3 -m grpc_tools.protoc \
	    -I . --python_out=../client --grpc_python_out=../client \
	    ./*.proto