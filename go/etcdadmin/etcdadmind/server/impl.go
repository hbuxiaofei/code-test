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

	imp.logger.Info(fmt.Sprintf("call GrpcAddMember: %v", req))

	imp.drv.AddMember(req.Member)

	return &pb.AddMemberReply{Errcode: pb.Retcode_OK}, nil
}

// GrpcManagerEtcd is used for private
func (imp *ImplEtcdAdminServer) GrpcManagerEtcd(
	ctx context.Context,
	req *pb.ManagerEtcdRequest) (*pb.ManagerEtcdReply, error) {

	imp.logger.Info(fmt.Sprintf("call GrpcManagerEtcd: %v", req))

	imp.drv.ManagerEtcd(req.Cmd, req.Clearwal, req.Cfgs)

	return &pb.ManagerEtcdReply{Errcode: pb.Retcode_OK}, nil
}

func (imp *ImplEtcdAdminServer) GrpcListMember(
	ctx context.Context,
	req *pb.ListMemberRequest) (*pb.ListMemberReply, error) {

	imp.logger.Info(fmt.Sprintf("call GrpcListMember: %v", req))

	memberList, err := imp.drv.ListMember()

	rep := &pb.ListMemberReply{
		Members: memberList,
	}

	return rep, err
}
