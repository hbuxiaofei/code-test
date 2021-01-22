# This code is used to test whether you make things right
# switching to protected mode, do not modify it, it will work
# Just as is

.code32

.global _start, begtext, begbss, begdata

_start:
	xor %ecx, %ecx			# Clear the counter
loop:
	mov $red_str, %ebx
	add %cx, %bx
	movb (%ebx), %al
	movb $0x0c, %ah
	mov $0xb8A00, %ebx		# 显存地址0xb8000-0xbffff共32KB的空间
	shl %ecx				# 左移一位
	add %ecx, %ebx
	shr %ecx				# 右移一位
	movw %ax, (%ebx)
	inc %ecx
	cmp $62, %ecx
	jne loop
halt:
	jmp halt

red_str:
	.ascii "You've entered protected mode!                           "
