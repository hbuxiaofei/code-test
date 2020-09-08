fn example_mut_borrow() {
    let val = 5;
    println!("val = {}", val);

    // val = 6; // error, val is immutable
    let mut val1 = val; // val1 borrow val, val1 is mutable
    println!("val1 = {}", val1);

    val1 = 6; // change val1
    println!("val1 = {}", val1);
}

fn example_addr_borrow() {
    let val = 5;
    println!("val = {}", val);

    let val1 = &val;
    println!("val = {}", val);

    println!("val1 = {}", *val1);
}

fn example_mut_addr_borrow() {
    let val = 5;
    let val0 = 6;

    let mut val1 = &val;
    println!("val = {}", val);
    println!("val1 = {}", *val1);

    val1 = &val0;
    println!("va0 = {}", val0);
    println!("val1 = {}", *val1);
}

fn example_mut_addr_borrow2() {
    let mut val = 5;

    let mut val1 = &mut val;
    println!("val1 = {}", *val1);

    *val1 = 6;
    println!("val1 = {}", *val1);

    let mut val0 = 50;
    val1 = &mut val0;
    println!("val1 = {}", *val1);
}

fn main() {
    let mut x = None;

    {
        let y: &mut u32 = x.get_or_insert(5);

        assert_eq!(y, &5);

        *y = 7;
    }

    assert_eq!(x, Some(7));

    println!("> example_mut_borrow:");
    example_mut_borrow();
    println!("> example_addr_borrow:");
    example_addr_borrow();
    println!("> example_mut_addr_borrow:");
    example_mut_addr_borrow();
    println!("> example_mut_addr_borrow2:");
    example_mut_addr_borrow2();
}
