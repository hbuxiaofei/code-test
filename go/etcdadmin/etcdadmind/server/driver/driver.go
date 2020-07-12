package driver

import (
	"etcdadmind/config"
	"etcdadmind/log"
	pb "etcdadmind/pb/etcdadminpb"
	"etcdadmind/server/driver/client"
	"fmt"
	"go.uber.org/zap"
)

type DriverInterface interface {
	AddMember(members []*pb.AddMemberRequest_Member)
}

type DriverImpl struct {
	logger *zap.Logger
	portS  string
}

func New() *DriverImpl {
	cfg := config.Init()

	drv := &DriverImpl{
		portS:  cfg.Get("GRPC_PORT"),
		logger: log.GetLogger(),
	}
	return drv
}

func (drv *DriverImpl) AddMember(members []*pb.AddMemberRequest_Member) {

	for _, m := range members {
		drv.logger.Info(fmt.Sprintf("add member: %v %v", m.Name, m.Ip))

		c := client.New(m.Ip, drv.portS)
		defer client.Release(c)
		cfgs := map[string]string{
			"key1": "value1",
			"key2": "value2",
		}
		c.GrpcClientManagerEtcd(cfgs)
	}
}
