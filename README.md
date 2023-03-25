# arm_system_register_parser
A python parser for decoding arm aarch32 and aarch64 system registers

This project is to help engineers, who are working on armv7-ar, armv8-a, armv8-r and armv9-a platforms, to decode the value (in Hex format) in all aarch32 and aarch64 system registers, so that they can debug a problem or find information easier.

It requires Python3, and please download the arm system register XML files from arm website, go to https://developer.arm.com/downloads/-/exploration-tools , and click 'Download XML' in Arm Architecture System Registers Tab. Then unzip the downloaded file, and put those *.xml files to the project folder ./sys_reg_xml .

How to decode the value of a register?
You can simply run sys_reg_parser.py, it will promote for the register name and the value as,

Enter the register name:esr_el1
Enter the register value(hex format): 0x0000000096000005

For register name, it should be lowercase. You do not need to specify whether it is aarch32 and aarch64 register, by default, system register name without '_elx' are treated as aarch32 registers,  and system register name with '_elx' are treated as aarch64 registers.

Here are a few examples:
*****************************************************************************

Enter the register name:esr_el1
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
Field Description: Synchronous Error Type. Used when a Syncronous External abort, not on a Translation table walk or hardware update of the Translation table, generated the Data Abort. Describes the PE error state after taking the Data Abort exception.
          
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

***************************************************************************************












An example of decoding the SCR_EL3 register.

********************************************************************************


-------------------------------------------------------------
bit[ 63 : 63 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 62 : 62 ] is 0b0
Field Name: NSE
Field Description: This field, evaluated with SCR_EL3.NS, selects the Security state of EL2 and lower Exception levels.
    
When FEAT_RME is implemented
-------------------------------------------------------------
bit[ 62 : 62 ] is 0b0
Field Name: NSE
Field Description: Reserved, RES0, and the Effective value of this bit is 0b0.
    
Otherwise
-------------------------------------------------------------
bit[ 61 : 60 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 59 : 59 ] is 0b0
Field Name: FGTEn2
Field Description: Fine-Grained Traps Enable 2.

When FEAT_FGT2 is implemented
0b0:EL2 accesses to the specified registers are trapped to EL3. The values in these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 59 : 59 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 58 : 56 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 55 : 55 ] is 0b0
Field Name: EnIDCP128
Field Description: Enables access to IMPLEMENTATION DEFINED 128-bit System registers.
    
When FEAT_SYSREG128 is implemented
0b0:Accesses at EL2, EL1, EL0 to IMPLEMENTATION DEFINED 128-bit System registers are trapped to EL3 using an ESR_EL3.EC value of 0x14, unless the access generates a higher priority exception.

-------------------------------------------------------------
bit[ 55 : 55 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 54 : 54 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 53 : 53 ] is 0b0
Field Name: PFAREn
Field Description: Enable access to Physical Fault Address Registers. When disabled, accesses to Physical Fault Address Registers generate a trap to EL3.
    
When FEAT_PFAR is implemented
0b0:Accesses of the specified Physical Fault Address Registers at EL2 and EL1 are trapped to EL3, unless the instruction generates a higher priority exception.
        
-------------------------------------------------------------
bit[ 53 : 53 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 52 : 52 ] is 0b0
Field Name: TWERR
Field Description: Trap writes of error record registers. Enables a trap to EL3 on writes of error record registers.
    
When FEAT_RASv2 is implemented
0b0:Writes of the specified error record registers are not trapped by this mechanism.
        
-------------------------------------------------------------
bit[ 52 : 52 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 51 : 51 ] is 0b0
Field Name: TMEA
Field Description: Trap Masked External Aborts. Controls whether a masked error exception at a lower Exception level is taken to EL3.
    
When FEAT_DoubleFault2 is implemented
0b0:Synchronous External Abort exceptions and SError exceptions at EL2, EL1, and EL0 are unaffected by this mechanism.
        
-------------------------------------------------------------
bit[ 51 : 51 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 50 : 50 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 49 : 49 ] is 0b0
Field Name: MECEn
Field Description: Enables access to the following EL2 MECID registers, from EL2:

When FEAT_MEC is implemented
0b0:Accesses from EL2 to a listed MECID register are trapped to EL3. The value of a listed EL2 MECID register is treated as 0 for all purposes other than direct reads or writes to the register from EL3.
        
-------------------------------------------------------------
bit[ 49 : 49 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 48 : 48 ] is 0b0
Field Name: GPF
Field Description: Controls the reporting of Granule protection faults at EL0, EL1 and EL2.
    
When FEAT_RME is implemented
0b0:This control does not cause exceptions to be routed from EL0, EL1 or EL2 to EL3.
        
-------------------------------------------------------------
bit[ 48 : 48 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 47 : 47 ] is 0b0
Field Name: D128En
Field Description: 128-bit System Register trap control. Enables access to 128-bit System Registers via MRRS, MSRR instructions.

When FEAT_D128 is implemented
0b0:EL1 and EL2 accesses to the specificed registers are disabled, and trapped to EL3.
        
-------------------------------------------------------------
bit[ 47 : 47 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 46 : 46 ] is 0b0
Field Name: AIEn
Field Description: MAIR2_ELx, AMAIR2_ELx Register access trap control.

When FEAT_AIE is implemented
0b0:EL1 and EL2 accesses to the specificed registers are disabled, and trapped to EL3. The values in these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 46 : 46 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 45 : 45 ] is 0b0
Field Name: PIEn
Field Description: Permission Indirection, Overlay Register access trap control. Enables access to Permission Indirection and Overlay registers.

When FEAT_S1PIE is implemented, or FEAT_S2PIE is implemented, or FEAT_S1POE is implemented or FEAT_S2POE is implemented
0b0:EL0, EL1 and EL2 accesses to the specificed registers are disabled, and trapped to EL3. The values in these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 45 : 45 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 44 : 44 ] is 0b0
Field Name: SCTLR2En
Field Description: SCTLR2_ELx register trap control. Enables access to SCTLR2_EL1 and SCTLR2_EL2 registers.
    
When FEAT_SCTLR2 is implemented
0b0:EL1 and EL2 accesses to SCTLR2_EL1 and SCTLR2_EL2 registers are disabled, and trapped to EL3. The values in these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 44 : 44 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 43 : 43 ] is 0b0
Field Name: TCR2En
Field Description: TCR2_ELx register trap control. Enables access to TCR2_EL1 and TCR2_EL2 registers.
    
When FEAT_TCR2 is implemented
0b0:EL1 and EL2 accesses to TCR2_EL1 and TCR2_EL2 registers are disabled, and trapped to EL3. The values in these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 43 : 43 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 42 : 42 ] is 0b0
Field Name: RCWMASKEn
Field Description: RCW and RCWS Mask register trap control. Enables access to RCWMASK_EL1, RCWSMASK_EL1.
    
When FEAT_THE is implemented
0b0:EL1 and EL2 accesses to RCWMASK_EL1 and RCWSMASK_EL1 registers are disabled, and trapped to EL3.
        
-------------------------------------------------------------
bit[ 42 : 42 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 41 : 41 ] is 0b0
Field Name: EnTP2
Field Description: Traps instructions executed at EL2, EL1, and EL0 that access TPIDR2_EL0 to EL3. The exception is reported using ESR_ELx.EC value 0x18.
    
When FEAT_SME is implemented
0b0:This control causes execution of these instructions at EL2, EL1, and EL0 to be trapped.
        
-------------------------------------------------------------
bit[ 41 : 41 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 40 : 40 ] is 0b0
Field Name: TRNDR
Field Description: Controls trapping of reads of RNDR and RNDRRS. The exception is reported using ESR_ELx.EC value 0x18.
    
When FEAT_RNG_TRAP is implemented
0b0:This control does not cause RNDR and RNDRRS to be trapped.

-------------------------------------------------------------
bit[ 40 : 40 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 39 : 39 ] is 0b0
Field Name: GCSEn
Field Description: Guarded control stack enable. Controls access to the Guarded Control Stack registers from EL2, EL1, and EL0, and controls whether the Guarded Control Stack is enabled.
    
When FEAT_GCS is implemented
0b0:Trap read and write accesses to all Guarded Control Stack registers to EL3. All Guarded Control Stack behavior is disabled at EL2, EL1, and EL0.
        
-------------------------------------------------------------
bit[ 39 : 39 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 38 : 38 ] is 0b0
Field Name: HXEn
Field Description: Enables access to the HCRX_EL2 register at EL2 from EL3.
    
When FEAT_HCX is implemented
0b0:Accesses at EL2 to HCRX_EL2 are trapped to EL3. Indirect reads of HCRX_EL2 return 0.
        
-------------------------------------------------------------
bit[ 38 : 38 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 37 : 37 ] is 0b0
Field Name: ADEn
Field Description: Enables access to the ACCDATA_EL1 register at EL1 and EL2.
    
When FEAT_LS64_ACCDATA is implemented
0b0:Accesses to ACCDATA_EL1 at EL1 and EL2 are trapped to EL3, unless the accesses are trapped to EL2 by the EL2 fine-grained trap.
        
-------------------------------------------------------------
bit[ 37 : 37 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 36 : 36 ] is 0b0
Field Name: EnAS0
Field Description: Traps execution of an ST64BV0 instruction at EL0, EL1, or EL2 to EL3.
    
When FEAT_LS64_ACCDATA is implemented
0b0:EL0 execution of an ST64BV0 instruction is trapped to EL3, unless it is trapped to EL1 by SCTLR_EL1.EnAS0, or to EL2 by either HCRX_EL2.EnAS0 or SCTLR_EL2.EnAS0.

-------------------------------------------------------------
bit[ 36 : 36 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 35 : 35 ] is 0b0
Field Name: AMVOFFEN
Field Description: Activity Monitors Virtual Offsets Enable.
    
When FEAT_AMUv1p1 is implemented
0b0:Accesses to AMEVCNTVOFF0&lt;n&gt;_EL2 and AMEVCNTVOFF1&lt;n&gt;_EL2 at EL2 are trapped to EL3. Indirect reads of the virtual offset registers are zero.
        
-------------------------------------------------------------
bit[ 35 : 35 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 34 : 34 ] is 0b0
Field Name: TME
Field Description: Enables access to the TSTART, TCOMMIT, TTEST and TCANCEL instructions at EL0, EL1 and EL2.
    
When FEAT_TME is implemented
0b0:EL0, EL1 and EL2 accesses to TSTART, TCOMMIT, TTEST and TCANCEL instructions are UNDEFINED.
        
-------------------------------------------------------------
bit[ 34 : 34 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 33 : 30 ] is 0b0
Field Name: TWEDEL
Field Description: TWE Delay. A 4-bit unsigned number that, when SCR_EL3.TWEDEn is 1, encodes the minimum delay in taking a trap of WFE* caused by SCR_EL3.TWE as 2(TWEDEL + 8) cycles.
    
When FEAT_TWED is implemented
-------------------------------------------------------------
bit[ 33 : 30 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 29 : 29 ] is 0b0
Field Name: TWEDEn
Field Description: TWE Delay Enable. Enables a configurable delayed trap of the WFE* instruction caused by SCR_EL3.TWE.

When FEAT_TWED is implemented
0b0:The delay for taking the trap is IMPLEMENTATION DEFINED.
        
-------------------------------------------------------------
bit[ 29 : 29 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 28 : 28 ] is 0b0
Field Name: ECVEn
Field Description: ECV Enable. Enables access to the CNTPOFF_EL2 register.
    
When FEAT_ECV is implemented
0b0:EL2 accesses to CNTPOFF_EL2 are trapped to EL3, and the value of CNTPOFF_EL2 is treated as 0 for all purposes other than direct reads or writes to the register from EL3.
        
-------------------------------------------------------------
bit[ 28 : 28 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 27 : 27 ] is 0b0
Field Name: FGTEn
Field Description: Fine-Grained Traps Enable. When EL2 is implemented, enables the traps to EL2 controlled by HAFGRTR_EL2, HDFGRTR_EL2, HDFGWTR_EL2, HFGRTR_EL2, HFGITR_EL2, and HFGWTR_EL2, and controls access to those registers.

When FEAT_FGT is implemented
0b0:EL2 accesses to HAFGRTR_EL2, HDFGRTR_EL2, HDFGWTR_EL2, HFGRTR_EL2, HFGITR_EL2 and HFGWTR_EL2 registers are trapped to EL3, and the traps to EL2 controlled by those registers are disabled.
        
-------------------------------------------------------------
bit[ 27 : 27 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 26 : 26 ] is 0b0
Field Name: ATA
Field Description: Allocation Tag Access. Controls access to Allocation Tags, System registers for Memory tagging, and prevention of Tag checking, at EL2, EL1 and EL0.
    
When FEAT_MTE2 is implemented
0b0:Access to Allocation Tags is prevented at EL2, EL1, and EL0.

-------------------------------------------------------------
bit[ 26 : 26 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 25 : 25 ] is 0b0
Field Name: EnSCXT
Field Description: Enables access to the SCXTNUM_EL2, SCXTNUM_EL1, and SCXTNUM_EL0 registers.
    
When FEAT_CSV2_2 is implemented or FEAT_CSV2_1p2 is implemented
0b0:Accesses at EL0, EL1 and EL2 to SCXTNUM_EL0, SCXTNUM_EL1, or SCXTNUM_EL2 registers are trapped to EL3 if they are not trapped by a higher priority exception, and the values of these registers are treated as 0.
        
-------------------------------------------------------------
bit[ 25 : 25 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 24 : 22 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 21 : 21 ] is 0b0
Field Name: FIEN
Field Description: Fault Injection enable. Trap accesses to the registers ERXPFGCDN_EL1, ERXPFGCTL_EL1, and ERXPFGF_EL1 from EL1 and EL2 to EL3, reported using an ESR_ELx.EC value of 0x18.
    
When FEAT_RASv1p1 is implemented
0b0:Accesses to the specified registers from EL1 and EL2 generate a Trap exception to EL3.
        
-------------------------------------------------------------
bit[ 21 : 21 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 20 : 20 ] is 0b0
Field Name: NMEA
Field Description: Non-maskable External Aborts. Controls whether PSTATE.A masks SError exceptions at EL3.
    
When FEAT_DoubleFault is implemented
0b0:SError exceptions are not taken at EL3 if PSTATE.A == 1.
        
-------------------------------------------------------------
bit[ 20 : 20 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 19 : 19 ] is 0b0
Field Name: EASE
Field Description: External aborts to SError interrupt vector.
    
When FEAT_DoubleFault is implemented
0b0:Synchronous External abort exceptions taken to EL3 are taken to the appropriate synchronous exception vector offset from VBAR_EL3.
        
-------------------------------------------------------------
bit[ 19 : 19 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 18 : 18 ] is 0b0
Field Name: EEL2
Field Description: Secure EL2 Enable.
    
When FEAT_SEL2 is implemented
0b0:All behaviors associated with Secure EL2 are disabled. All registers, including timer registers, defined by  are UNDEFINED, and those timers are disabled.
        
-------------------------------------------------------------
bit[ 18 : 18 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 17 : 17 ] is 0b0
Field Name: API
Field Description: Controls the use of the following instructions related to Pointer Authentication. Traps are reported using an ESR_ELx.EC value of 0x09:

When FEAT_SEL2 is implemented and FEAT_PAuth is implemented
0b0:The use of any instruction related to pointer authentication in any Exception level except EL3 when the instructions are enabled are trapped to EL3 unless they are trapped to EL2 as a result of the HCR_EL2.API bit.
        
-------------------------------------------------------------
bit[ 17 : 17 ] is 0b0
Field Name: API
Field Description: Controls the use of instructions related to Pointer Authentication:

When FEAT_SEL2 is not implemented and FEAT_PAuth is implemented
0b0:The use of any instruction related to pointer authentication in any Exception level except EL3 when the instructions are enabled are trapped to EL3 unless they are trapped to EL2 as a result of the HCR_EL2.API bit.
        
-------------------------------------------------------------
bit[ 17 : 17 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 16 : 16 ] is 0b0
Field Name: APK
Field Description: Trap registers holding "key" values for Pointer Authentication. Traps accesses to the following registers, using an ESR_ELx.EC value of 0x18, from EL1 or EL2 to EL3 unless they are trapped to EL2 as a result of the HCR_EL2.APK bit or other traps:

When FEAT_PAuth is implemented
0b0:Access to the registers holding "key" values for pointer authentication from EL1 or EL2 are trapped to EL3 unless they are trapped to EL2 as a result of the HCR_EL2.APK bit or other traps.
        
-------------------------------------------------------------
bit[ 16 : 16 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 15 : 15 ] is 0b0
Field Name: TERR
Field Description: Trap accesses of error record registers. Enables a trap to EL3 on accesses of error record registers.
    
When FEAT_RAS is implemented
0b0:Accesses of the specified error record registers are not trapped by this mechanism.
        
-------------------------------------------------------------
bit[ 15 : 15 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 14 : 14 ] is 0b0
Field Name: TLOR
Field Description: Trap LOR registers. Traps accesses to the LORSA_EL1, LOREA_EL1, LORN_EL1, LORC_EL1, and LORID_EL1 registers from EL1 and EL2 to EL3, unless the access has been trapped to EL2.
    
When FEAT_LOR is implemented
0b0:This control does not cause any instructions to be trapped.
        
-------------------------------------------------------------
bit[ 14 : 14 ] is 0b0
Field Description: Reserved, RES0.
    
Otherwise
-------------------------------------------------------------
bit[ 13 : 13 ] is 0b0
Field Name: TWE
Field Description: Traps EL2, EL1, and EL0 execution of WFE instructions to EL3, from any Security state and both Execution states, reported using an ESR_ELx.EC value of 0x01.

0b0:This control does not cause any instructions to be trapped.
        
-------------------------------------------------------------
bit[ 12 : 12 ] is 0b0
Field Name: TWI
Field Description: Traps EL2, EL1, and EL0 execution of WFI instructions to EL3, from any Security state and both Execution states, reported using an ESR_ELx.EC value of 0x01.

0b0:This control does not cause any instructions to be trapped.
        
-------------------------------------------------------------
bit[ 11 : 11 ] is 0b0
Field Name: ST
Field Description: Traps Secure EL1 accesses to the Counter-timer Physical Secure timer registers to EL3, from AArch64 state only, reported using an ESR_ELx.EC value of 0x18.
    
0b0:Secure EL1 using AArch64 accesses to the CNTPS_TVAL_EL1, CNTPS_CTL_EL1, and CNTPS_CVAL_EL1 are trapped to EL3 when Secure EL2 is disabled. If Secure EL2 is enabled, the behavior is as if the value of this field was 0b1.
        
-------------------------------------------------------------
bit[ 10 : 10 ] is 0b1
Field Name: RW
Field Description: Execution state control for lower Exception levels.
    
When EL1 is capable of using AArch32 or EL2 is capable of using AArch32
0b1:The next lower level is AArch64.

-------------------------------------------------------------
bit[ 10 : 10 ] is 0b1
Field Description: Reserved, RAO/WI.
    
Otherwise
-------------------------------------------------------------
bit[ 9 : 9 ] is 0b1
Field Name: SIF
Field Description: Secure instruction fetch. When the PE is in Secure state, this bit disables instruction execution from memory marked in the first stage of translation as being Non-secure.
    
0b1:Secure state instruction execution from memory marked in the first stage of translation as being Non-secure is not permitted.
        
-------------------------------------------------------------
bit[ 8 : 8 ] is 0b1
Field Name: HCE
Field Description: Hypervisor Call instruction enable. Enables HVC instructions at EL3 and, if EL2 is enabled in the current Security state, at EL2 and EL1, in both Execution states, reported using an ESR_ELx.EC value of 0x00.
    
0b1:HVC instructions are enabled at EL3, EL2, and EL1.
        
-------------------------------------------------------------
bit[ 7 : 7 ] is 0b0
Field Name: SMD
Field Description: Secure Monitor Call disable. Disables SMC instructions at EL1 and above, from any Security state and both Execution states, reported using an ESR_ELx.EC value of 0x00.
    
0b0:SMC instructions are enabled at EL3, EL2 and EL1.
        
-------------------------------------------------------------
bit[ 6 : 6 ] is 0b0
Field Description: Reserved, RES0.
    
-------------------------------------------------------------
bit[ 5 : 4 ] is 0b11
Field Description: Reserved, RES1.
    
-------------------------------------------------------------
bit[ 3 : 3 ] is 0b1
Field Name: EA
Field Description: External Abort and SError interrupt routing.
    
0b1:When executing at any Exception level, External aborts and SError interrupts are taken to EL3.
        
-------------------------------------------------------------
bit[ 2 : 2 ] is 0b1
Field Name: FIQ
Field Description: Physical FIQ Routing.
    
0b1:When executing at any Exception level, physical FIQ interrupts are taken to EL3.
        
-------------------------------------------------------------
bit[ 1 : 1 ] is 0b0
Field Name: IRQ
Field Description: Physical IRQ Routing.
    
0b0:When executing at Exception levels below EL3, physical IRQ interrupts are not taken to EL3.

-------------------------------------------------------------
bit[ 0 : 0 ] is 0b1
Field Name: NS
Field Description: Non-secure bit. This field is used in combination with SCR_EL3.NSE to select the Security state of EL2 and lower Exception levels.
    
When FEAT_RME is implemented
-------------------------------------------------------------
bit[ 0 : 0 ] is 0b1
Field Name: NS
Field Description: Non-secure bit.
    
Otherwise
0b1:Indicates that Exception levels lower than EL3 are in Non-secure state, so memory accesses from those Exception levels cannot access Secure memory.

********************************************************
        

