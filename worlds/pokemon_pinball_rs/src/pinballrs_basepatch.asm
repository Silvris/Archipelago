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

.org sub_153CC+0x406
    .thumb
    bl          EvoArrows

.org sub_153CC+0x680
    .thumb
    bl          GetArrows

//; Sapphire Board hooks
.org sub_1642C+0x5AA
    .thumb
    bl          EvoArrows

.org sub_1642C+0x796
    .thumb
    bl          GetArrows

.org sub_31498+0x6A
    .thumb
    bl          HatchLockSapphire

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

.org BuildSpeciesWeightsForEggMode+0x92
    .thumb
    bl          EggsCheckEvo

.org BuildSpeciesWeightsForEggMode+0x102
    .thumb
    bl          EggGroups

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
    mov         r2, #0
    strh        r2, [r1, #6]
    cmp         r0, #0
    beq         @@Return
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

.endarea

.org 0x6BC000
.byte "ARCHIPELAGO_DATA"
.fill 16
//; world version
.byte 0x00, 0x00, 0x00
//; basepatch version (if i remember to update it lol)
.byte 0x00, 0x01, 0x00
//; slot data at 0x6BC030
.org 0x6BC040
EggTableRuby:
.byte 0x00, 0x02, 0x03, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0F, 0x10, 0x11, 0x12, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1D, 0x1E, 0x1F
.align 32
EggTableSapphire:
.byte 0x00, 0x01, 0x03, 0x04, 0x06, 0x07, 0x09, 0x0A, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F
.align 32

.close