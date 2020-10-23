use std::cell::Cell;
use std::cell::RefCell;
use std::rc::Rc;
use std::sync::Arc;

fn rc_example() {
    println!("rc >>> example 1:");
    let five: Rc<u32> = Rc::new(5);
    let five2 = five.clone();

    let five_val: u32 = *five;
    println!("five is {}", five_val);
    assert_eq!(five_val, 5);

    let five2_val: u32 = *five2;
    println!("five2 is {}", five2_val);
    println!("five strong count is: {}", Rc::strong_count(&five));

    println!("rc >>> example 2:");
    let mut x = Rc::new(3);
    let y = x.clone();

    *Rc::make_mut(&mut x) = *x - 1;

    println!("x strong count is: {}", Rc::strong_count(&x));

    println!("x is {}, y is {}", *x, *y);
}

fn arc_example() {
    println!("\narc >>> example 1:");
    let five: Arc<u32> = Arc::new(5);
    let five2 = five.clone();

    let five_val: u32 = *five;
    println!("five is {}", five_val);
    assert_eq!(five_val, 5);

    let five2_val: u32 = *five2;
    println!("five2 is {}", five2_val);
    println!("five strong count is: {}", Arc::strong_count(&five));
}

#[derive(Debug)]
struct Point {
    x: Cell<i32>,
    y: RefCell<i32>,
}
fn arc_example2_modify(p: Arc<Point>) {
    p.x.set(10); // for Cell
    *(p.y.borrow_mut()) = 20; // for RefCell
    println!("modify x:{}", p.x.get());
    println!("modify y:{}", p.y.borrow());
    println!("modify p is {:?}", p);
}

fn arc_example2() {
    println!("\narc >>> example 2:");
    let p = Arc::new(Point {
        x: Cell::new(1),
        y: RefCell::new(2),
    });

    println!("last x:{}", p.x.get());
    println!("last y:{}", p.y.borrow());
    println!("before p is {:?}", p);

    arc_example2_modify(p.clone());

    println!("last x:{}", p.x.get());
    println!("last y:{}", p.y.borrow());
    println!("last p is {:?}", p);
}

fn main() {
    rc_example();
    arc_example();
    arc_example2();
}
