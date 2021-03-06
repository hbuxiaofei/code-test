/*
 * Default Routine to run after head.s
 *
 */

#define __LIBRARY__

#include <linux/kernel.h>
#include <linux/sched.h>
#include <unistd.h>
#include <asm/system.h>
#include <asm/io.h>
#include <linux/tty.h>
// Use to debug serial
#include <serial_debug.h>

extern void trap_init(void);
extern void video_init(void);
extern void sched_init(void);
extern void mem_init(unsigned long start_mem, unsigned long end_mem);
void init();

// Here contains sycall routines

static inline int fork(void) __attribute__((always_inline));
static inline int pause(void) __attribute__((always_inline));
static inline int sys_debug(char *str);
static inline _syscall0(int,fork)
static inline _syscall1(int, sys_debug, char *, str)

static inline int pause(void) {
    long __res;
    __asm__ volatile("int $0x80\n\t"
            :"=a" (__res)
            :"0" (__NR_pause));
    if( __res >= 0)
        return (int) __res;
    return -1;
}

#define move_to_user_mode() \
    __asm__ ("movl %%esp, %%eax\n\t" \
            "pushl $0x17\n\t" \
            "pushl %%eax\n\t" \
            "pushfl\n\t" \
            "pushl $0x0f\n\t" \
            "pushl $1f\n\t" \
            "iret\n" \
            "1:\t movl $0x17, %%eax\n\t" \
            "movw %%ax, %%ds\n\t" \
            "movw %%ax, %%es\n\t" \
            "movw %%ax, %%fs\n\t" \
            "movw %%ax, %%gs" \
            :::"ax");

int memtest_main(void);
void signal_demo_main(void);
void sched_abcd_demo(void);

int main() {
    video_init();
    trap_init();
    sched_init();
    mem_init(0x100000, 0x300000);
    tty_init();

    // 初始化物理页内存, 将 1MB - 16MB 地址空间的内存进行初始化
    sti();
    // s_printk("Test Serial mem_init = %x\n", mem_init);
    // mmtest_main();
    move_to_user_mode();
    sys_debug("User mode can print string use this syscall\n");
    // now user process can execute!
    // but why cannot schedule!
    if(!fork()) {
        if(!fork()) {
            // sched_abcd_demo();
        } else {
            // signal_demo_main();
        }
        while(1);
    }
}

void sched_abcd_demo() {
    // Here init process (pid = 1) will
    // print AABB randomly
    if(!fork()) {
        while(1)
            sys_debug("A\n");
    }
    if(!fork()) {
        while(1)
            sys_debug("B\n");
    }
    if(!fork()) {
        while(1)
            sys_debug("C\n");
    }
    if(!fork()) {
        while(1)
            sys_debug("D\n");
    }
    while(1);
}
