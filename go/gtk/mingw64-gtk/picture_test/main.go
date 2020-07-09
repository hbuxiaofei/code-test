package main

import (
	"fmt"
	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
	"log"
	"os"
	"path/filepath"
	"runtime"
)

const (
	appId          = "com.chinesechess.example"
	windowsTempDir = "C:\\Windows\\Temp\\" + appId
	linuxTempDir   = "/tmp/" + appId
)

func main() {

	// 解压资源文件
	resourcesRestore()

	app, _ := gtk.ApplicationNew(appId, glib.APPLICATION_FLAGS_NONE)
	_, err := app.Connect("activate", func() {
		createWindow(app)
	})
	if err != nil {
		log.Fatal(err)
	}

	app.Run(os.Args)
}

func createWindow(application *gtk.Application) {
	// 从文件中创建Builder
	resFile := filepath.Join(getTempDir(), "resources", "ui", "builder.ui")
	fmt.Println(resFile)
	builder, err := getBuilder(resFile)
	if err != nil {
		log.Fatal(err)
	}

	// 获取window窗口
	winObj, _ := builder.GetObject("window1")
	window := winObj.(*gtk.Window)
	application.AddWindow(window)

	// window 窗口设置
	window.SetSizeRequest(596, 651)        //设置窗口大小(width, height)
	window.SetTitle("Chinese Chess")       //设置标题
	window.SetResizable(false)             //设置不可伸缩
	window.SetPosition(gtk.WIN_POS_CENTER) //设置居中显示
	resFile = filepath.Join(getTempDir(), "resources", "image", "app.png")
	fmt.Println(resFile)
	err = window.SetIconFromFile(resFile) //设置icon
	if err != nil {
		log.Fatal(err)
	}

	//获取image控件
	imageObj, err := builder.GetObject("image1")
	if err != nil {
		log.Fatal(err)
	}
	image1 := imageObj.(*gtk.Image)

	//获取image控件大小
	w, h := image1.GetSizeRequest()
	fmt.Println(w, h)

	// 设置图片
	resFile = filepath.Join(getTempDir(), "resources", "image", "board.png")
	fmt.Println(resFile)
	image1.SetFromFile(resFile)

	resFile = filepath.Join(getTempDir(), "resources", "image", "app.png")
	fmt.Println(resFile)
	image1.SetFromFile(resFile)

	// 显示所有界面
	window.ShowAll()
}

func getBuilder(filename string) (*gtk.Builder, error) {

	b, err := gtk.BuilderNew()
	if err != nil {
		return nil, err
	}

	if filename != "" {
		err = b.AddFromFile(filename)
		if err != nil {
			return nil, err
		}
	}

	return b, nil
}

func getTempDir() string {
	if runtime.GOOS == "windows" {
		return windowsTempDir
	} else {
		return linuxTempDir
	}
}

func isDirectory(path string) bool {
	s, err := os.Stat(path)
	if err != nil {
		return false
	}
	return s.IsDir()
}

func resourcesRestore() error {
	// 设置需要释放的目录
	dirs := [][]string{{"resources", "image"}, {"resources", "ui"}}

	if isDirectory(getTempDir()) {
		os.RemoveAll(getTempDir())
	}

	isSuccess := true
	for i := range dirs {
		dir := ""
		for j := range dirs[i] {
			dir = filepath.Join(dir, dirs[i][j])
		}
		// 解压dir目录到当前目录
		if err := RestoreAssets(getTempDir(), dir); err != nil {
			isSuccess = false
			break
		}
	}

	if !isSuccess && isDirectory(getTempDir()) {
		os.RemoveAll(getTempDir())
	}
	return nil
}
