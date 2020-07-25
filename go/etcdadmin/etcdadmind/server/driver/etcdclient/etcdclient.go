package etcdclient

import (
	"fmt"
	pb "github.com/coreos/etcd/etcdserver/etcdserverpb"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
	"strings"
)

type EtcdClient struct {
	remote pb.ClusterClient
	ip     string
	port   string
	conn   *grpc.ClientConn
}

func New(ip string, port string) *EtcdClient {
	c := &EtcdClient{
		ip:   ip,
		port: port,
	}

	addr := fmt.Sprintf("%s:%s", c.ip, c.port)
	conn, err := grpc.Dial(addr, grpc.WithInsecure())

	if err != nil {
		return c
	}
	c.conn = conn
	c.remote = pb.NewClusterClient(conn)

	return c
}

func Release(c *EtcdClient) error {
	return c.conn.Close()
}

func (c *EtcdClient) MemberList() map[string]string {
	m := make(map[string]string)

	req := &pb.MemberListRequest{}

	res, _ := c.remote.MemberList(context.Background(), req)
	for i := range res.Members {
		member := res.Members[i]

		ip := strings.Split(member.PeerURLs[0], "//")[1]
		ip = strings.Split(ip, ":")[0]

		m[member.Name] = ip
	}

	return m
}

// peerUrl: http://<ip>:<port>
func (c *EtcdClient) MemberAdd(peerUrl string) error {
	req := &pb.MemberAddRequest{
		PeerURLs: []string{peerUrl},
	}
	_, err := c.remote.MemberAdd(context.Background(), req)

	return err
}
