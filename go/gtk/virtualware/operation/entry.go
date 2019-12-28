package operation

import (
	"github.com/gotk3/gotk3/gtk"
	"log"

	"virtualware/util"
)

const (
	OPERATI_COLUMN1 = iota
	OPERATI_COLUMN2
	OPERATI_COLUMN3
)

func operationaddRow(treeStore *gtk.TreeStore, iter *gtk.TreeIter, text1, text2, text3 string) *gtk.TreeIter {
	i := treeStore.Append(iter)

	err := treeStore.SetValue(i, OPERATI_COLUMN1, text1)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	err = treeStore.SetValue(i, OPERATI_COLUMN2, text2)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	err = treeStore.SetValue(i, OPERATI_COLUMN3, text3)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	return i
}

func Entry() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("operation/ui/entry.glade")
	util.ErrorCheck(err)

	obj, err := builder.GetObject("entry_window")
	util.ErrorCheck(err)
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	// getting treestore
	obj, err = builder.GetObject("treestore1")
	util.ErrorCheck(err)
	treeStore, err := util.IsTreeStore(obj)
	util.ErrorCheck(err)

	operationaddRow(treeStore, nil, "xiaoli", "18", "male")
	operationaddRow(treeStore, nil, "xiaoliang", "18", "male")
	operationaddRow(treeStore, nil, "xiaohong", "18", "female")

	// getting scrolledwindow
	obj, err = builder.GetObject("entry_scrolledwindow")
	util.ErrorCheck(err)
	scrolledWindow, err := util.IsScrolledWindow(obj)
	util.ErrorCheck(err)

	scrolledWindow.Connect("edge-reached", func() {
		operationaddRow(treeStore, nil, "xiaohua", "19", "female")
	})

	win.Remove(box)
	return box, nil
}
