package start

import (
	"log"

	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gdk"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/util"
)

const (
	COLUMN_1 = iota
	COLUMN_2
	COLUMN_3
)

func StartPrint() {
	log.Println("run StartPrint...")
}

func onEntryWindowDestroy() {
	log.Println("on_entry_window_destroy...")
	gtk.MainQuit()
}

func addRow(treeStore *gtk.TreeStore, iter *gtk.TreeIter, text1, text2, text3 string) *gtk.TreeIter {
	i := treeStore.Append(iter)

	err := treeStore.SetValue(i, COLUMN_1, text1)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	err = treeStore.SetValue(i, COLUMN_2, text2)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	err = treeStore.SetValue(i, COLUMN_3, text3)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	return i
}

func Entry() {
	builder, err := gtk.BuilderNewFromFile("start/ui/entry.glade")
	util.ErrorCheck(err)

	// getting secreen size
	scr, _ := gdk.ScreenGetDefault()
	rootwin, _ := scr.GetRootWindow()
	height := rootwin.WindowGetHeight()
	width := rootwin.WindowGetWidth()

	// getting window
	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	// setting window height and width
	win.SetDefaultSize(width-200, height-200)

	// setting window title
	win.SetTitle("VirtualWare")

	// setting window signal
	signals := map[string]interface{}{
		"on_entry_window_destroy": onEntryWindowDestroy,
	}
	builder.ConnectSignals(signals)

	// getting treestore
	obj, err = builder.GetObject("treestore1")
	util.ErrorCheck(err)
	treeStore, err := util.IsTreeStore(obj)
	util.ErrorCheck(err)

	addRow(treeStore, nil, "xiaoli", "18", "male")
	addRow(treeStore, nil, "xiaoliang", "18", "male")
	addRow(treeStore, nil, "xiaohua", "19", "female")
	addRow(treeStore, nil, "xiaohhont", "18", "female")

	// getting scrolledwindow
	obj, err = builder.GetObject("entry_scrolledwindow")
	util.ErrorCheck(err)
	scrolledWindow, err := util.IsScrolledWindow(obj)
	util.ErrorCheck(err)

	scrolledWindow.Connect("edge-reached", func() {
		addRow(treeStore, nil, "xiaohua", "19", "female")
		log.Printf("edge overshot...\n")
	})

	win.ShowAll()
}
