package main

import (
    "context"
    "fmt"
    "time"
)

func main() {
    //deadline保存了超时的时间，当超过这个时间，会触发cancel,
    //如果超过了过期时间，会自动撤销它的子context
    d := time.Now().Add(3 * time.Second)
    ctx, cancel := context.WithDeadline(context.Background(), d)

    // Even though ctx will be expired, it is good practice to call its
    // cancelation function in any case. Failure to do so may keep the
    // context and its parent alive longer than necessary.
    defer cancel()

    select {
    case <-time.After(5 * time.Second):
        fmt.Println("overslept")
    case <-ctx.Done():
        fmt.Println(ctx.Err())
    }

}
