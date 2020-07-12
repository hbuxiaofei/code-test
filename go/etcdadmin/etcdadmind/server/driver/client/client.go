package client

import (
	"etcdadmind/log"
	pb "etcdadmind/pb/etcdadminpb"
	"fmt"
	"go.uber.org/zap"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

type GrpcClient struct {
	caller pb.GrpcEtcdAdminClient
	conn   *grpc.ClientConn
	ip     string
	port   string
	logger *zap.Logger
}

func New(ip string, port string) *GrpcClient {
	c := &GrpcClient{
		ip:     ip,
		port:   port,
		logger: log.GetLogger(),
	}

	addr := fmt.Sprintf("%s:%s", c.ip, c.port)
	conn, err := grpc.Dial(addr, grpc.WithInsecure())

	if err != nil {
		fmt.Printf("Dial error: %v\n", addr)
		return c
	}
	c.conn = conn
	c.caller = pb.NewGrpcEtcdAdminClient(conn)

	return c
}

func Release(c *GrpcClient) error {
	return c.conn.Close()
}

func (c *GrpcClient) GrpcClientManagerEtcd(m map[string]string) (*pb.ManagerEtcdReply, error) {
	if c.logger != nil {
		c.logger.Info("call GrpcClientManagerEtcd")
	}

	var cfgs []*pb.ManagerEtcdRequest_Config

	for key := range m {
		cfg := pb.ManagerEtcdRequest_Config{Key: key, Value: m[key]}
		cfgs = append(cfgs, &cfg)
	}

	r, err := c.caller.GrpcManagerEtcd(context.Background(), &pb.ManagerEtcdRequest{Cfgs: cfgs})

	return r, err
}
