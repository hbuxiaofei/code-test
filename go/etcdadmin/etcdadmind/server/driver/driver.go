package driver

import (
	"etcdadmind/config"
	"etcdadmind/log"
	pb "etcdadmind/pb/etcdadminpb"
	"etcdadmind/server/driver/client"
	"etcdadmind/server/driver/etcdcfg"
	"etcdadmind/server/driver/etcdctl"
	"etcdadmind/utils"
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

func resetEtcdConfig() error {
	etcdCfgFile := config.Init().Get("ETCD_CONF_FILE")

	m, err := etcdcfg.EtcdConfigMapInit()

	if err != nil {
		return err
	}

	return etcdcfg.EtcdConfigWrite(etcdCfgFile, m)
}

func resetEtcd(isStart bool) error {
	var err error

	// Stop etcd, ignore error
	etcdctl.CmdEtcdctlStop()

	if err := resetEtcdConfig(); err != nil {
		goto exit
	}

	if err = etcdcfg.EtcdWalDelete(); err != nil {
		goto exit
	}

exit:
	if isStart == true {
		er := etcdctl.EtcdctlStart()
		if err == nil {
			err = er
		}
	}
	return err
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
		c := client.New(m.Ip, drv.portS)
		defer client.Release(c)

		drv.logger.Info(fmt.Sprintf("add member: %v %v", m.Name, m.Ip))
		ips, err := utils.GetHostIP4()
		if err != nil {
			continue
		}

		// reset remote etcd
		cfgs, _ := etcdcfg.EtcdConfigMapInit()
		c.GrpcClientManagerEtcd(cfgs, true, client.EtcdCmdStop)

		if utils.ContainsString(ips, m.Ip) >= 0 {
			c.GrpcClientManagerEtcd(map[string]string{}, false, client.EtcdCmdStart)
		} else {
			cfgs["ETCD_INITIAL_CLUSTER_STATE"] = "existing"
			c.GrpcClientManagerEtcd(cfgs, false, client.EtcdCmdStart)
		}
	}
}
