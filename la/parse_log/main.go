package main

import (
	"github.com/sharadmv/metasense/la/util"
	"os"
)

func main() {
	util.InitLogging()

	parseFile(os.Stdin)
}
