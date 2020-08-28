use std::thread;
use std::time::Duration;

fn closure_even() {
    let is_even = |x: i32| -> bool {
        x%2 == 0
    };

    let mut no = 13;
    println!("{} is even ?: {}", no, is_even(no));

    no = 12;
    println!("{} is even ?: {}", no, is_even(no));

    println!();
}

fn closure_outval() {
    let val = 10;

    // 访问外层作用域变量 val
    let calc = |x: i32| -> i32 {x + val};

    let x = 2;
    println!("{} plus {} is: {}", x, val, calc(x));

    println!();
}

fn closure_plus() {
    // 闭包可以省略类型声明, 自动判断类型
    let get_sum = |x, y|{
        x + y
    };

    let x = 2;
    let y = 3;
    println!("{} plus {} is: {}", x, y, get_sum(x, y));

    println!();
}

fn closure_move() {
    let mut num = 5;
    {
        let mut add_num = |x: i32| num += x;
        add_num(5);
    }
    println!("num is 10?: num={}", num);

    let mut num2 = 5;
    {
        // move, 实现copy trait的变量，是副本进了closure; 真身并没有影响
        let mut add_num2 = move |x: i32| num2 = num2 + x;
        add_num2(5);
    }
    println!("num2 is 5?: num2={}", num2);


    println!();
}

fn closure_thread() {
    let mut x = 1;

    // move, 实现copy trait的变量，是副本进了closure; 真身并没有影响
    thread::spawn(move || {
        println!("enter thread...");
        x = x + 1;
        println!("x is {}", x);
    });

    thread::sleep(Duration::from_millis(100));
    println!("exit thread...");
    println!("x is {}", x);
    println!();
}


fn main() {
    closure_even();
    closure_outval();
    closure_plus();
    closure_move();
    closure_thread();
}
