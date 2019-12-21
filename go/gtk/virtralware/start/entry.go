package start

import (
	"log"

	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/activator"
	"virtualware/navigator"
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

	// setting window
	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)
	signals := map[string]interface{}{
		"on_entry_window_destroy": onEntryWindowDestroy,
	}
	builder.ConnectSignals(signals)

	// setting navigator_box
	obj, err = builder.GetObject("navigator_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
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

	win.Show()
}
