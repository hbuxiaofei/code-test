package main

import (
	"fmt"
	"sync"
	"time"
)

type KeyLock struct {
	m sync.Map
}

func (k *KeyLock) TryLock(key interface{}) bool {
	_, ok := k.m.LoadOrStore(key, struct{}{})
	return !ok
}

func (k *KeyLock) WaitLock(key interface{}, retry int) bool {
	for i := 0; i < retry; i++ {
		if k.TryLock(key) {
			return true
		} else {
			time.Sleep(time.Microsecond)
		}
	}
	return false
}

func (k *KeyLock) UnLock(key interface{}) {
	k.m.Delete(key)
}

func main() {
	tmp1 := 0
	tmp2 := 0
	wg := sync.WaitGroup{}
	lock := &KeyLock{}

	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			for {
				if lock.TryLock("hello") {
					tmp1++
					lock.UnLock("hello")
					break
				} else {
					time.Sleep(time.Microsecond)
				}

			}
			wg.Done()
		}()

		wg.Add(1)
		go func() {
			tmp2++
			wg.Done()
		}()
	}

	wg.Wait()
	fmt.Println("tmp1 =", tmp1)
	fmt.Println("tmp2 =", tmp2)
	fmt.Println("结果：由于tmp2未加锁，因此tmp2会得到没法预料的值")
}
