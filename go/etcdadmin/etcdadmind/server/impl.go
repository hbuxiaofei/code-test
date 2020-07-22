package server

import (
	"etcdadmind/config"
	pb "etcdadmind/pb/etcdadminpb"
	"etcdadmind/server/driver"
	"etcdadmind/server/driver/etcdcfg"
	"etcdadmind/server/driver/etcdctl"
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

	imp.drv.AddMember(req.Members)

	return &pb.AddMemberReply{Errcode: pb.Retcode_OK}, nil
}

func (imp *ImplEtcdAdminServer) GrpcManagerEtcd(
	ctx context.Context,
	req *pb.ManagerEtcdRequest) (*pb.ManagerEtcdReply, error) {

	imp.logger.Info(fmt.Sprintf("call GrpcManagerEtcd: %v", req))

	cfgStore := config.Init()

	if req.Cmd != pb.EtcdCmd_NONE {
		etcdctl.CmdEtcdctlStop()
	}

	if len(req.Cfgs) > 0 {
		etcdCfgFile := cfgStore.Get("ETCD_CONF_FILE")
		m := map[string]string{}
		for _, c := range req.Cfgs {
			m[c.Key] = c.Value
		}

		etcdcfg.EtcdConfigWrite(etcdCfgFile, m)
	}

	if req.Clearwal == true {
		etcdcfg.EtcdWalDelete()
	}

	if req.Cmd == pb.EtcdCmd_START || req.Cmd == pb.EtcdCmd_RESTART {
		etcdctl.CmdEtcdctlStart()
	}

	return &pb.ManagerEtcdReply{Errcode: pb.Retcode_OK}, nil
}
