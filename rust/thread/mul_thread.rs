use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// 只有实现Send接口的数据，才能够在线程间转移所有权
// Arc 实现了 Send 接口，所以可以被其他子线程转移所有权

fn mul_thread_val() {
    let val = 100;
    let counter = Arc::new(Mutex::new(val));

    let mut handles = vec![];
    for i in 0..3{

        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut val = counter.lock().unwrap();
            *val+=1;

            println!("run thread {} val: {}", i, *val);

            thread::sleep(Duration::from_millis(10));
        });
        handles.push(handle);
    }
    for handel in handles {
        handel.join().unwrap();
    }

    println!("last val:{} ", val);
}

fn mul_thread_vec() {
    let val = vec![100, 200, 300];
    let counter = Arc::new(Mutex::new(val));

    let mut handles = vec![];
    for i in 0..3{

        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut val = (*counter).lock().unwrap();
            val[i] = val[i] + 1;

            println!("run thread val[{}]: {:?}", i, val[i]);

            thread::sleep(Duration::from_millis(10));
        });
        handles.push(handle);
    }
    for handel in handles {
        handel.join().unwrap();
    }

    // println!("last val:{:?} ", val);
}

fn main() {
    mul_thread_val();
    println!();

    mul_thread_vec();
}
