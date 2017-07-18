package main

import (
	"github.com/sharadmv/metasense/la/util"
	"os"
)

func main() {
	util.InitLogging()
	args := parseArgs()

	testFile(os.Stdin, *args.params)
}
