package start

import (
	"log"

	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gdk"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/activator"
	"virtualware/menu"
	"virtualware/navigator"
	"virtualware/operation"
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

	// setting cursor
	gdkWin, err := scr.GetRootWindow()
	if err == nil {
		display, err := gdk.DisplayGetDefault()
		if err == nil {
			cursor, err := gdk.CursorNewFromName(display, "default")
			if err == nil {
				gdkWin.SetCursor(cursor)
			}
		}
	}

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

	// setting menu_box
	obj, err = builder.GetObject("menu_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)
	menuBoxEntry, _ := menu.Entry()
	box.Add(menuBoxEntry)

	// setting navigator_box
	obj, err = builder.GetObject("navigator_box")
	util.ErrorCheck(err)
	box, err = util.IsBox(obj)
	util.ErrorCheck(err)
	navigatorBoxEntry, _ := navigator.Entry()
	box.Add(navigatorBoxEntry)

	// setting activator_box
	obj, err = builder.GetObject("activator_box")
	util.ErrorCheck(err)
	box, err = util.IsBox(obj)
	util.ErrorCheck(err)
	activatorBoxEntry, _ := activator.Entry()
	box.Add(activatorBoxEntry)

	// setting operation_box
	obj, err = builder.GetObject("operation_box")
	util.ErrorCheck(err)
	box, err = util.IsBox(obj)
	util.ErrorCheck(err)
	operationBoxEntry, _ := operation.Entry()
	box.Add(operationBoxEntry)

	win.Show()
}
