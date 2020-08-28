use std::thread;
use std::time::Duration;

fn spawn_function() {
    for i in 0..5 {
        println!("spawned thread print {}", i);

        thread::sleep(Duration::from_millis(100));
    }
}

fn main() {

    let handle = thread::spawn(spawn_function);

    let ret = handle.join().unwrap();
    println!("ret = {:?}", ret);
}
