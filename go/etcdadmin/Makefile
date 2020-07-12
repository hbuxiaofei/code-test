

all:
	find ./ -name pb | xargs rm -rf
	mkdir -p ./etcdadmind/pb/etcdadminpb
	mkdir -p ./etcdadminctl/pb/etcdadminpb
	protoc --go_out=plugins=grpc:./etcdadmind/pb/etcdadminpb -I./proto etcdadmin.proto
	protoc --go_out=plugins=grpc:./etcdadminctl/pb/etcdadminpb -I./proto etcdadmin.proto
	# protoc --go_out=./etcdadmind/server -I./proto etcdadmin.proto

