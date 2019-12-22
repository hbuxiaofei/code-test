package navigator

import (
	"log"

	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/activator"
	"virtualware/util"
)

// IDs to access the tree view columns by
const (
	STORE_COLUMN_TEXT = iota
)

// Append a toplevel row to the tree store for the tree view
func storeAddRow(treeStore *gtk.TreeStore, text string) *gtk.TreeIter {
	return storeAddSubRow(treeStore, nil, text)
}

// Append a sub row to the tree store for the tree view
func storeAddSubRow(treeStore *gtk.TreeStore, iter *gtk.TreeIter, text string) *gtk.TreeIter {
	// Get an iterator for a new row at the end of the list store
	i := treeStore.Append(iter)

	err := treeStore.SetValue(i, STORE_COLUMN_TEXT, text)
	if err != nil {
		log.Fatal("Unable set value:", err)
	}
	return i
}

// Add a column to the tree view (during the initialization of the tree view)
// We need to distinct the type of data shown in either column.
func storeCreateTextColumn(title string, id int) *gtk.TreeViewColumn {
	// In this column we want to show text, hence create a text renderer
	cellRenderer, err := gtk.CellRendererTextNew()
	if err != nil {
		log.Fatal("Unable to create text cell renderer:", err)
	}

	// Tell the renderer where to pick input from. Text renderer understands
	// the "text" property.
	column, err := gtk.TreeViewColumnNewWithAttribute(title, cellRenderer, "text", id)
	if err != nil {
		log.Fatal("Unable to create cell column:", err)
	}

	return column
}

func storeSelectionChangedHandler(st *gtk.TreeSelection, ts *gtk.TreeStore) {
	var iter *gtk.TreeIter
	var model gtk.ITreeModel
	var ok bool
	model, iter, ok = st.GetSelected()
	if ok {
		tpath, err := model.(*gtk.TreeModel).GetPath(iter)
		if err != nil {
			log.Printf("Could not get path from model: %s\n", err)
			return
		}

		val, _ := ts.GetValue(iter, 0)
		selectStr, _ := val.GetString()

		// log.Printf("path: %s select: %s \n", tpath, selectStr)
		activator.StoreBoxRefresh(ts, tpath, selectStr)
	}
}

func LoadStore(builder *gtk.Builder) error {

	// getting treeview
	obj, err := builder.GetObject("tv_store")
	util.ErrorCheck(err)
	computeTreeView, err := util.IsTreeView(obj)
	util.ErrorCheck(err)
	computeTreeView.AppendColumn(storeCreateTextColumn("StoreWare", STORE_COLUMN_TEXT))

	// setting treestore
	computeTreeStore, err := gtk.TreeStoreNew(glib.TYPE_STRING)
	if err != nil {
		log.Fatal("Unable to create tree store:", err)
	}
	computeTreeView.SetModel(computeTreeStore)
	iterDatacenter := storeAddRow(computeTreeStore, "StoreAdapter")
	iterCluster := storeAddSubRow(computeTreeStore, iterDatacenter, "StoreDevice")
	iterHOst := storeAddSubRow(computeTreeStore, iterCluster, "StorePool")
	storeAddSubRow(computeTreeStore, iterHOst, "localpool")
	storeAddSubRow(computeTreeStore, iterHOst, "iscsi")
	storeAddSubRow(computeTreeStore, iterHOst, "fc")

	// setting signal
	computeSelection, err := computeTreeView.GetSelection()
	if err != nil {
		log.Fatal("Could not get tree selection object.")
	}
	computeSelection.SetMode(gtk.SELECTION_SINGLE)
	computeSelection.Connect("changed", storeSelectionChangedHandler,
		computeTreeStore)

	return nil
}
