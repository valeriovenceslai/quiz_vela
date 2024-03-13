# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

# This line gets the directory where the Makefile resides
COMMON_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# This line gets all the source files in the COMMON_DIR directory ending with '.c'
COMMON_SRCS = $(wildcard $(COMMON_DIR)/*.c)

# This line specifies include directories for compilation
INCS := -I$(COMMON_DIR)

# This line sets the default architecture to rv32imc, but allows overriding it externally
# ARCH = rv32im # to disable compressed instructions
ARCH ?= rv32imc

# This block checks if the PROGRAM variable is defined, if so, it sets PROGRAM_C to PROGRAM.c
ifdef PROGRAM
PROGRAM_C := $(PROGRAM).c
endif

# Combine COMMON_SRCS, PROGRAM_C, and EXTRA_SRCS into SRCS
SRCS = $(COMMON_SRCS) $(PROGRAM_C) $(EXTRA_SRCS)

# Separate C source files from assembly source files
C_SRCS = $(filter %.c, $(SRCS))
ASM_SRCS = $(filter %.S, $(SRCS))

# Specify the path to the C compiler
CC = /mnt/rhea_hdd_raid5/opt_non_storage/backend/toolchains/risc/rv32imcb/bin/riscv32-unknown-elf-gcc

# Extract the prefix for cross-compilation from the CC variable
CROSS_COMPILE = $(patsubst %-gcc,%-,$(CC))

# Define default tools for object copying, dumping, and symbol listing
OBJCOPY ?= $(CROSS_COMPILE)objcopy
OBJDUMP ?= $(CROSS_COMPILE)objdump
NM ?= $(CROSS_COMPILE)nm

LINKER_SCRIPT ?= $(COMMON_DIR)/link.ld
CRT ?= $(COMMON_DIR)/crt0.S
# for other options https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html
# for ld debug this is useful -Wl,--print-memory-usage,--print-map 
# -flto[=n]
# This option runs the standard link-time optimizer. When invoked with source code, it generates GIMPLE (one of GCC’s internal representations) and writes192 Using the GNU Compiler Collection (GCC)
# it to special ELF sections in the object file. When the object files are linked together, all the function bodies are read from these ELF sections and instantiated as if they had been part of the same translation unit.
# -fstack-usage to print stack size of each function, note that -flto has to be disabled in this case 

# Compiler flags for C compilation
CFLAGS ?= -march=$(ARCH) -mabi=ilp32 -static -fstack-usage -mcmodel=medany -Wall -flto -g -fstack-usage -Os \
           -fvisibility=hidden -nostdlib -nostartfiles -ffreestanding -Wl,--print-memory-usage,--print-map,--gc-sections $(PROGRAM_CFLAGS)

# Object files generated from C and assembly source files
OBJS := ${C_SRCS:.c=.o} ${ASM_SRCS:.S=.o} ${CRT:.S=.o}

# Dependency files for each object file
DEPS = $(OBJS:%.o=%.d)

# If PROGRAM variable is defined, set output files to include elf, vmem, bin, dis, and log files
ifdef PROGRAM
OUTFILES := $(PROGRAM).elf $(PROGRAM).vmem $(PROGRAM).bin $(PROGRAM).dis $(PROGRAM).log
else
# Otherwise, set output files to object files
OUTFILES := $(OBJS)
endif

# Default target to build all output files
all: $(OUTFILES)

ifdef PROGRAM
# Rule to build the ELF file from object files using linker script
$(PROGRAM).elf: $(OBJS) $(LINKER_SCRIPT) $(COMMON_DIR)/makefile
    # -T passes linker script to GCC
	$(CC) $(CFLAGS) -T $(LINKER_SCRIPT) $(OBJS) -o $@ | tee $(PROGRAM).log
    # Display specific symbols from the ELF file
	$(NM) $(PROGRAM).elf | grep -E "_data_start_mba|network_info_dram_start"
endif

# Rule to generate disassembly file from ELF file
%.dis: %.elf
	$(OBJDUMP) -fhSD $^ > $@

# Rule to generate vmem file from ELF file using elf2vmem.py
%.vmem: %.elf /scratch/par/elf2vmem/elf2vmem.py /scratch/par/elf2vmem/mem.py
	# Remove .bss section
	$(OBJCOPY) --remove-section=.bss $< $<.modified
	# Convert modified ELF file to vmem using elf2vmem.py
	python /scratch/par/elf2vmem/elf2vmem.py $<.modified $@

# Rule to generate binary file from ELF file
%.bin: %.elf
	$(OBJCOPY) -O binary $^ $@

# Rule to compile C source files to object files
# -MMD adds a dependency file
# -c compile but don't link
%.o: %.c
	$(CC) $(CFLAGS) -fstack-usage -MMD -c $(INCS) -o $@ $<

# Rule to assemble assembly source files to object files
# -MMD adds a dependency file
# -c compile but don't link
%.o: %.S
	$(CC) $(CFLAGS) -fstack-usage -MMD -c $(INCS) -o $@ $<

# Clean rule to remove object files, dependency files, and output files
.PHONY: clean
clean:
	$(RM) -f $(OBJS) $(DEPS) $(OUTFILES)

# Print a warning message indicating the default goal
$(warning default goal is $(.DEFAULT_GOAL))
