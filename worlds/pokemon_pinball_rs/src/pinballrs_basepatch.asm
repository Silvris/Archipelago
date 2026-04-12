//; Base Patch for Pokemon Pinball Ruby & Sapphire Archipelago
.gba

.include "pokepinballrs_syms.asm"

.open "pokepinballrs.gba", "pinballrs_basepatch.gba", 0x0

.macro GetValue, rn, current, target
    ldr         rn, [pc, #(target-current-4)]
.endmacro

//; Main Loop Hook
.org MainLoopIter+0x2C
    .thumb
    bl          MainLoopHook

//; Board locking
.org FieldSelect_State1_8C7C+0xB0
    .thumb
    bl          BoardSelectHook

//; Block EReader
.org sub_1157C+2
    .thumb
    pop         {r4-r7, lr}

//; Ruby Board hooks
.org sub_153CC+0xA6
    .thumb
    bl          HatchLockRuby

.org sub_153CC+0x1E4
    .thumb
    bl          UpdateBumperCount

.org sub_153CC+0x406
    .thumb
    bl          EvoArrows

.org sub_153CC+0x4A8
    .thumb
    bl          CoinArrows

.org sub_153CC+0x4BA
    .thumb
    bl          DoubleCoinRuby

.org sub_153CC+0x680
    .thumb
    bl          GetArrows

.org sub_21D78+0x30
    .thumb
    bl          CheckAnyMonEvoR0Shift //; this is the main one, sets the evo mode enable

.org sub_1AFD4+0x14A
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org sub_1FF0C+0x220
    .thumb
    bl          CheckMaku
    nop
    nop

.org RubyPond_EntityLogic+0x7CE
    .thumb
    bl          CheckWhiscash

.org sub_4F0F0+0x74
    .thumb
    bl          UpdateRubyUpgrade

//; Sapphire Board hooks
.org sub_1642C+0x2C2
    .thumb
    bl          CheckPelipper
    
.org sub_1642C+0x31C
    .thumb
    bl          CheckZig
    nop
.org sub_1642C+0x516
    .thumb
    bl          CoinArrows

.org sub_1642C+0x52A
    .thumb
    bl          DoubleCoinSapphire

.org sub_1642C+0x5AA
    .thumb
    bl          EvoArrows

.org sub_1642C+0x796
    .thumb
    bl          GetArrowsSapphire

.org sub_2F79C+0x4C2
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org sub_31144+0x114
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org sub_31498+0x6A
    .thumb
    bl          HatchLockSapphire

.org sub_329F4+0x15C
    .thumb
    bl          CheckAnyMonEvoR0Shift

//; Evo mode hooks
.org sub_1B140+0x11B8
    .thumb
    bl          CheckIndividualMonEvo

.org sub_2A354+0x44E
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org sub_29D9C+0x1F8
    .thumb
    bl          CheckAnyMonEvoR0Shift

//; Handle areas
.org sub_25F64+0x38
    .thumb
    bl          HandleInitialAreaEx

.org sub_260B8+0x4B6
    .thumb
    bl          HandleInitialArea

.org sub_260B8+0x4EC
    .thumb
    bl          HandleAreas

.org sub_26A10+0x35C
    .thumb
    bl          HandleAreas

.org sub_26A10+0x374
    .thumb
    bl          HandleRuinsNatural

//; catch_hatch_picker
.org BuildSpeciesWeightsForCatchEmMode+0x110
    .thumb
    bl          ClampearlCheck

.org BuildSpeciesWeightsForCatchEmMode+0x162
    .thumb
    bl          WeightsCheckEvo

.org BuildSpeciesWeightsForCatchEmMode+0x216
    .thumb
    bl          ForceNormal

.org BuildSpeciesWeightsForEggMode+0x92
    .thumb
    bl          EggsCheckEvo

.org BuildSpeciesWeightsForEggMode+0x102
    .thumb
    bl          EggGroups

.org BuildSpeciesWeightsForEggMode+0x13C
    .thumb
    bl          ForceEgg

.org PickSpeciesForEggMode+0x16
    .thumb
    bne         thumb_8032604  //; fix Pichu bug

.org 0x32604
thumb_8032604:

//; spheal
.org sub_45E90+0x17E
    .thumb
    bl          SetSphealCheck

//; bonus_complete_scoring_transition
.org ProcessBonusBannerAndScoring+0x3A
    .thumb
    bl          SetBonusComplete

//; board_process2
.org sub_4E2F8+0x136 //; Preserve Pichu on fail
    .thumb
    bl          CheckPichu

.org sub_4E598+0xB6 //; Preserve full charge on fail
    .thumb
    bl          CheckPichu

.org sub_4E598+0x132 //; Set ball type on reset
    .thumb
    bl          GetStartingBall
    nop
    nop
    ldr         r3, [pc, #0x18]
    nop
    nop         //; have to remove this one, which sets the type to Master Ball

//; pinball_game_main
.org PinballGame_State0_49ED4+0xA6
    .thumb
    bl          GetStartingBall
    nop         //; some intentional cycle shuffling here?, does LSL into ASR identical amounts

.org PinballGame_State0_49ED4+0x1B0
    .thumb
    bl          GetStartingBall
    nop

.org sub_4A518+0x50
    //; Game state initialization
    //; Start by checking Pichu, he's easily the most complex of the set
    //; R5 - gCurrentPinballGame, R6 - gMain
    bl          CheckPichu
    cmp         r0, #0
    bne         @@Continue
    bl          sub_4A518+0x114
    @@Continue:
    ldr         r2, [r5, #0]
    mov         r1, #0xe3
    LSL         r1, r1, 1
    add         r0, r2, r1
    mov         r1, #168
    strh        r1, [r0, #0]
    strh        r1, [r0, #2]
    mov         r1, #13
    strh        r1, [r0, #4]
    strh        r1, [r0, #6]
    mov         r1, #0
    strh        r1, [r0, #10]
    strh        r1, [r0, #14]
    mov         r1, #120
    strh        r1, [r0, #16]
    mov         r1, #60
    strh        r1, [r0, #22]
    bl          HandleRemainingGameInit
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

.org sub_4A518+0xCA
    //; some PC relative stuff we need to skip over, still only relevant to a Pichu enabled setup
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    bl          HandleRemainingGameInit
    mov         r2, #0xC9
    lsl         r2, r2, #1
    add         r1, r0, r2
    bl          GetStartingCoins

.org sub_4A518+0x128
    //; No Pichu codepath, just redirect and get coins
    bl          HandleRemainingGameInit
    mov         r7, #0xC9
    lsl         r7, r7, #1
    add         r1, r0, r7
    bl          GetStartingCoins
    nop

.org 0x47344
.area 0x1B0

GetStartingLives:
    .thumb
    push        {r4}
    GetValue    r4, GetStartingLives, ArchipelagoInfo
    ldrb        r0, [r4, #0]
    pop         {r4}
    bx          lr
    .align      4

GetStartingCoins:
    .thumb
    push        {r4}
    GetValue    r4, GetStartingCoins, ArchipelagoInfo
    ldrb        r0, [r4, #1]
    pop         {r4}
    bx          lr
    .align      4

GetStartingBall:
    .thumb
    push        {r4}
    GetValue    r4, GetStartingBall, ArchipelagoInfo
    ldrb        r0, [r4, #2]
    pop         {r4}
    bx          lr
    .align      4

CheckPichu:
    .thumb
    push        {r4}
    GetValue    r4, CheckPichu, ArchipelagoInfo
    ldrb        r0, [r4, #3]
    pop         {r4}
    bx          lr
    .align      4

ArchipelagoInfo:
    //; 0 - starting lives, 1 - starting coins, 2 - starting ball, 3 - pichu, 4 - coin modifier, 5 - allowed boards, 6/7 - play sound, 0x10 - allowed stages
    .word 0x2033000

HandleRemainingGameInit:
    //; Just have to handle ball and lives, code paths converge on coins
    //; R5 - gCurrentPinballGame, R6 - gMain
    push        {lr}
    ldr         r2, [r5, #0]
    bl          GetStartingBall
    cmp         r0, #0
    beq         @@Lives
    @@Get1:
    GetValue    r1, @@Get1, CurrentPinballPtr
    add         r1, r1, r2
    strb        r0, [r1, #0]
    mov         r0, #0xE1
    lsl         r0, r0, #4
    strh        r0, [r1, #2]
    @@Lives:
    mov         r1, #0x30
    add         r1, r1, r2
    bl          GetStartingLives
    strb        r0, [r1, #0]
    ldr         r0, [r5, #0]
    pop         {lr}
    bx          lr
    .align      4

CurrentPinballPtr:
.word 0x5F6 //; beautifully horrible number

HandleAreas:
    push        {r0-r6}
    nop
    @@Get1:
    GetValue    r6, @@Get1, HandleAreasCurrentPinball
    ldr         r1, [r6, #0] //; gCurrentPinballGame, have to do this here for alignment purposes
    @@Get2:
    GetValue    r5, @@Get2, HandleAreasGMain
    add         r1, #0x32
    ldrb        r0, [r1, #0] //; get current stage
    ldrb        r3, [r5, #4] //; board
    @@Get3:
    GetValue    r2, @@Get3, ArchipelagoStages
    cmp         r3, #0
    beq         @@Compare
    add         r2, #7
    @@Compare:
    mov         r5, r0
    add         r0, #1
    mov         r3, #0
    mov         r4, #1
    @@Loop:
    ldrb        r3, [r2, r0]
    cmp         r3, #0
    bne         @@Set
    add         r0, #1
    @@Check:
    cmp         r0, r5
    beq         @@Set
    cmp         r0, #6
    blt         @@Loop
    mov         r0, 0
    b           @@Check
    @@Set:
    strb        r0, [r1, r4]
    add         r0, #1
    add         r4, #1
    cmp         r4, #2
    bgt         @@Return
    b           @@Loop
    @@Return:
    pop         {r0-r6}
    bx          lr
    .align 4

HandleAreasCurrentPinball:
.word 0x20314E0

HandleAreasGMain:
.word 0x200B0C0

ArchipelagoStages:
.word 0x2033010

HandleRuinsNatural:
//; called when the player has gone through 5 areas, overwrite the standard pick with Ruins if unlocked
//; assume gCurrentPinballGame+0x32 in r1
    push        {r0-r3}
    mov         r0, #6
    @@Get1:
    GetValue    r2, @@Get1, HandleRuinsNaturalGMain
    ldrb        r3, [r2, #4]
    @@Get2:
    GetValue    r2, @@Get2, HandleRuinsNaturalArchipelagoStages
    cmp         r3, #0
    beq         @@Check
    add         r2, #7
    @@Check:
    ldrb        r3, [r2, r0]
    cmp         r3, #0
    beq         @@Return
    strb        r0, [r1, #0]
    @@Return:
    pop         {r0-r3}
    bx          lr
    .align      4

HandleRuinsNaturalGMain:
.word 0x200B0C0

HandleRuinsNaturalArchipelagoStages:
.word 0x2033010

HandleInitialArea:
    //; r0 - return next stage
    push        {r1-r5}
    mov         r5, r0
    @@Get1:
    GetValue    r2, @@Get1, HandleInitialNaturalGMain
    ldrb        r3, [r2, #4]
    @@Get2:
    GetValue    r2, @@Get2, HandleInitialArchipelagoStages
    cmp         r3, #0
    beq         @@Compare
    add         r2, #7
    @@Compare:
    add         r0, #1
    mov         r3, #0
    mov         r4, #1
    @@Loop:
    ldrb        r3, [r2, r0]
    cmp         r3, #0
    bne         @@Return
    add         r0, #1
    @@Check:
    cmp         r0, r5
    beq         @@Return
    cmp         r0, #6
    blt         @@Loop
    mov         r0, 0
    b           @@Check
    @@Return:
    pop         {r1-r5}
    mov         r1, #6
    bx          lr
    .align      4

HandleInitialNaturalGMain:
    .word 0x200B0C0

HandleInitialArchipelagoStages:
    .word 0x2033010

HandleInitialAreaEx:
    //; set the first entry
    push        {r1-r7, lr}
    bl          HandleInitialArea
    pop         {r1-r7}
    add         r4, #0x32
    strb        r0, [r4, #0]
    pop         {lr}

MainLoopHook:
    //; handle the two things we need to keep
    push        {r0-r7, lr}
    add         r0, #1
    str         r0, [r1, #0x4C]
    //; free reign, r0 is immediately used for return
    @@GetSound:
    GetValue    r1, @@GetSound, MainLoopAP
    ldrh        r0, [r1, #6]
    cmp         r0, #0
    beq         @@Return
    mov         r2, #0
    strh        r2, [r1, #6]
    bl          m4aSongNumStart
    @@Return:
    pop         {r0-r7, lr}
    .align      4

MainLoopAP:
    .word 0x2033000

BoardSelectHook:
    //; preserve r4, r2-gMain, r3-gFieldSelectInfo
    //; this is a bit hacky, reliant on specific return handling
    //; 
    push        {lr}
    ldrb        r2, [r2, #4]
    mov         r3, #1
    lsl         r3, r2
    @@Get1:
    GetValue    r2, @@Get1, BoardSelectAP
    ldrb        r2, [r2, #5]
    and         r2, r3
    bne         @@True
    mov         r0, #0x8A
    bl          m4aSongNumStart
    pop         {r1}
    add         r1, #0x7A
    bx          r1
    @@True:
    bl          m4aSongNumStart
    pop         {lr}
    .align      4

BoardSelectAP:
    .word 0x2033000

HatchLockRuby:
//; rather jank, but the alternative is digging in a bunch of collision code
//; i'm not insane enough for that
    push        {r2, lr}
    mov         r0, #0
    @@Get1:
    GetValue    r2, @@Get1, HatchLockRubyAP
    ldrb        r2, [r2, #10]
    cmp         r2, #0
    beq         @@Set
    mov         r0, #2
    @@Set:
    add         r1, #0x25
    pop         {r2, lr}
    .align 4

HatchLockRubyAP:
    .word 0x2033000

HatchLockSapphire:
//; Sapphire is easy though, but a little hacky
    push        {r0-r2}
    ldrh        r0, [r4, r0]
    @@Get1:
    GetValue    r2, @@Get1, HatchLockSapphireAP
    ldrb        r2, [r2, #10]
    cmp         r2, #0
    bne         @@Set
    mov         r0, #0x4
    @@Set:
    cmp         r0, #2
    pop         {r0-r2}
    @@Return:
    bx          lr
    .align 4

HatchLockSapphireAP:
    .word 0x2033000

GetArrowsSapphire:
    add         r0, #1
    nop

GetArrows:
    push        {r2, lr}
    cmp         r0, #2
    ble         @@Set
    nop
    @@Get1:
    GetValue    r2, @@Get1, GetArrowsAP
    ldrb        r2, [r2, #8]
    cmp         r2, #0
    bne         @@Set
    @@True:
    mov         r0, #2
    @@Set:
    strb        r0, [r1, #0]
    pop         {r2, lr}
    .align 4

GetArrowsAP:
    .word 0x2033000

.endarea

.org EReaderMain
.area 0x1154
//; cannibalize the EReader functionality, we fake rando the cards anyways
EvoArrows:
    push        {r2, lr}
    add         r0, #1
    @@Get1:
    GetValue    r2, @@Get1, EvoArrowsAP
    ldrb        r2, [r2, #9]
    cmp         r0, r2
    bgt         @@Return
    strb        r0, [r1, #0]
    @@Return:
    pop         {r2, lr}
    .align 4

EvoArrowsAP:
    .word 0x2033000

WeightsCheckEvo:
    push        {r2}
    ldrb        r6, [r0, #0x15]
    @@Get1:
    GetValue    r2, @@Get1, WeightsCheckEvoAP
    ldrb        r2, [r2, #9]
    cmp         r2, #3
    bge         @@Return
    mov         r6, #0xCD
    @@Return:
    pop         {r2}
    add         r0, r6, #0
    bx          lr

WeightsCheckEvoAP:
    .word 0x2033000

ClampearlCheck:
    //; clampearl is a special little baby
    push        {r0-r2}
    nop
    @@Get1:
    GetValue    r2, @@Get1, ClampearlCheckAP
    ldrb        r2, [r2, #0]
    cmp         r2, #3
    bge         @@Return
    mov         r0, #0xBA
    add         lr, r0
    @@Return:
    pop         {r0-r2}
    lsl         r2, r2, #0x10
    asr         r0, r2, #0x10
    bx          lr

ClampearlCheckAP:
    .word 0x2033000

EggsCheckEvo:
    push        {r2}
    ldrb        r5, [r0, #0x15]
    @@Get1:
    GetValue    r2, @@Get1, EggsCheckEvoAP
    ldrb        r2, [r2, #9]
    cmp         r2, #3
    bge         @@Return
    mov         r5, #0xCD
    @@Return:
    pop         {r2}
    add         r0, r5, #0
    bx          lr

EggsCheckEvoAP:
    .word 0x2033000

EggGroups:
    //; r0- current species, r4 - gCurrentPinballGame, r12 - gMain, r8 - species index shifted 0x10 left
    lsl         r0, r5, #0x10
    asr         r0, r0, #0x10
    push        {r0}
    nop
    @@Get1:
    GetValue    r2, @@Get1, EggGroupsTable
    mov         r0, r12
    ldrb        r0, [r0, #4]
    cmp         r0, #0
    beq         @@LoadMask
    add         r2, #32
    @@LoadMask:
    mov         r0, r8
    asr         r0, r0, #0x10
    ldrb        r2, [r2, r0]
    mov         r0, #1
    lsl         r0, r2
    nop
    @@Get2:
    GetValue    r2, @@Get2, EggGroupsAP
    ldr         r2, [r2, #0x20]
    and         r2, r0
    pop         {r0}
    cmp         r2, #0
    bne         @@Return
    mov         r1, r0
    @@Return:
    bx          lr

EggGroupsTable:
    .word EggTableRuby | 0x8000000

EggGroupsAP:
    .word 0x2033000

SetBonusComplete:
    push        {r2-r4}
    ldrb        r0, [r1, #0x04]
    sub         r0, #2
    //; r0 is return value here, but it's still useful
    mov         r2, #1
    @@Get:
    GetValue    r3, @@Get, SetBonusCompleteAP
    lsl         r2, r0
    ldrb        r4, [r3, #0xD]
    orr         r2, r4
    strb        r2, [r3, #0xD]
    pop         {r2-r4}
    bx          lr
    .align      4


SetBonusCompleteAP:
    .word 0x2033000

CheckIndividualMonEvo:
    //; r5 contains gCurrentPinballGame
    push        {r1-r5, lr}
    mov         r0, #1
    and         r0, r1
    cmp         r0, #0
    beq         @@Return
    mov         r2, #0xB3
    //; now free to handle whatever is needed
    @@Get:
    GetValue    r3, @@Get, CheckIndividualMonEvoAP
    lsl         r2, #3
    @@Get2:
    GetValue    r1, @@Get2, CheckIndividualMonEvoSpecies
    ldr         r5, [r5, #0]
    ldrh        r2, [r5, r2]
    mov         r4, #0x18
    mul         r2, r4
    add         r1, r2
    ldrb        r2, [r1, #0x14]
    mov         r1, #1
    lsl         r1, r2
    ldrh        r2, [r3, #0x24]
    and         r1, r2
    cmp         r1, #0
    bne         @@Return
    //; failure state, mov 0 into r0, ensure we take the branch
    mov         r0, #0x8A
    bl          m4aSongNumStart
    mov         r0, #0
    @@Return:
    cmp         r0, #0
    pop         {r1-r5, pc}
    .align      4


CheckIndividualMonEvoAP:
    .word 0x2033000

CheckIndividualMonEvoSpecies:
    .word 0x86A3700

CheckAnyMonEvo:
//; r0 - evolvablePartySize
//; returns 0 in r0 if no evolvable, else 1
//; r6 - AP, r5 - currentPinballGame, r4 - gSpeciesInfo, r3 - evolvePartyIndex,  r1/r2 flex

    push        {r1-r6}
    cmp         r0, #0 //; trivial false
    beq         @@False
    mov         r3, #0
    @@Get1:
    GetValue    r5, @@Get1, CheckAnyMonEvoPinball
    ldr         r5, [r5, #0]
    @@Get2:
    GetValue    r4, @@Get2, CheckAnyMonEvoSpecies
    mov         r2, #0x9C
    @@Get3:
    GetValue    r6, @@Get3, CheckAnyMonEvoAP
    lsl         r2, #2
    add         r5, r2
    @@Loop:
    ldrb        r2, [r5, r3]
    mov         r1, #0x18
    mul         r2, r1
    add         r1, r4, r2
    ldrb        r2, [r1, #0x14]
    mov         r1, #1
    lsl         r1, r2
    ldrh        r2, [r6, #0x24]
    and         r1, r2
    cmp         r1, #0
    bne         @@True
    add         r3, #1
    cmp         r3, r0
    bne         @@Loop
    @@False:
    mov         r0, #0
    @@Return:
    pop         {r1-r6}
    bx          lr
    @@True:
    mov         r0, #1
    b           @@Return

    .align      4


CheckAnyMonEvoPinball:
    .word 0x20314E0

CheckAnyMonEvoSpecies:
    .word 0x86A3700

CheckAnyMonEvoAP:
    .word 0x2033000

CheckAnyMonEvoR0Shift:
    push        {lr}
    asr         r0, #0x18
    bl          CheckAnyMonEvo
    cmp         r0, #0
    pop         {pc}

CoinArrows:
    push        {r2, lr}
    add         r0, #1
    @@Get1:
    GetValue    r2, @@Get1, CoinArrowsAP
    ldrb        r2, [r2, #14]
    cmp         r0, r2
    bgt         @@Return
    strb        r0, [r1, #0]
    @@Return:
    pop         {r2, lr}
    .align 4

CoinArrowsAP:
    .word 0x2033000

DoubleCoin:
    push        {r0-r2, lr}
    mov         r2, #0xCA
    @@Get1:
    GetValue    r1, @@Get1, DoubleCoinAP
    ldrb        r1, [r1, #4]
    cmp         r1, #0
    beq         @@Return
    lsl         r2, #1
    add         r0, r2
    ldrb        r2, [r0, #0]
    lsl         r2, #1
    strb        r2, [r0, #0]
    @@Return:
    pop         {r0-r2, pc}
    .align      4

DoubleCoinAP:
    .word 0x2033000

DoubleCoinRuby:
    push        {lr}
    bl          DoubleCoin
    add         r0, r2
    strh        r1, [r0, #0]
    pop         {pc}

DoubleCoinSapphire:
    push        {lr}
    bl          DoubleCoin
    add         r0, r4
    strh        r1, [r0, #0]
    pop         {pc}

CheckHelper:
    push        {r2, r4}
    mov         r4, #1
    @@Get:
    GetValue    r2, @@Get, CheckHelperAP
    add         r2, #0x26
    ldrb        r2, [r2, #0]
    lsl         r4, r3
    and         r2, r4
    cmp         r2, #0
    beq         @@False
    mov         r0, #1
    @@Return:
    pop         {r2, r4}
    bx          lr
    @@False:
    mov         r0, #0
    b           @@Return
    .align      4

CheckHelperAP:
    .word 0x2033000

CheckZig:
    push        {r3, lr}
    cmp         r0, #0
    bne         @@False
    mov         r3, #0
    bl          CheckHelper
    @@Return:
    pop         {r3, pc}
    @@False:
    mov         r0, #0
    b           @@Return

CheckPelipper:
    push        {r0-r3, lr}
    mov         r3, #1
    bl          CheckHelper
    //; r1 is preserved here, take the chance to update our total hits on mult
    mov         r2, #0x28
    @@Get:
    GetValue    r3, @@Get, CheckPelipperAP
    strb        r0, [r1, #0]
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3, pc}
    .align      4

CheckPelipperAP:
    .word 0x2033000

CheckMaku:
    //; easy, just call for the value
    push        {r3, lr}
    cmp         r0, #0
    bne         @@False
    mov         r3, #2
    bl          CheckHelper
    @@Return:
    pop         {r3, pc}
    @@False:
    mov         r0, #0
    b           @@Return
    .align      4

CheckWhiscash:
    //; easy, just call for the value
    push        {r3, lr}
    lsl         r0, #0x10
    lsr         r0, #0x10
    mov         r3, #3
    bl          CheckHelper
    @@Return:
    pop         {r3, pc}
    @@False:
    mov         r0, #0
    b           @@Return
    .align      4

ForceNormal:
    mov         r9, r4
    mov         r10, r5
    push        {r0-r5}
    mov         r2, #0xE7
    @@GetPinball:
    GetValue    r4, @@GetPinball, ForceNormalPinball
    ldr         r4, [r4, #0]
    @@GetWild:
    GetValue    r3, @@GetWild, ForceNormalWild
    lsl         r2, #3
    ldrb        r1, [r4, r2]
    mov         r2, #0
    cmp         r1, #3
    bne         @@ContinueSetup
    mov         r2, #0x10
    @@ContinueSetup:
    //; from here, make r3 store the current table of 8 we're referencing
    mov         r1, #0x35
    ldrb        r1, [r4, r1]
    lsl         r1, #5
    add         r3, r2
    add         r3, r1
    mov         r1, #0x27
    mov         r0, #0
    @@GetAP:
    GetValue    r5, @@GetAP, ForceNormalAP
    ldrb        r1, [r5, r1]
    sub         r1, #1
    @@ScanLoop:
    ldrh        r2, [r3, r0]
    cmp         r2, r1
    beq         @@Apply
    add         r0, #2
    cmp         r0, #0x10
    beq         @@Return
    b           @@ScanLoop
    @@Apply:
    //; r0 has the index we need to keep
    //; first check if we have enough coins
    mov         r3, #0x98
    lsl         r3, #1
    add         r4, r3
    mov         r2, #0x62
    ldrb        r1, [r4, r2]
    cmp         r1, #0x1E
    blt         @@Return
    sub         r1, #0x1E
    strb        r1, [r4, r2]
    mov         r1, #0
    mov         r2, #0
    @@ApplyLoop:
    cmp         r0, r1
    beq         @@Skip
    strh        r2, [r4, r1]
    @@Skip:
    add         r1, #2
    cmp         r1, #0x10
    blt         @@ApplyLoop
    @@ApplyCurrent:
    //; we have to also update r0 with the totalWeight
    //; and remove the value in AP
    mov         r1, #0x27
    strb        r2, [r5, r1]
    sub         r4, #2
    ldrh        r1, [r4, #0]
    add         r4, #2
    strh        r1, [r4, r0]
    @@Return:
    pop         {r0-r5}
    bx          lr
    .align      4

ForceNormalPinball:
    .word 0x20314E0

ForceNormalWild:
    .word 0x8055A84

ForceNormalAP:
    .word 0x2033000

ForceEgg:
    mov         r9, r4
    mov         r10, r5
    push        {r0-r5}
    mov         r2, #0x4
    @@GetMain:
    GetValue    r1, @@GetMain, ForceEggMain
    ldrb        r1, [r1, r2]
    @@GetWild:
    GetValue    r3, @@GetWild, ForceEggWild
    mov         r2, #0
    @@GetPinball:
    GetValue    r4, @@GetPinball, ForceEggPinball
    ldr         r4, [r4, #0]
    cmp         r1, #0
    beq         @@ContinueSetup
    add         r3, #0x34
    @@ContinueSetup:
    mov         r2, #0x98
    lsl         r2, #1
    add         r4, r2
    @@GetAP:
    GetValue    r5, @@GetAP, ForceEggAP
    mov         r1, #0x27
    ldrb        r1, [r5, r1]
    sub         r1, #1
    mov         r0, #0
    @@ScanLoop:
    //; change compared to normal, check if we've already nulled the weight here
    ldrh        r2, [r4, r0]
    cmp         r2, #0
    beq         @@NoWeight
    ldrh        r2, [r3, r0]
    cmp         r2, r1
    beq         @@Apply
    @@NoWeight:
    add         r0, #2
    cmp         r0, #0x32
    beq         @@Return
    b           @@ScanLoop
    @@Apply:
    //; r0 has the index we need to keep
    //; first check if we have enough coins
    mov         r2, #0x62
    ldrb        r1, [r4, r2]
    cmp         r1, #0x1E
    blt         @@Return
    sub         r1, #0x1E
    strb        r1, [r4, r2]
    mov         r1, #0
    mov         r2, #0
    @@ApplyLoop:
    cmp         r0, r1
    beq         @@Skip
    strh        r2, [r4, r1]
    @@Skip:
    add         r1, #2
    cmp         r1, #0x32
    blt         @@ApplyLoop
    @@ApplyCurrent:
    //; we have to also update r0 with the totalWeight
    //; and remove the value in AP
    mov         r1, #0x27
    strb        r2, [r5, r1]
    sub         r4, #2
    ldrh        r1, [r4, #0]
    add         r4, #2
    strh        r1, [r4, r0]
    @@Return:
    pop         {r0-r5}
    bx          lr
    .align      4

ForceEggMain:
    .word 0x200B0C0

ForceEggWild:
    .word 0x86A4A38

ForceEggPinball:
    .word 0x20314E0

ForceEggAP:
    .word 0x2033000

SetSphealCheck:
    //; r2 - gCurrentPinballGame
    lsl         r0, #2
    strh        r0, [r3, #0]
    push        {r0-r4}
    mov         r3, #0xA6
    @@Get:
    GetValue    r1, @@Get, SetSphealCheckAP
    lsl         r3, #3
    sub         r3, #4
    ldrb        r0, [r2, r3]
    add         r3, #1
    ldrb        r3, [r2, r3]
    mov         r4, r0
    add         r4, r3
    mov         r2, #0
    cmp         r0, #5
    blt         @@Spheals
    add         r2, #1
    @@Spheals:
    cmp         r3, #5
    blt         @@Combined
    add         r2, #2
    @@Combined:
    cmp         r4, #10
    blt         @@Return
    add         r2, #4
    @@Return:
    lsl         r2, #5
    ldrb        r0, [r1, #0xD]
    orr         r0, r2
    strb        r0, [r1, #0xD]
    pop         {r0-r4}
    bx          lr
    .align      4

SetSphealCheckAP:
    .word 0x2033000

UpdateBumperCount:
    push        {r0-r3}
    mov         r2, #0x28
    @@Get:
    GetValue    r3, @@Get, UpdateBumperCountAP
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3}
    add         r0, r2, #1
    strb        r0, [r1, #0]
    bx          lr
    .align      4

UpdateBumperCountAP:
    .word 0x2033000

UpdateRubyUpgrade:
    push        {r0-r3}
    mov         r2, #0x29
    @@Get:
    GetValue    r3, @@Get, UpdateRubyUpgradeAP
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3}
    mov         r0, #0
    ldrh        r0, [r1, r0]
    bx          lr
    .align      4

UpdateRubyUpgradeAP:
    .word 0x2033000
.endarea

.org 0x6BC000
.byte "ARCHIPELAGO_DATA"
.fill 16
//; world version
.byte 0x00, 0x00, 0x00
//; basepatch version (if i remember to update it lol)
.byte 0x00, 0x01, 0x02
//; slot data at 0x6BC030
.org 0x6BC040
EggTableRuby:
.byte 0x00, 0x02, 0x03, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0F, 0x10, 0x11, 0x12, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1D, 0x1E, 0x1F
.align 32
EggTableSapphire:
.byte 0x00, 0x01, 0x03, 0x04, 0x06, 0x07, 0x09, 0x0A, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F
.align 32

.close