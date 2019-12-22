package activator

import (
	"errors"
	"log"
	"strings"

	// "github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"

	"virtualware/util"
)

var (
	StoreChildBoxMap map[string]*gtk.Box
	StoreBox         *gtk.Box
)

// get box and remove it from window
func storeGetBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/store.glade")
	util.ErrorCheck(err)

	util.ErrorCheck(err)
	obj, err := builder.GetObject("entry_window")
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	// add sub box
	boxstoreRoot, _ := storeGetRootBox()
	boxstoreRoot.SetVisible(true)
	box.Add(boxstoreRoot)
	StoreChildBoxMap["root"] = boxstoreRoot

	// add sub box
	boxstoreDatacenter, _ := storeGetDatacenterBox()
	boxstoreDatacenter.SetVisible(false)
	box.Add(boxstoreDatacenter)
	StoreChildBoxMap["datacenter"] = boxstoreDatacenter

	// add sub box
	boxstoreCluster, _ := storeGetClusterBox()
	boxstoreCluster.SetVisible(false)
	box.Add(boxstoreCluster)
	StoreChildBoxMap["cluster"] = boxstoreCluster

	// add sub box
	boxstoreHost, _ := storeGetHostBox()
	boxstoreHost.SetVisible(false)
	box.Add(boxstoreHost)
	StoreChildBoxMap["host"] = boxstoreHost

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func storeGetRootBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/store_root.glade")
	util.ErrorCheck(err)

	util.ErrorCheck(err)
	obj, err := builder.GetObject("entry_window")
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func storeGetDatacenterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/store_datacenter.glade")
	util.ErrorCheck(err)

	util.ErrorCheck(err)
	obj, err := builder.GetObject("entry_window")
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func storeGetClusterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/store_cluster.glade")
	util.ErrorCheck(err)

	util.ErrorCheck(err)
	obj, err := builder.GetObject("entry_window")
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func storeGetHostBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/store_host.glade")
	util.ErrorCheck(err)

	util.ErrorCheck(err)
	obj, err := builder.GetObject("entry_window")
	win, err := util.IsWindow(obj)
	util.ErrorCheck(err)

	obj, err = builder.GetObject("entry_box")
	util.ErrorCheck(err)
	box, err := util.IsBox(obj)
	util.ErrorCheck(err)

	win.Remove(box)
	return box, nil
}

func storeSetBoxAllInvisible() {
	for key := range StoreChildBoxMap {
		box := StoreChildBoxMap[key]
		box.SetVisible(false)
	}
}

func storeSetBoxVisible(key string) error {
	var isMatched bool = false

	for k := range StoreChildBoxMap {
		if key == k {
			isMatched = true
			break
		}
	}

	if isMatched == true {
		for k := range StoreChildBoxMap {
			if k != key {
				box := StoreChildBoxMap[k]
				box.SetVisible(false)
			}
		}

		box := StoreChildBoxMap[key]
		if box.GetVisible() == true {
			return nil
		} else {
			box.SetVisible(true)
		}
	} else {
		return errors.New("mode not matched")
	}
	return nil
}

func StoreBoxRefresh(ts *gtk.TreeStore, tpath *gtk.TreePath, key string) {

	arryPath := strings.Split(tpath.String(), ":")
	arryLen := len(arryPath)
	log.Printf("> store path:(%d)%s key:%s \n", arryLen, tpath.String(), key)

	switch arryLen {
	case 1:
		storeSetBoxVisible("root")
	case 2:
		storeSetBoxVisible("datacenter")
	case 3:
		storeSetBoxVisible("cluster")
	case 4:
		storeSetBoxVisible("host")
	default:
		log.Printf("refresh store key not found: %d\n", arryLen)
	}
}

func StoreBoxSetParent(box *gtk.Box) error {
	StoreChildBoxMap = make(map[string]*gtk.Box)

	// add sub box
	boxstore, _ := storeGetBox()
	StoreBox = boxstore
	boxstore.SetVisible(false)
	box.Add(boxstore)

	return nil
}
