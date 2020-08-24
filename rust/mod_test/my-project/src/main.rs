use restaurant::hosting;
use restaurant::serving;

fn main() {
    println!("Hello, world!");

    hosting::add_to_waitlist();
    hosting::seat_at_table();

    serving::take_order();
    serving::server_order();
    serving::take_payment();

    serving::movies::play();
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
