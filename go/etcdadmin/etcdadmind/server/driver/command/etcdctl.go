package command

import (
	"fmt"
)

func EtcdctlStart() error {
	result := CmdEtcdctlStart()
	if result.err != nil {
		return result.err
	}
	return nil
}

func GetMemberList() (*map[string]string, error) {

	m := &map[string]string{}
	var err error

	result := CmdEtcdctlMemberList()

	if len(result.stdout) > 0 {
		fmt.Printf("stdout: %v\n", result.stdout)
	}
	if len(result.stderr) > 0 {
		fmt.Printf("stderr: %v\n", result.stderr)
	}
	if result.err != nil {
		fmt.Printf("err: %v\n", result.err)
	}

	return m, err
}
