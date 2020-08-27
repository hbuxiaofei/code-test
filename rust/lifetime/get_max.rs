fn get_max<'a>(x: &'a u32, y: &'a u32) -> &'a u32 {
    if x > y {
        x
    } else {
        y
    }
}

fn main() {
    let x = 10;
    let y = 20;

    // borrowing（借用）,函数是借用
    let max = get_max(&x, &y);

    println!("{} and {} max is: {}", x, y, max);

    // References（引用）,赋值是引用
    let x_ref = &x;
    println!("x {} ref is: {}", x, x_ref);
}

