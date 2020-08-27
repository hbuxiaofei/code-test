fn max(array: &[i32]) -> i32 {
    let mut max_index = 0;
    let mut i = 1;

    while i < array.len() {
        if array[i] > array[max_index] {
            max_index = i;
        }
        i += 1;
    }
    array[max_index]
}

fn max2<T: PartialOrd + Copy>(array: &[T]) -> T {
    let mut max_index = 0;
    let mut i = 1;

    while i < array.len() {
        if array[i] > array[max_index] {
            max_index = i;
        }
        i += 1;
    }
    array[max_index]
}

fn max3<T>(array: &[T]) -> T
    where T: PartialOrd + Copy
{

    let mut max_index = 0;
    let mut i = 1;

    while i < array.len() {
        if array[i] > array[max_index] {
            max_index = i;
        }
        i += 1;
    }
    array[max_index]
}

fn main() {
    let a = [2, 4, 6, 3, 1];
    println!("max = {}", max(&a));
    println!("max2 = {}", max2(&a));
    println!("max3 = {}", max3(&a));
}
