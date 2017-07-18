package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"github.com/sharadmv/metasense/la/util"
	"io"
	"io/ioutil"
	"strconv"
)

type GasParams struct {
	Weights   []float64 `json:weights`
	Intercept float64   `json:intercept`
}

type Params struct {
	O3  GasParams `json:O3`
	CO  GasParams `json:CO`
	NO2 GasParams `json:NO2`
}

type Record struct {
}

func CO(coA float64, coW float64, o3A float64, o3W float64, no2A float64, no2W float64,
	temperature float64, humidity float64, weights []float64, intercept float64) float64 {
	COppm := 0.0
	coVector := []float64{1, coA, coW, temperature, humidity, coA * coA, coA * coW, coA * temperature, coA * humidity, coW * coW, coW * temperature, coW * humidity, temperature * temperature, temperature * humidity, humidity * humidity}
	for i := 0; i < 15; i++ {
		COppm += coVector[i] * weights[i]
	}
	COppm += intercept
	return COppm
}

func readParams(paramsPath string) Params {
	byt, err := ioutil.ReadFile(paramsPath)
	var dat Params
	err = json.Unmarshal(byt, &dat)
	util.CheckErr(err)
	return dat
}

func parseLine(record []string) {
}

func testFile(file io.Reader, paramsPath string) {
	params := readParams(paramsPath)
	reader := csv.NewReader(file)
	first := true
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		} else {
			util.CheckErr(err)
		}
		if first {
			first = false
			continue
		}
		datetime := record[0]
		no2A, _ := strconv.ParseFloat(record[1], 32)
		no2W, _ := strconv.ParseFloat(record[2], 32)
		o3A, _ := strconv.ParseFloat(record[3], 32)
		o3W, _ := strconv.ParseFloat(record[4], 32)
		coA, _ := strconv.ParseFloat(record[5], 32)
		coW, _ := strconv.ParseFloat(record[6], 32)
		temperature, _ := strconv.ParseFloat(record[7], 32)
		humidity, _ := strconv.ParseFloat(record[9], 32)
		actualCO, _ := strconv.ParseFloat(record[12], 32)
		fmt.Printf("%s,%.3f,%.3f\n", datetime, CO(coA, coW, o3A, o3W, no2A, no2W, temperature, humidity, params.CO.Weights, params.CO.Intercept), actualCO)
	}
}
