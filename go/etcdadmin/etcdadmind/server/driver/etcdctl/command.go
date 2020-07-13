package etcdctl

import (
	"bytes"
	"context"
	"os/exec"
	"syscall"
	"time"
)

type CmdResult struct {
	stdout string
	stderr string
	err    error
}

const (
	// command timeout 10s
	cmdtimeout = 10
)

func startCmd(ctx context.Context, cmd *exec.Cmd) error {
	if err := cmd.Start(); err != nil {
		return err
	}

	errCh := make(chan error, 1)
	go func() {
		errCh <- cmd.Wait()
	}()

	done := ctx.Done()
	for {
		select {
		case <-done:
			pid := cmd.Process.Pid
			if err := syscall.Kill(-1*pid, syscall.SIGKILL); err != nil {
				return err
			}
		case err := <-errCh:
			if done == nil {
				return ctx.Err()
			}
			return err
		}
	}
}

func cmdExec(env []string, name string, args ...string) *CmdResult {
	var outInfo bytes.Buffer
	var errInfo bytes.Buffer

	cmd := exec.Command(name, args...)
	cmd.Stdout = &outInfo
	cmd.Stderr = &errInfo
	cmd.Env = env

	// timeout: cmdtimeout
	ctx, cancel := context.WithTimeout(context.Background(),
		time.Second*cmdtimeout)
	defer cancel()

	err := startCmd(ctx, cmd)

	result := &CmdResult{}
	result.err = err
	result.stdout = outInfo.String()
	result.stderr = errInfo.String()

	return result
}

func CmdEtcdctl(args ...string) *CmdResult {
	env := []string{"ETCDCTL_API=3"}
	name := "etcdctl"
	argsWithDefault := append(args, "--dial-timeout=2s", "--command-timeout=3s")

	return cmdExec(env, name, argsWithDefault...)
}
