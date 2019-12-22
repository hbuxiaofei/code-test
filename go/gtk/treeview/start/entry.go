package start

import (
	"log"

	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gdk"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/util"
)

func StartPrint() {
	log.Println("run StartPrint...")
}

func onEntryWindowDestroy() {
	log.Println("on_entry_window_destroy...")
	gtk.MainQuit()
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

	obj, err = builder.GetObject("tv_col1")
	util.ErrorCheck(err)
	tvCol1, err := util.IsTreeViewColumn(obj)
	util.ErrorCheck(err)
	tvCol1.SetTitle("1234")

	obj, err = builder.GetObject("tv_col2")
	util.ErrorCheck(err)
	tvCol1, err = util.IsTreeViewColumn(obj)
	util.ErrorCheck(err)
	tvCol1.SetTitle("5678")

	obj, err = builder.GetObject("tv_col3")
	util.ErrorCheck(err)
	tvCol1, err = util.IsTreeViewColumn(obj)
	util.ErrorCheck(err)
	tvCol1.SetTitle("abcd")

	obj, err = builder.GetObject("tv_col4")
	util.ErrorCheck(err)
	tvCol1, err = util.IsTreeViewColumn(obj)
	util.ErrorCheck(err)
	tvCol1.SetTitle("efgh")
	win.Show()
}
