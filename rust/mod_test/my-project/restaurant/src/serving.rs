use eat;

pub fn take_order() {
    println!("restaurant::serving : take_order");
}

pub fn server_order() {
    println!("restaurant::serving : server_order");
}

pub fn take_payment() {
    println!("restaurant::serving : take_payment");
    eat::dog_eat_at_restaurant();
}

pub mod movies {
    use eat;
    pub fn play(){
        println!("Playing movies");
        eat::cat_eat_at_restaurant();
    }
}
