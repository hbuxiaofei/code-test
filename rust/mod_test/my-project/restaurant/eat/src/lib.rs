pub fn cat_eat_at_restaurant() {
    println!("cat eat at restaurant...");
}

pub fn dog_eat_at_restaurant() {
    println!("dog eat at restaurant...");
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
