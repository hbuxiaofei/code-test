use serde_json::json;

use serde::Deserialize;

use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::path::Path;

////////////////////example1////////////////////////////////////////////////////

fn example1() {
    // The type of `john` is `serde_json::Value`
    let john = json!({
	"name": "John Doe",
	"age": 43,
	"phones": [
	    "+44 1234567",
	    "+44 2345678"
	]
    });

    // Convert to a string of JSON and print it out
    println!("> Json: {:?}", john.to_string());

    println!("> First phone number: {:?}\n", john["phones"][0]);
}


////////////////////example2////////////////////////////////////////////////////

#[derive(Deserialize, Debug)]
struct User {
    name: String,
    age: u32,
    address: String,
    phones: String,
}

fn read_user_from_file<P: AsRef<Path>>(path: P) -> Result<User, Box<Error>> {
    // Open the file in read-only mode with buffer.
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    // Read the JSON contents of the file as an instance of `User`.
    let u = serde_json::from_reader(reader)?;

    // Return the `User`.
    Ok(u)
}
fn example2(){
    let u = read_user_from_file("src/strong.json").unwrap();
    println!("> Json: {:#?} \n", u);
}

////////////////////example3////////////////////////////////////////////////////
fn example3() {
    let f = File::open("src/weak.json").unwrap();
    let v: serde_json::Value = serde_json::from_reader(f).unwrap();
    println!("> Json: {:#?} ", v);
    println!("> Name: {:?}  ", v["name"].as_str().unwrap());
    println!("> Age: {:?} ", v["age"].as_i64().unwrap());
    println!("> First phone number: {:?}\n", v["phones"][0]);
}

fn main() {
    println!(">>> run example1: ");
    example1();
    println!(">>> run example2: ");
    example2();
    println!(">>> run example3: ");
    example3();
}
