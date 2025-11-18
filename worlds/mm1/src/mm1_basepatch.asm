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
!unlocked_weapons = $5D
!current_weapon = $5F
!megaman_hp = $6A
!bonus_balls = $AE
; !received_index = $C0
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


macro org(address,bank)
    if <bank> == $07
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
    JMP ForceGameOver
    NOP
ContinuePlayerControl:

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

%org($B72A, $06)
HijackStageSelect:
    JMP BlockStageSelect
    NOP

%org($B741, $06)
RerouteStage:
    JSR RerouteWily
    NOP

%org($BB39, $06)
RerouteWilyVisual3:
    JSR RerouteWily
    NOP

%org($C0F2, $07)
RerouteBonusBall:
    JSR SetStageClear
    NOP #2

%org($C125, $07)
RerouteStageClear:
    LDA !cleared_robot_master
    ORA $C148, X
    STA !cleared_robot_master

%org($C863, $07)
HookConsumableDrop:
    JMP Energylink

%org($C86B, $07)
Hook1Up:
    JMP ELLife
    NOP

%org($C875, $07)
HookMagnetBeam:
    ORA !magnet_beam_acquired
    STA !magnet_beam_acquired

%org($C918, $07)
HookBossKill:
    JSR SetBossRefight

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

assert realbase() <= $01AB00 ;


%org($FF00, $07)
BlockStageSelect:
    AND #$C0
    BEQ .Continue
    JMP $B72E
    .Continue:
    LDA $31
    CMP #$06
    BEQ .Apply
    TAX
    LDA !unlocked_robot_master
    AND $BFCC, X
    BNE .Apply
    JMP $B75E
    .Apply:
    JMP $B775

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
    LDA !controller_flip
    AND !CONTROLLER_SELECT_START
    JMP ContinuePlayerControl
    .GameOver:
    LDA #$FF
    STA $A6
    JSR $D495 ; fade to black
    LDA #$00
    STA $47
    STA $B4
    STA $55
    STA $94
    STA $95
    JMP $9038
    .Deathlink:
    LDA #$00
    STA !megaman_hp ; set HP to 0 so client can pick up on the death
    STA !deathlink
    JMP $C219

Energylink:
    TAX
    print "Energylink: ", hex(realbase())
    LDA #$00
    BEQ .ApplyNormal
    TXA
    STA !energylink_packet
    RTS
    .ApplyNormal:
    TXA
    STA $AD
    RTS

ELLife:
    LDA Energylink+2
    BEQ .ApplyNormal
    ; we kinda get free reign to put anything here
    LDA #$FE
    STA !energylink_packet
    LDA #$00
    JMP $C87F
    .ApplyNormal:
    LDA #$32
    CPX #$63
    BCS .RetFalse
    JMP $C86F
    .RetFalse:
    JMP $C87F

SetStageClear:
    JSR $C01B ; this first, so we're just adding a new subroutine to our check
    DEC !bonus_balls
    BNE .Return
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
    RTS

SetBossRefight:
    STA $06C1
    LDA !current_stage
    CMP #$07
    BEQ .Continue
    CMP #$09
    BNE .Return
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
assert realbase() <= $01FFE0 ;