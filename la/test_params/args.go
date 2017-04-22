package main

import (
	"github.com/alecthomas/kingpin"
)

type Args struct {
	params *string
}

func parseArgs() Args {
	args := Args{}
	args.params = kingpin.Arg("params", "Name of file.").Required().String()
	kingpin.Parse()
	return args
}
