Q ?= @

all: clean install

build-pre:
	mkdir -p etcdadmind/pb/etcdadminpb || :
	mkdir -p etcdadminctl/pb/etcdadminpb || :
	protoc --go_out=plugins=grpc:./etcdadmind/pb/etcdadminpb -I./proto etcdadmin.proto
	protoc --go_out=plugins=grpc:./etcdadminctl/pb/etcdadminpb -I./proto etcdadmin.proto

install: build-pre
	make -C etcdadmind install
	make -C etcdadminctl install
	bash contrib/install

build: build-pre
	make -C etcdadmind build
	make -C etcdadminctl build

clean:
	$Q find . -type d -name pb | xargs rm -rf
	$Q rm -f etcdadminctl/etcdadminctl || :
	$Q rm -f etcdadmind/etcdadmind || :

uninstall:
	make -C etcdadmind uninstall
	make -C etcdadminctl uninstall
	bash contrib/install uninstall
