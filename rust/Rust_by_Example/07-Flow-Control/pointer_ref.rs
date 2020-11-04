// 对指针来说，解引用（dereferencing）和解构（destructuring）要区分开，
// 因为这两者的概念是不同的，和 C 那样的语言用法不一样。
//
// - 解引用使用 *
// - 解构使用 &，ref， 和 ref mut
//

fn main() {
    //
    let reference = &4;

    match reference {
        &val => println!("Got a value via destructuring: {:?}", val),
    }

    // 为了避免 `&` 的使用，需要在匹配前解引用。
    match *reference {
        val => println!("Got a value via destructuring: {:?}", val),
    }
}
