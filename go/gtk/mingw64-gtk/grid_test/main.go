package main

import (
	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
	"os"
)

func main() {
	const appId = "com.nayoso.example"

	app, _ := gtk.ApplicationNew(appId, glib.APPLICATION_FLAGS_NONE)
	app.Connect("activate", func() {
		onActivate(app)
	})
	app.Run(os.Args)
}

func onActivate(application *gtk.Application) {
	appWindow, _ := gtk.ApplicationWindowNew(application)
	appWindow.SetTitle("Grid example")
	//-- 以上，通常的代码输入完了，接下就是这个例子的重点了:-D

	grid, _ := gtk.GridNew() //创建容器
	appWindow.Add(grid)      //将容器添加到window中

	//现在再让我们创建一些按钮来展示grid的效果
	button1, _ := gtk.ButtonNewWithLabel("Button 1")
	button2, _ := gtk.ButtonNewWithLabel("Button 2")
	button3, _ := gtk.ButtonNewWithLabel("Button 3")
	//将buttons添加到grid中
	grid.Attach(button1, 0, 0, 1, 1) //参数：左,上,宽,高
	grid.Attach(button2, 1, 0, 1, 1)
	grid.Attach(button3, 0, 1, 2, 1)
	//-- 注意一下，按钮的位置就像在一个坐标轴中，原点在左上，x轴向右，y轴向下
	//-- 如果你不是很喜欢或者很懂这种方式也没关系，后面我还会介绍可视化的UI设计工具

	appWindow.ShowAll()
}
