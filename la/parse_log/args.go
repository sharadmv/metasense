package main

import (
	"github.com/alecthomas/kingpin"
)

type Args struct {
	filename *string
}

func parseArgs() Args {
	args := Args{}
	args.filename = kingpin.Arg("filename", "Name of file.").Required().String()
	kingpin.Parse()
	return args
}
