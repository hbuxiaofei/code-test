#!/bin/sh

# ref: https://github.com/cirosantilli/linux-kernel-module-cheat

set -ex

# Our modules does not the PCI device yet.
lspci -k
# => 00:04.0 Class 00ff: 1234:11e8 qemu_edu

# Interrupt counts before we generate our interrupts.
cat /proc/interrupts

# Setup.
insmod qemu_edu.ko
./mknode.sh qemu_edu

# Shows that this module owns the PCI device.
lspci -k
# => 00:04.0 Class 00ff: 1234:11e8 qemu_edu

# Identifiction: just returns some fixed magic bytes.
dd bs=4 status=none if=/dev/edu0 count=1 skip=0 | od -An -t x1
# => 010000ed

# Negator. Sanity check that the hardware is getting updated.
dd bs=4 status=none if=/dev/edu0 count=1 skip=1 | od -An -t x1
printf '\xF0\xF0\xF0\xF0' | dd bs=4 status=none of=/dev/edu0 count=1 seek=1
dd bs=4 status=none if=/dev/edu0 count=1 skip=1 | od -An -t x1
# => 0F0F0F0F

# Factorial calculator.
# Request interrupt when the computation is over.
printf '\x80\x00\x00\x00' | dd bs=4 status=none of=/dev/edu0 count=1 seek=8
# factorial(0x3) = 0x06000000
printf '\x03\x00\x00\x00' | dd bs=4 status=none of=/dev/edu0 count=1 seek=2
# => irq_handler .* (cat /proc/kmsg)
# Yes, we should use the interrupt to notify poll, but lazy.
sleep 1
dd bs=4 status=none if=/dev/edu0 count=1 skip=2 | od -An -t x1
dd bs=4 status=none if=/dev/edu0 count=1 skip=8 | od -An -t x1
# => 06000000 (3! = 3*2*1 = 6(0x06))

# Manual IRQ raising.
printf '\x04\x03\x02\x01' | dd bs=4 status=none of=/dev/edu0 count=1 seek=24
# => irq_handler .* (cat /proc/kmsg)
sleep 1
printf '\x08\x07\x06\x05' | dd bs=4 status=none of=/dev/edu0 count=1 seek=24
# => irq_handler .* (cat /proc/kmsg)
sleep 1

# Teardown.
rm /dev/edu0
rmmod qemu_edu

# Interrupt counts after we generate our interrupts.
# Compare with before.
cat /proc/interrupts
