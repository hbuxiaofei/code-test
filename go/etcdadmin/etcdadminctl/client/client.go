package client

import (
	pb "etcdadminctl/pb/etcdadminpb"
	"fmt"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

type GrpcClient struct {
	caller pb.GrpcEtcdAdminClient
	conn   *grpc.ClientConn
	ip     string
	port   string
}

func New(ip string, port string) *GrpcClient {
	c := &GrpcClient{
		ip:   ip,
		port: port,
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

func (c *GrpcClient) GrpcClientAddmember(name string, ip string) {
	member := pb.AddMemberRequest_Member{Name: name, Ip: ip}
	members := []*pb.AddMemberRequest_Member{&member}

	r, err := c.caller.GrpcAddMember(context.Background(),
		&pb.AddMemberRequest{Members: members})

	if err == nil {
		fmt.Printf("%v \n", r.Errcode)
	} else {
		fmt.Printf("%v %v\n", r.Errcode, r.Errmsg)
	}
}
