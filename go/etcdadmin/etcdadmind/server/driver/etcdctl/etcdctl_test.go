package etcdctl

import (
	"fmt"
	"testing"
)

func TestGetMemberList(t *testing.T) {
	members, _ := GetMemberList()

	fmt.Printf("member list: %v\n", members)

}
