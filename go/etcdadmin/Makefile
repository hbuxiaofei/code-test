Q ?= @

build: build-pre
	make -C etcdadmind build
	make -C etcdadminctl build

install: build-pre
	make -C etcdadmind install
	make -C etcdadminctl install

uninstall:
	make -C etcdadmind uninstall
	make -C etcdadminctl uninstall

all: clean install

contrib: all
	bash contrib/install

uncontrib: uninstall
	bash contrib/install uninstall

build-pre:
	mkdir -p etcdadmind/pb/etcdadminpb || :
	mkdir -p etcdadminctl/pb/etcdadminpb || :
	protoc --go_out=plugins=grpc:./etcdadmind/pb/etcdadminpb -I./proto etcdadmin.proto
	protoc --go_out=plugins=grpc:./etcdadminctl/pb/etcdadminpb -I./proto etcdadmin.proto

clean:
	$Q find . -type d -name pb | xargs rm -rf
	$Q rm -f etcdadminctl/etcdadminctl || :
	$Q rm -f etcdadmind/etcdadmind || :

.PHONY: contrib
