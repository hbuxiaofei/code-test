package main

import (
	"fmt"
	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
	"log"
	"os"
)

func main() {
	const appId = "com.nayoso.example"

	app, err := gtk.ApplicationNew(appId, glib.APPLICATION_FLAGS_NONE)

	if err != nil {
		log.Fatal("Could not create application.", err)
	}

	app.Connect("activate", func() {
		onActivate(app)
	})

	app.Run(os.Args)
}

func onActivate(application *gtk.Application) {

	appWindow, err := gtk.ApplicationWindowNew(application)
	if err != nil {
		log.Fatal("Could not create application window.", err)
	}
	appWindow.SetTitle("Basic Application.")
	appWindow.SetDefaultSize(400, 400)

	// 以水平布局创建一个容器, 第二个参数是其中控件的像素间隔
	buttonBox, err := gtk.BoxNew(gtk.ORIENTATION_HORIZONTAL, 2)
	if err != nil {
		log.Fatal(err)
	}

	// 将布局添加到window中
	appWindow.Add(buttonBox)

	// 创建一个按钮
	button, err := gtk.ButtonNewWithLabel("Hello World")
	if err != nil {
		log.Fatal(err)
	}

	// 将按钮添加到box容器中
	buttonBox.Add(button)

	button.Connect("clicked", func() {
		// 为按钮点击添加一个函数，每次点击都会在命令行输出Hello World
		fmt.Println("Hello World")
		// 摧毁窗口
		appWindow.Destroy()
	})

	// 与Show()不同在于，它会输出Window中的子控件。你可以修改，查看不同的效果
	appWindow.ShowAll()
}
