use std::str;


fn if_let() {
    enum Book {
        Papery(u32),
        Electronic(String)
    }

    let book1 = Book::Papery(100);
    if let Book::Papery(index) = book1 {
        println!("Papery: {}", index);
    } else {
        println!("Not papery book");
    }

    let book2 = Book::Electronic(String::from("http://"));
    if let Book::Papery(index) = book2 {
        println!("Papery: {}", index);
    } else {
        println!("Not papery book");
    }

    let book3 = Book::Electronic(String::from("http://"));
    if let Book::Papery(index) = book3 {
        println!("Papery: {}", index);
    } else if let Book::Electronic(url) = book3  {
        println!("Electronic: {}", url);
    } else {
        println!("Not papery book");
    }
}

fn main() {
    let strtest: &str = "hello world!";

    println!("{}", strtest);

    enum Book {
        Papery(u32),
        Electronic {url: String},
    }

    let book1 = Book::Papery(1001);
    match book1 {
        Book::Papery(i) => {
            println!("{}", i);
        },
        Book::Electronic { url } => {
            println!("{}", url);
        }
    }

    let book2 = Book::Electronic{url: String::from( "http://")};
    match book2 {
        Book::Papery(i) => {
            println!("{}", i);
        },
        Book::Electronic { url } => {
            println!("{}", url);
        }
    }

    println!("\n-------------\n");

    if_let();
}
