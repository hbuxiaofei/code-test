// #[derive(Debug, Copy, Clone)]
struct Person {
    name: String,
    age: u8
}


trait Descriptive {
    // 默认的方法
    fn describe(&self) -> String {
        String::from("[Object]")
    }
}
impl Descriptive for Person {
    // override 默认方法
    fn describe(&self) -> String {
        format!("My name is: {}, age: {}", self.name, self.age)
    }
}


// 特性做参数
fn output(object: &impl Descriptive) {
    println!("output       : {}", object.describe());
}

fn output2<T: Descriptive>(object: &T) {
    println!("output2      : {}", object.describe());
}

fn output2_two<T: Descriptive>(arg1: &T, arg2: &T) {
    println!("output2_two 1: {}", arg1.describe());
    println!("output2_two 2: {}", arg2.describe());
}


fn main() {
    let xiaoli = &Person {
        name: String::from("Xiaoli"),
        age: 24
    };

    println!("{}", xiaoli.describe());
    output(xiaoli);
    output2(xiaoli);
    output2_two(xiaoli, xiaoli);

}
