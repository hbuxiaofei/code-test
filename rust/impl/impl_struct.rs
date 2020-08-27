// struct
struct Example {
    number: i32,
}

// impl
// 结构体 impl 块可以写几次，效果相当于它们内容的拼接
impl Example {
    fn boo(&self) {
        println!("boo! Example::boo() was called!");
    }
}

impl Example {
    fn answer(&mut self) {
        self.number += 42;
    }

    fn get_number(&self) -> i32 {
        self.number
    }
}

fn main() {
    let mut ex = Example{number: 10};
    ex.boo();

    println!("number answer is: {}", ex.get_number());
    ex.answer();
    println!("number result is: {}", ex.get_number());
}
