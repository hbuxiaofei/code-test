use std::cell::Cell;
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

// Cell 只能包裹实现了 Copy 的类型，RefCell 用于更普遍的情况（其它情况都用 RefCell）。
//
// RefCell 的特点：
// 1. 在不确定一个对象是否实现了 Copy 时，直接选 RefCell；
// 2. 如果被包裹对象，同时被可变借用了两次，则会导致线程崩溃。所以需要用户自行判断；
// 3. RefCell 只能用于线程内部，不能跨线程；
// 4. RefCell 常常与 Rc 配合使用（都是单线程内部使用）；
//

//
// Rc 和 Arc 使用引用计数的方法，让程序在同一时刻，实现同一资源的多个所有权拥有者，多个拥有者共享资源。
// 通过 Cell, RefCell，我们可以在需要的时候，就可以修改里面的对象。
//

fn cell_example1() {
    let x = Cell::new(1);
    let y = &x;

    println!("x is {:?}", x);

    x.set(2);
    println!("x is {:?}", x);

    y.set(3);
    println!("x is {:?}", x);
    println!("y is {:?}", y.get());
}

fn cell_example2() {
    #[derive(Debug)]
    struct Point {
        x: Cell<i32>,
        y: Cell<i32>,
    }

    let p = Point {
        x: Cell::new(1),
        y: Cell::new(2),
    };
    let p1 = &p;
    let p2 = &p;

    p1.x.set(4);
    p2.y.set(5);

    println!("p is {:?}", p);
}

fn refcell_example1() {
    #[derive(Debug)]
    struct Point {
        x: RefCell<i32>,
        y: RefCell<i32>,
    }

    let p = Point {
        x: RefCell::new(1),
        y: RefCell::new(2),
    };

    let p1 = &p;
    let p2 = &p;

    *p1.x.borrow_mut() = 40;
    *p2.y.borrow_mut() = 50;

    println!("p is {:?}", p);
}

fn rc_refcell_example() {
    let shared_map: Rc<RefCell<_>> = Rc::new(RefCell::new(HashMap::new()));
    shared_map.borrow_mut().insert("africa", 92388);
    shared_map.borrow_mut().insert("kyoto", 11837);
    println!("shared map is {:?}", shared_map);
}

fn main() {
    cell_example1();
    cell_example2();
    refcell_example1();
    rc_refcell_example();
}
