/*
 * linux input 模拟鼠标键盘事件
 *
 * ```
 * # cat /proc/bus/input/devices
 * # ls /dev/input/by-path/ -lh
 * ```
 */

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/input.h>
#include <linux/uinput.h>
#include <stdio.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>

#define KEY_L            38
#define KEY_S            31
#define KEY_KPENTER      96


void simulate_key(int fd, int kval)
{
    struct input_event event;
    event.type = EV_KEY;
    event.value = 1;
    event.code = kval;
    gettimeofday(&event.time, 0);
    write(fd, &event, sizeof(event)) ;
    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));

    memset(&event, 0, sizeof(event));
    gettimeofday(&event.time, NULL);
    event.type = EV_KEY;
    event.code = kval;
    event.value = 0;
    write(fd, &event, sizeof(event));
    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));
}

void simulate_mouse(int fd, int x, int y)
{
    struct input_event event;
    memset(&event, 0, sizeof(event));
    gettimeofday(&event.time, NULL);
    event.type = EV_REL;
    event.code = REL_X;
    event.value = x;
    write(fd, &event, sizeof(event));
    event.type = EV_REL;
    event.code = REL_Y;
    event.value = y;
    write(fd, &event, sizeof(event));
    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));
}


void simulate_mouse_left_click(int fd)
{
    struct input_event event;
    memset(&event, 0, sizeof(event));
    gettimeofday(&event.time, NULL);
    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));

    event.type = EV_KEY;
    event.code = BTN_LEFT;
    event.value = 1;
    write(fd, &event, sizeof(event));

    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));

}

void simulate_mousedoubleclick(int fd)
{
    struct input_event event;
    memset(&event, 0, sizeof(event));
    gettimeofday(&event.time, NULL);

    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));

    event.type = EV_KEY;
    event.code = BTN_LEFT;
    event.value = 1;
    write(fd, &event, sizeof(event));

    event.type = EV_KEY;
    event.code = BTN_LEFT;
    event.value = 1;
    write(fd, &event, sizeof(event));

    event.type = EV_SYN;
    event.code = SYN_REPORT;
    event.value = 0;
    write(fd, &event, sizeof(event));

    event.type = EV_KEY;
    event.code = BTN_LEFT;
    event.value = 0;
    write(fd, &event, sizeof(event));
}

int main(int argc, char *argv[])
{
    int fd_kbd;
    int fd_mouse;
    fd_kbd = open("/dev/input/event1", O_RDWR);
    if(fd_kbd <= 0) {
        printf("error open keyboard:\n");
        return -1;
    }
    fd_mouse = open("/dev/input/event0", O_RDWR);
    if(fd_mouse <= 0)
    {
        printf("error open mouse\n");
        return -1;
    }
    /* simulate_key(fd_kbd, atoi(argv[1])); */
    simulate_key(fd_kbd, KEY_L);
    simulate_key(fd_kbd, KEY_S);
    simulate_key(fd_kbd, KEY_KPENTER);
    sleep(1);
    /*
     * simulate_mouse(fd_mouse, atoi(argv[1]), atoi(argv[2]));
     * sleep(1);
     * simulate_mouse_left_click(fd_mouse);
     * sleep(1);
     * simulate_mousedoubleclick(fd_mouse);
     * sleep(1);
     */
    close(fd_kbd);
    close(fd_mouse);
}
