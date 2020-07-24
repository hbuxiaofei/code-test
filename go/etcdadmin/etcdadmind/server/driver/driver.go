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
	ManagerEtcd(cmd pb.EtcdCmd, clearwal bool, cfgs []*pb.ManagerEtcdRequest_Config)
}

type DriverImpl struct {
	logger    *zap.Logger
	portGrpc  string
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
		portGrpc:  cfg.Get("GRPC_PORT"),
		logger: log.GetLogger(),
	}
	return drv
}

func (drv *DriverImpl) AddMember(members []*pb.AddMemberRequest_Member) {

	for _, m := range members {
		c := client.New(m.Ip, drv.portGrpc)
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

func (drv *DriverImpl) ManagerEtcd(cmd pb.EtcdCmd, clearwal bool, cfgs []*pb.ManagerEtcdRequest_Config){
    cfgStore := config.Init()

    if cmd != pb.EtcdCmd_NONE {
            etcdctl.CmdEtcdctlStop()
    }

    if len(cfgs) > 0 {
            etcdCfgFile := cfgStore.Get("ETCD_CONF_FILE")
            m := map[string]string{}
            for _, c := range cfgs {
                    m[c.Key] = c.Value
            }

            etcdcfg.EtcdConfigWrite(etcdCfgFile, m)
    }

    if clearwal == true {
            etcdcfg.EtcdWalDelete()
    }

    if cmd == pb.EtcdCmd_START || cmd == pb.EtcdCmd_RESTART {
            etcdctl.CmdEtcdctlStart()
    }

}
