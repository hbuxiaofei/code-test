#############################################################
#															#
#		Lesson 4 设置IDT 对8259A进行编程					#
#															#
#############################################################

.code16

.text

.equ SETUPSEG, 0x9020
.equ INITSEG, 0x9000
.equ SYSSEG, 0x1000
.equ LEN, 55

.global _start, begtext, begdata, begbss, endtext, enddata, endbss

.text
	begtext:
.data
	begdata:
.bss
	begbss:
.text


show_text:
	mov $SETUPSEG, %ax
	mov %ax, %es
	mov $0x03, %ah
	xor %bh, %bh
	int $0x10					# these two line read the cursor position
	mov $0x000a, %bx			# Set video parameter
	mov $0x1301, %ax
	mov $LEN, %cx
	mov $msg, %bp
	int $0x10

# 下面的代码调用BIOS中断将硬件的一些状态保存在0x9000:0000开始的内存处
# （注意这里会覆盖bootsect，不过无所谓，因为我们不再需要它了)
	ljmp $SETUPSEG, $_start
_start:

# 保存光标位置
# Comment for routine 10 service 3
# AH = 03
# BH = video page
# on return:
# CH = cursor starting scan line (low order 5 bits)
# CL = cursor ending scan line (low order 5 bits)
# DH = row
# DL = column
	mov $INITSEG, %ax
	mov %ax, %ds
	mov $0x03, %ah
	xor %bh, %bh
	int $0x10
	mov %dx, %ds:0
# 取扩展内存大小的值
# Comment for routine 0x15 service 0x88
# AH = 88h
# on return:
# CF = 80h for PC, PCjr
# = 86h for XT and Model 30
# = other machines, set for error, clear for success
# AX = number of contiguous 1k blocks of memory starting
# at address 1024k (100000h)
	mov $0x88, %ah
	int $0x15
	mov %ax, %ds:2

# 取显卡显示模式
# Comment for routine 10 service 0xf
# AH = 0F
# on return:
# AH = number of screen columns
# AL = mode currently set (see VIDEO MODES)
# BH = current display page
	mov $0x0f, %ah
	int $0x10
	mov %bx, %ds:4
	mov %ax, %ds:6

# 检查显示方式(EGA/VGA)并取参数
# Comment for routine 10 service 0x12
# We use bl 0x10
# BL = 10  return video configuration information
# on return:
# BH = 0 if color mode in effect
# = 1 if mono mode in effect
# BL = 0 if 64k EGA memory
# = 1 if 128k EGA memory
# = 2 if 192k EGA memory
# = 3 if 256k EGA memory
# CH = feature bits
# CL = switch settings
	mov $0x12, %ah
	mov $0x10, %bl
	int $0x10
	mov %ax, %ds:8
	mov %bx, %ds:10
	mov %cx, %ds:12

# 复制硬盘参数表信息
# 比较奇怪的是硬盘参数表存在中断向量里
# 第0个硬盘参数表的首地址在0x41中断向量处，
# 第1个硬盘参数的首地址表在0x46中断向量处，紧跟着第一个参数表, 每个参数表长度为0x10 Byte

# 第0块硬盘参数表
	mov $0x0000, %ax
	mov %ax, %ds
	lds %ds:4*0x41, %si
	mov $INITSEG, %ax
	mov %ax, %es
	mov $0x0080, %di
	mov $0x10, %cx
	rep movsb           # 0x10字节从ds:si 搬到es:di
# 第1块硬盘参数表
	mov $0x0000, %ax
	mov %ax, %ds
	lds %ds:4*0x46, %si
	mov $INITSEG, %ax
	mov %ax, %es
	mov $0x0090, %di
	mov $0x10, %cx
	rep movsb			# 0x10字节从ds:si 搬到es:di

# 检查第1块硬盘是否存在，如果不存在的话就清空相应的参数表(
# Comment for routine 0x13 service 0x15
# AH = 15h
# DL = drive number (0=A:, 1=2nd floppy, 80h=drive 0, 81h=drive 1)
# on return:
# AH = 00 drive not present
# = 01 diskette, no change detection present
# = 02 diskette, change detection present
# = 03 fixed disk present
# CX:DX = number of fixed disk sectors; if 3 is returned in AH
# CF = 0 if successful
# = 1 if error
	mov $0x1500, %ax
	mov $0x81, %dl
	int $0x13
	jc no_disk1
	cmp $3, %ah
	je is_disk1
no_disk1:				# 没有第1块硬盘，那么就对第1个硬盘表清零，使用stosb
	mov $INITSEG, %ax
	mov %ax, %es
	mov $0x0090, %di
	mov $0x10, %cx
	mov $0x00, %ax
	rep stosb           # 从DI所指的内存开始，将连续的CX个字节写成 AL 的内容

is_disk1:
	# 下面该切换到保护模式了～（终于要离开这个不安全，文档匮乏，调试费力的16bit实模式了）
	# 进行切换保护模式的准备操作
	cli					# 关中断

	# 我们先将system从0x1000:0000移动到0x0000:0000处
	mov $0x0000, %ax
	cld					# Direction = 0 move forward
do_move:
	mov %ax, %es
	add $0x1000, %ax
	cmp $0x9000, %ax	# Does we finish the move
	jz end_move			# 为 0 则跳转
	mov %ax, %ds
	sub %di, %di
	sub %si, %si
	mov $0x8000, %cx	# Move 0x8000 word = 0x10000 Byte (64KB)
	rep movsw
	jmp do_move

# 下面我们加载 GDT, IDT 等
# 在这里补充加载GDT的代码，并在下面补充GDT表的结构

end_move:
	mov $SETUPSEG, %ax
	mov %ax, %ds
	lidt idt_48				# 加载中断描述符
	lgdt gdt_48				# 加载全局描述符
							# lgdt指令是从内存中读取48位的内存数据，存入GDTR寄存器
							# lgdt总共需要6个字节，其中两个字节为GDT表的长度，另外4个字节表明GDT表的基址


# 开启A20地址线，使得可以访问64KB以上的内存
	inb $0x92, %al			# 从I/O端口读取一个字节
	orb $0b00000010, %al
	outb %al, $0x92			# 写一个字节到I/O端口

# 这里我们会对8259A进行编程, 不建议大家搞OwO(所以注释都是英文的辣)
	mov $0x11, %al					# Init ICW1, 0x11 is init command

	out %al, $0x20					# 0x20 is 8259A-1 Port
	.word 0x00eb, 0x00eb			# Time Delay jmp $+2, jmp $+2
	out %al, $0xA0					# And init 8259A-2
	.word 0x00eb, 0x00eb
	mov $0x20, %al					# Send Hardware start intterupt number(0x20)
	out %al, $0x21					# From 0x20 - 0x27
	.word 0x00eb, 0x00eb
	mov $0x28, %al
	out %al, $0xA1					# From 0x28 - 0x2F
	.word 0x00eb, 0x00eb
	mov $0x04, %al					# 8259A-1 Set to Master
	out %al, $0x21
	.word 0x00eb, 0x00eb
	mov $0x02, %al					# 8259A-2 Set to Slave
	out %al, $0xA1
	.word 0x00eb, 0x00eb
	mov $0x01, %al					# 8086 Mode
	out %al, $0x21
	.word 0x00eb, 0x00eb
	out %al, $0xA1
	.word 0x00eb, 0x00eb
	mov $0xFF, %al
	out %al, $0x21					# Mask all the interrupts now
	.word 0x00eb, 0x00eb
	out %al, $0xA1

# 开启保护模式！
	mov %cr0, %eax		# 控制寄存器 (cr0-cr3)
	bts $0, %eax		# Turn on Protect Enable (PE) bit
						# 寄存器 eax 的第0位放入 cf, 并置位
	mov %eax, %cr0

# Jump to protected mode
	.equ sel_cs0, 0x0008
	mov $0x10, %ax
	mov %ax, %ds
	mov %ax, %es
	mov %ax, %fs
	mov %ax, %gs
	ljmp $sel_cs0, $0	# 1000b:
						# 0-1位 请求特权, 2位 全局描述表还是局部描述表, 3-15位 gdt索引
						# 0x0008>>3 = 1, 因此这里索引为gdt[1], base address 是0,
						# 因此gdt[1].base + 0 = 0

# GDTR信息
gdt_48:					# This is the GDT Descriptor
	.word 0x800			# limit=2048(0x800)
	.word 512+gdt, 0x9	# 512 = 0x200, This give the GDT Base address 0x90200
						# 0x0009<<16 + 0x0200+gdt

idt_48:
	.word 0
	.word 0, 0

gdt:
	# gdt[0]
	.word	0,0,0,0		# dummy

	# gdt[1]
    .word   0x07FF      # 8Mb - limit=2047 (2048*4096=8Mb)
    .word   0x0000      # base address=0
    .word   0x9A00      # code read/exec
    .word   0x00C0      # granularity=4096, 386

	# gdt[2]
    .word   0x07FF      # 8Mb - limit=2047 (2048*4096=8Mb)
    .word   0x0000      # base address=0
    .word   0x9200      # data read/write
    .word   0x00C0      # granularity=4096, 386

msg:
	.byte 0x0d, 0x0a	# 回车换行 /r/n
	.ascii "You've successfully load the floppy data into RAM"
	.byte 0x0d, 0x0a, 0x0d, 0x0a
