package util

import (
	"errors"
	"log"

	"github.com/gotk3/gotk3/glib"
	"github.com/gotk3/gotk3/gtk"
)

func IsWindow(obj glib.IObject) (*gtk.Window, error) {
	if wd, ok := obj.(*gtk.Window); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.Window")
}

func IsOffscreenWindow(obj glib.IObject) (*gtk.OffscreenWindow, error) {
	if wd, ok := obj.(*gtk.OffscreenWindow); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.OffscreenWindow")
}

func IsBox(obj glib.IObject) (*gtk.Box, error) {
	if wd, ok := obj.(*gtk.Box); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.Box")
}
func IsMenu(obj glib.IObject) (*gtk.Menu, error) {
	if wd, ok := obj.(*gtk.Menu); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.Menu")
}

func IsMenuItem(obj glib.IObject) (*gtk.MenuItem, error) {
	if wd, ok := obj.(*gtk.MenuItem); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.MenuItem")
}

func IsTreeView(obj glib.IObject) (*gtk.TreeView, error) {
	if wd, ok := obj.(*gtk.TreeView); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.TreeView")
}
func IsTreeStore(obj glib.IObject) (*gtk.TreeStore, error) {
	if wd, ok := obj.(*gtk.TreeStore); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.TreeStore")
}

func IsListStore(obj glib.IObject) (*gtk.ListStore, error) {
	if wd, ok := obj.(*gtk.ListStore); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.ListStore")
}
func IsTreeViewColumn(obj glib.IObject) (*gtk.TreeViewColumn, error) {
	if wd, ok := obj.(*gtk.TreeViewColumn); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.TreeViewColumn")
}

func IsNotebook(obj glib.IObject) (*gtk.Notebook, error) {
	if wd, ok := obj.(*gtk.Notebook); ok {
		return wd, nil
	}
	return nil, errors.New("not a *gtk.NoteBook")
}

func ErrorCheck(e error) {
	if e != nil {
		// panic for any errors.
		log.Panic(e)
	}
}
