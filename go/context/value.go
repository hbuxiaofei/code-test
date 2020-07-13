package main

import (
    "context"
    "fmt"
)


func storeValue(ctx context.Context) {
    ret, _ := ctx.Value("id").(int)
    fmt.Printf("id: %v\n", ret)

    str , _ := ctx.Value("session").(string)
    fmt.Printf("session: %v\n", str)
}

func storeValueTest() {
    ctx := context.WithValue(context.Background(), "id", 3361)
    ctx = context.WithValue(ctx, "session", "3ad2-3dae-34fe-2fe4")
    storeValue(ctx)
}

func main() {
    storeValueTest()
}
