use std::fmt;

#[derive(Debug)]
struct Structure(i32);

#[derive(Debug)]
struct Deep(Structure);

impl fmt::Display for Deep {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.0.0)
    }
}

fn main() {
    println!("{:?} months in a year.", 12);

    println!(
        "{1:?} {0:?} is the {actor:?} name.",
        "Slater",
        "Christian",
        actor = "actor's"
    );

    println!("Now {:?} will print!", Structure(3));

    // 使用 `derive` 的一个问题是不能控制输出的形式。
    // 比如我只想展示一个 `7`
    println!("Now {:?} will print!", Deep(Structure(7)));

    // 实现只展示一个 `7`，需要实现 `fmt::Display` 这个 `trait`
    println!("Now {} will print!", Deep(Structure(7)));
}
