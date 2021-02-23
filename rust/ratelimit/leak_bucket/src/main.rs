use std::thread;

use std::thread::sleep;
use std::time::{Duration, Instant};

use vmm_sys_util::eventfd::EventFd;

/// Used to improve the accuracy of bucket level.
const ACCURACY_SCALE: u64 = 1000;
/// Nanoseconds per second.
const NANOS_PER_SEC: u64 = 1000000000;

/// Structure used to describe a Leaky Bucket.
pub struct LeakBucket {
    /// Indicate the capacity of bucket, which is config by user.
    capacity: u64,
    /// Current water level.
    level: u64,
    /// Internal used to calculate the delay of timer.
    prev_time: Instant,
    /// Indicate whether the timer started.
    timer_started: bool,
    /// When bucket is ready for allowing more IO operation, the internal callback will write this FD.
    /// This FD should be listened by IO thread.
    timer_wakeup: EventFd,
}

impl LeakBucket {
    /// Construct function
    ///
    /// # Arguments
    ///
    /// * `units_ps` - iops value, eg. 100
    pub fn new(units_ps: u64) -> Self {
        LeakBucket {
            capacity: units_ps * ACCURACY_SCALE,
            level: 0,
            prev_time: Instant::now(),
            timer_started: false,
            timer_wakeup: EventFd::new(libc::EFD_NONBLOCK).unwrap(),
        }
    }

    /// Return true if the bucket is full, and caller must return directly instead of launching IO.
    /// Otherwise, caller should not be affected.
    ///
    /// # Arguments
    ///
    pub fn throttled(&mut self) -> bool {
        // capacity value is zero, indicating that there is no need to limit
        if self.capacity == 0 {
            return false;
        }
        if self.timer_started {
            return true;
        }

        // update the water level
        let now = Instant::now();
        let nanos = (now - self.prev_time).as_nanos();
        if nanos > (self.level * NANOS_PER_SEC / self.capacity) as u128 {
            self.level = 0;
        } else {
            self.level -= nanos as u64 * self.capacity / NANOS_PER_SEC;
        }

        self.prev_time = now;

        // need to be throttled
        if self.level > self.capacity {
            sleep(Duration::from_nanos(
                (self.level - self.capacity) * NANOS_PER_SEC / self.capacity,
            ));
            return true;
        }

        self.level += ACCURACY_SCALE;

        false
    }
}

fn main() {
    println!("Hello, world!");

    let mut leak_bucket = LeakBucket::new(4);

    let mut i = 0;
    loop {
        if !leak_bucket.throttled() {
            println!("num: {}", i);
            i += 1;
        }

        if i >= 20 {
            break;
        }
        thread::sleep(Duration::from_millis(10));
    }
}
