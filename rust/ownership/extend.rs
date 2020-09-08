fn concat_literal(s: &mut String) {
    s.extend("world!".chars());
}

fn main() {
    let mut s = "hello, ".to_owned();
    println!("{}", s);
    concat_literal(&mut s);
    println!("{}", s);
}
