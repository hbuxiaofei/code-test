#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <sys/mman.h>

#include <linux/kvm.h>


int main()
{
    int ret;
    int kvmfd = open("/dev/kvm", O_RDWR);            // 获取系统中KVM子系统的文件描述符kvmfd
    ioctl(kvmfd, KVM_GET_API_VERSION, NULL);         // 获取KVM版本号
    int vmfd = ioctl(kvmfd, KVM_CREATE_VM, 0);       // 创建一个虚拟机

    unsigned char *ram = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0); // 为虚拟机分配内存，大小4K
    int kfd = open("bootimg", O_RDONLY);             // 打开第一个例子的程序
    read(kfd, ram, 4096);                            // 把程序的读入到虚拟机中，这样等会虚拟机运行的时候就会先开始执行这个打开的程序了

    struct kvm_userspace_memory_region mem = {       // 设置虚拟机内存布局
        .slot = 0,
        .guest_phys_addr = 0,
        .memory_size = 0x1000,
        .userspace_addr = (unsigned long)ram,
    };

    ret = ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &mem);      // 分配虚拟机内存

    int vcpufd = ioctl(vmfd, KVM_CREATE_VCPU, 0);             // 创建VCPU
    int mmap_size = ioctl(kvmfd, KVM_GET_VCPU_MMAP_SIZE, 0);  // 获取VCPU对应的kvm_run结构的大小
    struct kvm_run *run = mmap(NULL, mmap_size, PROT_READ | PROT_WRITE, MAP_SHARED, vcpufd, 0); // 给VCPU分配内存空间

    struct kvm_sregs sregs;
    ret = ioctl(vcpufd, KVM_GET_SREGS, &sregs);               // 获取特殊寄存器
    sregs.cs.base = 0;
    sregs.cs.selector = 0;
    ret = ioctl(vcpufd, KVM_SET_SREGS, &sregs);               // 设置特殊寄存器的值

    struct kvm_regs regs = {
        .rip = 0,
    };
    ret = ioctl(vcpufd, KVM_SET_REGS, &regs);                 // 设置通用寄存器的值

    while(1){
        ret = ioctl(vcpufd, KVM_RUN, NULL);                   // 开始运行虚拟机
        if(ret == -1){
            printf("exit unknown\n");
            return -1;
        }
        switch(run->exit_reason){                             // 检测VM退出的原因
            case KVM_EXIT_HLT:
                puts("KVM_EXIT_HLT");
                return 0;
            case KVM_EXIT_IO:
                putchar(*(((char *)run) + run->io.data_offset));
                break;
            case KVM_EXIT_FAIL_ENTRY:
                puts("entry error");
                return -1;
            default:
                puts("other error");
                printf("exit_reason： %d\n",run->exit_reason);
                return -1;
        }
    }
    return 0;
}

