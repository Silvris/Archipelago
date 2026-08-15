norom
!headersize = 16

!controller_flip = $14 ; only on first frame of input, used by crash man, etc
!controller_mirror = $16
!vram_toggle = $19
!current_stage = $22
!mega_man_state = $30
!current_weapon = $A0
!completed_rbm_stages = $A9
!completed_cossack_stages = $AA
; !deathlink = $30, set to $0E
!bank_1_read = $F3
!bank_2_read = $F4
!bank_1_write = $F5
!bank_2_write = $F6
!vram_buffer = $0780
!received_items = $6000
!received_rbm_stages = $6001
!received_cossack_stages = $6002
!current_cossack_wily = $6003
!rbm_strobe = $6004
!sound_effect_strobe = $6005
!returning_latch = $6006
!energylink_health = $6007
!energylink_weapon = $6008
!energylink_lives = $6009
!bank_store = $600A
!received_charge_buster = $600B

!sent_items = $6064 ; this one is done really weird frankly, but this has it hit at $60B0, which is the actual weapons array
!sent_weapons = $60B0 ; this is equivalent to the above, but only used by weapons and not wire/balloon

!CONTROLLER_START = #$10
!CONTROLLER_SELECT = #$20
!CONTROLLER_SELECT_START = #$30
!CONTROLLER_ALL_BUTTON = #$F0

!PpuControl_2000 = $2000
!PpuMask_2001 = $2001
!PpuStatus_2002 = $2002
!PpuAddr_2006 = $2006
!PpuData_2007 = $2007

macro org(address,bank)
    if <bank> == $3E
        org <address>-$C000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
        base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
    else 
      if <bank> == $3F
          org <address>-$E000+($2000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
          base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
      else
        if <address> >= $A000
          org <address>-$A000+($2000*<bank>)+!headersize
          base <address>
        else
          org <address>-$8000+($2000*<bank>)+!headersize
          base <address>
        endif
      endif
    endif
endmacro

org 6
; We need to edit the NES 2.0 header here too
db $40, $08, $00, $00, $07, $07, $00, $00, $00, $01

%org($80BD, $39)
    JMP     StageSelectLoopHook

%org($80D8, $39)
    JMP     CheckStageAccess

%org($80E1, $39)
    JMP     CheckCossackWily
    NOP

%org($80FE, $39)
    JMP     CheckWilyStage
    NOP

%org($81F3, $39)
    JMP     RemapCossackStage
    NOP

%org($8305, $39)
    BEQ     RemoveCossack ; forces unreachable code here, we don't want to trigger the cossack sequence

%org($833B, $39)
RemoveCossack:

%org($8457, $39)
    JMP     RemapWilyStage2
    NOP

%org($846C, $39)
    JMP     RemapWilyStage

%org($8525, $39)
    JMP     InvertRBMSprites
    NOP

%org($86C2, $39)
    JMP     RemapCossackStage2
    NOP

%org($8C85, $39)
    JMP     ReturnToStageSelect
    NOP

%org($8CAB, $39)
    JMP     ReturnCossackToStageSelect
    NOP

%org($8D77, $39)
    JMP     RemapWeaponReceive
    NOP

%org($8DC5, $39)
    JMP     RemapRushReceive
    NOP

%org($9C86, $39)
CheckStageAccess:
    LDA     $8870, Y
    CMP     #$08
    BPL     .ReturnSkip
    BEQ     .ReturnSkip
    PHA
    TAX
    LDA     #$01
    .Loop:
    CPX     #$00
    BEQ     .Continue
    ASL
    DEX
    CLC
    BCC     .Loop
    .Continue:
    AND     !received_rbm_stages
    CMP     #$00
    BNE     .ReturnSkipWithPull
    PLA
    JMP     $80C0
    .ReturnSkipWithPull:
    PLA
    .ReturnSkip:
    JMP     $80DB

RemapWeaponReceive:
    LDA     #$01
    STA     !sent_weapons, X
    JMP     $8D7B

RemapRushReceive:
    LDA     #$01
    STA     !sent_weapons, X
    JMP     $8DC9

StageSelectLoopHook:
    LDA     !controller_flip
    AND     !CONTROLLER_SELECT
    BEQ     .SoundEffects
    LDA     !current_cossack_wily
    CLC
    ADC     #$01
    CMP     #$08
    BNE     .SetCurrent
    LDA     #$00
    .SetCurrent:
    STA     !current_cossack_wily
    LDA     #$2E
    STA     !sound_effect_strobe
    LDY     #$00
    LDA     #$22
    STA     !vram_buffer, Y
    INY
    LDA     #$2F
    STA     !vram_buffer, Y
    INY
    LDA     #$01
    STA     !vram_buffer, Y
    INY
    LDA     !current_cossack_wily
    CMP     #$04
    BMI     .Cossack
    LDA     #$96
    JMP     .SetDisplay
    .Cossack:
    LDA     #$82
    .SetDisplay:
    STA     !vram_buffer, Y
    INY
    LDA     !current_cossack_wily
    CMP     #$04
    BMI     .SetValue
    SEC
    SBC     #$04
    .SetValue:
    CLC
    ADC     #$F0
    STA     !vram_buffer, Y
    INY
    LDA     #$FF
    STA     !vram_buffer, Y
    LDA     #$01
    STA     !vram_toggle
    .SoundEffects:
    LDA     !sound_effect_strobe
    BEQ     .RbmStrobe
    JSR     $F6BE
    LDA     #$00
    STA     !sound_effect_strobe
    .RbmStrobe:
    JSR     $8237
    LDA     !rbm_strobe
    BEQ     .Return
    LDA     #$97
    STA     $0200
    LDA     #$00
    STA     !rbm_strobe
    LDA     #$02
    STA     $10
    LDA     #$00
    STA     $2A
    JSR     $8495
    .Return:
    JMP     $80C0

CheckWilyStage:
    LDA     !current_cossack_wily
    CMP     #$04
    JMP     $8102

InvertRBMSprites:
    LDA     !received_rbm_stages
    EOR     #$FF
    STA     $02
    JMP     $8529

CheckCossackWily:
    LDA     !current_cossack_wily
    CMP     #$04
    BEQ     .Wily1
    BMI     .Cossack
    ; we are trying to access wily 2/3/4, just check their previous flag
    TAX     
    DEX
    LDA     #$01
    .WilyLoop:
    CPX     #$00
    BEQ     .WilyContinue
    ASL
    DEX
    CLC
    BCC     .WilyLoop
    .WilyContinue:
    BIT     !completed_cossack_stages
    BEQ     .ReturnFalse
    BNE     .ReturnTrue
    .Wily1:
    LDA     !completed_cossack_stages
    AND     #$0F
    CMP     #$0F
    BEQ     .ReturnTrue
    BNE     .ReturnFalse
    .Cossack:
    TAX
    LDA     #$01
    .CossackLoop:
    CPX     #$00
    BEQ     .CossackContinue
    ASL
    DEX
    CLC
    BCC     .CossackLoop
    .CossackContinue:
    BIT     !received_cossack_stages
    BNE     .ReturnTrue
    BEQ     .ReturnFalse
    .ReturnTrue:
    LDA     #$FF
    BNE     .Return
    .ReturnFalse:
    LDA     #$2D
    STA     !sound_effect_strobe
    LDA     #$00
    .Return:
    CMP     #$FF
    JMP     $80E5

RemapCossackStage:
    LDX     !current_cossack_wily
    LDA     #$01
    .Loop:
    CPX     #$00
    BEQ     .Continue
    ASL
    CLC
    ADC     #$01
    DEX
    CLC
    BCC     .Loop
    .Continue:
    LSR
    STA     $03
    JMP     $81F7

RemapCossackStage2:
    LDY     #$00
    LDX     !current_cossack_wily
    LDA     #$01
    .Loop:
    CPX     #$00
    BEQ     .Continue
    ASL
    CLC
    ADC     #$01
    DEX
    CLC
    BCC     .Loop
    .Continue:
    LSR
    JMP     $86C6

RemapWilyStage:
    LDX     !current_cossack_wily
    DEX
    LDA     #$01
    .Loop:
    CPX     #$00
    BEQ     .Continue
    ASL
    CLC
    ADC     #$01
    DEX
    CLC
    BCC     .Loop
    .Continue:
    LSR
    JMP     $846F

RemapWilyStage2:
    LDX     !current_cossack_wily
    DEX
    LDA     #$01
    .Loop:
    CPX     #$00
    BEQ     .Continue
    ASL
    CLC
    ADC     #$01
    DEX
    CLC
    BCC     .Loop
    .Continue:
    CMP     #$7F
    JMP     $845B

ReturnCossackToStageSelect:
    LDA     !current_stage
    CMP     #$0C
    BCS     .ReturnTrue
    JMP     $8E78
    .ReturnTrue:
    LDA     !current_cossack_wily
    CLC
    ADC     #$01
    STA     !current_cossack_wily
    LDA     !completed_cossack_stages
    CMP     #$0F
    JMP     $8CAF

ReturnToStageSelect:
    LDA     !returning_latch
    BEQ     .ReturnNormal
    LDA     #$00
    STA     !returning_latch
    JMP     $8E78
    .ReturnNormal:
    LDY     !current_stage
    CPY     #$08
    JMP     $8C89

assert realbase() <= $074010 ;

%org($814E, $3A)
    JMP     FlashStopperCheck

%org($BBF6, $3B)
    JMP     EnergylinkOneUp
    NOP

%org($BC15, $3B)
    JMP     EnergylinkBuster
    NOP

%org($BC19, $3B)
    JMP     EnergylinkEnergy

%org($BC66, $3B)
    LDA     #$01
    STA     !sent_items, Y

%org($BCB2, $3B)
EnergylinkEnergy:
    print "Energylink: ", hex(realbase())
    LDA     #$00
    BEQ     .Normal
    LDA     $BC87, Y ; this gets the send amount
    CPX     #$00
    BEQ     .Health
    STA     !energylink_weapon
    LDA     #$00
    BEQ     .Set
    .Health:
    STA     !energylink_health
    LDA     #$00
    .Set:
    JMP     $BC3B
    .Normal:
    LDA     $BC87, Y
    JMP     $BC1C

EnergylinkBuster:
    ; called if you pick up weapon energy with Buster equipped
    LDX     EnergylinkEnergy+1
    BEQ     .Normal
    LDA     $BC87, Y
    STA     !energylink_weapon
    .Normal:
    LDA     !current_weapon
    BEQ     .False
    .Return:
    JMP     $BC19
    .False:
    JMP     $BC3B


EnergylinkOneUp:
    LDA     EnergylinkEnergy+1
    BEQ     .Normal
    LDA     #$01
    STA     !energylink_lives
    JMP     $BC41
    .Normal:
    LDA     $A1
    CMP     #$09
    JMP     $BBFA

%org($8B07, $3C)
    JMP     Wily3Requirement
    NOP

%org($8CB7, $3C)
    JMP     MarkComplete
    NOP

%org($8D39, $3C)
    JMP     JammedBuster

%org($993F, $3C)
    JMP     WeaponSoftlock
    NOP

%org($9970, $3C)
    ;JMP     WeaponSoftlock
    ;NOP

%org($BD9A, $3D)
Wily3Requirement:
    LDY     #$00
    LDA     $AC
    .Loop:
    PHA
    AND     #$01
    BEQ     .Skip
    INY
    .Skip:
    PLA
    LSR
    CMP     #$00
    BNE     .Loop
    .Check:
    CPY     RealWily3Req+1
    BMI     .False
    LDA     #$FF
    BNE     .Return
    .False:
    LDA     #$00
    .Return:
    CMP     #$FF
    JMP     $8B0B

JammedBuster:
    print   "Jammed Buster: ", hex(realbase())
    LDA     #$00
    BEQ     .Inc
    LDA     !received_charge_buster
    BEQ     .Return
    .Inc:
    INY
    .Return:
    STY     $35
    JMP     $8D3C

MarkComplete:
    LDA     #$80
    ORA     !completed_cossack_stages
    STA     !completed_cossack_stages
    LDA     #$D0
    STA     $0528
    RTS

%org($C53D, $3E)
    NOP     ; don't grant Rush Coil on startup
    NOP
    NOP
    NOP

%org($C70D, $3E)
    JMP     MegaManInputHook
    NOP

%org($D66D, $3E)
    JMP     Wily3Requirement2
    NOP

%org($E814, $3F)
MegaManInputHook:
    LDA     !controller_mirror
    AND     !CONTROLLER_ALL_BUTTON
    CMP     !CONTROLLER_ALL_BUTTON
    BNE     .SoundEffects
    LDA     #$08
    STA     !mega_man_state
    LDA     #$01
    STA     !returning_latch
    JMP     $C740
    .SoundEffects:
    LDA     !sound_effect_strobe
    BEQ     .Return
    JSR     $F6BE
    LDA     #$00
    STA     !sound_effect_strobe
    .Return:
    LDA     !controller_flip
    AND     !CONTROLLER_START
    JMP     $C711

FlashStopperCheck:
    LDA     !current_weapon
    CMP     #$0C ; Flash Stopper
    BNE     .Normal
    ; Flash Stopper info is in bank 2C, while we load 20 for Mega Buster
    LDA     !bank_2_read
    STA     !bank_store
    LDA     #$2C
    STA     !bank_2_write
    JSR     ChangeBanks
    LDA     $B700, Y
    PHA
    LDA     !bank_store
    STA     !bank_2_write
    JSR     ChangeBanks
    PLA
    CMP     #$00
    BEQ     .Set
    LDA     #$01
    BNE     .Set
    .Normal:
    LDA     $B700, Y
    .Set:
    STA     $12
    .Return:
    JMP     $8153

Wily3Requirement2:
    PHA
    LDY     #$00
    LDA     $AC
    .Loop:
    PHA
    AND     #$01
    BEQ     .Skip
    INY
    .Skip:
    PLA
    LSR
    CMP     #$00
    BNE     .Loop
    RealWily3Req:
    print "Wily 3 Requirement:", hex(realbase())
    CPY     #$08
    BMI     .False
    LDY     #$FF
    BNE     .Return
    .False:
    LDY     $AC
    .Return:
    PLA
    CPY     #$FF
    JMP     $D671
    
WeaponSoftlock:
    AND     #$08
    STA     $00
    PHA     
    TYA 
    PHA
    ORA     #$07
    TAY
    DEY
    .Loop
    LDX     $9B71, Y
    LDA     $B0, X
    BNE     .ContinueTrue
    DEY
    CPY     $00
    BNE     .Loop
    ; we're in the false case, jump out to a safe spot
    LDA     #$00
    STA     $0138
    PLA
    TAY
    PLA
    JMP     $9992
    .ContinueTrue:
    ; true case, pull and return
    PLA
    TAY
    PLA
    JMP     $9943

%org($EF00, $3F)
db "MM4_ARCHIPELAGO_BASE", $00
db $00 ; deathlink
db $FF, $FF, $FF ; world version

assert realbase() <= $07EFFF ;

%org($FDE7, $3F)
EnableSaveRam:
    STA     $93
    LDA     #$80
    STA     $A001
    LDA     #$00
    JMP     $FE9E


%org($FE9A, $3F)
    JMP     EnableSaveRam
    NOP

%org($FF37, $3F)
ChangeBanks:
; write target banks into bank_1_write and bank_2_write

