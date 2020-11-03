// 隐藏未使用代码警告的属性
#![allow(dead_code)]

enum Status {
    Rich,
    Poor,
}

enum Work {
    Civilian,
    Soldier,
}

fn main() {
    use Status::{Poor, Rich};
    let status = Poor;
    match status {
        Rich => println!("The rich have lots of money!"),
        Poor => println!("The poor have no money..."),
    }

    use Work::*;
    let work = Civilian;
    match work {
        Civilian => println!("Civilian work!"),
        Soldier => println!("Soldier fight!"),
    }
}
