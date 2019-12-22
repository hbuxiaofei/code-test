package menu

import (
	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
	// "log"
	// "reflect"

	"virtualware/util"
)

func Entry() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("menu/ui/entry.glade")
	util.ErrorCheck(err)

	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	// getting menu quit
	obj, err = builder.GetObject("mb_file_quit")
	util.ErrorCheck(err)
	menuQuit, err := util.IsMenuItem(obj)
	util.ErrorCheck(err)
	menuQuit.Connect("activate", func(menuItem *gtk.MenuItem) {
		gtk.MainQuit()
	})

	win.Remove(box)
	return box, nil
}
