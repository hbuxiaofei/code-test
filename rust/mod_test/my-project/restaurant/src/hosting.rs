pub fn seat_at_table() {
    println!("restaurant::hosting : seat_at_table");
}

pub fn add_to_waitlist() {
    println!("restaurant::hosting : add_to_waitlist");
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
