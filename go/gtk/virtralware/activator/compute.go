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
	ComputeChildBoxMap map[string]*gtk.Box
	ComputeBox         *gtk.Box
)

// get box and remove it from window
func computeGetBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/compute.glade")
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
	boxComputeRoot, _ := computeGetRootBox()
	boxComputeRoot.SetVisible(true)
	box.Add(boxComputeRoot)
	ComputeChildBoxMap["root"] = boxComputeRoot

	// add sub box
	boxComputeDatacenter, _ := computeGetDatacenterBox()
	boxComputeDatacenter.SetVisible(false)
	box.Add(boxComputeDatacenter)
	ComputeChildBoxMap["datacenter"] = boxComputeDatacenter

	// add sub box
	boxComputeCluster, _ := computeGetClusterBox()
	boxComputeCluster.SetVisible(false)
	box.Add(boxComputeCluster)
	ComputeChildBoxMap["cluster"] = boxComputeCluster

	// add sub box
	boxComputeHost, _ := computeGetHostBox()
	boxComputeHost.SetVisible(false)
	box.Add(boxComputeHost)
	ComputeChildBoxMap["host"] = boxComputeHost

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func computeGetRootBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/compute_root.glade")
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
func computeGetDatacenterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/compute_datacenter.glade")
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
func computeGetClusterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/compute_cluster.glade")
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
func computeGetHostBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/compute_host.glade")
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

func computeSetBoxAllInvisible() {
	for key := range ComputeChildBoxMap {
		box := ComputeChildBoxMap[key]
		box.SetVisible(false)
	}
}

func computeSetBoxVisible(key string) error {
	var isMatched bool = false

	for k := range ComputeChildBoxMap {
		if key == k {
			isMatched = true
			break
		}
	}

	if isMatched == true {
		for k := range ComputeChildBoxMap {
			if k != key {
				box := ComputeChildBoxMap[k]
				box.SetVisible(false)
			}
		}

		box := ComputeChildBoxMap[key]
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

func ComputeBoxRefresh(ts *gtk.TreeStore, tpath *gtk.TreePath, key string) {

	arryPath := strings.Split(tpath.String(), ":")
	arryLen := len(arryPath)
	log.Printf("> compute path:(%d)%s key:%s \n", arryLen, tpath.String(), key)

	switch arryLen {
	case 1:
		computeSetBoxVisible("root")
	case 2:
		computeSetBoxVisible("datacenter")
	case 3:
		computeSetBoxVisible("cluster")
	case 4:
		computeSetBoxVisible("host")
	default:
		log.Printf("refresh compute key not found: %d\n", arryLen)
	}
}

func ComputeBoxSetParent(box *gtk.Box) error {
	ComputeChildBoxMap = make(map[string]*gtk.Box)

	// add sub box
	boxCompute, _ := computeGetBox()
	ComputeBox = boxCompute
	boxCompute.SetVisible(true)
	box.Add(boxCompute)

	return nil
}
