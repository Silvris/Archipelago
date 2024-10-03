;norom
;org $5FFFFF
;    db $FF

;org $407FC0 ; copy header
;    dd read4($7FC0)
;    dd read4($7FC4)
;    dd read4($7FC8)
;    dd read4($7FCC)
;    dd read4($7FD0)
;    dd read4($7FD4)
;    dd read4($7FD8)
;    dd read4($7FDC)
;    dd read4($7FE0)
;    dd read4($7FE4)
;    dd read4($7FE8)
;    dd read4($7FEC)
;    dd read4($7FF0)
;    dd read4($7FF4)
;    dd read4($7FF8)
;    dd read4($7FFC)

;org $7FD7
;db $0D ; 33Mbit~64Mbit
;org $407FD7
;db $0D ; 33MBit~64Mbit

sa1rom

; SNES hardware registers
!VMADDL = $002116
!VMDATAL = $002118
!MDMAEN = $00420B
!DMAP0 = $004300
!BBAD0 = $004301
!A1T0L = $004302
!A1B0 = $004304
!DAS0L = $004305

; Menu select bitflag
; This is not initially a bitflag, we are converting it
; b00000001 - Spring Breeze
; b00000010 - Dyna Blade
; b00000100 - Gourmet Race
; b00001000 - The Great Cave Offensive
; b00010000 - Revenge of Meta Knight
; b00100000 - Milky Way Wishes
; b01000000 - The Arena
; b10000000 - Sound Test (use as completion flag?)
!spring_breeze = #$0000
!dyna_blade = #$0001
!gourmet_race = #$0002
!great_cave_offensive = #$0003
!revenge_of_meta_knight = #$0004
!milky_way_wishes = #$0005
!the_arena = #$0006
!sound_test = #$0007
!samurai_kirby = #$0008
!megaton_punch = #$0009
!stereo = #$000A
!no_sub_game = #$00FF

; Menu Directions
!up = #$0000
!right = #$0001
!down = #$0002
!left = #$0003

; Game variables
!received_sub_games = $7A85
!current_selected_sub_game = $7A91
!completed_sub_games = $7A93
!great_cave_treasures = $7B05
!great_cave_gold = $7B0F
!received_copy_abilities = $7B1D ; Milky Way Wishes Deluxe Copy Essence, 3-bytes
!rainbow_hearts = $7A6B

; AP save variables
!ap_sub_games = $408000
!received_items = $408002
!received_planets = $408004


org $008C29
    JSL WriteBWRAM
    NOP
    NOP

org $00C46F
hook_set_star_complete:
    JSL set_treasure

org $00FFC0
    db "KSS__BASEPATCH_ARCHI"

org $00FFD8
    db $06

org $02A34B
    JML hook_copy_ability
    NOP

org $CAA6F8
    JML block_mww_planets
    NOP 

org $CAB682
handle_menu_remap:
    LDA #$0000
    CLC
    ADC $00
    TAY
    LDA !current_selected_sub_game
    ASL
    TAX
    LDA.l remap_table, X
    STA $14
    LDA #$00CA
    STA $16
    JML [$3714]
    menu_return:
    NOP

org $CAB86E
    PHX
    print "Starting Stage: ", hex(snestopc(realbase()))
    LDA #$0001
    PHA
    ORA !ap_sub_games
    STA !received_sub_games
    PLA
    LDX #$0000
    .Loop:
    BIT #$0001
    BNE .Break
    INX
    LSR
    BRA .Loop
    .Break:
    STX $7A91
    STX $7A87
    PLX
    RTL
    NOP #19

org $CAB8AA
    LDA #$0005

org $CAF830
remap_table:
    dw remap_spring_breeze
    dw remap_dyna_blade
    dw remap_gourmet_race
    dw remap_great_cave
    dw remap_meta_knight
    dw remap_milky_way_wishes
    dw remap_arena
    dw remap_sound_test
    dw remap_samurai
    dw remap_megaton
    dw remap_stereo

check_level_access:
    PHA
    PHX
    TAX
    LDA #$0001
    .Loop:
    CPX #$0000
    BEQ .Test
    ASL
    DEX
    BRA .Loop
    .Test:
    AND !received_sub_games
    BNE .ReturnTrue
    CLC
    BRA .Return
    .ReturnTrue:
    SEC
    .Return:
    PLX
    PLA
    RTS

remap_spring_breeze:
    CPY !left
    BEQ .ReturnFalse
    CPY !up
    BEQ .ReturnFalse
    CPY !right
    BEQ .Right
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Right:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_dyna_blade:
    CPY !left
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !down
    BEQ .Down
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Down:
    LDA !stereo
    BRA .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_gourmet_race:
    CPY !up
    BEQ .ReturnFalse
    CPY !left
    BEQ .Left
    CPY !down
    BEQ .Down
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Down:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Left:
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

remap_great_cave:
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    CPY !left
    BEQ .Left
    ; Down
    LDA !stereo
    BRA .Return
    .Up:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Right:
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Left:
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_meta_knight:
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    CPY !left
    BEQ .Left
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Right:
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Left:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_milky_way_wishes:
    CPY !up
    BEQ .ReturnFalse
    CPY !right
    BEQ .ReturnFalse
    CPY !left
    BEQ .Left
    .Down:
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Left:
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_arena:
    CPY !down
    BEQ .ReturnFalse
    CPY !right
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    LDA !samurai_kirby
    BRA .Return
    .Up:
    ; Only check MWW and Revenge, check others on Stereo so menu access is safe
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_sound_test:
    CPY !down
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !right
    BEQ .Right
    LDA !stereo
    BRA .Return
    .Right:
    LDA !megaton_punch
    BRA .Return
    .Up
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_megaton:
    CPY !left
    BEQ .Left
    CPY !up
    BEQ .Up
    LDA !samurai_kirby
    BRA .Return
    .Left:
    LDA !sound_test
    JSR check_level_access
    BCS .Return
    LDA !stereo
    BRA .Return
    .Up
    LDA !revenge_of_meta_knight
    JSR check_level_access
    BCS .Return
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !milky_way_wishes
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_samurai:
    CPY !down
    BEQ .ReturnFalse
    CPY !right
    BEQ .Right
    LDA !megaton_punch
    BRA .Return
    .Right:
    LDA !the_arena
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return
remap_stereo:
    CPY !down
    BEQ .ReturnFalse
    CPY !up
    BEQ .Up
    CPY !left
    BEQ .Left
    LDA !sound_test
    JSR check_level_access
    BCS .Return
    LDA !megaton_punch
    BRA .Return
    .Up:
    LDA !great_cave_offensive
    JSR check_level_access
    BCS .Return
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    LDA !spring_breeze
    JSR check_level_access
    BCS .Return
    LDA !gourmet_race
    JSR check_level_access
    BCS .Return
    BRA .ReturnFalse
    .Left:
    LDA !dyna_blade
    JSR check_level_access
    BCS .Return
    ;Fall through
    .ReturnFalse:
    LDA !no_sub_game
    .Return:
    JMP menu_return

determine_treasure:
    ; mostly a copy of 00EA71
    ; but we can't use it because of JSL
    LDX #$0022
    .Find:
    DEX
    DEX
    CMP $00EA8E, X
    BCC .Find
    TXY
    AND #$0007
    TAX
    TYA
    LSR
    TAY
    LDA #$0001
    .Loop:
    DEX
    BMI .Return
    ASL
    BRA .Loop
    .Return:
    RTS

check_treasure:
    STX $14
    LDX #$0040
    STX $16
    JSR determine_treasure
    AND [$14], Y
    STA $28
    RTL

set_treasure:
    STX $14
    LDX #$0040
    STX $16
    JSR determine_treasure
    ORA [$14], Y
    STA [$14], Y
    RTL

hook_copy_ability:
    PHY
    PHX
    PHA
    LDA $746D, X
    LDY #$0000
    SEC
    SBC #$0001
    .Loop1:
    CMP #$0008
    BCC .CheckLoop
    INY
    SEC
    SBC #$0008
    BRA .Loop1
    .CheckLoop:
    TAX
    LDA #$0001
    .Loop2:
    CPX #$0000
    BEQ .CheckCopy
    ASL
    DEX
    BRA .Loop2
    .CheckCopy:
    AND !received_copy_abilities, Y
    BEQ .NoAbility
    PLA
    PLX
    PLY
    CMP #$0005
    BNE .Return
    JML $02A350
    .NoAbility:
    PLA
    PLX
    PLY
    LDA #$0000
    STZ $746D, X
    STZ $7471, X
    .Return
    JML $02A37E

WriteBWRAM:
    LDA #$1EFE
    MVN $00, $00
    PHB
    LDX #$0000
    LDY #$0014
    .LoopHead:
    LDA $408100, X ; rom header
    CMP $FFC0, X ; compare to real rom name
    BNE .InitializeRAM ; area is uninitialized or corrupt, reset
    INX
    DEY
    BMI .Return ; if Y is negative, rom header matches, valid bwram
    BRA .LoopHead ; else continue loop
    .InitializeRAM:
    LDA #$0000
    STA $402000
    LDX #$2000
    LDY #$2001
    LDA #$EFFE
    MVN $40, $40
    LDX #$D000 ; seed info 0x3D000
    LDY #$9000 ; target location
    LDA #$1000
    MVN $40, $07
    LDX #$FFC0 ; ROM name
    LDY #$8100 ; target
    LDA #$0015
    MVN $40, $00
    .Return:
    PLB
    RTL

block_mww_planets:
    CMP #$0008
    BEQ .ReturnSpecial
    PHA
    PHX
    TAX
    LDA #$0001
    .Loop:
    CPX #$0000
    BEQ .Check
    ASL
    DEX
    BRA .Loop
    .Check:
    AND !received_planets
    BEQ .ReturnFalse
    PLX
    PLA
    JML $CAA70C
    .ReturnSpecial:
    JML $CAA6FD
    .ReturnFalse:
    PLX
    PLA
    LDA #$0008
    STA $6D56, X
    JML $CAA72C

block_ability_essence:
    PHY
    PHX
    PHA
    LDY #$0000
    SEC
    SBC #$0001
    .Loop1:
    CMP #$0008
    BCC .CheckLoop
    INY
    SEC
    SBC #$0008
    BRA .Loop1
    .CheckLoop:
    TAX
    LDA #$0001
    .Loop2:
    CPX #$0000
    BEQ .CheckCopy
    ASL
    DEX
    BRA .Loop2
    .CheckCopy:
    AND !received_copy_abilities, Y
    BEQ .NoAbility
    PLA
    PLX
    PLY
    BNE .Return
    .NoAbility:
    PLA
    PLX
    PLY
    JML $CF7699
    .Return
    CMP $749F, X
    BEQ .NoAbility
    JML $CF76A4


org $CF3FB1
hook_check_treasure:
    JSL check_treasure

org $CF44BD
hook_set_treasure:
    JSL set_treasure

org $CF73B1
hook_deluxe_ability:
    JSL set_treasure

org $CF7694
hook_ability_essence:
    JML block_ability_essence
    NOP

org $CFAA16
remap_deluxe_essence:
    db $00, $00, $01, $02, $03, $04, $05, $06, $07, $08, $09, $0A, $0B, $0C, $0D, $0E, $0F, $10, $11, $12