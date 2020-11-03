#![allow(unreachable_code)]

fn loop_label() {
    'outer: loop {
        println!("Entered the outer loop");

        'inner: loop {
            println!("Entered the inner loop");

            // 这里只是中断内部循环
            // break;

            // 这会终端外层循环
            break 'outer;
        }
        println!("This poinit will never be reached");
    }

    println!("Exited the outer loop");
}

fn loop_infinite() {
    let mut count = 0u32;

    println!("Let's count until infinity!");

    // 无限循环
    loop {
        count += 1;

        if count == 3 {
            println!("three");

            // 跳过这次迭代的剩下内容
            continue;
        }

        println!("{}", count);

        if count == 5 {
            println!("OK, this's enough");

            // 推出循环
            break;
        }
    }
}

fn loop_return() {
    let mut counter = 0;

    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };
    println!("loop return result: {}", result);
}

fn main() {
    loop_infinite();
    loop_label();
    loop_return();
}
