package main

import (
    "context"
    "fmt"
    "time"
)

func test() {
    // 3s timeout
    ctx, cancel := context.WithTimeout(context.Background(), time.Second * 3)
    defer cancel()

    over := false
    c := make(chan int)
    go func() {
        i := 0
        for ; i < 5; i++  {
            fmt.Printf("timer: %v\n", i)
            time.Sleep(time.Second)
            if over == true {
                break
            }
        }
        c <- i
    }()

    select {
        case <-ctx.Done():
            fmt.Println("timer timeout, 3s ...")
            over = true
        case ret := <- c:
            fmt.Printf("timer over: %v\n", ret)
    }
}

func main() {
    test()
}
