	.file	"longestsubstring.c"
	.text
	.section	.rodata
.LC0:
	.string	"duplicat i = %d , j = %d "
.LC1:
	.string	"max length is %d"
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$80, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movabsq	$7306073769693635169, %rax
	movabsq	$7598257998534111841, %rdx
	movq	%rax, -48(%rbp)
	movq	%rdx, -40(%rbp)
	movabsq	$7308341053099696754, %rax
	movq	%rax, -32(%rbp)
	movw	$26994, -24(%rbp)
	movb	$0, -22(%rbp)
	leaq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	strlen@PLT
	movl	%eax, -56(%rbp)
	movl	$0, -68(%rbp)
	movl	$0, -64(%rbp)
	jmp	.L2
.L10:
	movl	-64(%rbp), %eax
	addl	$1, %eax
	movl	%eax, -60(%rbp)
	jmp	.L3
.L7:
	movl	-60(%rbp), %eax
	cltq
	movzbl	-48(%rbp,%rax), %edx
	movl	-64(%rbp), %eax
	cltq
	movzbl	-48(%rbp,%rax), %eax
	cmpb	%al, %dl
	je	.L4
	movl	-56(%rbp), %eax
	subl	$1, %eax
	cmpl	%eax, -60(%rbp)
	jne	.L5
.L4:
	movl	-60(%rbp), %edx
	movl	-64(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	-60(%rbp), %eax
	subl	-64(%rbp), %eax
	movl	%eax, -52(%rbp)
	movl	-52(%rbp), %eax
	cmpl	-68(%rbp), %eax
	jle	.L5
	movl	-52(%rbp), %eax
	movl	%eax, -68(%rbp)
	jmp	.L6
.L5:
	addl	$1, -60(%rbp)
.L3:
	movl	-60(%rbp), %eax
	cmpl	-56(%rbp), %eax
	jl	.L7
.L6:
	movl	-56(%rbp), %eax
	subl	-64(%rbp), %eax
	cmpl	%eax, -68(%rbp)
	jg	.L13
	addl	$1, -64(%rbp)
.L2:
	movl	-64(%rbp), %eax
	cmpl	-56(%rbp), %eax
	jl	.L10
	jmp	.L9
.L13:
	nop
.L9:
	movl	-68(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC1(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L12
	call	__stack_chk_fail@PLT
.L12:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
