package main

import (
	"github.com/sharadmv/metasense/la/util"
)

func main() {
	util.InitLogging()

	args := parseArgs()
	util.Log.Debugf("Parsing log file: %s\n", *args.filename)
	parseFile(*args.filename)
}
