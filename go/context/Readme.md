一个 Context 被 cancel，那么它的派生 context 都会收到取消信号（表现为 context.Done() 返回的 channel 收到值）。
有四种方法派生 context ：
```go
func WithCancel(parent Context) (ctx Context, cancel CancelFunc)

func WithDeadline(parent Context, d time.Time) (Context, CancelFunc)

func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)

func WithValue(parent Context, key, val interface{}) Context
```
- WithCancel
最常用的派生 context 方法。该方法接受一个父 context。父 context 可以是一个 background context 或其他 context。
返回的 cancelFunc，如果被调用，会导致 Done channel 关闭。因此，绝不要把 cancelFunc 传给其他方法。

- WithDeadline
该方法会创建一个带有 deadline 的 context。当 deadline 到期后，该 context 以及该 context 的可能子 context 会受到 cancel 通知。另外，如果 deadline 前调用 cancelFunc 则会提前发送取消通知。

- WithTimeout
与 WithDeadline 类似。创建一个带有超时机制的 context。

- WithValue
WithValue 方法创建一个携带信息的 context，可以是 user 信息、认证 token等。该 context 与其派生的子 context 都会携带这些信息。

