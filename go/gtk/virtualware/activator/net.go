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
	NetChildBoxMap map[string]*gtk.Box
	NetBox         *gtk.Box
)

// get box and remove it from window
func netGetBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/net.glade")
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
	boxnetRoot, _ := netGetRootBox()
	boxnetRoot.SetVisible(true)
	box.Add(boxnetRoot)
	NetChildBoxMap["root"] = boxnetRoot

	// add sub box
	boxnetDatacenter, _ := netGetDatacenterBox()
	boxnetDatacenter.SetVisible(false)
	box.Add(boxnetDatacenter)
	NetChildBoxMap["datacenter"] = boxnetDatacenter

	// add sub box
	boxnetCluster, _ := netGetClusterBox()
	boxnetCluster.SetVisible(false)
	box.Add(boxnetCluster)
	NetChildBoxMap["cluster"] = boxnetCluster

	// add sub box
	boxnetHost, _ := netGetHostBox()
	boxnetHost.SetVisible(false)
	box.Add(boxnetHost)
	NetChildBoxMap["host"] = boxnetHost

	win.Remove(box)
	return box, nil
}

// get box and remove it from window
func netGetRootBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/net_root.glade")
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
func netGetDatacenterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/net_datacenter.glade")
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
func netGetClusterBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/net_cluster.glade")
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
func netGetHostBox() (*gtk.Box, error) {
	builder, err := gtk.BuilderNewFromFile("activator/ui/net_host.glade")
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

func netSetBoxAllInvisible() {
	for key := range NetChildBoxMap {
		box := NetChildBoxMap[key]
		box.SetVisible(false)
	}
}

func netSetBoxVisible(key string) error {
	var isMatched bool = false

	for k := range NetChildBoxMap {
		if key == k {
			isMatched = true
			break
		}
	}

	if isMatched == true {
		for k := range NetChildBoxMap {
			if k != key {
				box := NetChildBoxMap[k]
				box.SetVisible(false)
			}
		}

		box := NetChildBoxMap[key]
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

func NetBoxRefresh(ts *gtk.TreeStore, tpath *gtk.TreePath, key string) {

	arryPath := strings.Split(tpath.String(), ":")
	arryLen := len(arryPath)
	log.Printf("> net path:(%d)%s key:%s \n", arryLen, tpath.String(), key)

	switch arryLen {
	case 1:
		netSetBoxVisible("root")
	case 2:
		netSetBoxVisible("datacenter")
	case 3:
		netSetBoxVisible("cluster")
	case 4:
		netSetBoxVisible("host")
	default:
		log.Printf("refresh net key not found: %d\n", arryLen)
	}
}

func NetBoxSetParent(box *gtk.Box) error {
	NetChildBoxMap = make(map[string]*gtk.Box)

	// add sub box
	boxnet, _ := netGetBox()
	NetBox = boxnet
	boxnet.SetVisible(false)
	box.Add(boxnet)

	return nil
}
