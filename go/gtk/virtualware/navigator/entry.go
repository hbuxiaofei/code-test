package navigator

import (
	"github.com/gotk3/gotk3/gtk"
	"log"

	"virtualware/activator"
	"virtualware/util"
)

func notebookChangedHandler(nb *gtk.Notebook, wd *gtk.Widget, page uint) {
	log.Printf("notebook change, page:%d\n", page)
	switch page {
	case 0:
		activator.StoreBox.SetVisible(false)
		activator.NetBox.SetVisible(false)
		activator.ComputeBox.SetVisible(true)
	case 1:
		activator.ComputeBox.SetVisible(false)
		activator.NetBox.SetVisible(false)
		activator.StoreBox.SetVisible(true)
	case 2:
		activator.ComputeBox.SetVisible(false)
		activator.StoreBox.SetVisible(false)
		activator.NetBox.SetVisible(true)
	default:
		log.Printf("notebook change, page:%d not found\n", page)
	}
}

func Entry() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("navigator/ui/entry.glade")
	util.ErrorCheck(err)

	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	// getting notebook
	obj, err = builder.GetObject("entry_notebook")
	util.ErrorCheck(err)
	notebook, err := util.IsNotebook(obj)
	util.ErrorCheck(err)
	notebook.Connect("switch-page", notebookChangedHandler)

	// load compute
	LoadCompute(builder)

	// load store
	LoadStore(builder)

	// load net
	LoadNet(builder)

	win.Remove(box)
	return box, nil
}
