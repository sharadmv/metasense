package util

import (
	"github.com/op/go-logging"
	"os"
)

var Log = logging.MustGetLogger("example")

var format = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000} %{shortfunc} ▶ %{level:.4s} %{id:03x}%{color:reset} %{message}`,
)
var backend = logging.NewLogBackend(os.Stderr, "", 0)
var backendFormatter = logging.NewBackendFormatter(backend, format)

func InitLogging() {
	logging.SetBackend(backendFormatter)
}
