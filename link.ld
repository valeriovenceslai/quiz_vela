/* Copyright lowRISC contributors.
   Licensed under the Apache License, Version 2.0, see LICENSE for details.
   SPDX-License-Identifier: Apache-2.0 */

OUTPUT_ARCH(riscv)

MEMORY
{
    MBA         : ORIGIN = 0x00000000, LENGTH = 4M
    MBA_LUC     : ORIGIN = 0x00000800, LENGTH = 9K /* 8KB  at 'h00000 (from sim) << 3 */
    IMEM        : ORIGIN = 0x00800000, LENGTH = 4K
    DMEM        : ORIGIN = 0x00801000, LENGTH = 4K

}
/* stack goes from high addresses to low address*/
 
/* Stack information variables for the compiler*/
_stack_len     = LENGTH(DMEM)/2;
/* stack starts at the very end of DMEM */
_stack_start   = ORIGIN(DMEM) + LENGTH(DMEM);

_entry_point = _vectors_start_mba + 0x80;
ENTRY(_entry_point)

SECTIONS
{

    .vectors : 
    {
        . = ALIGN(4);                        // . = ALIGN(4): This directive ensures that the current location counter (. here) is aligned to a 4-byte boundary. Alignment ensures that the subsequent section starts at an address divisible by 4, which is often a requirement for RISC-V architectures.
		_vectors_start_imem = .;             // This assigns the current location to the variable _vectors_start_imem. It marks the beginning of the vector table in memory.
        KEEP(*(.vectors))                    // This directive tells the linker to keep all contents found in the .vectors section. This is important because the vector table contains critical information for the program, such as interrupt handlers, and should not be removed or optimized out.
		_vectors_end_imem = .;               // This assigns the current location to the variable _vectors_end_imem. It marks the end of the vector table in memory.
    } > MBA_LUC                              // This specifies that the .vectors section should be placed in the MBA_LUC memory region.
    _vectors_start_mba = LOADADDR(.vectors); // This command calculates the load address of the .vectors section and assigns it to the variable _vectors_start_mba. The load address is the address where the section will be loaded into memory during program execution.

    .text.startup :  
    {
        . = ALIGN(4);
        *(.text.startup) // This command tells the linker to place all code from the .text.startup section into the MBA_LUC memory region. The * is a wildcard that matches any input section name, and .text.startup specifies the specific section containing the startup code.
    } > MBA_LUC
    /* NOTE: TODO: .data can be after .text to simplify movememt from MBA to IMEM and MBA to DMEM, but this requires to keep updating axi_lmc_write_sequence_luc */
    /* note that in that case .text is moved directly after .vectors NOTE: that text.startup is not moved to IMEM */

    // This section of the linker script handles the placement of initialized data (.data section) into the DMEM memory region, with the data being loaded from MBA_LUC
    .data : // This is the name of the section where initialized data is stored. Initialized data typically includes global and static variables that are explicitly initialized with values.
    {
        . = ALIGN(4);
        _data_start_dmem = .;
        /* Small RO data before large RO data */
        *(.srodata)                    // These lines specify that the linker should include sections containing read-only data (.srodata and .rodata) into the .data section. The * wildcard matches any input section name.
        *(.srodata.*)
        *(.rodata);
        *(.rodata.*)
        /* Small data before large data */
        *(.sdata)                      // These lines specify that the linker should include sections containing initialized data (.sdata and .data) into the .data section.
        *(.sdata.*)
        *(.data);
        *(.data.*)
        _data_end_dmem = .;
    } > DMEM AT > MBA_LUC              // This specifies that the .data section should be placed in the DMEM memory region. Additionally, it indicates that the data should be loaded from MBA_LUC. 
                                       // The AT > MBA_LUC part ensures that the data will be physically located in DMEM, but it will be loaded from MBA_LUC during runtime.
    
                                        // The DMEM part part of the .data definition in your example specifies the virtual memory address (VMA) of the .data section, 
                                        // whereas the the MBA_LUC part specifies the load memory address (LMA).
    _data_start_mba = LOADADDR(.data);

    .bss (NOLOAD) : //  The (NOLOAD) attribute indicates that this section does not need to be loaded from the input file into the output file; instead, it only specifies the memory region where the BSS section will reside during runtime.
    {
        . = ALIGN(4);
        _bss_start_dmem = .;
        /* Small BSS before large BSS */
                       // These lines specify that the linker should include sections containing uninitialized data (.sbss and .bss) into the .bss section.
        *(.sbss)       // This matches all sections named .sbss. Typically, .sbss sections contain uninitialized static variables with local scope. 
        *(.sbss.*)     // The .* wildcard matches any characters after .sbss.. This allows matching multiple sections with variations of the .sbss prefix, such as .sbss_init, .sbss_extra, etc.
        *(.bss)        // Similar to .sbss, .bss sections typically contain uninitialized static variables, but they may have a broader scope than .sbss sections, potentially including global variables.
        *(.bss.*)
        *(COMMON)      // This line includes any common symbols (uninitialized global variables) into the .bss section.
        _bss_end_dmem = .;
    } > DMEM
    
    .text :  // This section of the linker script is responsible for placing the program's executable code (.text section) into the IMEM memory region, with the code being loaded from MBA_LUC
    {
        . = ALIGN(4);
        _text_start_imem = .;
        *(.text)       // This command tells the linker to place all code from the .text section into the output file. The * wildcard matches any input section name, and .text specifies the specific section containing the program's code.
        _text_end_imem = .;
    } > IMEM AT > MBA_LUC
    _text_start_mba = LOADADDR(.text);

}
