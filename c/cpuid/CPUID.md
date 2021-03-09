{{short description|X86 instruction}}
{{update|date=July 2014}}
In the [[x86]] architecture, the '''CPUID''' instruction (identified by a <code>CPUID</code> [[opcode]]) is a [[processor supplementary instruction]] (its name derived from [[Central processing unit|CPU]] IDentification) allowing software to discover details of the processor. It was introduced by [[Intel]] in 1993 with the launch of the [[Pentium]] and [[SL-enhanced 486]] processors.<ref>{{cite web|url=http://www.intel.com/design/processor/manuals/253668.pdf |title=Intel 64 and IA-32 Architectures Software Developer's Manual |publisher=Intel.com |access-date=2013-04-11}}</ref>

A program can use the <code>CPUID</code> to determine processor type and whether features such as [[MMX (instruction set)|MMX]]/[[Streaming SIMD Extensions|SSE]] are implemented. 

== History ==
Prior to the general availability of the <code>CPUID</code> instruction, programmers would write esoteric [[machine code]] which exploited minor differences in CPU behavior in order to determine the processor make and model.<ref>{{cite web|url=http://www.rcollins.org/ddj/Sep96/Sep96.html |title=Detecting Intel Processors - Knowing the generation of a system CPU |publisher=Rcollins.org |access-date=2013-04-11}}</ref><ref>{{cite web |url=http://lxr.linux.no/source/arch/i386/kernel/head.S?v=1.2.13#L92 |archive-url=https://archive.today/20120713012856/http://lxr.linux.no/source/arch/i386/kernel/head.S?v=1.2.13%23L92#L92 |url-status=dead|title=LXR linux-old/arch/i386/kernel/head.S |publisher=Lxr.linux.no |access-date=2013-04-11 |archive-date = 2012-07-13}}</ref> With the introduction of the 80386 processor, EDX on reset indicated the revision but this was only readable after reset and there was no standard way for applications to read the value.

Outside the x86 family, developers are mostly still required to use esoteric processes (involving instruction timing or CPU fault triggers) to determine the variations in CPU design that are present.

In the Motorola 680x0 family — that never had a CPUID instruction of any kind — certain specific instructions required elevated privileges. These could be used to tell various CPU family members apart. In the [[Motorola 68010]] the instruction ''MOVE from SR'' became privileged. This notable instruction (and state machine) change allowed the 68010 to meet the [[Popek and Goldberg virtualization requirements]]. Because the 68000 offered an unprivileged ''MOVE from SR'' the 2 different CPUs could be told apart by a CPU error condition being triggered.

While the <code>CPUID</code> instruction is specific to the x86 architecture, other architectures (like ARM) often provide on-chip registers which can be read in prescribed ways to obtain the same sorts of information provided by the x86 CPUID instruction.

== Calling CPUID ==
The <code>CPUID</code> opcode is <tt>0Fh, A2h</tt> (as two bytes, or <tt>A20Fh</tt> as a single <tt>word</tt>).

In [[assembly language]], the <code>CPUID</code> instruction takes no parameters as <code>CPUID</code> implicitly uses the EAX register to determine the main category of information returned. In Intel's more recent terminology, this is called the CPUID leaf. <code>CPUID</code> should be called with <code>EAX = 0</code> first, as this will store in the EAX register the highest EAX calling parameter (leaf) that the CPU implements.

To obtain extended function information <code>CPUID</code> should be called with the most significant bit of EAX set. To determine the highest extended function calling parameter, call <code>CPUID</code> with <code>EAX = 80000000h</code>.

CPUID leaves greater than 3 but less than 80000000 are accessible only when the [[model-specific register]]s have IA32_MISC_ENABLE.BOOT_NT4 [bit 22] = 0 (which is so by default). As the name suggests, [[Windows NT 4.0]] until SP6 did not boot properly unless this bit was set,<ref>{{cite web|url=https://software.intel.com/en-us/forums/topic/306523?language=en#comment-1590394 |title=CPUID, EAX=4 - Strange results (Solved) |publisher=Software.intel.com |access-date=2014-07-10}}</ref>{{dead link|date=October 2020}} but later versions of Windows do not need it, so basic leaves greater than 4 can be assumed visible on current Windows systems. {{As of|July 2014}}, basic valid leaves go up to 14h, but the information returned by some leaves are not disclosed in publicly available documentation, i.e. they are "reserved".

Some of the more recently added leaves also have sub-leaves, which are selected via the ECX register before calling CPUID.

=== [[X86#32-bit|EAX]]=0: Highest Function Parameter and Manufacturer ID===

This returns the CPU's manufacturer ID string{{snd}} a twelve-character [[ASCII]] string stored in EBX, EDX, ECX (in that order). The highest basic calling parameter (largest value that EAX can be set to before calling <code>CPUID</code>) is returned in EAX.

Here is a list of processors and the highest function implemented.

{| class="wikitable"
|+ Highest Function Parameter
! Processors || Basic || Extended
|-
|| Earlier [[Intel 80486|Intel 486]] || colspan=2 | ''CPUID Not Implemented''
|-
|| Later Intel 486 and [[Pentium]] || 0x01 || ''Not Implemented''
|-
|| [[Pentium Pro]], [[Pentium II]] and [[Celeron]] || 0x02 || ''Not Implemented''
|-
|| [[Pentium III]] || 0x03 || ''Not Implemented''
|-
|| [[Pentium 4]] || 0x02 || 0x8000 0004
|-
|| [[Xeon]] || 0x02 || 0x8000 0004
|-
|| [[Pentium M]] || 0x02 || 0x8000 0004
|-
|| Pentium 4 with [[Hyper-Threading]] || 0x05 || 0x8000 0008
|-
|| [[Pentium D]] (8xx) || 0x05 || 0x8000 0008
|-
|| Pentium D (9xx) || 0x06 || 0x8000 0008
|-
|| [[Intel_Core#Core_Duo|Core Duo]] || 0x0A || 0x8000 0008
|-
|| [[Intel_Core#Core 2 Duo|Core 2 Duo]] || 0x0A || 0x8000 0008
|-
|| Xeon [[List of Intel Nehalem-based Xeon microprocessors#Xeon 3000-series (uniprocessor)|3000]], 5100, 5200, 5300, 5400 ([[List of Intel Nehalem-based Xeon microprocessors#Xeon 5000-series (dual-processor)|5000 series]]) || 0x0A || 0x8000 0008
|-
|| Core 2 Duo [[Wolfdale (microprocessor)#Wolfdale|8000 series]] || 0x0D || 0x8000 0008
|-
|| Xeon 5200, 5400 series || 0x0A || 0x8000 0008
|-
|| [[Intel Atom|Atom]] || 0x0A || 0x8000 0008
|-
|| [[Nehalem (microarchitecture)|Nehalem]]-based processors || 0x0B || 0x8000 0008
|-
|[[Ivy_Bridge_(microarchitecture)|Ivy Bridge]]-based processors
|0x0D
|0x8000 0008
|-
|[[Skylake (microarchitecture)|Skylake]]-based processors (proc base & max freq; Bus ref. freq)
|0x16
|0x8000 0008
|-
|[[System on a chip|System-On-Chip]] Vendor Attribute Enumeration Main Leaf
|0x17
|0x8000 0008
|}

The following are known processor manufacturer ID strings:
* <tt>"AMDisbetter!"</tt>{{snd}} early engineering samples of [[AMD K5]] processor
* <tt>"AuthenticAMD"</tt>{{snd}} [[Advanced Micro Devices|AMD]]
* <tt>"CentaurHauls"</tt>{{snd}} [[Integrated_Device_Technology|IDT]] WinChip/[[Centaur Technology|Centaur]] (Including some VIA CPU)
* <tt>"CyrixInstead"</tt>{{snd}} [[Cyrix]]/early [[STMicroelectronics]] and [[IBM]]
* <tt>"GenuineIntel"</tt>{{snd}} [[Intel Corporation|Intel]]
* <tt>"TransmetaCPU"</tt>{{snd}} [[Transmeta]]
* <tt>"GenuineTMx86"</tt>{{snd}} [[Transmeta]]
* <tt>"Geode by NSC"</tt>{{snd}} [[National Semiconductor]]
* <tt>"NexGenDriven"</tt>{{snd}} [[NexGen]]
* <tt>"RiseRiseRise"</tt>{{snd}} [[Rise Technology|Rise]]
* <tt>"SiS SiS SiS "</tt>{{snd}} [[Silicon Integrated Systems|SiS]]
* <tt>"UMC UMC UMC "</tt>{{snd}} [[United Microelectronics Corporation|UMC]]
* <tt>"VIA VIA VIA "</tt>{{snd}} [[VIA Technologies|VIA]]
* <tt>"Vortex86 SoC"</tt>{{snd}} DM&P [[Vortex86|Vortex]]
* <tt>"&nbsp; Shanghai &nbsp;"</tt>{{snd}} [[Zhaoxin]]
* <tt>"HygonGenuine"</tt>{{snd}} [[AMD–Chinese joint venture|Hygon]]
* <tt>"E2K MACHINE"</tt>{{snd}} [[Elbrus_(computer)|MCST Elbrus]]

The following are ID strings used by open source [[Soft microprocessor|soft CPU cores]]:
* <tt>"GenuineAO486"</tt>{{snd}} ao486 CPU<ref>{{cite web |title=ao486 CPUID instruction |url=https://github.com/MiSTer-devel/ao486_MiSTer/blob/master/rtl/ao486/commands/CMD_CPUID.txt}}</ref>
* <tt>"GenuineIntel"</tt>{{snd}} v586 core<ref>{{cite web |title=v586: 586 compatible soft core for FPGA |url=https://github.com/valptek/v586}}</ref> (this is identical to the Intel ID string)

The following are known ID strings from virtual machines:
* <tt>"bhyve bhyve "</tt>{{snd}} [[bhyve]]
* <tt>" KVMKVMKVM  "</tt>{{snd}} [[Kernel-based Virtual Machine|KVM]]
* <tt>"TCGTCGTCGTCG"</tt>{{snd}} [[QEMU]]
* <tt>"Microsoft Hv"</tt>{{snd}} [[Hyper-V|Microsoft Hyper-V]] or [[Windows Virtual PC]]
* <tt>" lrpepyh  vr"</tt>{{snd}} [[Parallels (company)|Parallels]] (it possibly should be "prl hyperv  ", but it is encoded as " lrpepyh  vr" due to an [[endianness]] mismatch)
* <tt>"VMwareVMware"</tt>{{snd}} [[VMware]]
* <tt>"XenVMMXenVMM"</tt>{{snd}} [[Xen|Xen HVM]]
* <tt>"ACRNACRNACRN"</tt>{{snd}} [https://projectacrn.org/ Project ACRN]
* <tt>" QNXQVMBSQG "</tt>{{snd}} [[QNX]] Hypervisor
* <tt>"VirtualApple"</tt>{{snd}} [[Rosetta (software)|Apple Rosetta]] 
* <tt>"GenuineIntel"</tt>{{snd}} [[Rosetta (software)|Apple Rosetta 2]] <ref>https://cpufun.substack.com/p/fun-with-timers-and-cpuid</ref>

For instance, on a GenuineIntel processor values returned in EBX is 0x756e6547, EDX is 0x49656e69 and ECX is 0x6c65746e. The following code is written in [[GNU Assembler]] for the [[x86-64]] architecture and displays the vendor ID string as well as the highest calling parameter that the CPU implements.

<syntaxhighlight lang="asm">
	.data

s0:	.asciz	"CPUID: %x\n"
s1:	.asciz	"Largest basic function number implemented: %i\n"
s2:	.asciz	"Vendor ID: %.12s\n"

	.text

	.align	32
	.globl	main

main:
	pushq	%rbp
	movq	%rsp,%rbp
	subq	$16,%rsp

	movl	$1,%eax
	cpuid

	movq	$s0,%rdi
	movl	%eax,%esi
	xorl	%eax,%eax
	call	printf

	pushq	%rbx  // -fPIC

	xorl	%eax,%eax
	cpuid

	movl	%ebx,0(%rsp)
	movl	%edx,4(%rsp)
	movl	%ecx,8(%rsp)

	popq	%rbx  // -fPIC

	movq	$s1,%rdi
	movl	%eax,%esi
	xorl	%eax,%eax
	call	printf

	movq	$s2,%rdi
	movq	%rsp,%rsi
	xorl	%eax,%eax
	call	printf

	movq	%rbp,%rsp
	popq	%rbp
//	ret
	movl	$1,%eax
	int	$0x80
</syntaxhighlight>

=== EAX=1: Processor Info and Feature Bits ===

This returns the CPU's [[Stepping (version numbers)|stepping]], model, and family information in register EAX (also called the ''signature'' of a CPU), feature flags in registers EDX and ECX, and additional feature info in register EBX.<ref>{{cite book |author=<!--Staff writer(s); no by-line.--> |chapter-url=https://software.intel.com/en-us/download/intel-64-and-ia-32-architectures-sdm-combined-volumes-1-2a-2b-2c-2d-3a-3b-3c-3d-and-4 |chapter-format=PDF |title=Intel® 64 and IA-32 Architectures Software Developer's Manual |chapter=Chapter 3 Instruction Set Reference, A-L |publisher=Intel Corporation  |date=2018-12-20 |access-date=2018-12-20}}</ref> 

{| class="wikitable" style="margin-left: auto; margin-right: auto; border: none;"
|+ Processor Version Information
|-
! colspan="32" | EAX
|-
! style="width: 75px" | 31
! style="width: 75px" | 30
! style="width: 75px" | 29
! style="width: 75px" | 28
! style="width: 75px" | 27
! style="width: 75px" | 26
! style="width: 75px" | 25
! style="width: 75px" | 24
! style="width: 75px" | 23
! style="width: 75px" | 22
! style="width: 75px" | 21
! style="width: 75px" | 20
! style="width: 75px" | 19
! style="width: 75px" | 18
! style="width: 75px" | 17
! style="width: 75px" | 16
! style="width: 75px" | 15
! style="width: 75px" | 14
! style="width: 75px" | 13
! style="width: 75px" | 12
! style="width: 75px" | 11
! style="width: 75px" | 10
! style="width: 75px" | 9
! style="width: 75px" | 8
! style="width: 75px" | 7
! style="width: 75px" | 6
! style="width: 75px" | 5
! style="width: 75px" | 4
! style="width: 75px" | 3
! style="width: 75px" | 2
! style="width: 75px" | 1
! style="width: 75px" | 0
|- style="text-align: center"
| colspan="4" style="background: lightgrey" | Reserved
| colspan="8" | Extended Family ID
| colspan="4" | Extended Model ID
| colspan="2" style="background: lightgrey" | Reserved
| colspan="2" | Processor Type
| colspan="4" | Family ID
| colspan="4" | Model
| colspan="4" | Stepping ID
|}

* Stepping ID is a product revision number assigned due to fixed [[errata]] or other changes.

* The actual processor model is derived from the Model, Extended Model ID and Family ID fields. If the Family ID field is either 6 or 15, the model is equal to the sum of the Extended Model ID field shifted left by 4 bits and the Model field. Otherwise, the model is equal to the value of the Model field.

* The actual processor family is derived from the Family ID and Extended Family ID fields. If the Family ID field is equal to 15, the family is equal to the sum of the Extended Family ID and the Family ID fields. Otherwise, the family is equal to value of the Family ID field.

* The meaning of the Processor Type field is given by the table below.

{| class="wikitable"
|+ Processor Type
|-
! Type
! Encoding in [[Binary number|Binary]]
|-
| Original [[Original equipment manufacturer|OEM]] Processor
| style="text-align: center" | 00
|-
| [[Pentium OverDrive|Intel Overdrive Processor]]
| style="text-align: center" | 01
|-
| Dual processor (not applicable to Intel486 processors)
| style="text-align: center" | 10
|-
| Reserved value
| style="text-align: center" | 11
|}

{| class="wikitable"
|+ Additional Information
!Bits
!EBX
!Valid
|-
|7:0
|Brand Index
|
|-
|15:8
|CLFLUSH line size (Value . 8 = cache line size in bytes) 
|if CLFLUSH feature flag is set.

CPUID.01.EDX.CLFSH [bit 19]= 1
|-
|23:16
|Maximum number of addressable IDs for logical processors in this physical package; 

The nearest power-of-2 integer that is not smaller than this value is the number of unique initial APIC IDs reserved for addressing different logical processors in a physical package.

Former use: Number of logical processors per physical processor; two for the Pentium 4 processor with Hyper-Threading Technology.<ref>http://bochs.sourceforge.net/techspec/24161821.pdf</ref>
|if [[Hyper-threading]] feature flag is set.

CPUID.01.EDX.HTT [bit 28]= 1
|-
|31:24
|Local APIC ID: The initial APIC-ID is used to identify the executing logical processor. 

It can also be identified via the cpuid 0BH leaf ( CPUID.0Bh.EDX[x2APIC-ID] ).
|Pentium 4 and subsequent processors.
|}
The processor info and feature flags are manufacturer specific but usually the Intel values are used by other manufacturers for the sake of compatibility.

{| class="wikitable"
|+ Feature Information
!rowspan=2| Bit ||colspan=2| EDX ||colspan=2 | ECX
|-
! Short || Feature || Short || Feature
|-
! 0
| fpu || Onboard [[x87]] FPU || sse3|| [[Prescott New Instructions]]-SSE3 (PNI)
|-
! 1
| vme || [[Virtual 8086 Mode Extensions|Virtual 8086 mode extensions]] (such as VIF, VIP, PIV) || pclmulqdq || [[CLMUL instruction set|PCLMULQDQ]]
|-
! 2
| de || Debugging extensions ([[Control register#CR4|CR4]] bit 3) || dtes64 || 64-bit debug store (edx bit 21)
|-
! 3
| pse || [[Page Size Extension]] || monitor || MONITOR and MWAIT instructions ([[SSE3]])
|-
! 4
| tsc || [[Time Stamp Counter]] || ds-cpl || CPL qualified debug store
|-
! 5
| msr || [[Model-specific register]]s || vmx || [[x86 virtualization|Virtual Machine eXtensions]]
|-
! 6
| pae || [[Physical Address Extension]] || smx || Safer Mode Extensions ([[LaGrande]])
|-
! 7
| mce || [[Machine Check Exception]] || est || Enhanced [[SpeedStep]]
|-
! 8
| cx8 || CMPXCHG8 ([[compare-and-swap]]) instruction || tm2 || [[Tm2|Thermal Monitor 2]]
|-
! 9
| apic || Onboard [[Advanced Programmable Interrupt Controller]] || ssse3 || [[SSSE3|Supplemental SSE3]] instructions
|-
! 10
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || cnxt-id || L1 Context ID
|-
! 11
| sep || SYSENTER and SYSEXIT instructions || sdbg || Silicon Debug interface
|-
! 12
| mtrr || [[Memory Type Range Registers]] || fma || [[FMA instruction set|Fused multiply-add]] (FMA3)
|-
! 13
| pge || [[Page table|Page]] Global Enable bit in [[Control register#CR4|CR4]] || cx16 || CMPXCHG16B instruction
|-
! 14
| mca || [[Machine check architecture]] || xtpr || Can disable sending task priority messages
|-
! 15
| cmov || Conditional move and [[FCMOV]] instructions || pdcm || Perfmon & debug capability
|-
! 16
| pat || [[Page Attribute Table]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 17
| pse-36 || [[PSE-36|36-bit page size extension]] || pcid || [[Process context identifiers]] ([[Control register#CR4|CR4]] bit 17)
|-
! 18
| psn || [[Processor Serial Number#Controversy about privacy issues|Processor Serial Number]] || dca || Direct cache access for DMA writes<ref>{{Cite journal | last1 = Huggahalli | first1 = Ram| last2 = Iyer | first2 = Ravi| last3 = Tetrick | first3 = Scott| doi = 10.1145/1080695.1069976 | title = Direct Cache Access for High Bandwidth Network I/O | journal = [[ACM SIGARCH Computer Architecture News]] | volume = 33 | issue = 2 | pages = 50–59| year = 2005 | id = [[CiteSeerX]]:{{URL|1=citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.957|2=10.1.1.91.957}}}}</ref><ref>{{Citation |title=What Every Programmer Should Know About Memory |year=2007 |first=Ulrich |last=Drepper |id = [[CiteSeerX]]:{{url|1=citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.957|2=10.1.1.91.957}} }}</ref>
|-
! 19
| clfsh || CLFLUSH instruction ([[SSE2]]) || sse4.1 || [[SSE4.1]] instructions
|-
! 20
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || sse4.2 || [[SSE4.2]] instructions
|-
! 21
| ds || Debug store: save trace of executed jumps || x2apic || [[x2APIC]]
|-
! 22
| acpi || Onboard thermal control MSRs for [[Advanced Configuration and Power Interface|ACPI]] || movbe || MOVBE instruction ([[big-endian]])
|-
! 23
| mmx || [[MMX (instruction set)|MMX]] instructions || popcnt || [[Popcnt|POPCNT]] instruction
|-
! 24
| fxsr || FXSAVE, FXRESTOR instructions, [[Control register#CR4|CR4]] bit 9 || tsc-deadline || APIC implements one-shot operation using a TSC deadline value
|-
! 25
| sse || [[Streaming SIMD Extensions|SSE]] instructions (a.k.a. Katmai New Instructions) || aes || [[AES instruction set]]
|-
! 26
| sse2 || [[SSE2]] instructions || xsave || XSAVE, XRESTOR, XSETBV, XGETBV
|-
! 27
| ss || CPU cache implements self-[[Cache snooping|snoop]] || osxsave || XSAVE enabled by OS
|-
! 28
| htt || [[Hyper-threading]] || avx || [[Advanced Vector Extensions]]
|-
! 29
| tm || Thermal monitor automatically limits temperature || f16c || [[F16C]] ([[half-precision]]) FP feature
|-
! 30
| ia64 || [[IA64]] processor emulating x86 || rdrnd || [[RDRAND]] (on-chip random number generator) feature
|-
! 31
| pbe || Pending Break Enable (PBE# pin) wakeup capability || hypervisor || [[Hypervisor]] present (always zero on physical CPUs)<ref name="VMware KB 1009458">{{cite web |url=https://kb.vmware.com/s/article/1009458 |title=Mechanisms to determine if software is running in a VMware virtual machine |work=VMware Knowledge Base |publisher=[[VMWare]] |date=2015-05-01 |quote=Intel and AMD CPUs have reserved bit 31 of ECX of CPUID leaf 0x1 as the hypervisor present bit. This bit allows hypervisors to indicate their presence to the guest operating system. Hypervisors set this bit and physical CPUs (all existing and future CPUs) set this bit to zero. Guest operating systems can test bit 31 to detect if they are running inside a virtual machine. }}</ref><ref>{{cite web |url=https://lore.kernel.org/lkml/1222881242.9381.17.camel@alok-dev1/ |title=Hypervisor CPUID Interface Proposal |last=Kataria |first=Alok |last2=Hecht |first2=Dan |publisher=[[LKML]] Archive on lore.kernel.org |date=2008-10-01 |url-status=live |archive-url=https://web.archive.org/web/20190315105121/https://lore.kernel.org/lkml/1222881242.9381.17.camel@alok-dev1/ |archive-date=2019-03-15 |quote=Bit 31 of ECX of CPUID leaf 0x1. This bit has been reserved by Intel & AMD for use by hypervisors, and indicates the presence of a hypervisor. Virtual CPU's (hypervisors) set this bit to 1 and physical CPU's (all existing and future cpu's) set this bit to zero. This bit can be probed by the guest software to detect whether they are running inside a virtual machine. }}</ref>
|}
Reserved fields should be masked before using them for processor identification purposes.

=== EAX=2: Cache and TLB Descriptor information ===
This returns a list of descriptors indicating cache and [[Translation Lookaside Buffer|TLB]] capabilities in EAX, EBX, ECX and EDX registers.

=== EAX=3: Processor Serial Number ===
{{see also|Pentium III#Controversy about privacy issues}}
This returns the processor's serial number. The processor serial number was introduced on Intel [[Pentium III]], but due to privacy concerns, this feature is no longer implemented on later models (the PSN feature bit is always cleared). [[Transmeta|Transmeta's]] Efficeon and Crusoe processors also provide this feature. AMD CPUs however, do not implement this feature in any CPU models.

For Intel Pentium III CPUs, the serial number is returned in the EDX:ECX registers. For Transmeta Efficeon CPUs, it is returned in the EBX:EAX registers. And for Transmeta Crusoe CPUs, it is returned in the EBX register only.

Note that the processor serial number feature must be enabled in the [[BIOS]] setting in order to function.

=== EAX=4 and EAX=Bh: Intel thread/core and cache topology ===
These two leaves are used for processor topology (thread, core, package) and cache hierarchy enumeration in Intel multi-core (and hyperthreaded) processors.<ref name="topo">{{cite web|url=https://software.intel.com/en-us/articles/intel-64-architecture-processor-topology-enumeration/|title=Intel® 64 Architecture Processor Topology Enumeration|author=Shih Kuo|date=Jan 27, 2012}}</ref> {{As of|2013}} AMD does not use these leaves but has alternate ways of doing the core enumeration.<ref>{{cite web |url=http://developer.amd.com/resources/documentation-articles/articles-whitepapers/processor-and-core-enumeration-using-cpuid/ |title=Processor and Core Enumeration Using CPUID &#124; AMD |publisher=Developer.amd.com |access-date=2014-07-10 |archive-url=https://web.archive.org/web/20140714221717/http://developer.amd.com/resources/documentation-articles/articles-whitepapers/processor-and-core-enumeration-using-cpuid/ |archive-date=2014-07-14 |url-status=dead }}</ref>

Unlike most other CPUID leaves, leaf Bh will return different values in EDX depending on which logical processor the CPUID instruction runs; the value returned in EDX is actually the [[x2APIC]] id of the logical processor. The x2APIC id space is not continuously mapped to logical processors, however; there can be gaps in the mapping, meaning that some intermediate x2APIC ids don't necessarily correspond to any logical processor. Additional information for mapping the x2APIC ids to cores is provided in the other registers. Although the leaf Bh has sub-leaves (selected by ECX as described further below), the value returned in EDX is only affected by the logical processor on which the instruction is running but not by the subleaf.

The processor(s) topology exposed by leaf Bh is a hierarchical one, but with the strange caveat that the order of (logical) levels in this hierarchy doesn't necessarily correspond the order in the physical hierarchy ([[Simultaneous multithreading|SMT]]/core/package). However, every logical level can be queried as an ECX subleaf (of the Bh leaf) for its correspondence to a "level type", which can be either SMT, core, or "invalid". The level id space starts at 0 and is continuous, meaning that if a level id is invalid, all higher level ids will also be invalid. The level type is returned in bits 15:08 of ECX, while the number of logical processors at the level queried is returned in EBX. Finally, the connection between these levels and x2APIC ids is returned in EAX[4:0] as the number of bits that the x2APIC id must be shifted in order to obtain a unique id at the next level.

As an example, a dual-core [[Westmere (microarchitecture)|Westmere]] processor capable of [[hyperthreading]] (thus having two cores and four threads in total) could have x2APIC ids 0, 1, 4 and 5 for its four logical processors. Leaf Bh (=EAX), subleaf 0 (=ECX) of CPUID could for instance return 100h in ECX, meaning that level 0 describes the SMT (hyperthreading) layer, and return 2 in EBX because there are two logical processors (SMT units) per physical core. The value returned in EAX for this 0-subleaf should be 1 in this case, because shifting the aforementioned x2APIC ids to the right by one bit gives a unique core number (at the next level of the level id hierarchy) and erases the SMT id bit inside each core. A simpler way to interpret this information is that the last bit (bit number 0) of the x2APIC id identifies the SMT/hyperthreading unit inside each core in our example. Advancing to subleaf 1 (by making another call to CPUID with EAX=Bh and ECX=1) could for instance return 201h in ECX, meaning that this is a core-type level, and 4 in EBX because there are 4 logical processors in the package; EAX returned could be any value greater than 3, because it so happens that bit number 2 is used to identify the core in the x2APIC id. Note that bit number 1 of the x2APIC id is not used in this example. However EAX returned at this level could well be 4 (and it happens to be so on a Clarkdale Core i3 5x0) because that also gives a unique id at the package level (=0 obviously) when shifting the x2APIC id by 4 bits. Finally, you may wonder what the EAX=4 leaf can tell us that we didn't find out already. In EAX[31:26] it returns the APIC mask bits ''reserved'' for a package; that would be 111b in our example because bits 0 to 2 are used for identifying logical processors inside this package, but bit 1 is also reserved although not used as part of the logical processor identification scheme. In other words, APIC ids 0 to 7 are reserved for the package, even though half of these values don't map to a logical processor.

The cache hierarchy of the processor is explored by looking at the sub-leaves of leaf 4. The APIC ids are also used in this hierarchy to convey information about how the different levels of cache are shared by the SMT units and cores. To continue our example, the L2 cache, which is shared by SMT units of the same core but not between physical cores on the Westmere is indicated by EAX[26:14] being set to 1, while the information that the L3 cache is shared by the whole package is indicated by setting those bits to (at least) 111b. The cache details, including cache type, size, and associativity are communicated via the other registers on leaf 4.

Beware that older versions of the Intel app note 485 contain some misleading information, particularly with respect to identifying and counting cores in a multi-core processor;<ref>{{cite web|url=https://software.intel.com/en-us/forums/topic/352709#comment-1719904 |title=Sandybridge processors report incorrect core number? |publisher=Software.intel.com |date=2012-12-29 |access-date=2014-07-10}}</ref> errors from misinterpreting this information have even been incorporated in the Microsoft sample code for using cpuid, even for the 2013 edition of Visual Studio,<ref>{{cite web|url=http://msdn.microsoft.com/en-us/library/hskdteyh.aspx |title=cpuid, __cpuidex |publisher=Msdn.microsoft.com |date=2014-06-20 |access-date=2014-07-10}}</ref> and also in the sandpile.org page for CPUID,<ref>{{cite web|url=http://www.sandpile.org/x86/cpuid.htm |title=x86 architecture - CPUID |publisher=sandpile.org |access-date=2014-07-10}}</ref> but the Intel code sample for identifying processor topology<ref name="topo"/> has the correct interpretation, and the current Intel Software Developer’s Manual has more clear language. The (open source) cross-platform production code<ref name="wildfire">{{cite web|url=http://trac.wildfiregames.com/browser/ps/trunk/source/lib/sysdep/arch/x86_x64/topology.cpp |title=topology.cpp in ps/trunk/source/lib/sysdep/arch/x86_x64 – Wildfire Games |publisher=Trac.wildfiregames.com |date=2011-12-27 |access-date=2014-07-10}}</ref> from [[Wildfire Games]] also implements the correct interpretation of the Intel documentation.

Topology detection examples involving older (pre-2010) Intel processors that lack x2APIC (thus don't implement the EAX=Bh leaf) are given in a 2010 Intel presentation.<ref>[https://software.intel.com/en-us/articles/hyper-threading-technology-and-multi-core-processor-detection Hyper-Threading Technology and Multi-Core Processor Detection]</ref> Beware that using that older detection method on 2010 and newer Intel processors may overestimate the number of cores and logical processors because the old detection method assumes there are no gaps in the APIC id space, and this assumption is violated by some newer processors (starting with the Core i3 5x0 series), but these newer processors also come with an x2APIC, so their topology can be correctly determined using the EAX=Bh leaf method.

=== EAX=6: Thermal and power management ===
{{expand section|date=April 2020}}

=== <span id="IBC"></span><span id="IBPB"></span><span id="IBRS"></span><span id="STIBP"></span><span id="SSBD"></span>EAX=7, ECX=0: Extended Features ===
This returns extended feature flags in EBX, ECX, and EDX. Returns the maximum ECX value for EAX=7 in EAX.

{| class="wikitable"
|+ EAX=7 CPUID feature bits
!rowspan=2| Bit ||colspan=2| EBX ||colspan=2 | ECX || colspan="2"| EDX
|-
! Short || Feature || Short || Feature || Short || Feature
|-
! 0
| fsgsbase || Access to base of %fs and %gs || prefetchwt1|| PREFETCHWT1 instruction || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 1
| || IA32_TSC_ADJUST || avx512_vbmi || [[AVX-512]] Vector Bit Manipulation Instructions || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 2
| sgx || [[Software Guard Extensions]] || umip || User-mode Instruction Prevention || avx512_4vnniw || [[AVX-512]] 4-register Neural Network Instructions 
|-
! 3
| bmi1 || [[Bit Manipulation Instruction Sets#BMI1|Bit Manipulation Instruction Set 1]] || pku || Memory Protection Keys for User-mode pages || avx512_4fmaps || [[AVX-512]] 4-register Multiply Accumulation Single precision
|-
! 4
| hle || [[Transactional Synchronization Extensions|TSX]] Hardware Lock Elision || ospke || PKU enabled by OS || fsrm || Fast Short REP MOVSB
|-
! 5
| avx2 || [[Advanced Vector Extensions 2]] || waitpkg || Timed pause and user-level monitor/wait  || rowspan=3 colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 6
| || FDP_EXCPTN_ONLY || avx512_vbmi2 || [[AVX-512]] Vector Bit Manipulation Instructions 2
|-
! 7
| smep || [[Supervisor Mode Execution Prevention]] || cet_ss || Control flow enforcement (CET) shadow stack 
|-
! 8
| bmi2 || [[Bit Manipulation Instruction Sets#BMI2|Bit Manipulation Instruction Set 2]] || gfni || Galois Field instructions || avx512_vp2intersect || [[AVX-512#New_instructions_in_AVX-512_VP2INTERSECT|AVX-512 VP2INTERSECT]] Doubleword and Quadword Instructions
|-
! 9
| erms || Enhanced REP MOVSB/STOSB || vaes || Vector [[AES instruction set]] (VEX-256/EVEX) || SRBDS_CTRL || Special Register Buffer Data Sampling Mitigations
|-
! 10
| invpcid || INVPCID instruction || vpclmulqdq || [[CLMUL instruction set]] (VEX-256/EVEX) || md_clear || VERW instruction clears CPU buffers 
|-
! 11
| rtm || [[Transactional Synchronization Extensions|TSX]] Restricted Transactional Memory || avx512_vnni || [[AVX-512]] Vector Neural Network Instructions || rowspan=2 colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' 
|-
! 12
| pqm || Platform Quality of Service Monitoring || avx512_bitalg || [[AVX-512]] BITALG instructions
|-
! 13
| || FPU CS and FPU DS deprecated || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || tsx_force_abort 
|-
! 14
| mpx || [[Intel MPX]] (Memory Protection Extensions) || avx512_vpopcntdq || AVX-512 Vector Population Count Double and Quad-word || SERIALIZE || Serialize instruction execution
|-
! 15
| pqe || Platform Quality of Service Enforcement || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''||  Hybrid || 
|-
! 16
| avx512_f || [[AVX-512]] Foundation || || [[Intel 5-level paging|5-level paging]] || TSXLDTRK || TSX suspend load address tracking
|-
! 17
| avx512_dq || [[AVX-512]] Doubleword and Quadword Instructions || rowspan="5"| mawau || rowspan="5"| The value of userspace MPX Address-Width Adjust used by the BNDLDX and BNDSTX [[Intel MPX]] instructions in 64-bit mode || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 18
| rdseed || [[RDSEED]] instruction || pconfig || Platform configuration (Memory Encryption Technologies Instructions) 
|-
! 19
| adx || [[Intel ADX]] (Multi-Precision Add-Carry Instruction Extensions) || lbr || Architectural Last Branch Records
|-
! 20
| smap || [[Supervisor Mode Access Prevention]] || cet_ibt || Control flow enforcement (CET) indirect branch tracking
|-
! 21
| avx512_ifma || [[AVX-512]] Integer Fused Multiply-Add Instructions || rowspan=1 colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 22
| pcommit || PCOMMIT instruction || rdpid || Read Processor ID and IA32_TSC_AUX || amx-bf16 || Tile computation on bfloat16 numbers
|-
! 23
| clflushopt || CLFLUSHOPT instruction || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 24
| clwb || CLWB instruction || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || amx-tile || Tile architecture
|-
! 25
| intel_pt || Intel Processor Trace || cldemote || Cache line demote || amx-int8 || Tile computation on 8-bit integers
|-
! 26
| avx512_pf || [[AVX-512]] Prefetch Instructions || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || IBRS_IBPB / spec_ctrl || Speculation Control, part of Indirect Branch Control (IBC):<br/>Indirect Branch Restricted Speculation (IBRS) and<br/>Indirect Branch Prediction Barrier (IBPB)<ref name="Intel_2018_SESEM">{{cite web |title=Speculative Execution Side Channel Mitigations |version=Revision 2.0 |date=May 2018 |orig-year=January 2018 |id=Document Number: 336996-002 |publisher=[[Intel]] |url=https://software.intel.com/sites/default/files/managed/c5/63/336996-Speculative-Execution-Side-Channel-Mitigations.pdf |access-date=2018-05-26}}</ref><ref>{{Cite web | url=https://lwn.net/Articles/743019/ | title=IBRS patch series &#91;LWN.net&#93;}}</ref>

|-
! 27
| avx512_er || [[AVX-512]] Exponential and Reciprocal Instructions || MOVDIRI|| || stibp&nbsp;|| Single Thread Indirect Branch Predictor, part of IBC<ref name="Intel_2018_SESEM"/>
|-
! 28
| avx512_cd || [[AVX-512]] Conflict Detection Instructions || MOVDIR64B || || L1D_FLUSH || IA32_FLUSH_CMD MSR
|-
! 29
| sha || [[Intel SHA extensions]] ||  ENQCMD ||  Enqueue Stores || IA32_ARCH_CAPABILITIES || Speculative Side Channel Mitigations<ref name="Intel_2018_SESEM"/>
|-
! 30
| avx512_bw || [[AVX-512]] Byte and Word Instructions || sgx_lc || SGX Launch Configuration ||  IA32_CORE_CAPABILITIES || Support for a MSR listing model-specific core capabilities
|-
! 31
| avx512_vl || [[AVX-512]] Vector Length Extensions || pks || Protection keys for supervisor-mode pages || ssbd || Speculative Store Bypass Disable,<ref name="Intel_2018_SESEM"/> as mitigation for [[Speculative Store Bypass]]  (IA32_SPEC_CTRL)
|}

=== <span id="IBC"></span><span id="IBPB"></span><span id="IBRS"></span><span id="STIBP"></span><span id="SSBD"></span>EAX=7, ECX=1: Extended Features ===
This returns extended feature flags in EAX.


{| class="wikitable"
|+ EAX=7 CPUID feature bits
!rowspan=2| Bit ||colspan=2| EAX 
|-
! Short || Feature
|-
! 0
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 1
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 2
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 3
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 4
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 5
| avx512_bf16 || [[AVX-512]] [[Bfloat16 floating-point format|BFLOAT16]] instructions 
|-
! 6
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 7
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 8
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 9
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 10
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 11
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 12
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 13
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 14
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 15
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 16
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 17
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 18
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 19
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 20
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 21
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 22
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 23
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 24
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 25
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 26
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 27
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 28
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 29
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 30
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 31
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|}

=== EAX=80000000h: Get Highest Extended Function Implemented ===
The highest calling parameter is returned in EAX.

=== EAX=80000001h: Extended Processor Info and Feature Bits ===
This returns extended feature flags in EDX and ECX.

'''AMD feature flags''' are as follows:<ref>{{Citation |url=http://developer.amd.com/wordpress/media/2012/10/254811.pdf |title=CPUID Specification |publisher=[[AMD]] |date=September 2010 |access-date=2013-04-02}}</ref><ref>[https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/arch/x86/include/asm/cpufeature.h?id=HEAD Linux kernel source code]</ref>
{| class="wikitable"
|+ EAX=80000001h CPUID feature bits
!rowspan=2| Bit ||colspan=2| EDX ||colspan=2 | ECX
|-
! Short || Feature || Short || Feature
|-
! 0
| fpu || Onboard [[x87]] FPU || lahf_lm || LAHF/SAHF in long mode
|-
! 1
| vme || Virtual mode extensions (VIF) || cmp_legacy || [[Hyperthreading]] not valid
|-
! 2
| de || Debugging extensions ([[Control register#CR4|CR4]] bit 3) || svm || [[Secure Virtual Machine]]
|-
! 3
| pse || [[Page Size Extension]] || extapic || Extended [[Advanced Programmable Interrupt Controller|APIC]] space
|-
! 4
| tsc || [[Time Stamp Counter]] || cr8_legacy || [[Control register#CR8|CR8]] in 32-bit mode
|-
! 5
| msr || [[Model-specific register]]s || abm || [[Advanced Bit Manipulation|Advanced bit manipulation]] ([[lzcnt]] and [[popcnt]])
|-
! 6
| pae || [[Physical Address Extension]] || sse4a || [[SSE4a]]
|-
! 7
| mce || [[Machine Check Exception]] || misalignsse || Misaligned [[Streaming SIMD Extensions|SSE]] mode
|-
! 8
| cx8 || CMPXCHG8 ([[compare-and-swap]]) instruction || 3dnowprefetch || PREFETCH and PREFETCHW instructions
|-
! 9
| apic || Onboard [[Advanced Programmable Interrupt Controller]] || osvw || OS Visible Workaround
|-
! 10
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || ibs || [[Hardware performance counter#Instruction based sampling|Instruction Based Sampling]]
|-
! 11
| syscall || SYSCALL and SYSRET instructions || xop || [[XOP instruction set]]
|-
! 12
| mtrr || [[Memory Type Range Registers]] || skinit || SKINIT/STGI instructions
|-
! 13
| pge || Page Global Enable bit in [[Control register#CR4|CR4]] || wdt || [[Watchdog timer]]
|-
! 14
| mca || [[Machine check architecture]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 15
| cmov || Conditional move and [[FCMOV]] instructions || lwp || Light Weight Profiling<ref>{{Citation |url=http://support.amd.com/us/Processor_TechDocs/43724.pdf |title=Lightweight Profiling Specification |publisher=[[AMD]] |date=August 2010 |access-date=2013-04-03}}</ref>
|-
! 16
| pat || [[Page Attribute Table]] || fma4 || [[FMA instruction set#FMA4 instruction set|4 operands fused multiply-add]]
|-
! 17
| pse36 || [[PSE-36|36-bit page size extension]] || tce || Translation Cache Extension
|-
! 18
| colspan="4" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 19
| mp || [[Multiprocessor]] Capable || nodeid_msr || NodeID MSR
|-
! 20
| nx || [[NX bit]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 21
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || tbm || [[Bit Manipulation Instruction Sets#TBM|Trailing Bit Manipulation]]
|-
! 22
| mmxext || [[3DNow!#3DNow extensions|Extended MMX]] || topoext || Topology Extensions
|-
! 23
| mmx || [[MMX (instruction set)|MMX]] instructions || perfctr_core || Core performance counter extensions
|-
! 24
| fxsr || FXSAVE, FXRSTOR instructions, [[Control register#CR4|CR4]] bit 9 || perfctr_nb || NB performance counter extensions
|-
! 25
| fxsr_opt || FXSAVE/FXRSTOR optimizations || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 26
| pdpe1gb || [[Gibibyte]] pages || dbx || Data breakpoint extensions
|-
! 27
| rdtscp || RDTSCP instruction || perftsc || Performance TSC
|-
! 28
| colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)'' || pcx_l2i || L2I perf counter extensions
|-
! 29
| lm || [[Long mode]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 30
| 3dnowext || [[3DNow!#3DNow extensions|Extended 3DNow!]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|-
! 31
| 3dnow || [[3DNow!]] || colspan="2" style="text-align:center; background:lightgrey;"| ''(reserved)''
|}

=== EAX=80000002h,80000003h,80000004h: Processor Brand String ===
These return the processor brand string in EAX, EBX, ECX and EDX. <code>CPUID</code> must be issued with each parameter in sequence to get the entire 48-byte null-terminated ASCII processor brand string.<ref name="intel1">{{cite web|url=http://download.intel.com/design/processor/applnots/24161832.pdf |title=Intel® Processor Identification and the CPUID Instruction |publisher=Download.intel.com |date=2012-03-06 |access-date=2013-04-11}}</ref> It is necessary to check whether the feature is present in the CPU by issuing <code>CPUID</code> with <code>EAX = 80000000h</code> first and checking if the returned value is greater or equal to 80000004h.
<syntaxhighlight lang="c">
#include <cpuid.h>  // GCC-provided
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t brand[12];

    if (!__get_cpuid_max(0x80000004, NULL)) {
        fprintf(stderr, "Feature not implemented.");
        return 2;
    }

    __get_cpuid(0x80000002, brand+0x0, brand+0x1, brand+0x2, brand+0x3);
    __get_cpuid(0x80000003, brand+0x4, brand+0x5, brand+0x6, brand+0x7);
    __get_cpuid(0x80000004, brand+0x8, brand+0x9, brand+0xa, brand+0xb);
    printf("Brand: %s\n", brand);
}
</syntaxhighlight>

=== EAX=80000005h: L1 Cache and TLB Identifiers ===
This function contains the processor’s L1 cache and TLB characteristics.

=== EAX=80000006h: Extended L2 Cache Features ===
Returns details of the L2 cache in ECX, including the line size in bytes (Bits 07 - 00), type of associativity (encoded by a 4 bits field; Bits 15 - 12) and the cache size in KiB (Bits 31 - 16).
<syntaxhighlight lang=C>
#include <cpuid.h>  // GCC-provided
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t eax, ebx, ecx, edx;
    if (__get_cpuid(0x80000006, &eax, &ebx, &ecx, &edx)) {
        printf("Line size: %d B, Assoc. Type: %d; Cache Size: %d KB.\n", ecx & 0xff, (ecx >> 12) & 0x07, (ecx >> 16) & 0xffff);
        return 0;
    } else {
        fputs(stderr, "CPU does not support 0x80000006");
        return 2;
    }
}
</syntaxhighlight>

=== EAX=80000007h: Advanced Power Management Information ===
This function provides advanced power management feature identifiers. EDX bit 8 indicates support for invariant TSC.

=== EAX=80000008h: Virtual and Physical address Sizes ===
Returns largest virtual and physical address sizes in EAX.
* Bits 07-00: #Physical Address Bits.
* Bits 15-8: #Linear Address Bits.
* Bits 31-16: Reserved = 0.
It could be used by the hypervisor in a virtual machine system to report physical/virtual address sizes possible with the virtual CPU.

EBX is used for features：
* Bit 0: CLZERO, Clear cache line with address in RAX.
* Bit 4: RDPRU, Read MPERF or APERF from ring 3.
* Bit 8: MCOMMIT, commit stores to memory. For memory fencing and retrieving ECC errors.
* Bit 9: WBNOINVD, Write Back and Do Not Invalidate Cache.

ECX provides core count.
* Bits 07-00: #Physical Cores minus one.
* Bits 11-8: Reserved = 0.
* Bits 15-12: #APIC ID Bits. 2 raised to this power would be the physical core count, as long as it's non-zero.
* Bits 17-16: Performance time-stamp counter size.
* Bits 31-18: Reserved = 0.

EDX provides information specific to RDPRU (the maximum register identifier allowed) in 31-16. The current number as of Zen 2 is 1 for MPERF and APERF.

=== EAX=8FFFFFFFh: AMD Easter Egg ===
Specific to AMD K7 and K8 CPUs, this returns the string "IT'S HAMMER TIME" in EAX, EBX, ECX and EDX,<ref>{{cite web|last1=Ferrie|first1=Peter|title=Attacks on Virtual Machine Emulators|url=http://www.symantec.com/avcenter/reference/Virtual_Machine_Threats.pdf|website=symantec.com|publisher=Symantec Advanced Threat Research|access-date=15 March 2017|archive-url=https://web.archive.org/web/20070207103157/http://www.symantec.com/avcenter/reference/Virtual_Machine_Threats.pdf|archive-date=2007-02-07}}</ref> a reference to the [[MC Hammer]] song [[U Can't Touch This]].

== CPUID usage from high-level languages ==

=== Inline assembly ===
This information is easy to access from other languages as well. For instance, the C code for gcc below prints the first five values, returned by the cpuid:

<syntaxhighlight lang=c>
#include <stdio.h>

/* This works on 32 and 64-bit systems. See [[Inline assembler#In actual compilers]] for hints on reading this code. */
int main()
{
  /* The four registers do not need to be initialized as the processor will write over it. */
  int infotype, a, b, c, d;

  for (infotype = 0; infotype < 5; infotype ++)
  {
    __asm__("cpuid"
            : "=a" (a), "=b" (b), "=c" (c), "=d" (d)   // The output variables. EAX -> a and vice versa.
            : "0" (infotype));                         // Put the infotype into EAX.
    printf ("InfoType %x\nEAX: %x\nEBX: %x\nECX: %x\nEDX: %x\n", infotype, a, b, c, d);
  }

  return 0;
}
</syntaxhighlight>

In MSVC and Borland/Embarcadero C compilers (bcc32) flavored inline assembly, the clobbering information is implicit in the instructions:

<syntaxhighlight lang="c">
#include <stdio.h>
int main()
{
  unsigned int InfoType = 0;
  unsigned int a, b, c, d;
  __asm {
    /* Do the call. */
    mov EAX, InfoType;
    cpuid;
    /* Save results. */
    mov a, EAX;
    mov b, EBX;
    mov c, ECX;
    mov d, EDX;
  }
  printf ("InfoType %x\nEAX: %x\nEBX: %x\nECX: %x\nEDX: %x\n", InfoType, a, b, c, d);
  return 0;
}
</syntaxhighlight>

If either version was written in plain assembly language, the programmer must manually save the results of EAX, EBX, ECX, and EDX elsewhere if they want to keep using the values.

=== Wrapper functions ===

GCC also provides a header called <code>&lt;cpuid.h&gt;</code> on systems that have CPUID. The <code>__cpuid</code> is a macro expanding to inline assembly. Typical usage would be:
<syntaxhighlight lang="c">
#include <cpuid.h>
#include <stdio.h>

int
main (void)
{
  int a, b, c, d;
  __cpuid (0 /* vendor string */, a, b, c, d);
  printf ("EAX: %x\nEBX: %x\nECX: %x\nEDX: %x\n", a, b, c, d);
  return 0;
}
</syntaxhighlight>
But if one requested an extended feature not present on this CPU, they would not notice and might get random, unexpected results. Safer version is also provided in <code>&lt;cpuid.h&gt;</code>. It checks for extended features and does some more safety checks. The output values are not passed using reference-like macro parameters, but more conventional pointers.

<syntaxhighlight lang="c">
#include <cpuid.h>
#include <stdio.h>

int
main (void)
{
  int a, b, c, d;
  if (!__get_cpuid (0x81234567 /* nonexistent, but assume it exists */, &a, &b, &c, &d))
    {
      fprintf (stderr, "Warning: CPUID request 0x81234567 not valid!\n");
    }
  printf("EAX: %x\nEBX: %x\nECX: %x\nEDX: %x\n", a, b, c, d);
  return 0;
}
</syntaxhighlight>

Notice the ampersands in <code>&amp;a, &amp;b, &amp;c, &amp;d</code> and the conditional statement. If the <code>__get_cpuid</code> call receives a correct request, it will return a non-zero value, if it fails, zero.<ref>https://github.com/gcc-mirror/gcc/blob/master/gcc/config/i386/cpuid.h</ref>

Microsoft Visual C compiler has builtin function <code>__cpuid()</code> so the cpuid instruction may be embedded without using inline assembly, which is handy since the x86-64 version of MSVC does not allow inline assembly at all. The same program for [[MSVC]] would be:

<syntaxhighlight lang=cpp>
#include <iostream>
#include <intrin.h>

int main()
{
  int cpuInfo[4];

  for (int a = 0; a < 5; a++)
  {
    __cpuid(cpuInfo, a);
    std::cout << "The code " << a << " gives " << cpuInfo[0] << ", " << cpuInfo[1] << ", " << cpuInfo[2] << ", " << cpuInfo[3] << '\n';
  }

  return 0;
}
</syntaxhighlight>

Many interpreted or compiled scripting languages are capable of using CPUID via an [[Foreign function interface|FFI]] library. [https://web.archive.org/web/20150429190703/http://www.cstrahan.com/posts/pure-ruby-cpuid-via-ffi.html One such implementation] shows usage of the Ruby FFI module to execute assembly language that includes the CPUID opcode.

== CPU-specific information outside x86 ==
Some of the non-x86 CPU architectures also provide certain forms of structured information about the processor's abilities, commonly as a set of special registers:

* [[ARM architecture]]s have a <code>CPUID</code> coprocessor register which requires EL1 or above to access.<ref>{{cite web|url=http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0395b/CIHCAGHH.html |title=ARM Information Center |publisher=Infocenter.arm.com |access-date=2013-04-11}}</ref>
* The [[IBM System z]] mainframe processors have a ''Store CPU ID'' (<code>STIDP</code>) instruction since the 1983 [[IBM 4300|IBM 4381]]<ref>{{cite web |url=https://www-304.ibm.com/servers/resourcelink/lib03060.nsf/pages/srmindex#Toc1 |title=Processor version codes and SRM constants |access-date=2014-09-08 |archive-url=https://web.archive.org/web/20140908232904/https://www-304.ibm.com/servers/resourcelink/lib03060.nsf/pages/srmindex#Toc1#Toc1 |archive-date=2014-09-08 |url-status=dead }}</ref> for querying the processor ID.<ref name=":0">{{cite web|url=http://www.redbooks.ibm.com/redbooks/pdfs/sg247516.pdf | title=IBM System z10 Enterprise Class Technical Guide}}</ref>
* The [[IBM System z]] mainframe processors also have a ''Store Facilities List Extended'' (<code>STFLE</code>) instruction which lists the installed hardware features.<ref name=":0" />
* The [[MIPS architecture|MIPS32/64]] architecture defines a mandatory ''Processor Identification'' (<code>PrId</code>) and a series of daisy-chained ''Configuration Registers''.<ref>{{cite web|url=http://www.cs.cornell.edu/courses/cs3410/2008fa/MIPS_Vol3.pdf | title=MIPS32 Architecture For Programmers, Volume III: The MIPS32 Privileged Resource Architecture|date=2001-03-12|publisher=MIPS Technologies, Inc.}}</ref>
* The [[PowerPC]] processor has the 32-bit read-only ''Processor Version Register'' (<code>PVR</code>) identifying the processor model in use. The instruction requires supervisor access level.<ref>{{cite web|url=http://moss.csc.ncsu.edu/~mueller/cluster/ps3/SDK3.0/docs/arch/PPC_Vers202_Book3_public.pdf | title=PowerPC Operating Environment Architecture, book III}}</ref>

[[Digital signal processor|DSP]] and [[transputer]]-like chip families have not taken up the instruction in any noticeable way, in spite of having (in relative terms) as many variations in design. Alternate ways of silicon identification might be present; for example, DSPs from [[Texas Instruments]] contain a memory-based register set for each functional unit that starts with identifiers determining the unit type and model, its [[ASIC]] design revision and features selected at the design phase, and continues with unit-specific control and data registers. Access to these areas is performed by simply using the existing load and store instructions; thus, for such devices there is no need for extending the register set for the device identification purposes.{{Citation needed|date=September 2015}}

== See also ==
* [[CPU-Z]], a Windows utility that uses <code>CPUID</code> to identify various system settings
* [[Spectre (security vulnerability)]]
* [[Speculative Store Bypass]] (SSB)
* [[Cpuinfo|{{mono|/proc/cpuinfo}}]], a text file generated by certain systems containing some of the CPUID information

== References ==
{{Reflist}}

== Further reading ==
* {{cite web |title=AMD64 Technology Indirect Branch Control Extension |version=Revision 4.10.18 |date=2018 |type=White paper |publisher=[[Advanced Micro Devices, Inc.]] (AMD) |url=https://developer.amd.com/wp-content/resources/Architecture_Guidelines_Update_Indirect_Branch_Control.pdf |access-date=2018-05-09 |url-status=live |archive-url=https://web.archive.org/web/20180509093400/https://developer.amd.com/wp-content/resources/Architecture_Guidelines_Update_Indirect_Branch_Control.pdf |archive-date=2018-05-09}}

== External links ==
* Intel [https://web.archive.org/web/20120625025623/http://www.intel.com/Assets/PDF/appnote/241618.pdf  Processor Identification and the CPUID Instruction] (Application Note 485), last published version. Said to be incorporated into the [http://www.intel.com/Assets/PDF/appnote/241618.pdf Intel® 64 and IA-32 Architectures Software Developer’s Manual] [https://web.archive.org/web/20130626034554/http://www.intel.com/content/dam/www/public/us/en/documents/application-notes/processor-identification-cpuid-instruction-note.pdf in 2013], but {{As of|July 2014|lc=1}} the manual still directs the reader to note 485.
** Contains some information that can be ''and was'' easily misinterpreted though, particularly with respect to [[#EAX=4 and EAX=Bh: Intel thread/core and cache topology|processor topology identification]].
** The big Intel manuals tend to lag behind the Intel ISA document, available at the top of [https://software.intel.com/en-us/intel-isa-extensions this page], which is updated even for processors not yet publicly available, and thus usually contains more CPUID bits. For example, as of this writing the ISA book (at revision 19, dated May 2014) documents the CLFLUSHOPT bit in leaf 7, but the big manuals although apparently more up-to-date (at revision 51, dated June 2014) don't mention it.
* [https://www.amd.com/system/files/TechDocs/24594.pdf AMD64 Architecture Programmer’s Manual Volume 3: General-Purpose and System Instructions]
* cpuid.exe, an open source command-line tool for Windows, available in [https://github.com/JFLarvoire/SysToolsLib/releases SysTools.zip]. Ex: ''cpuid -v'' displays the value of every CPUID feature flag.
* [http://users.atw.hu/instlatx64/ instlatx64] - collection of x86/x64 Instruction Latency, Memory Latency and CPUID dumps

{{Multimedia extensions}}

{{DEFAULTSORT:Cpuid}}
[[Category:X86 architecture]]
[[Category:Machine code]]
[[Category:X86 instructions]]

