pushd src
go mod init bindata
popd

go-bindata -o=./src/resources.go resources

pushd src
go buld
popd
