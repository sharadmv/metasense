package util

func CheckErr(err error) {
	if err != nil {
		Log.Fatal(err)
	}
}
