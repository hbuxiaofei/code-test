package activator

import (
	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/util"
)

func Entry() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/entry.glade")
	util.ErrorCheck(err)

	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	// set parent for compute boxes
	ComputeBoxSetParent(box)

	// set parent for store boxes
	StoreBoxSetParent(box)

	win.Remove(box)
	return box, nil
}
