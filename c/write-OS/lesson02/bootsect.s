#################################################################
#                                                               #
#  Lesson 2: 加载软盘中的内容到内存，并执行相应代码				#
#  Goal: 了解 int 0x13 的使用方法，以及了解如何使用ljmp切换     #
#  CS 和IP														#
#                                                               #
#################################################################

	.code16			     # 指定语法为 十六位汇编
	.equ SYSSIZE, 0x3000 # System Size in Clicks

# rewrite with AT&T syntax by falcon <wuzhangjin@gmail.com> at 081012
# Modified by VOID001<zhangjianqiu13@gmail.com> at 2017 03 05
# loads pretty fast by getting whole sectors at a time whenever possible.

	#.global _start, begtext, begdata, begbss, endtext, enddata, endbss
	.global _start # 程序开始处
	.global begtext, begdata, begbss, endtext, enddata, endbss
	.text
	begtext:
	.data
	begdata:
	.bss
	begbss:
	.text

	.equ BOOTSEG, 0x07c0		# 当此扇区被BIOS识别为启动扇区装载到内存中时，装载到0x07c0段处
								# 此时我们处于实模式(REAL MODE)中，对内存的寻址方式为
								# (段地址 << 4 + 偏移量) 可以寻址的线性空间为 20 位
	.equ INITSEG, 0x9000
	.equ FLOPPYSEG, 0x1000		# floppy 要调用的函数在的段地址 0x1000 = 4096

	.equ ROOTDEV, 0x301			# first partition on first drive etc, 指定/dev/fda为系统镜像所在的设备
								# 0x300 /dev/hd0 系统中第一个硬盘
								# 0x301 /dev/hd1 系统中第一个硬盘的第一分区
								# 0x302 /dev/hd2 系统中第一个硬盘的第二分区

	ljmp $BOOTSEG, $_start		# 修改 cs 寄存器为BOOTSEG, 并跳转到_start处执行我们的代码

_start:
	mov $BOOTSEG, %ax
	mov %ax, %es			# 设置好 es 寄存器，为后续输出字符串准备
	mov	$0x03, %ah			# 在输出我们的信息前读取光标的位置, 会将光标当前所在行/列存储在dx里（dh为行, dl为列）
	xor	%bh, %bh
	int	$0x10				# BIOS 中断INT 0x10 显示字符和字符串

	mov	$18, %cx			# Set the output length
	mov	$0x0007, %bx		# page 0, color = 0x07 (from wikipedia https://en.wikipedia.org/wiki/INT_10H)
	mov $msg1, %bp
	mov	$0x1301, %ax		# write string, move cursor
	int	$0x10				# 使用这个中断0x10的时候，输出的内容是从 es:bp 中取得的，因而要设置好 es 和 bp

load_floppy:
	# 这里我们需要将软盘中的内容加载到内存中，并且跳转到相应地址执行代码
	mov $0x0000, %dx		# 选择磁盘号0，磁头号0进行读取
	mov $0x0002, %cx		# 从2号扇区，0轨道开始读(注意扇区是从1开始编号的)
	mov $FLOPPYSEG, %ax		# es:bx 指向装载目的地址
	mov %ax, %es            # es 附加段寄存器
	mov $0x0200, %bx
	mov $02, %ah			# ah = 02h, 读磁盘扇区
							# ah = 03h, 写磁盘扇区
	mov $4, %al				# 读取的扇区数
	int $0x13				# 调用BIOS中断读取, int 0x13中断向量将指定扇区的代码加载到内存的指定位置
	jnc floppy_load_ok		# 没有异常，加载成功
	jmp load_floppy			# 并一直重试，直到加载成功

floppy_load_ok:				# Here will jump to where the floppy program is
	mov $FLOPPYSEG, %ax
	# mov %ax, %cs			# This is awful!! Do not change CS alone!! It will result in GDB cannot debug the code
							# And, of course the code will not work
	mov %ax, %ds			# 数据段寄存器
	ljmp $0x1020, $0		# jump to where the floppy program exists

sectors:
	.word 0

msg1:
	.byte 0x0d, 0x0a			# 回车换行 /r/n
	.ascii "Hello World!"
	.byte 0x0d, 0x0a, 0x0d, 0x0a

	.= 0x1fe                    # 这里是对齐语法 等价于 .org 表示在该处补零，一直补到 地址为 510 的地方 (即第一扇区的最后两字节)
								# 然后在这里填充好0xaa55魔术值，BIOS会识别硬盘中第一扇区以0xaa55结尾的为启动扇区，于是BIOS会装载
								# 代码并且运行
boot_flag:
	.word 0xAA55
