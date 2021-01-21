.code16

# use to prove the floppy disk data is loaded correctly
# 此代码不需要进行修改，这段代码在bootsect.s编写正确之后会正确装载

.text

.equ FLOPPYSEG, 0x1020
.equ MSGLEN, 54

.global _start

_start:
	mov $FLOPPYSEG, %ax
	mov %ax, %es
	mov $0x03, %ah
	xor %bh, %bh
	int $0x10				# these two line read the cursor position
	mov $0x000a, %bx		# Set video parameter
	mov $0x1301, %ax
	mov $MSGLEN, %cx
	mov $msg, %bp
	int $0x10

loop_forever:
	jmp loop_forever

msg:
	.byte 0x0d, 0x0a
	.ascii "You've successfully load the floppy data into RAM"
	.byte 0x0d, 0x0a, 0x0d, 0x0a

