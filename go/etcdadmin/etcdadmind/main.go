package main

import (
	"etcdadmind/config"
	"etcdadmind/log"
	"etcdadmind/server"
	"fmt"
	"go.uber.org/zap"
	"os"
	"os/signal"
	"syscall"

	"github.com/takama/daemon"
)

const (
	// name of the service
	name        = "etcdadmin"
	description = "Etcd admin daemon"
)

var (
	logger *zap.Logger
)

// Service has embedded daemon
type Service struct {
	daemon.Daemon
}

// Manage by daemon commands or run the daemon
func (service *Service) Manage() (string, error) {

	usage := "Usage: myservice install | remove | start | stop | status"

	// if received any kind of command, do it
	if len(os.Args) > 1 {
		command := os.Args[1]
		switch command {
		case "install":
			return service.Install()
		case "remove":
			return service.Remove()
		case "start":
			return service.Start()
		case "stop":
			return service.Stop()
		case "status":
			return service.Status()
		default:
			return usage, nil
		}
	}

	// Do something, call your goroutines, etc
	run()

	// Set up channel on which to send signal notifications.
	// We must use a buffered channel or risk missing the signal
	// if we're not ready to receive when the signal is sent.
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, os.Kill, syscall.SIGTERM)

	// loop work cycle with accept connections or interrupt
	// by system signal
	for {
		select {
		case killSignal := <-interrupt:
			fmt.Println("Got signal:", killSignal)
			if killSignal == os.Interrupt {
				return "Daemon was interruped by system signal", nil
			}
			return "Daemon was killed", nil
		}
	}

	// never happen, but need to complete code
	return usage, nil
}

func run() {
	cfg := config.Init()

	log.Init(log.Config{
		Level: cfg.Get("LOG_LEVEL"),
		File:  cfg.Get("LOG_FILE"),
	})
	logger = log.GetLogger()

	logger.Info("etcdadmind start.")
	server.Init(cfg.Get("GRPC_PORT"))
}

func main() {
	var dependencies = []string{}

	srv, err := daemon.New(name, description, dependencies...)
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(1)
	}
	service := &Service{srv}
	status, err := service.Manage()
	if err != nil {
		fmt.Println(status, "\nError: ", err)
		os.Exit(1)
	}
	fmt.Println(status)
}
