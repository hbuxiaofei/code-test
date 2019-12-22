package operation

import (
	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
	"log"

	"virtualware/util"
)

const (
	OPERATI_COLUMN1 = iota
	OPERATI_COLUMN2
	OPERATI_COLUMN3
	OPERATI_COLUMN4
)

// Add a column to the tree view (during the initialization of the tree view)
func operationCreateColumn(title string, id int) *gtk.TreeViewColumn {
	cellRenderer, err := gtk.CellRendererTextNew()
	if err != nil {
		log.Fatal("Unable to create text cell renderer:", err)
	}

	column, err := gtk.TreeViewColumnNewWithAttribute(title, cellRenderer, "text", id)
	if err != nil {
		log.Fatal("Unable to create cell column:", err)
	}

	return column
}

func operationAddRow(listStore *gtk.ListStore, str1, str2, str3, str4 string) {
	// Get an iterator for a new row at the end of the list store
	iter := listStore.Append()

	// Set the contents of the list store row that the iterator represents
	err := listStore.Set(iter,
		[]int{OPERATI_COLUMN1, OPERATI_COLUMN2, OPERATI_COLUMN3, OPERATI_COLUMN4},
		[]interface{}{str1, str2, str3, str4})

	if err != nil {
		log.Fatal("Unable to add row:", err)
	}
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

	// getting treeview
	obj, err = builder.GetObject("tv_operation")
	util.ErrorCheck(err)
	treeViewOperation, err := util.IsTreeView(obj)
	util.ErrorCheck(err)

	treeViewOperation.AppendColumn(operationCreateColumn("USER", OPERATI_COLUMN1))
	treeViewOperation.AppendColumn(operationCreateColumn("IP", OPERATI_COLUMN2))
	treeViewOperation.AppendColumn(operationCreateColumn("DATE", OPERATI_COLUMN3))
	treeViewOperation.AppendColumn(operationCreateColumn("OPERATION", OPERATI_COLUMN4))

	// Creating a list store. This is what holds the data that will be shown on our tree view.
	listStore, err := gtk.ListStoreNew(glib.TYPE_STRING, glib.TYPE_STRING,
		glib.TYPE_STRING, glib.TYPE_STRING)
	if err != nil {
		log.Fatal("Unable to create list store:", err)
	}
	treeViewOperation.SetModel(listStore)

	operationAddRow(listStore, "andy", "172.23.2.123", "12:00", "shutdown")
	operationAddRow(listStore, "panda", "196.169.23.45", "1:20", "loggin")
	operationAddRow(listStore, "panda", "196.169.23.45", "1:20", "loggin")
	operationAddRow(listStore, "panda", "196.169.23.45", "1:20", "loggin")

	win.Remove(box)
	return box, nil
}
