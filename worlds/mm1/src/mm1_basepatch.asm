norom
!headersize = 16

!CONTROLLER_SELECT = #$04
!CONTROLLER_SELECT_START = #$0C
!CONTROLLER_ALL_BUTTON = #$0F

!WEAPON_MAGNET_BEAM = #$80
!WEAPON_GUTS_ELEC = #$70
!WEAPON_ALL = #$7F

!controller_mirror = $14
!controller_flip = $18
!current_stage = $31
!current_bank = $42
!unlocked_weapons = $5D
!current_weapon = $5F
!megaman_hp = $6A
!bonus_balls = $AE
!cleared_robot_master = $C1
!unlocked_robot_master = $C2
!deathlink = $C3
!energylink_packet = $C4
!magnet_beam_acquired = $C5
!last_wily = $C6
!cleared_stages = $C7 ; $C8
!play_sfx = $C9
!rbm_strobe = $CA ; unsure on feasibility here, but better to reserve early
!boss_refights = $CB 
; !received_index = $CC
!jmp_bank = $CD
!jmp_target = $00CE
;!jmp_target+1 = $CF
!last_bank = $D0
!return_target = $00D1
;!return_target+1 = $D2
!jmp_table_ind = $D3

!PpuControl_2000 = $2000
!PpuMask_2001 = $2001
!PpuAddr_2006 = $2006
!PpuData_2007 = $2007

macro org(address,bank)
    if <bank> == $0F
        org <address>-$C000+($4000*<bank>)+!headersize ; org sets the position in the output file to write to (in norom, at least)
        base <address> ; base sets the position that all labels are relative to - this is necessary so labels will still start from $8000, instead of $0000 or somewhere
    else
        org <address>-$8000+($4000*<bank>)+!headersize
        base <address>
    endif
endmacro

%org($906C, $05)
HookStageLoad:
    JMP SetLastWily
    NOP
StageWilyReturn:

%org($9075, $05)
StageNormalReturn:

%org($9165, $05)
HookPlayerControl:
    JMP ForceGameOverJump
    NOP
ContinuePlayerControl:

%org($A7AF, $05)
HookHyperBomb:
    JMP HyperBombJump
    NOP

%org($A82F, $05)
HookSuperArm:
    JMP SuperArmJump
    NOP

%org($A889, $05)
SuperArmGraphics:
db $6C, $6C, $6C

%org($B552, $06)
CatchRefreshStandard:
    JMP RBMRefreshEarlyHook

%org($B5B8, $06)
RerouteRBMVisual:
    LDA !unlocked_robot_master

%org($B5E8, $06)
ReverseRBMVisual:
    BNE ReverseBranchTarget

%org($B5EE, $06)
ReverseBranchTarget:

%org($B63C, $06)
RerouteWilyVisual:
    JSR RerouteWily
    NOP

%org($B6AE, $06)
HookRBMTiles:
    JMP RBMRefreshHook
    NOP

%org($B665, $06)
RerouteWilyVisual2:
    JSR RerouteWily
    NOP

%org($B69B, $06)
RerouteGutsCheck:
    LDA !unlocked_robot_master
    AND #$08
    BNE GutsCheckTarget

%org($B6AE, $06)
GutsCheckTarget:

%org($B724, $06)
HookStageSelectLoop:
    JMP StageSelectLoopHook

%org($B72A, $06)
HijackStageSelect:
    JMP BlockStageSelectJump
    NOP

%org($B741, $06)
RerouteStage:
    JSR RerouteWily
    NOP

%org($BB39, $06)
RerouteWilyVisual3:
    JSR RerouteWily
    NOP

%org($C0E3, $0F)
RerouteBonusBall:
    JMP SetStageClearJump
    NOP

%org($C125, $0F)
RerouteStageClear:
    LDA !cleared_robot_master
    ORA $C148, X
    STA !cleared_robot_master

%org($C847, $0F)
ConsumableFunc:
    JMP ConsumableCheckJump

%org($C863, $0F)
HookConsumableDrop:
    JMP EnergylinkJump

%org($C86B, $0F)
Hook1Up:
    JMP ELLifeJump
    NOP

%org($C875, $0F)
HookMagnetBeam:
    ORA !magnet_beam_acquired
    STA !magnet_beam_acquired

%org($C918, $0F)
HookBossKill:
    JSR SetBossRefightJump

; free space hooks

%org($BF80, $05)
SetLastWily:
    CPX #$06
    BCC .ReturnNormal
    BNE .ReturnWily
    PHA
    LDX !last_wily
    BEQ .ReturnWilyRead
    LDA !controller_mirror
    AND !CONTROLLER_SELECT
    BNE .ReturnWilyRead
    PLA
    STX !current_stage
    SEC
    BCS .ReturnWily
    .ReturnWilyRead:
    PLA
    LDX !current_stage
    .ReturnWily:
    JMP StageWilyReturn
    .ReturnNormal:
    JMP StageNormalReturn

assert realbase() <= $018000 ;

%org($AA80, $06)
RerouteWily:
    TYA
    PHA
    TXA
    PHA
    LDA !unlocked_weapons
    TAY
    AND !WEAPON_MAGNET_BEAM
    BEQ .False
    TYA
    AND !WEAPON_GUTS_ELEC
    BEQ .False
    TYA
    AND !WEAPON_ALL
    TAY
    LDX #$00
    .Loop:
    TYA
    AND #$01
    BEQ .Not
    INX
    .Not:
    TYA
    LSR A
    TAY
    CMP #$00
    BNE .Loop
    TXA
    print "Wily Requirement: ", hex(realbase())
    CMP #$06
    BCC .False
    PLA
    TAX
    PLA
    TAY
    LDA #$7E
    RTS
    .False:
    PLA
    TAX
    PLA
    TAY
    LDA #$00
    RTS

StageSelectLoopHook:
    LDA !rbm_strobe
    BEQ .Continue
    ;// beware ye who enter here
    LDA !PpuMask_2001
    AND #$E7
    STA !PpuMask_2001
    JMP $B59C
    .ReturnFrom:
    LDA !PpuMask_2001
    ORA #$18
    STA !PpuMask_2001
    LDA #$00
    STA !rbm_strobe
    .Continue:
    LDA $18
    AND #$C8
    BEQ .ReturnFalse
    JMP $B72A
    .ReturnFalse:
    JMP $B75E

RBMRefreshHook:
    ;// this one is done differently than usual
    ;// we hook to return rather than to start
    LDA !rbm_strobe
    BNE .ReturnTrue
    ;// false code path, a real load
    LDY #$00
    LDX #$40
    JMP HookRBMTiles+3
    .ReturnTrue:
    JMP StageSelectLoopHook_ReturnFrom

RBMRefreshEarlyHook:
    ;// this one checks early if we're in a real code path
    ;// and just removes strobe
    ;// don't have to load A, already primed to 0
    STA !rbm_strobe
    STA !PpuAddr_2006
    JMP $B555
print hex(realbase())
assert realbase() <= $01AB10 ;

%org($8000, $07)

JumpToFunction:
    PHA
    TXA
    PHA
    LDA !jmp_table_ind
    ASL
    TAX
    LDA JumpTable, X
    STA !jmp_target
    LDA JumpTable+1, X
    STA !jmp_target+1
    PLA
    TAX
    PLA
    JMP (!jmp_target)

JumpTable:
    dw Energylink, ELLife, SetStageClear, SetBossRefight, BlockStageSelect, ForceGameOver, ConsumableCheck, SuperArm, HyperBomb

Energylink:
    print "Energylink: ", hex(realbase())
    LDX #$00
    BEQ .ApplyNormal
    STA !energylink_packet
    .ApplyNormal:
    STA $AD
    RTS

ELLife:
    LDA Energylink+2
    BEQ .ApplyNormal
    ; we kinda get free reign to put anything here
    LDA #$32
    STA !energylink_packet
    .ApplyNormal:
    CPX #$63
    BCS .RetFalse
    JMP $C86F
    .RetFalse:
    RTS

SetStageClear:
    LDX #$00
    LDA !current_stage
    CMP #$08
    BCC .SkipInc
    INX
    SEC
    SBC #$08
    .SkipInc:
    TAY
    INY
    LDA #$00
    SEC
    .Loop:
    ROL
    DEY
    BNE .Loop
    .Set:
    ORA !cleared_stages, X
    STA !cleared_stages, X
    LDA !current_stage
    CMP #$06
    BCC .Return
    STA !last_wily
    .Return:
    LDA $AE
    PHA
    BEQ .ReturnFalse
    LDA #$E7
    STA !return_target
    LDA #$C0
    STA !return_target+1
    PLA
    RTS
    .ReturnFalse:
    LDA #$F9
    STA !return_target
    LDA #$C0
    STA !return_target+1
    PLA
    RTS


SetBossRefight:
    STA $06C1
    LDA !current_stage
    CMP #$07
    BCC .Return
    .Continue:
    LDY $AC
    CPY #$06
    BCS .Return
    INY
    LDA #$00
    SEC
    .Loop:
    ROL
    DEY
    BNE .Loop
    ORA !boss_refights
    STA !boss_refights
    .Return:
    RTS

BlockStageSelect:
    PHA
    AND #$C0
    BEQ .Continue
    LDA #$2E
    BNE .Return
    .Continue:
    LDA $31
    CMP #$06
    BEQ .Apply
    TAX
    LDA !unlocked_robot_master
    AND RobotMasters, X
    BNE .Apply
    LDA #$5E
    BNE .Return
    .Apply:
    LDA #$75
    .Return:
    STA !return_target
    LDA #$B7
    STA !return_target+1
    PLA
    RTS

RobotMasters:
    db $20, $10, $02, $40, $04, $08

ForceGameOver:
    LDA !deathlink
    BNE .Deathlink
    LDA !play_sfx
    BEQ .CheckController
    JSR $C477
    LDA #$00
    STA !play_sfx
    .CheckController:
    LDA !controller_mirror
    AND !CONTROLLER_SELECT_START
    CMP !CONTROLLER_SELECT_START
    BEQ .GameOver
    LDA.b #ContinuePlayerControl>>8
    STA !return_target+1
    LDA.b #ContinuePlayerControl
    STA !return_target
    LDA !controller_flip
    AND !CONTROLLER_SELECT_START
    RTS
    .GameOver:
    LDA #$FF
    STA $A6
    JSR $D495 ; fade to black
    LDA #$38
    STA !return_target
    LDA #$90
    STA !return_target+1
    LDA #$00
    STA $47
    STA $B4
    STA $55
    STA $94
    STA $95
    RTS
    .Deathlink:
    LDA #$19
    STA !return_target
    LDA #$C2
    STA !return_target+1
    LDA #$00
    STA !megaman_hp ; set HP to 0 so client can pick up on the death
    STA !deathlink
    RTS

ConsumableCheck:
    CPY #$12
    BEQ .QuickCheck
    CPY #$0C
    BCS .QuickJump
    .QuickCheck:
    LDY $0640, X
    BEQ .Check
    .QuickJump:
    ; $0004 is already populated with the return value, so just copy it
    PHA
    LDA $0004
    STA !return_target
    LDA $0005
    STA !return_target+1
    PLA
    RTS
    .Check:
    TYA
    PHA
    LDY #$00
    .Loop:
    LDA $07E0, Y
    BEQ .Set
    INY
    INY
    INY
    CPY #$1E
    BCC .Loop
    LDY #$00 ; if we've managed to run 5 consumables in a row and the client hasn't cleared any of them, there's nothing we can do but overwrite the oldest.
    .Set:
    LDA $0460, X
    STA $07E0, Y
    LDA $0480, X
    STA $07E1, Y
    LDA !current_stage
    STA $07E2, Y
    PLA
    TAY
    RTS

SuperArm:
    CPY #$FF
    BNE .ReturnNormal ; we need to actually remove a super arm block, thus can trust everything in the state
    print "Enhanced Super Arm: ", hex(realbase())
    LDA #$00
    BEQ .ReturnFalse
    ; now we semi-copy the normal codepath but skip the removal
    LDA !current_weapon
    ORA #$80
    STA $60
    LDA #$00
    STA $61
    LDA #$04
    STA $0721, Y
    JSR $F76A
    ; skipped function would go here
    LDA #$F8
    STA $0605
    LDA #$02
    LDX #$05
    RTS ; we have to do the rest in bank F, since we need to JSR into the original bank
    .ReturnNormal:
    LDA #$33
    STA !return_target
    LDA #$A8
    STA !return_target+1
    RTS
    .ReturnFalse:
    LDA #$5D
    STA !return_target
    LDA #$A8
    STA !return_target+1
    RTS

HyperBomb:
    LDA $60
    BEQ .ReturnStart
    ; bomb is active, do we have enhanced enabled?
    print "Enhanced Hyper Bomb: ", hex(realbase())
    LDA #$00
    BEQ .ReturnFalse
    ; bug? this is immediately called again after spawning the bomb, before a single frame can pass
    ; just check that a frame has passed
    LDA $61
    BEQ .ReturnFalse
    CMP #$8F
    BCS .ReturnFalse
    LDA !controller_flip
    AND #$02
    BEQ .ReturnFalse
    LDA #$90
    ; this should make it so the bomb has about ~16 frames before explosion
    STA $61
    .ReturnFalse:
    LDA #$CA
    STA !return_target
    LDA #$A7
    STA !return_target+1
    RTS
    .ReturnStart:
    LDA #$B3
    STA !return_target
    LDA #$A7
    STA !return_target+1
    RTS

%org($C000, $0F)
BankTable:

%org($C007, $0F)
db $0F ;// should never be called, but just in case

%org($FF00, $0F)
ExpandedBankTable:
db $00, $01, $02, $03, $04, $05, $06, $07, $08, $09, $0A, $0B, $0C, $0D, $0E, $0F
SafeCall:
    ; call as subroutine
    ; assume jmp_target and jmp_bank is preset
    PHA
    TXA
    PHA
    LDA !current_bank
    STA !last_bank
    LDA !jmp_bank
    STA !current_bank
    TAX
    STA ExpandedBankTable, X
    PLA
    TAX
    PLA
    JSR JumpToFunction
    PHA
    LDA !last_bank
    STA !current_bank
    TAX
    STA ExpandedBankTable, X
    PLA
    RTS

SafeCallWithReturn:
    ; call as direct jump
    ; function has to set the return addr and rts to come back here
    ; use in cases where a direct jump out of the function is needed
    JSR SafeCall
    JMP (!return_target)

SafeCallOut:
    ; call as 

EnergylinkJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$00
    STA !jmp_table_ind
    PLA
    JMP SafeCall

ELLifeJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$01
    STA !jmp_table_ind
    PLA
    JMP SafeCall

SetStageClearJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$02
    STA !jmp_table_ind
    PLA
    JMP SafeCallWithReturn

SetBossRefightJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$03
    STA !jmp_table_ind
    PLA
    JMP SafeCall

BlockStageSelectJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$04
    STA !jmp_table_ind
    PLA
    JMP SafeCallWithReturn

ForceGameOverJump:
    PHA
    LDA #$07
    STA !jmp_bank
    LDA #$05
    STA !jmp_table_ind
    PLA
    JMP SafeCallWithReturn

ConsumableCheckJump:
    ; the val in A is useless here, but we're gonna have to manually prep the return address here
    LDA #$00
    STA !return_target
    STA !return_target+1
    LDA #$07
    STA !jmp_bank
    LDA #$06
    STA !jmp_table_ind
    JSR SafeCall
    ; if return_target is populated, we need to skip to it
    LDA !return_target
    BEQ .Return
    JMP (!return_target)
    .Return:
    ; else we have to follow through the return address ourself
    RTS

SuperArmJump:
    ; we're gonna have to manually prep the return address here
    PHA
    LDA #$00
    STA !return_target
    STA !return_target+1
    LDA #$07
    STA !jmp_bank
    LDA #$07
    STA !jmp_table_ind
    PLA
    JSR SafeCall
    ; if return_target is populated, we need to skip to it
    LDA !return_target
    BEQ .Return
    JMP (!return_target)
    .Return:
    ; else we have to follow through the return address ourself
    ; also finish the last steps here
    JSR $A913
    LDY !current_stage
    LDA $A888, Y
    STA $0400, X
    RTS

HyperBombJump:
    ; much simpler thankfully
    LDA #$07
    STA !jmp_bank
    LDA #$08
    STA !jmp_table_ind
    JMP SafeCallWithReturn


print hex(realbase())
assert realbase() <= $03FFEC ;