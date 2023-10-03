#!/bin/bash
# Script to find number of assembly code references to SSE or AVX-128 registers (xmm),
#   AVX-256 registers (ymm), and AVX-512 registers (zmm), as well as AVX-specific instructions.
#   Assume collection of .s files generated from, e.g., "ifort -S"
echo -n 'XMM register (SSE or AVX-128) reference count: '
grep %xmm *.s | wc -l
echo -n 'YMM register (AVX-256) reference count: '
grep %ymm *.s | wc -l
echo -n 'ZMM register (AVX-512) reference count: '
grep %zmm *.s | wc -l
echo -n 'VBROADCASTSS instructions (copy 32-bit operand to xmm or ymm register): '
grep vbroadcastss *.s | wc -l
echo -n 'VBROADCASTSD instructions (copy 64-bit operand to xmm or ymm register): '
grep vbroadcastsd *.s | wc -l
echo -n 'VBROADCASTF128 instructions (copy 128-bit operand to xmm or ymm register): '
grep vbroadcastf128 *.s | wc -l
echo -n 'VINSERTF128 instructions (replace half of YMM reg with 128-bit operand): '
grep vinsertf128 *.s | wc -l   
echo -n 'VEXTRACTF128 instructions (Half of 256-bit register to 128-bit destination): '
grep vextractf128 *.s | wc -l
echo -n 'VMASKMOVP[SD] instructions (Read some SIMD vector operands into register, leave rest of dest zeros): '
grep 'vmaskmovp[sd]' *.s | wc -l
echo -n 'VPERMILP[SD] instructions (Shuffle vector elements of input within common 128-bit window of output): '
grep 'vpermilp[sd]' *.s | wc -l
echo -n 'VPERM2F128 instructions (Shuffle 4 128-bit elements of 2 256-bit elements into 1 256-bit destination): '
grep vperm2f128 *.s | wc -l
echo -n 'VZEROALL instructions (Set all YMM registers to 0 and tag as unused when switching between 128- and 256-bit): '
grep vzeroall *.s | wc -l
echo -n 'VZEROUPPER instructions (Set upper half of all YMM registers to 0 when switching between 128- and 256-bit): '
grep vzeroupper *.s | wc -l
