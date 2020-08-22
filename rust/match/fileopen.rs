use std::fs::File;

fn main() {
    let f = File::open("hello.txt");


    match f {
        Ok(f) => {
            println!("File opened successfully: {:?}", &f);
            println!("File opened successfully: {:#?}", &f);
        },
        Err(err) => {
            println!("Failed to open the file: \n{:?}", err);
            println!("Failed to open the file: \n{:#?}", err);
        }
    }
}
