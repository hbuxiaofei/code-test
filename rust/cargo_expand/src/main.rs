// stringify! 作用是将其参数直接转换为字符串描述，类型为&'static str
// let one_plus_one = stringify!(1 + 1);
// assert_eq!(one_plus_one, "1 + 1");

macro_rules! m {
    ($($s:stmt)*) => {
        $(
            {  stringify!($s); 1 }
        )<<*
    };
}

fn main() {
    println!(
        "{}{}{}",
        m! { return || true },
        m! { (return) || true },
        m! { {return} || true },
    );
}
