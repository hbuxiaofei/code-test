fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}

fn first_word2(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}

fn main() {
    let mut s = String::from("hello world");

    let word_pos = first_word(&s);
    let word_first = first_word2(&s);

    println!("firs word position: {}", word_pos);
    println!("firs word 1: {}", word_first);

    let slice = &s[0..5];
    println!("firs word 2: {}", slice);

    s.clear();
}
