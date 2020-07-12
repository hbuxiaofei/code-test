package server

import (
	pb "etcdadmind/pb/etcdadminpb"
	"etcdadmind/server/driver"
	"fmt"
	"go.uber.org/zap"
	"golang.org/x/net/context"
)

type ImplEtcdAdminServer struct {
	drv    driver.DriverInterface
	logger *zap.Logger
	port   string
}

func (imp *ImplEtcdAdminServer) GrpcAddMember(
	ctx context.Context,
	req *pb.AddMemberRequest) (*pb.AddMemberReply, error) {

	imp.logger.Info(fmt.Sprintf("call GrpcAddMember"))

	imp.drv.AddMember(req.Members)

	return &pb.AddMemberReply{Errcode: pb.Retcode_OK}, nil
}

func (imp *ImplEtcdAdminServer) GrpcManagerEtcd(
	ctx context.Context,
	req *pb.ManagerEtcdRequest) (*pb.ManagerEtcdReply, error) {

	imp.logger.Info(fmt.Sprintf("call GrpcManagerEtcd"))

	if len(req.Cfgs) > 0 {
		imp.logger.Info(fmt.Sprintf("config etcd: %v", req.Cfgs))
	}
	return &pb.ManagerEtcdReply{Errcode: pb.Retcode_OK}, nil
}
