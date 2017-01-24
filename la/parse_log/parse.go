package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"github.com/sharadmv/metasense/la/util"
	"io"
)

type BoardLogMessage struct {
	Msg   string
	Ts    int
	Rt    int
	Rts   string
	Raw   RawGasData
	Hu_pr EnvironmentSensorData
	Conf  ConfData
}

type ConfData struct {
	PTV int
}

type RawGasData struct {
	Rng float64
	S1A float64
	S1W float64
	S2A float64
	S2W float64
	S3A float64
	S3W float64
	PT  float64
	NC  float64
}

type EnvironmentSensorData struct {
	BT float64
	BP float64
	HT float64
	HH float64
}

func convertRaw(val float64, rng float64) float64 {
	gain := 2.0 / 3.0

	if rng > 0 {
		gain = rng + 0.0
	}
	maxBit := 32767.0
	maxVolt := 4.096 * 1000
	mV := maxVolt * (val / (gain * maxBit))
	return mV
}

func parseLine(line string) BoardLogMessage {
	logMessage := BoardLogMessage{}
	json.Unmarshal([]byte(line), &logMessage)
	return logMessage
}

func printMessage(message BoardLogMessage, negCount *int) {
	if message.Conf.PTV == -1 {
		return
	}
	if message.Rt < 0 {
		*negCount++
	}
	rng := float64(message.Raw.Rng)
	fmt.Printf("%d,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n",
		message.Rt,
		message.Rts,
		convertRaw(message.Raw.S1A, rng),
		convertRaw(message.Raw.S1W, rng),
		convertRaw(message.Raw.S2A, rng),
		convertRaw(message.Raw.S2W, rng),
		convertRaw(message.Raw.S3A, rng),
		convertRaw(message.Raw.S3W, rng),
		message.Hu_pr.BT, message.Hu_pr.BP, message.Hu_pr.HH,
		convertRaw(message.Raw.PT, rng), convertRaw(message.Raw.NC, rng))
}

func parseFile(file io.Reader) {
	fmt.Println("unixtime,datetime,no2-A,no2-W,o3-A,o3-W,co-A,co-W,temperature,pressure,humidity,pt,nc")
	//file, err := os.Open(path)
	totalCount := 0
	negCount := 0
	//util.CheckErr(err)
	//defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		printMessage(parseLine(scanner.Text()), &negCount)
		totalCount++
	}
	util.Log.Infof("Parsed %d lines.", totalCount)
	util.Log.Warningf("Found %d negative timestamps.", negCount)
	util.CheckErr(scanner.Err())

}
