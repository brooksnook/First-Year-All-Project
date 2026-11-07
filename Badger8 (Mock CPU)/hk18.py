"""
Badger-8: A self-contained 8-bit CPU simulator.

This is the student template.  You must implement the functions below;
do not change their names or signatures.
"""

# some ai autocomplete used throughout for comments
# some functions also taken from the lecturer

from re import match

from debugger_b8 import debugger, print_registers
from helpers_b8 import *

# ============================================================================
#
# TODO (Task 1): implement the following 8-bit arithmetic and logic functions.
# Use the half_add / full_add / half_sub / full_sub / multiplex_four_to_one
# building blocks provided in badger4.py as your starting point.
#
#   eight_bit_add(a7..a0, b7..b0, c0)        → (carry_out, s7..s0)
#   eight_bit_sub(x7..x0, y7..y0, b0)        → (borrow_out, d7..d0)
#   eight_bit_and(a7..a0, b7..b0)            → (r7..r0)
#   eight_bit_not(a7..a0)                    → (r7..r0)
#   eight_bit_multiplex_four_to_one(         → (z7..z0)
#       a7..a0, b7..b0, c7..c0, d7..d0,
#       s1, s0)
#
# You may also keep any helper functions you need (half_add, full_add, etc.)
# see badger4.py / lecture16.py / lecture17.py
# ============================================================================
def half_add(a, b):
  """1-bit half adder
     a = first bit
     b = second bit"""
  s = a ^ b
  c = a & b
  return c, s

def full_add(a, b, c_in):
  """1-bit full adder
      a = first bit
      b = second bit
      c_in = carry in (1 if adding 1, 0 otherwise)"""
  c1, intermediate = half_add(a, b)
  c2, s = half_add(intermediate, c_in) 
  c_out = c1 | c2
  return c_out, s

def half_sub(x, y):
  """Half subtractor
     x = minuend bit
     y = subtrahend bit"""
  d = ((not x) & y) | (x & (not y))
  b = (not x) & y
  return b, d

def full_sub(x, y, b_in):
  """Full subtractor
     x = minuend bit
     y = subtrahend bit
     b_in = borrow in (1 if subtracting 1, 0 otherwise)"""
  b1, intermediate = half_sub(x, b_in)
  b2, d = half_sub(intermediate, y)
  b_out = b1 | b2
  return b_out, d

def eight_bit_add(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, c0):
  """8-bit adder
     a7..a0 = first 8-bit number 
     b7..b0 = second 8-bit number 
     c0 = carry in (1 if adding 1, 0 otherwise)"""
  
  # adds numbers by chaining together 8 bit full adders
  # takes the carry and adds it to the next bit
  c1, s0 = full_add(a0, b0, c0)
  c2, s1 = full_add(a1, b1, c1)
  c3, s2 = full_add(a2, b2, c2)
  c4, s3 = full_add(a3, b3, c3)
  c5, s4 = full_add(a4, b4, c4)
  c6, s5 = full_add(a5, b5, c5)
  c7, s6 = full_add(a6, b6, c6)
  c8, s7 = full_add(a7, b7, c7)

  return (c8, s7, s6, s5, s4, s3, s2, s1, s0)

def eight_bit_sub(x7, x6, x5, x4, x3, x2, x1, x0, y7, y6, y5, y4, y3, y2, y1, y0, b0):
  """8 bit subtractor"""
  """x7..x0 = first 8-bit number
     y7..y0 = second 8-bit number
     b0 = borrow in (1 if subtracting 1, 0 otherwise)"""

  # subtracts numbers by chaining together 8 bit full subtractors
  # takes the borrow and adds it to the next bit
  b1, d0 = full_sub(x0, y0, b0)
  b2, d1 = full_sub(x1, y1, b1)
  b3, d2 = full_sub(x2, y2, b2)
  b4, d3 = full_sub(x3, y3, b3)
  b5, d4 = full_sub(x4, y4, b4)
  b6, d5 = full_sub(x5, y5, b5)
  b7, d6 = full_sub(x6, y6, b6)
  b8, d7 = full_sub(x7, y7, b7)
  return b8, d7, d6, d5, d4, d3, d2, d1, d0

def eight_bit_add_no_carry(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0):
  """8-bit adder ignoring carry in/out — used for IP arithmetic."""
  """a7..a0 = first 8-bit number
     b7..b0 = second 8-bit number"""
  _, s7, s6, s5, s4, s3, s2, s1, s0 = eight_bit_add (a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, 0)
  return s7, s6, s5, s4, s3, s2, s1, s0

def sixteen_bit_add_no_carry(a15, a14, a13, a12, a11, a10, a9, a8, a7, a6, a5, a4, a3, a2, a1, a0,
                              b15, b14, b13, b12, b11, b10, b9, b8, b7, b6, b5, b4, b3, b2, b1, b0):
  """16-bit adder (two chained 8-bit adds). No carry out.
     a15..a0 = first 16-bit number
     b15..b0 = second 16-bit number"""
  c, s7, s6, s5, s4, s3, s2, s1, s0 = eight_bit_add(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, 0)
  _, s15, s14, s13, s12, s11, s10, s9, s8 = eight_bit_add(a15, a14, a13, a12, a11, a10, a9, a8, b15, b14, b13, b12, b11, b10, b9, b8, c)
  return s15, s14, s13, s12, s11, s10, s9, s8, s7, s6, s5, s4, s3, s2, s1, s0

def eight_bit_and(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0):
  """8-bit bitwise AND"""
  """a7..a0 = first 8-bit number
     b7..b0 = second 8-bit number"""

  return ((a7 & b7), (a6 & b6), (a5 & b5), (a4 & b4), (a3 & b3), (a2 & b2), (a1 & b1), (a0 & b0))


def eight_bit_not(a7, a6, a5, a4, a3, a2, a1, a0):
    """8-bit bitwise NOT"""
    """a7..a0 = 8-bit number"""

    return ((not a7), (not a6), (not a5), (not a4), (not a3), (not a2), (not a1), (not a0))

def multiplex_four_to_one(a, b, c, d, s1, s0):
  """1-bit 4-1 multiplexer"""
  """a, b, c, d = inputs
     s1, s0 = selector bits
     a, b, c, d = inputs"""
  
  # only one possible comination of selector bits can be true at any given time
  # this means that the function will return will return whatever the selector bits point to
  z = ((a & (not s1) & (not s0))
      |(b & (not s1) & s0)
      |(c & s1 & (not s0))
      |(d & s1 & s0))
  return z

def eight_bit_multiplex_four_to_one(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, c7, c6, c5, c4, c3, c2, c1, c0, d7, d6, d5, d4, d3, d2, d1, d0, s1, s0):
  """8-bit 4-1 multiplexer"""
  """a7, a6, a5, a4, a3, a2, a1, a0 = input a
     b7, b6, b5, b4, b3, b2, b1, b0 = input b
     c7, c6, c5, c4, c3, c2, c1, c0 = input c
     d7, d6, d5, d4, d3, d2, d1, d0 = input d
     s1, s0 = selector bits"""

  # takes many different inputs, uses each bit as an input
  # to a four to one multiplexer, and returns the result
  z7 = multiplex_four_to_one(a7, b7, c7, d7, s1, s0)
  z6 = multiplex_four_to_one(a6, b6, c6, d6, s1, s0)
  z5 = multiplex_four_to_one(a5, b5, c5, d5, s1, s0)
  z4 = multiplex_four_to_one(a4, b4, c4, d4, s1, s0)
  z3 = multiplex_four_to_one(a3, b3, c3, d3, s1, s0)
  z2 = multiplex_four_to_one(a2, b2, c2, d2, s1, s0)
  z1 = multiplex_four_to_one(a1, b1, c1, d1, s1, s0)
  z0 = multiplex_four_to_one(a0, b0, c0, d0, s1, s0)
  return z7, z6, z5, z4, z3, z2, z1, z0  

def alu(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, f1, f0, opcode1, opcode0):
  """
  4-opcode 8-bit ALU.
  
  a7..a0 = first operand, b7..b0 = second operand (unused for NOT)

  Opcodes (opcode1, opcode0):
    0 0 = ADD   (use f1 as carry-in)
    0 1 = SUB   (use f1 as borrow-in)
    1 0 = AND
    1 1 = NOT   (operates on first operand only)

  f1 = carry/borrow flag in,  f0 = zero flag in (unused by ALU logic itself).

  Returns: (carry_flag_out, zero_flag_out, r7, r6, r5, r4, r3, r2, r1, r0)
    carry_flag_out  — carry out for ADD, borrow out for SUB, unchanged otherwise
    zero_flag_out   — 1 when the result is all zeros
  """

  # TODO (Task 1): implement this function using your eight_bit_* functions above.

  # performs each of the operations the alu performs 
  add_carry_out, add7, add6, add5, add4, add3, add2, add1, add0 = eight_bit_add(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, f1)
  borrow_out, sub7, sub6, sub5, sub4, sub3, sub2, sub1, sub0 = eight_bit_sub(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0, f1)
  and7, and6, and5, and4, and3, and2, and1, and0 = eight_bit_and(a7, a6, a5, a4, a3, a2, a1, a0, b7, b6, b5, b4, b3, b2, b1, b0)
  not7, not6, not5, not4, not3, not2, not1, not0 = eight_bit_not(a7, a6, a5, a4, a3, a2, a1, a0)
  multiplex7, multiplex6, multiplex5, multiplex4, multiplex3, multiplex2, multiplex1, multiplex0 = eight_bit_multiplex_four_to_one(
    add7, add6, add5, add4, add3, add2, add1, add0,
    sub7, sub6, sub5, sub4, sub3, sub2, sub1, sub0,
    and7, and6, and5, and4, and3, and2, and1, and0,
    not7, not6, not5, not4, not3, not2, not1, not0,

    opcode1, opcode0
  )

  carry_flag_out = multiplex_four_to_one(add_carry_out, borrow_out, 0, 0, opcode1, opcode0)
  # does a not of the or of all the bits. if any of them are one, then the result will of the or will be one. 
  # the not negates this to show that the result is not zero.
  # int added because the result of the expression gives a boolean
  zero_flag_out = int(not(multiplex7 | multiplex6 | multiplex5 | multiplex4 | multiplex3 | multiplex2 | multiplex1 | multiplex0))

  return (carry_flag_out, zero_flag_out, multiplex7, multiplex6, multiplex5, multiplex4, multiplex3, multiplex2, multiplex1, multiplex0)

# ============================================================================
# badger-8 CPU Implementation
# ============================================================================

def sel_register(register_file, sel3, sel2, sel1, sel0):
  """Select a register from the register file using a 4-bit selector."""
  """register_file = mapping of register numbers to register names"""
  """sel3..sel0 = 4-bit selector for the register file (e.g., from an instruction operand)"""
  return register_file[bits_to_integer([sel3, sel2, sel1, sel0])]

def cpu(memory, debug=False):
  """Execute a program loaded into memory on the Badger-8 CPU."""
  # ── Registers ──────────────────────────────────────────────────────────────

  # numbering for programmer accessable registers
  register_file = {
    0: "al",
    1: "ah",
    2: "bl",
    3: "bh",
    4: "cl",
    5: "ch",
    6: "dl",
    7: "dh",
    8: "cs",
    9: "ds",
    10: "inp",
    11: "out",
    14: "flags",
  }

  # all registers
  registers = {
    "al": Register(8, "al"),
    "ah": Register(8, "ah"),
    "bl": Register(8, "bl"),
    "bh": Register(8, "bh"),
    "cl": Register(8, "cl"),
    "ch": Register(8, "ch"),
    "dl": Register(8, "dl"),
    "dh": Register(8, "dh"),
    "cs": Register(8, "cs"),
    "ip": Register(8, "ip"),
    "ds": Register(8, "ds"),
    "inp": Register(8, "inp"),
    "out": Register(8, "out"),
    "flags": Register(8, "flags"),
  }

  #   Start the background keyboard thread (Task 4).
  #   passing it the flags and inp registers
  #   Uncomment the next line when you reach Task 4.
  if not debug:
    start_keyboard_hardware(registers["flags"], registers["inp"])

  # ── Main loop ──────────────────────────────────────────────────────────────
  while True:
    jump_performed = False
    # TODO (Task 2): check the halt flag (HF = bit 7 of flags).
    #   If it is 1, break out of the loop, then call print_registers(...).
    if registers["flags"].read()[0]:
      break

    # ── FETCH ─────────────────────────────────────────────────────────────────
    # TODO (Task 2): fetch opcode from CS:IP and operand from CS:IP+1.
    # Use sixteen_bit_add_no_carry to compute the operand address.

    # cs points to where instructions start
    cs_data = registers["cs"].read()
    ip_data = registers["ip"].read()
    opcode_location = list(cs_data) + list(ip_data)

    # operand is one byte after the opcode
    operand_location = sixteen_bit_add_no_carry(
      *opcode_location,
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
    )

    opcode = memory.read(opcode_location)
    operand = memory.read(operand_location)

    # ── DEBUG hook (leave this block as-is) ───────────────────────────────────
    # Uncomment the below once you are have defined the registers
    if debug:
      if not debugger(registers["al"], registers["ah"], registers["bl"], registers["bh"], registers["cl"], registers["ch"], registers["dl"], registers["dh"], registers["cs"], registers["ip"], registers["ds"], registers["inp"], registers["out"], registers["flags"], opcode, operand, memory):
        break

    # ── DECODE operand type ───────────────────────────────────────────────────
    # TODO (Task 2): 
    # if the first bit of the opcode is one then operand is immediate
    # also used for jumps (if the first bit the opcode is one then jump above)
    is_immediate = opcode[0]

    # ── DECODE opcode and EXECUTE ─────────────────────────────────────────────
    # TODO (Task 2):
    
    # operation is first three bits after bit determining whether the operand is an immediate
    operation = (opcode[1], opcode[2], opcode[3])
    # destination register is the last four bits
    destination_register = (opcode[4], opcode[5], opcode[6], opcode[7])
    match operation:
      # mov
      case (1, 0, 0):
        if is_immediate:
          # simply writes the operand to the destination register
          registers[sel_register(register_file, *destination_register)].write(operand)
        else:
          # reads the data to be written from the register in the operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # writes the data
          registers[sel_register(register_file, *destination_register)].write(operand_data)
        # detects if out register was written to and prints to the screen if it has
        if registers[sel_register(register_file, *destination_register)].name == "out":
          # converts bits in output register to integer, gets corrosponding output character, then prints
          # end="" added to remove newline
          print(chr(bits_to_integer(registers["out"].read())), end="")
          # sets output flag to 1 to indicate that we have finished producing an output
          set_flag(registers["flags"], 4, 1)
      # add
      case (0, 0, 0):
        if is_immediate:
          # reads the destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # takes the data in the destination register and adds it to the operand
          result = alu(
            *destination_data,
            *operand,
            0, 0, 0, 0
          )
          # writes the result to the destination register  
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # writes the carry and zero flags respectively to the flags register
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
        else:
          # reads the data to be written from the register in the operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # reads the destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # takes the data in the destination register and adds it to the data read from the register
          # in the operand
          result = alu(
            *destination_data,
            *operand_data,
            0, 0, 0, 0
          )

          # writes the result to the destination register
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # writes the carry and zero flags respectively to the flags register
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
      # subtraction
      case (0, 0, 1):
        if is_immediate:
          # reads the destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # subtracts the data in the operand from the destination register
          result = alu(
            *destination_data,
            *operand,
            0, 0, 0, 1
          )
          # writes the result to the destination register
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # writes the carry and zero flags respectively to the flags register
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
        else:
          # reads the data in the register in the operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # reads the destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # subtracts the data in the operand from the destination register
          result = alu(
            *destination_data,
            *operand_data,
            0, 0, 0, 1
          )

          # writes the result to the destination register
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # writes the carry and zero flags respectively to the flags register
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
      # load
      case (1, 0, 1):
        if is_immediate:
          # gets the memory address by taking the data segment and adding the operand
          memory_address = registers["ds"].read() + operand
          # reads the data at that memory address
          data = memory.read(memory_address)
          # writes data from memory to destination register
          registers[sel_register(register_file, *destination_register)].write(data)
        else:
          # gets the data from the register in the operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # gets the memory address by taking the data segment and adding what we read from the register
          # in the operand
          memory_address = registers["ds"].read() + operand_data
          # reads data at memory address
          data = memory.read(memory_address)
          # writes data from memory to destination register
          registers[sel_register(register_file, *destination_register)].write(data)
      # store
      case (1, 1, 0):
        if is_immediate:
          # gets memory address to be written to by reading the data segment and appending
          # the operand
          memory_address = registers["ds"].read() + operand
          # reads the data in the register
          data = registers[sel_register(register_file, *destination_register)].read()
          # writes the data in the register to the memory address
          memory.write(memory_address, data)
        else:
          # reads the data in the register in the operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # gets the memory address to be written to by reading the data segment and appending
          # the data from the register in the operand
          memory_address = registers["ds"].read() + operand_data
          # reads the data to be written from the register
          data = registers[sel_register(register_file, *destination_register)].read()
          # writes the data in the register to the memory address
          memory.write(memory_address, data)
      # not
      case (0, 1, 1):
        # gets data from destination register
        destination_data = registers[sel_register(register_file, *destination_register)].read()
        # does a not operation on said data
        result = alu(
          *destination_data,
          0, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 1, 1)
        # writes result to destination register
        registers[sel_register(register_file, *destination_register)].write(result[2:10])
        # sets flags
        registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
      # and
      case (0, 1, 0):
        if is_immediate:
          # gets data from destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # does and operation with data from operand
          result = alu(
            *destination_data,
            *operand,
            0, 0, 1, 0
          )
          # writes result to destination register
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # sets flags
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
        else:
          # reads data from register in operand
          operand_data = registers[sel_register(register_file, operand[0], operand[1], operand[2], operand[3])].read()
          # gets data from destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # does and operation with data from register in operand
          result = alu(
            *destination_data,
            *operand_data,
            0, 0, 1, 0
          )

          # writes result to destination register
          registers[sel_register(register_file, *destination_register)].write(result[2:10])
          # sets flags
          registers["flags"].write([0, 0, 0, 0, 0, 0, result[0], result[1]])
      # jumps
      case (1, 1, 1):
        # jump above
        if is_immediate:
          # reads flags
          carry_flag = registers["flags"].read()[6]
          zero_flag = registers["flags"].read()[7]
          # gets instruction to jump to from destination register
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # perform jump if carry flag is zero and result is not zero
          if carry_flag == 0 and zero_flag == 0: 
            # writes destination data to instruction pointer
            registers["ip"].write(destination_data)
            # make sure we don't increment the instruction pointer after jump
            jump_performed = True
        # jump if equal
        else:
          zero_flag = registers["flags"].read()[7]
          destination_data = registers[sel_register(register_file, *destination_register)].read()
          # performs jump if operation was equal to zero
          if zero_flag == 1: 
            # writes instruction to jump to to instruction pointer
            registers["ip"].write(destination_data)
            # make sure we don't increment the instruction pointer after jump
            jump_performed = True
      # nop
      case (0, 1, 1):
        # simply does nothing and increments the instruction pointer
        pass

    # ── ADVANCE IP ────────────────────────────────────────────────────────────
    # TODO (Task 2): advance ip by 2 using eight_bit_add_no_carry,
    #   but only when no jump has occurred (Task 3).

    # don't increment if we have performed a jump
    if not jump_performed:
      # adds two to move to the next instruction
      # two bytes added to move past current instruction and operand
      next_instruction = sixteen_bit_add_no_carry(
        *registers["cs"].read(),
        *registers["ip"].read(),
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
      )
      registers["cs"].write(next_instruction[0:8])
      registers["ip"].write(next_instruction[8:16])

  # If we exited print final registers
  # comment this out once you have implemented more
  print_registers(registers["al"], registers["ah"], registers["bl"], registers["bh"], registers["cl"], registers["ch"], registers["dl"], registers["dh"], registers["cs"], registers["ds"], registers["inp"], registers["out"], registers["flags"], registers["ip"])


# ============================================================================
# Main Program
# ============================================================================

if __name__ == '__main__':
  import sys

  # Setup memory
  memory = Memory(8, 2**16)
  size = 0
  # Check if a binary file is provided
  if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(f"Loading program from {filename}...")
    size = memory.load_binary(filename)
  else:
    raise ValueError("Please specify the .o binary file")

  if len(sys.argv) > 2 and sys.argv[2] == '--debug':
    # Run the CPU with debugger
    print("\nStarting Badger-8 CPU...")
    print("Commands: 's' to step, 'x <addr>' to examine memory, 'i' to provide an input character, 'q' to quit\n")
    cpu(memory, debug=True)
  else:
    cpu(memory, debug=False)
