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
)

var (
	logger *zap.Logger
)

// Manage run the daemon
func manage() (string, error) {

	// Do something, call goroutines, etc
	run()

	// Set up channel on which to send signal notifications.
	// We must use a buffered channel or risk missing the signal
	// if we're not ready to receive when the signal is sent.
	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt, os.Kill, syscall.SIGTERM)

	// loop work cycle with accept interrupt by system signal
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
	return "Exit", nil
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
	status, err := manage()
	if err != nil {
		fmt.Println(status, "\nError: ", err)
		os.Exit(1)
	}
	fmt.Println(status)
}
