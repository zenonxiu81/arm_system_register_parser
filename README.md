# arm_system_register_parser
A python parser for decoding arm aarch32 and aarch64 system registers

This project is to help engineers, who are working on armv7-ar, armv8-a, armv8-r and armv9-a platforms, to decode the value (in Hex format) in all aarch32 and aarch64 system registers, so that they can debug a problem or find information easier.

It requires Python3, and please download the arm system register XML files from arm website, go to https://developer.arm.com/downloads/-/exploration-tools , and click 'Download XML' in Arm Architecture System Registers Tab. Then unzip the downloaded file, and put those *.xml files to the project folder ./sys_reg_xml .

How to decode the value of a register?
You can simply run sys_reg_parser.py, it will promote for the register name and the value as,

Enter the register name:esr_el1
Enter the register value(hex format): 0x0000000096000005

For register name, it should be lowercase. You do not need to specify whether it is aarch32 and aarch64 register, by default, system register name without '_elx' are treated as aarch32 registers,  and system register name with '_elx' are treated as aarch64 registers.

Here is an examples:

```
Enter the register name: esr
Enter the register value(hex format): 0x0000000096000005
-------------------------------------------------------------
bit[ 63 : 56 ] is 0b0
Field Description: Reserved, RES0.

-------------------------------------------------------------
bit[ 55 : 32 ] is 0b0
Field Name: ISS2
Field Description: ISS2 encoding for an exception, the bit assignments are:

-------------------------------------------------------------
bit[ 31 : 26 ] is 0b100101
Field Name: EC
Field Description: Exception Class. Indicates the reason for the exception that this register holds information about.

0b100101:Data Abort exception taken without a change in Exception level.

-------------------------------------------------------------
bit[ 24 : 24 ] is 0b0
Field Name: ISV
Field Description: Instruction Syndrome Valid. Indicates whether the syndrome information in ISS[23:14] is valid.

0b0:No valid instruction syndrome. ISS[23:14] are RES0.

-------------------------------------------------------------
bit[ 23 : 22 ] is 0b0
Field Name: SAS
Field Description: Syndrome Access Size. Indicates the size of the access attempted by the faulting operation.

When ISV == 1
0b00:Byte

-------------------------------------------------------------
bit[ 23 : 22 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 21 : 21 ] is 0b0
Field Name: SSE
Field Description: Syndrome Sign Extend. For a byte, halfword, or word load operation, indicates whether the data item must be sign extended.

When ISV == 1
0b0:Sign-extension not required.

-------------------------------------------------------------
bit[ 21 : 21 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 20 : 16 ] is 0b0
Field Name: SRT
When ISV == 1
-------------------------------------------------------------
bit[ 20 : 18 ] is 0b0
Field Description: Reserved, RES0.

When ISV == 0, FEAT_RASv2 is implemented and (DFSC == 0b010000, or DFSC == 0b01001x or DFSC == 0b0101xx)
-------------------------------------------------------------
bit[ 17 : 16 ] is 0b0
Field Name: WU
Field Description: Write Update. Describes whether a store instruction that generated an External abort updated the location.

When ISV == 0, FEAT_RASv2 is implemented and (DFSC == 0b010000, or DFSC == 0b01001x or DFSC == 0b0101xx)
0b00:Not a store instruction or translation table update, or the location might have been updated.

-------------------------------------------------------------
bit[ 20 : 16 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 15 : 15 ] is 0b0
Field Name: SF
Field Description: Sixty Four bit general-purpose register transfer. Width of the register accessed by the instruction is 64-bit.

When ISV == 1
0b0:Instruction loads/stores a 32-bit general-purpose register.

-------------------------------------------------------------
bit[ 15 : 15 ] is 0b0
Field Name: FnP
Field Description: FAR not Precise.

When ISV == 0
0b0:The FAR holds the faulting virtual address that generated the Data Abort.

-------------------------------------------------------------
bit[ 15 : 15 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 14 : 14 ] is 0b0
Field Name: AR
Field Description: Acquire/Release.

When ISV == 1
0b0:Instruction did not have acquire/release semantics.

-------------------------------------------------------------
bit[ 14 : 14 ] is 0b0
Field Name: PFV
Field Description: FAR Valid. Describes whether the PFAR_EL1 is valid.

When FEAT_PFAR is implemented and (DFSC == 0b010000, or DFSC == 0b01001x or DFSC == 0b0101xx)
0b0:PFAR_EL1 is UNKNOWN.

-------------------------------------------------------------
bit[ 14 : 14 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 13 : 13 ] is 0b0
Field Name: VNCR
Field Description: Indicates that the fault came from use of VNCR_EL2 register by EL1 code.

0b0:The watchpoint was not generated by the use of VNCR_EL2 by EL1 code.

-------------------------------------------------------------
bit[ 12 : 11 ] is 0b0
Field Name: LST
Field Description: Load/Store Type. Used when a Translation fault, Access flag fault, or Permission fault generates a Data Abort.

When (DFSC == 0b00xxxx || DFSC == 0b101011) && DFSC != 0b0000xx
0b00:The instruction that generated the Data Abort is not specified.

-------------------------------------------------------------
bit[ 12 : 11 ] is 0b0
Field Name: SET
Field Description: Synchronous Error Type. Used when a Syncronous External abort, not on a Translation table walk or hardware update of the Translation table, generated the Data Abort. 
Describes the PE error state after taking the Data Abort exception.

When FEAT_RAS is implemented and (DFSC == 0b010000, or DFSC == 0b01001x or DFSC == 0b0101xx)
0b00:Recoverable state (UER).

-------------------------------------------------------------
bit[ 12 : 11 ] is 0b0
Field Description: Reserved, RES0.

Otherwise
-------------------------------------------------------------
bit[ 10 : 10 ] is 0b0
Field Name: FnV
Field Description: FAR not Valid, for a synchronous External abort other than a synchronous External abort on a translation table walk.

0b0:FAR is valid.

-------------------------------------------------------------
bit[ 9 : 9 ] is 0b0
Field Name: EA
Field Description: External abort type. This bit can provide an IMPLEMENTATION DEFINED classification of External aborts.

-------------------------------------------------------------
bit[ 8 : 8 ] is 0b0
Field Name: CM
Field Description: Cache maintenance. Indicates whether the Data Abort came from a cache maintenance or address translation instruction:

0b0:The Data Abort was not generated by the execution of one of the System instructions identified in the description of value 1.

-------------------------------------------------------------
bit[ 7 : 7 ] is 0b0
Field Name: S1PTW
Field Description: For a stage 2 fault, indicates whether the fault was a stage 2 fault on an access made for a stage 1 translation table walk:

0b0:Fault not on a stage 2 translation for a stage 1 translation table walk.

-------------------------------------------------------------
bit[ 6 : 6 ] is 0b0
Field Name: WnR
Field Description: Write not Read. Indicates whether a synchronous abort was caused by an instruction writing to a memory location, or by an instruction reading from a memory location. 

0b0:Abort caused by an instruction reading from a memory location.

-------------------------------------------------------------
bit[ 5 : 0 ] is 0b101
Field Name: DFSC
Field Description: Data Fault Status Code.

0b000101:Translation fault, level 1.

-------------------------------------------------------------
bit[ 25 : 25 ] is 0b1
Field Name: IL
Field Description: Instruction Length for synchronous exceptions. Possible values of this bit are:

0b1:32-bit instruction trapped. This value is also used when the exception is one of the following:

-------------------------------------------------------------
bit[ 24 : 0 ] is 0b101
Field Name: ISS
Field Description: Instruction Specific Syndrome. Architecturally, this field can be defined independently for each defined Exception class. However, in practice, some ISS encodings are used for more than one Exception class.

```
