# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

/* C runtime system (crt0) */
/* The C Runtime system must carry out the following tasks. */
/* - Set up the target platform in a consistent state. For example setting up appropriate exception vectors. */
/* - Initialize the stack and frame pointers */
/* - Invoke the C constructor initialization and ensure destructors are called on exit. */
/* - Carry out any further platform specific initialization. */
/* - Call the C main function. */
/* - Exit with the return code supplied if the C main function ever terminates. */
/* The code is invariably assembler, although it may call out to C functions,  */
/* and is best illustrated by example from the OpenRISC 1000 . */


.section .text.startup
mba_mem_copy:
  // void function that copies from a0 (included)...a1 (excluded) to a2 
  // uses x28 as scratch register
  // a0 points to start address in I/Dmem
  // a1 points to end address in I/Dmem
  // a2 points to start address in mba
  bge a0, a1, mba_mem_copy_end
mba_mem_copy_loop:
  lw x28, 0(a2)
  addi a2, a2, 4
  addi a0, a0, 4
  sw x28, -4(a0)
  blt a0, a1, mba_mem_copy_loop
mba_mem_copy_end:
  jr ra

default_exc_handler:
  jal x0, reset_handler
/* TODO: consider just copying from bootaddr to rodata*/
reset_handler:
  /* set all registers to zero */
  /* TODO: set to zero only non temporary registers*/

  // mv  x1, x0
  // mv  x2, x1
  // mv  x3, x1
  // mv  x4, x1
  // mv  x5, x1
  // mv  x6, x1
  // mv  x7, x1
  // mv  x8, x1
  // mv  x9, x1
  // mv x10, x1
  // mv x11, x1
  // mv x12, x1
  // mv x13, x1
  // mv x14, x1
  // mv x15, x1
  // mv x16, x1
  // mv x17, x1
  // mv x18, x1
  // mv x19, x1
  // mv x20, x1
  // mv x21, x1
  // mv x22, x1
  // mv x23, x1
  // mv x24, x1
  // mv x25, x1
  // mv x26, x1
  // mv x27, x1
  // mv x28, x1
  // mv x29, x1
  // mv x30, x1
  // mv x31, x1

  /* initialize stack */
  lui  sp, %hi(_stack_start)
  addi sp, sp, %lo(_stack_start)

_start:
  .global _start

  /* load .vector in IMEM*/
  // lui  a0, %hi(_vectors_start_imem)
  // addi a0, a0, %lo(_vectors_start_imem)
  // lui  a1, %hi(_vectors_end_imem)
  // addi a1, a1, %lo(_vectors_end_imem)
  // lui  a2, %hi(_vectors_start_mba)
  // addi a2, a2, %lo(_vectors_start_mba)
  //TODO: we can move all vectors/imem (not startup though) at once packing them together
  // this should also allow easier load symbol lla and pc based

  // jal ra, mba_mem_copy

  /* load .text in IMEM */
  lui  a2, %hi(_text_start_mba)
  addi a2, a2, %lo(_text_start_mba)
  lui  a0, %hi(_text_start_imem)
  addi a0, a0, %lo(_text_start_imem)
  lui  a1, %hi(_text_end_imem)
  addi a1, a1, %lo(_text_end_imem)
  
  jal ra, mba_mem_copy

/* to prevent unaligned copy from ROM to RAM fill _text_end_imem with 0s*/
  sw x0, (a1)

/*load .data (contains both .data and .rodata) in D_MEM*/
  lui  a0, %hi(_data_start_dmem)
  addi a0, a0, %lo(_data_start_dmem)
  lui  a1, %hi(_data_end_dmem)
  addi a1, a1, %lo(_data_end_dmem)
  lui  a2, %hi(_data_start_mba)
  addi a2, a2, %lo(_data_start_mba)

  jal ra, mba_mem_copy

/* load bss */
  /* set 0s in the BSS */
  lui  a0, %hi(_bss_start_dmem)
  addi a0, a0, %lo(_bss_start_dmem)
  lui  a1, %hi(_bss_end_dmem)
  addi a1, a1, %lo(_bss_end_dmem)

  bge a0, a1, bss_load_loop_end
bss_load_loop:
  sw x0, 0(a0)
  addi a0, a0, 4
  blt a1, a0, bss_load_loop
bss_load_loop_end:


main_entry:
  /* jump to main program entry point (argc = argv = 0) */
  addi a0, x0, 0
  addi a1, x0, 0
  lui  x26, %hi(main)
  addi x26, x26, %lo(main)
  jalr x1, x26

  /* If execution ends up here just put the core to sleep */
sleep_loop:
  wfi /* wait for interrupt */
  j sleep_loop

/* =================================================== [ exceptions ] === */
/* This section has to be down here, since we have to disable rvc for it  */

interrupt_service_routine_mba:
  // save context according to ABI and
  // relay the call to isr that sits in 
  // save return address
  addi sp, sp, -64
  sw x1, (sp)
  // save temp
  sw x5 , +4(sp)
  sw x6 , +8(sp)
  sw x7 , +12(sp)
  sw x28, +16(sp)
  sw x29, +20(sp)
  sw x30, +24(sp)
  sw x31, +28(sp)
  // save args
  sw x10, +32(sp)
  sw x11, +36(sp)
  sw x12, +40(sp)
  sw x13, +44(sp)
  sw x14, +48(sp)
  sw x15, +52(sp)
  sw x16, +56(sp)
  sw x17, +60(sp)
  
  lui  x6, %hi(interrupt_service_routine)
  addi x6, x6, %lo(interrupt_service_routine)
  // jump to interrupt_service_routine
  jalr x1, x6 

  lw x1, (sp)
  // save temp
  lw x5 , +4(sp)
  lw x6 , +8(sp)
  lw x7 , +12(sp)
  lw x28, +16(sp)
  lw x29, +20(sp)
  lw x30, +24(sp)
  lw x31, +28(sp)
  // save args
  lw x10, +32(sp)
  lw x11, +36(sp)
  lw x12, +40(sp)
  lw x13, +44(sp)
  lw x14, +48(sp)
  lw x15, +52(sp)
  lw x16, +56(sp)
  lw x17, +60(sp)
  addi sp, sp, 64

  mret

.section .vectors, "ax"
.option norvc;

  /* All unimplemented interrupts/exceptions go to the default_exc_handler.*/
  /* we have a table with 32 entries for fast interrupts and then the start address */
  .org 0x00
  .rept 11
  jal x0, default_exc_handler
  .endr
  jal x0, interrupt_service_routine_mba
  .rept 20
  jal x0, default_exc_handler
  .endr

  /* reset vector */
  .org 0x80
  jal x0, reset_handler
