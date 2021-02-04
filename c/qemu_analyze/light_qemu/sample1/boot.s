start:
	mov $0x48, %al	# 'H'
	outb %al, $0xf1
	mov $0x65, %al	# 'e'
	outb %al, $0xf1
	mov $0x6C, %al	# 'l'
	outb %al, $0xf1
	mov $0x6C, %al	# 'l'
	outb %al, $0xf1
	mov $0x6F, %al	# 'o'
	outb %al, $0xf1
	mov $0x0A, %al	# '\n'
	outb %al, $0xf1

	hlt				# CPU休眠, 直到下一个硬件中断
