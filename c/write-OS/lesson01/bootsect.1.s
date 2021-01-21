# 计算机启动运行在实模式,主要经过以下几个步骤进入保护模式
# Ref 自己动手写操作系统(一)--bootloader

.text

# .code16 表示16位代码段
.code16
.global _start

_start:
	# 1、将ds、es和ss段寄存器均设置成cs段寄存器的值，并将栈顶指针esp指向0x7c00，
	# 栈向低地址增长。这步操作其实也可省略，因为在16位代码段中还用不到其他段寄存器，
	# 在需要使用的时候再初始化也不迟。
	movw %cs, %ax
	movw %ax, %ds           # -> Data Segment
	movw %ax, %es           # -> Extra Segment
	movw %ax, %ss           # -> Stack Segment
	movl $0x7C00, %esp

    # 2、关中断，在后面我们在内存中会建立中断向量表，所以事先关好中断，
    # 防止在建表过程中来了中断，所以事先屏蔽，防止这种情况产生。
	cli

# 3、打开地址线A20。实际上若我们使用qemu跑这个程序时，A20默认已经打开了，
# 但为了兼容性，最好还是手动将A20地址线打开，读者可以试一试将打开A20代码删去后，
# 在保护模式(32位代码段#)下用回滚机制测试时是否仍然显示字符
# 8042(键盘控制器)端口的P21和A20相连，置1则打开
# 0x64端口 读：位1=1 输入缓冲器满(0x60/0x64口有给8042的数据）
# 0x64端口 写: 0xd1->写8042的端口P2，比如位2控制P21 当写时，0x60端口提供数据，比如0xdf，这里面把P2置1

waitforbuffernull1:
	# 先确定8042是不是为空,如果不为空，则一直等待
	xorl %eax,%eax
	inb $0x64,%al
	testb $0x2,%al
	jnz waitforbuffernull1
	# 8042中没有命令，则开始向0x64端口发出写P2端口的命令
	movb $0xd1,%al
	outb %al,$0x64

waitforbuffernull2:
	# 再确定8042是不是为空,如果不为空，则一直等待
	xorl  %eax, %eax
	inb   $0x64, %al
	testb $0x2, %al
	jnz waitforbuffernull2
	# 向0x60端口发送数据，即把P2端口设置为0xdf
	movb $0xdf, %al
	outb %al,   $0x60

	# 在实模式下，不能通过BIOS中断输出字符来判断A20是否真的打开。
	# 因为16位代码段只能进行16位寻址，所以你无法访问到第20位，也就不可能判断A20是否为1了。
	/**
	movl $0x1,%eax
	movl %eax,0x136f20 # loop forever if it isn't
	cmpl %eax,0x036f20
	je disperror
	dispsuccess:
	movw $success      ,%ax
	movw %ax        ,%bp                             # es:bp = 串地址
	movw $12         ,%cx                              # cs = 串长度
	movw $0x1301 ,%ax                              # ah=0x13：显示字符串 ,al=0x1：显示输出方式
	movw $0x000c ,%bx                              # bh=0 ：第0页,  bl=0xc ：高亮 黑底红字
	movb $0           ,%dl                               # 在0行0列显示
	int $0x10                                # 调用BIOS提供的int服务0x10的0x13功能：显示字符串  
	# ret
	disperror:
	*/

	# 4、加载gdtr，将内存中的gdt表结构读入gdtr寄存器
	lgdt gdt_48

	# 5、打开保护模式，将cr0的位0置为1,一般而言BIOS中断只在实模式下进行调用
	movl %cr0, %eax
	orl  $0x1, %eax
	movl %eax, %cr0
	# 6、进入到32位代码段。0x8代表段选择子(16位)——0000000000001000，其中最后2为代表特权级，

	# linux内核只使用了2个特权级(0和3)，00代表0特权级(内核级)，
	# 倒数第3位的代表是gdt(全局描述符表)还是idt(局部描述#符表)，
	# 0代表全局描述符表，前13位代表gdt的项数(第1项)，代码段。
	# 所以0x8代表特权级为0(内核级)的全局代码段,promode代表偏移地址。
	ljmp $0x8, $promode

# 7、32位代码段
promode:
.code32
# 注意, 此时不能再像实模式下的16位代码段一样将ds、es、ss设置成cs的值了，
# 因为此时是32位保护模式，将代码段和数据段分开了，尽管它们的基地址一样，
# 段限长一样，即指向同一段地址空间，但 #两个段的属性不同，
# 具体看IA32手册中对gdt表中的描述符属性。ds、es、ss均可看作数据段的内容，
# 如果要设置的话，按如下代码进行设置。
# 同样，此段程序中仍未用到这些段寄存器，
# 所以这段代码可#写可不写，0x10按照选择子的描述——000000000001000，
# 前13位代表gdt的项数(第2项),数据段。所以0x10代表特权级为0(内核级)的全局数据段。
	movw $0x10, %ax
	movw %ax,   %ds  # -> Data Segment
	movw %ax,   %es  # -> Extra Segment
	movw %ax,   %ss  # -> Stack Segment

	# 8、用回滚机制判断0x100000内存地址的数据和0x000000内存地址的数据是否相同，从而确定是否已经打开A20
	movl $0x1,%eax
	movl %eax,0x100200
	cmpl 0x000200,%eax

	# 9、若两个内存的数据不相同，则说明A20为1，即A20地址线已经打开了，跳
	# 转到display程序中在VGA中显示字符'Y'，若没打开则跳转到loop0死循环。
	jne display
	jmp loop0

# 10、此时处于保护模式，不能调用BIOS中断，只能通过VGA来显示字符从而判断A20是否真的打开。
display:
	# 11、0x18代表gdt的第3项，本程序中设置的是VGA段(显示器内存)
	movw $0x18,%ax
	movw %ax,%gs
	movl $((80*1+1)*2),%edi /*第11行，79列*/
	movb $0x0c,%ah          /*高四位表示黑底,低四位表示红字*/
	movb $'Y',%al           /*显示的字符*/
	movw %ax,%gs:(%edi)

loop0:                    /* 无限循环 */
	jmp loop0

/**
success:
.string "open A20 Success!"
error:
.string "open A20 Error!"
*/

# 在内存中做一块GDT表
.align 2
gdt:
.word 0,0,0,0

.word 0xFFFF  # 第1项 CS  基地址为0
.word 0x0000
.word 0x9A00
.word 0x00C0

.word 0xFFFF  # 第2项 DS  基地址为0
.word 0x0000
.word 0x9200
.word 0x00C0

.word 0xFFFF  # 第3项 VGA 基地址位0xb8000
.word 0x8000
.word 0x920b
.word 0x0000

# 将gdtr专用寄存器指向我们在内存中做的一块GDT表,GDTR寄存器格式:48位(高32位地址+低16位限长)，intel是小端方式
gdt_48:
# gdt表限长 sizeof(gdt)-1 低地址，放在gdtr的低字节
.word 0x1f
# gdt表基址  高地址，放在gdtr的高字节
.long gdt
.org  0x1fe, 0x00  /* 0x1fe=510，表示从ret后的位置开始，直到510处结束的代码/数据空间，填写0x00 */
.word 0xaa55       /* 合法的主引导扇区标识 */

