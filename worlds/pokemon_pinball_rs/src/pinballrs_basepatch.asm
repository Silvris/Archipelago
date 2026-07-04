//; Base Patch for Pokemon Pinball Ruby & Sapphire Archipelago
.gba

.include "pokepinballrs_syms.asm"

.open "pokepinballrs.gba", "pinballrs_basepatch.gba", 0x8000000

.definelabel gArchipelago, 0x2033000
.definelabel gArchipelagoStrings, 0x2035000
.definelabel gArchipelagoStringEnable, 0x2035100  //; byte
.definelabel gArchipelagoStringTimer, 0x2035102 //; half, frames
.definelabel gArchipelagoStringItem, 0x2035104  //; half
.definelabel gArchipelagoStringPlayer, 0x2035108  //; half
.definelabel gArchipelagoSlot, 0x86BC030

//; Main Loop Hook
.org MainLoopIter+0x2C
    .thumb
    bl          MainLoopHook

//; Board locking
.org FieldSelect_State1_8C7C+0xB0
    .thumb
    bl          BoardSelectHook

//; Block EReader
.org CheckEReaderAccessCombo+2
    .thumb
    pop         {r4-r7, lr}

//; Ruby Board hooks
.org ProcessRubyCollisionEvent+0xA6
    .thumb
    bl          HatchLockRuby

.org ProcessRubyCollisionEvent+0x1E4
    .thumb
    bl          UpdateBumperCount

.org ProcessRubyCollisionEvent+0x406
    .thumb
    bl          EvoArrows

.org ProcessRubyCollisionEvent+0x4A8
    .thumb
    bl          CoinArrows

.org ProcessRubyCollisionEvent+0x4BA
    .thumb
    bl          DoubleCoinRuby

.org ProcessRubyCollisionEvent+0x52E
    .thumb
    bl          UpdateRubyUpgrade

.org ProcessRubyCollisionEvent+0x59A
    .thumb
    bl          UpdateRubyUpgrade

.org ProcessRubyCollisionEvent+0x60A
    .thumb
    bl          UpdateRubyUpgrade

.org ProcessRubyCollisionEvent+0x680
    .thumb
    bl          GetArrows

.org ProcessRubyCollisionEvent+0x9D6
    .thumb
    bl          UpdateMakuUpgrade

.org UpdateEvolutionShopSprite+0x30
    .thumb
    bl          CheckAnyMonEvoR0Shift //; this is the main one, sets the evo mode enable

.org AnimateRubyEvolutionShopSequence+0x14A
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org UpdateRubySideBumperAnimation+0x220
    .thumb
    bl          CheckMaku
    nop
    nop

.org RubyPond_EntityLogic+0x7CE
    .thumb
    bl          CheckWhiscash

//; Sapphire Board hooks
.org ProcessSapphireCollisionEvent+0x2C0
    .thumb
    bl          CheckPelipper
    
.org ProcessSapphireCollisionEvent+0x31C
    .thumb
    bl          CheckZig
    nop
.org ProcessSapphireCollisionEvent+0x516
    .thumb
    bl          CoinArrows

.org ProcessSapphireCollisionEvent+0x52A
    .thumb
    bl          DoubleCoinSapphire

.org ProcessSapphireCollisionEvent+0x5AA
    .thumb
    bl          EvoArrows

.org ProcessSapphireCollisionEvent+0x63A
    .thumb
    bl          UpdateSapphireUpgrade

.org ProcessSapphireCollisionEvent+0x6AE
    .thumb
    bl          UpdateSapphireUpgrade

.org ProcessSapphireCollisionEvent+0x722
    .thumb
    bl          UpdateSapphireUpgrade

.org ProcessSapphireCollisionEvent+0x796
    .thumb
    bl          GetArrowsSapphire

.org UpdateSapphireBumperLogic+0x4C2
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org UpdateSapphireShopSignAnimation+0x114
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org UpdateSapphireEggMachine+0x6A
    .thumb
    bl          HatchLockSapphire

.org UpdateSapphireEvolutionShopSequence+0x15C
    .thumb
    bl          CheckAnyMonEvoR0Shift


//; Roulette hooks
.org GivePrize+0x5A4
    .thumb
    bl          RingLinkRoulette

//; Evo mode hooks
.org UpdateShopEntryAnimation+0x11B8
    .thumb
    bl          CheckIndividualMonEvo

.org GivePrize+0x44E
    .thumb
    bl          CheckAnyMonEvoR0Shift

.org InitRouletteWheel+0x1F8
    .thumb
    bl          CheckAnyMonEvoR0Shift

//; Shop hooks
.org UpdateShopEntryAnimation+0x656
    .thumb
    bl          ShopBlockHelpers

.org UpdateShopEntryAnimation+0x6A0
    .thumb
    bl          RingLinkShop

//; Handle areas
.org InitBoardIntroMode+0x38
    .thumb
    bl          HandleInitialAreaEx

.org UpdateBoardIntroMode+0x334
    .thumb
    bl          CheckRuinsAndCardRoulette

.org UpdateBoardIntroMode+0x474
    .thumb
    bl          CheckRuinsAndCardEx

.org UpdateBoardIntroMode+0x494
    .thumb
    bl          HandleRuinsCardTravel

.org UpdateBoardIntroMode+0x4B6
    .thumb
    bl          HandleInitialArea

.org UpdateBoardIntroMode+0x4EC
    .thumb
    bl          HandleAreas

.org UpdateTravelMode+0x35C
    .thumb
    bl          HandleAreas

.org UpdateTravelMode+0x374
    .thumb
    bl          HandleRuinsNatural

//; catch_hatch_picker
.org BuildSpeciesWeightsForCatchEmMode+0x110
    .thumb
    bl          ClamperlCheck

.org BuildSpeciesWeightsForCatchEmMode+0x162
    .thumb
    bl          WeightsCheckEvo

.org BuildSpeciesWeightsForCatchEmMode+0x216
    .thumb
    bl          ForceNormal

.org PickSpeciesForCatchEmMode+0x2C6
    .thumb
    bl          ClearForceSpecial

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

.org PickSpeciesForEggMode+0xF8
    .thumb
    bl          ClearForcePichu

.org 0x8032604
thumb_8032604:

//; spheal
.org UpdateSphealResultsScreen+0x17E
    .thumb
    bl          SetSphealCheck

//; bonus_complete_scoring_transition
.org ProcessBonusBannerAndScoring+0x3A
    .thumb
    bl          SetBonusComplete

//; end of ball
.org EndOfBallSequence+0x15C
    .thumb
    bl          CheckGoalEndOfBall

//; board_process2
.org ProcessMainBoardBallDrainAndLaunch+0x136 //; Preserve Pichu on fail
    .thumb
    bl          CheckPichu

.org ResetBoardStateOnDeath+0xB6 //; Preserve full charge on fail
    .thumb
    bl          CheckPichu

.org ResetBoardStateOnDeath+0x132 //; Set ball type on reset
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

.org InitPinballGameState+0x50
    //; Game state initialization
    //; Start by checking Pichu, he's easily the most complex of the set
    //; R5 - gCurrentPinballGame, R6 - gMain
    bl          CheckPichu
    cmp         r0, #0
    bne         @@Continue
    bl          InitPinballGameState+0x114
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

.org InitPinballGameState+0xCA
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

.org InitPinballGameState+0x128
    //; No Pichu codepath, just redirect and get coins
    bl          HandleRemainingGameInit
    mov         r7, #0xC9
    lsl         r7, r7, #1
    add         r1, r0, r7
    bl          GetStartingCoins
    nop

.org BonusStage_HandleModeChangeFlags+0x2
    //; hook here to always run during main gameplay
    .thumb
    bl          StringHandlingMainLoop

.org 0x8047344
.area 0x1B0

GetStartingLives:
    .thumb
    push        {r4}
    ldr         r4, =gArchipelago
    ldrb        r0, [r4, #0]
    pop         {r4}
    bx          lr
    .align      4

GetStartingCoins:
    .thumb
    push        {r4}
    ldr         r4, =gArchipelago
    ldrb        r0, [r4, #1]
    pop         {r4}
    bx          lr
    .align      4

GetStartingBall:
    .thumb
    push        {r4}
    ldr         r4, =gArchipelago
    ldrb        r0, [r4, #2]
    pop         {r4}
    bx          lr
    .align      4

CheckPichu:
    .thumb
    push        {r4}
    ldr         r4, =gArchipelago
    ldrb        r0, [r4, #3]
    pop         {r4}
    bx          lr
    .align      4

.pool

HandleRemainingGameInit:
    //; Just have to handle ball and lives, code paths converge on coins
    //; R5 - gCurrentPinballGame, R6 - gMain
    push        {lr}
    ldr         r2, [r5, #0]
    bl          GetStartingBall
    cmp         r0, #0
    beq         @@Lives
    @@Get1:
    ldr         r1, =0x5F6
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

.pool

HandleRuinsNatural:
//; called when the player has gone through 5 areas, overwrite the standard pick with Ruins if unlocked
//; assume gCurrentPinballGame+0x32 in r1
    push        {r0-r3}
    mov         r0, #6
    @@Get1:
    ldr         r2, =gMain
    ldrb        r3, [r2, #4]
    @@Get2:
    ldr         r2, =gArchipelago+0x10
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

.pool

HandleInitialArea:
    //; r0 - return next stage
    push        {r1-r5}
    mov         r5, r0
    @@Get1:
    ldr         r2, =gMain
    ldrb        r3, [r2, #4]
    @@Get2:
    ldr         r2, =gArchipelago+0x10
    cmp         r3, #0
    beq         @@Compare
    add         r2, #7
    @@Compare:
    add         r0, #1
    cmp         r0, #6
    blt         @@CompContinue
    mov         r0, #0
    @@CompContinue:
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

.pool

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
    ldr         r1, =gArchipelago
    ldrh        r0, [r1, #6]
    cmp         r0, #0
    beq         @@Return
    mov         r2, #0
    strh        r2, [r1, #6]
    bl          m4aSongNumStart
    @@Return:
    pop         {r0-r7, lr}
    .align      4

.pool

BoardSelectHook:
    //; preserve r4, r2-gMain, r3-gFieldSelectInfo
    //; this is a bit hacky, reliant on specific return handling
    //; 
    push        {lr}
    ldrb        r2, [r2, #4]
    mov         r3, #1
    lsl         r3, r2
    @@Get1:
    ldr         r2, =gArchipelago
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

.pool

HatchLockRuby:
//; rather jank, but the alternative is digging in a bunch of collision code
//; i'm not insane enough for that
    push        {r2, lr}
    mov         r0, #0
    @@Get1:
    ldr         r2, =gArchipelago
    ldrb        r2, [r2, #10]
    cmp         r2, #0
    beq         @@Set
    mov         r0, #2
    @@Set:
    add         r1, #0x25
    pop         {r2, lr}
    .align 4

HatchLockSapphire:
//; Sapphire is easy though, but a little hacky
    push        {r0-r2}
    ldrh        r0, [r4, r0]
    @@Get1:
    ldr         r2, =gArchipelago
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

.pool

GetArrowsSapphire:
    add         r0, #1
    nop

GetArrows:
    push        {r2, lr}
    cmp         r0, #2
    ble         @@Set
    nop
    @@Get1:
    ldr         r2, =gArchipelago
    ldrb        r2, [r2, #8]
    cmp         r2, #0
    bne         @@Set
    @@True:
    mov         r0, #2
    @@Set:
    strb        r0, [r1, #0]
    pop         {r2, lr}
    .align 4

.pool

.endarea

.org EReaderMain
.area 0x1154
//; cannibalize the EReader functionality, we fake rando the cards anyways
EvoArrows:
    push        {r2, lr}
    add         r0, #1
    @@Get1:
    ldr         r2, =gArchipelago
    ldrb        r2, [r2, #9]
    cmp         r0, r2
    bgt         @@Return
    strb        r0, [r1, #0]
    @@Return:
    pop         {r2, lr}
    .align 4

.pool

WeightsCheckEvo:
    push        {r1-r4}
    ldrb        r6, [r0, #0x15]
    @@Get1:
    ldr         r4, =gArchipelago
    ldrb        r2, [r4, #9]
    cmp         r6, #0xCD
    beq         @@Return
    cmp         r2, #3
    blt         @@Fail
    mov         r1, #1
    ldrb        r2, [r0, #0x14]
    lsl         r1, r2
    mov         r3, #0x24
    ldrh        r2, [r4, r3]
    and         r1, r2
    cmp         r1, #0
    bne         @@Return
    @@Fail:
    mov         r6, #0xCD
    @@Return:
    pop         {r1-r4}
    add         r0, r6, #0
    bx          lr

.pool

ClamperlCheck:
    //; clamperl is a special little baby
    push        {r0-r3}
    nop
    @@Get1:
    ldr         r3, =gArchipelago
    ldrb        r2, [r3, #9]
    cmp         r2, #3
    bge         @@Return
    mov         r2, #0x24
    ldr         r3, [r3, r2]
    mov         r2, #0x10
    and         r3, r2
    cmp         r3, #0
    bne         @@Return
    mov         r0, #0xBA
    add         lr, r0
    @@Return:
    pop         {r0-r3}
    lsl         r2, r2, #0x10
    asr         r0, r2, #0x10
    bx          lr

.pool

EggsCheckEvo:
    push        {r1-r4}
    ldrb        r5, [r0, #0x15]
    @@Get1:
    ldr         r2, =gArchipelago
    ldrb        r2, [r2, #9]
    cmp         r5, #0xCD
    beq         @@Return
    cmp         r2, #3
    blt         @@Fail
    mov         r1, #1
    ldrb        r2, [r0, #0x14]
    lsl         r1, r2
    mov         r3, #0x24
    ldrh        r2, [r4, r3]
    and         r1, r2
    cmp         r1, #0
    bne         @@Return
    @@Fail:
    mov         r5, #0xCD
    @@Return:
    pop         {r1-r4}
    add         r0, r5, #0
    bx          lr

.pool

EggGroups:
    //; r0- current species, r4 - gCurrentPinballGame, r12 - gMain, r8 - species index shifted 0x10 left
    lsl         r0, r5, #0x10
    asr         r0, r0, #0x10
    push        {r0}
    nop
    @@Get1:
    ldr         r2, =EggTableRuby | 0x8000000
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
    ldr         r2, =gArchipelago
    ldr         r2, [r2, #0x20]
    and         r2, r0
    pop         {r0}
    cmp         r2, #0
    bne         @@Return
    mov         r1, r0
    @@Return:
    bx          lr

.pool

SetBonusComplete:
    push        {r2-r4, lr}
    ldrb        r0, [r1, #0x04]
    sub         r0, #2
    //; r0 is return value here, but it's still useful
    mov         r2, #1
    @@Get:
    ldr         r3, =gArchipelago
    lsl         r2, r0
    ldrb        r4, [r3, #0xD]
    orr         r2, r4
    strb        r2, [r3, #0xD]
    ldr         r4, =GoalTrigger
    ldrb        r4, [r4, #0]
    cmp         r4, #1
    beq         @@GroudonKyogre
    cmp         r4, #2
    bne         @@Return
    @@Rayquaza:
    cmp         r0, #4
    bne         @@Return
    @@Check:
    mov         r2, r0
    bl          CheckGoal
    cmp         r0, #0
    beq         @@ReturnCheck
    mov         r4, #0x2F
    strb        r0, [r3, r4]
    ldr         r3, =gArchipelagoStringEnable
    mov         r4, #3
    strb        r4, [r3, #0]
    mov         r4, #0
    strh        r4, [r3, #2]
    @@ReturnCheck:
    mov         r0, r2
    @@Return:
    pop         {r2-r4, pc}
    @@GroudonKyogre:
    cmp         r0, #2
    beq         @@Check
    cmp         r0, #3
    beq         @@Check
    b           @@Return
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
    ldr         r3, =gArchipelago
    lsl         r2, #3
    @@Get2:
    ldr         r1, =gSpeciesInfo
    ldr         r5, [r5, #0]
    ldrh        r2, [r5, r2]
    cmp         r2, #88
    beq         @@Gloom
    cmp         r2, #175
    beq         @@Clamperl
    cmp         r2, #13
    beq         @@Wurmple
    mov         r4, #0x18
    mul         r2, r4
    add         r1, r2
    ldrb        r2, [r1, #0x14]
    @@Check:
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
    @@Wurmple:
    mov         r2, #1
    b           @@Check
    @@Clamperl:
    mov         r2, #4
    b           @@Check
    //; the complex one
    nop
    @@Gloom:
    ldr         r2, =gMain
    ldrb        r2, [r2, #4]
    cmp         r2, #0
    bne         @@Sapphire
    mov         r2, #2
    b           @@Check
    @@Sapphire:
    mov         r2, #8
    b           @@Check
    .align      4


.pool

CheckAnyMonEvo:
//; r0 - evolvablePartySize
//; returns 0 in r0 if no evolvable, else 1
//; r6 - AP, r5 - currentPinballGame, r4 - gSpeciesInfo, r3 - evolvePartyIndex,  r1/r2 flex

    push        {r1-r6}
    cmp         r0, #0 //; trivial false
    beq         @@False
    mov         r3, #0
    @@Get1:
    ldr         r5, =gCurrentPinballGame
    ldr         r5, [r5, #0]
    @@Get2:
    ldr         r4, =gSpeciesInfo
    mov         r2, #0x9C
    @@Get3:
    ldr         r6, =gArchipelago
    lsl         r2, #2
    add         r5, r2
    @@Loop:
    ldrb        r2, [r5, r3]
    cmp         r2, #88
    beq         @@Gloom
    cmp         r2, #175
    beq         @@Clamperl
    cmp         r2, #13
    beq         @@Wurmple
    mov         r1, #0x18
    mul         r2, r1
    add         r1, r4, r2
    ldrb        r2, [r1, #0x14]
    @@Check:
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
    @@Wurmple:
    mov         r2, #1
    b           @@Check
    @@Clamperl:
    mov         r2, #4
    b           @@Check
    @@Gloom:
    //; the complex one
    ldr         r2, =gMain
    ldrb        r2, [r2, #4]
    cmp         r2, #0
    bne         @@Sapphire
    mov         r2, #2
    b           @@Check
    @@Sapphire:
    mov         r2, #8
    b           @@Check
    .align      4


.pool

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
    ldr         r2, =gArchipelago
    ldrb        r2, [r2, #14]
    cmp         r0, r2
    bgt         @@Return
    strb        r0, [r1, #0]
    @@Return:
    pop         {r2, lr}
    .align 4

.pool

DoubleCoin:
//; doubles as ringlink packet sender
    push        {r0-r3, lr}
    mov         r2, #0xCA
    @@Get1:
    ldr         r3, =gArchipelago
    ldrb        r1, [r3, #4]
    lsl         r2, #1
    add         r0, r2
    ldrb        r2, [r0, #0]
    cmp         r1, #0
    beq         @@Return
    lsl         r2, #1
    strb        r2, [r0, #0]
    @@Return:
    mov         r1, #0x2D
    strb        r2, [r3, r1]
    pop         {r0-r3, pc}
    .align      4

.pool

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
    ldr         r2, =gArchipelago
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

.pool

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
    ldr         r2, =gTitlescreen
    ldrb        r2, [r2, #6]
    cmp         r2, #1
    bne         @@Return
    mov         r2, #0x29
    @@Get:
    ldr         r3, =gArchipelago
    strb        r0, [r1, #0]
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3, pc}
    .align      4

.pool

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
    push        {r0-r5, lr}
    mov         r2, #0xE7
    @@GetPinball:
    ldr         r4, =gCurrentPinballGame
    ldr         r4, [r4, #0]
    @@GetWild:
    ldr         r3, =gWildMonLocations
    lsl         r2, #3
    add         r2, #5
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
    @@GetAP:
    ldr         r5, =gArchipelago
    mov         r0, #0
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
    pop         {r0-r5, pc}
    bx          lr
    .align      4

.pool

ForceEgg:
    mov         r9, r4
    mov         r10, r5
    push        {r0-r5}
    mov         r2, #0x4
    @@GetMain:
    ldr         r1, =gMain
    ldrb        r1, [r1, r2]
    @@GetWild:
    ldr         r3, =gEggLocations
    mov         r2, #0
    @@GetPinball:
    ldr         r4, =gCurrentPinballGame
    ldr         r4, [r4, #0]
    cmp         r1, #0
    beq         @@ContinueSetup
    add         r3, #0x34
    @@ContinueSetup:
    mov         r2, #0x98
    lsl         r2, #1
    add         r4, r2
    @@GetAP:
    ldr         r5, =gArchipelago
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
    mov         r2, #0x1E
    mov         r1, #0x2E
    strb        r2, [r5, r1]
    sub         r4, #2
    ldrh        r1, [r4, #0]
    add         r4, #2
    strh        r1, [r4, r0]
    @@Return:
    pop         {r0-r5}
    bx          lr
    .align      4

.pool

SetSphealCheck:
    //; r2 - gCurrentPinballGame
    lsl         r0, #2
    strh        r0, [r3, #0]
    push        {r0-r4}
    mov         r3, #0xA6
    @@Get:
    ldr         r1, =gArchipelago
    lsl         r3, #3
    sub         r3, #4
    ldrb        r0, [r2, r3]
    add         r3, #1
    ldrb        r3, [r2, r3]
    mov         r4, r0
    add         r4, r3
    mov         r2, #0
    cmp         r0, #5
    blt         @@Pokeballs
    add         r2, #1
    @@Pokeballs:
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

.pool

UpdateBumperCount:
    push        {r0-r3}
    ldr         r2, =gTitlescreen
    ldrb        r2, [r2, #6]
    cmp         r2, #1
    bne         @@Return
    mov         r2, #0x28
    @@Get:
    ldr         r3, =gArchipelago
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

.pool

UpdateRubyUpgrade:
    push        {r0-r4}
    ldr         r2, =gTitlescreen
    ldrb        r2, [r2, #6]
    cmp         r2, #1
    bne         @@Return
    mov         r2, #0x2A
    @@Get:
    ldr         r3, =gArchipelago
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r4}
    strb        r4, [r3, #0]
    ldr         r0, [r5, #0]
    bx          lr
    .align      4

.pool

UpdateSapphireUpgrade:
    push        {r0-r3}
    ldr         r2, =gTitlescreen
    ldrb        r2, [r2, #6]
    cmp         r2, #1
    bne         @@Return
    mov         r2, #0x2B
    @@Get:
    ldr         r3, =gArchipelago
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3}
    strb        r4, [r3, #0]
    mov         r3, r9
    bx          lr
    .align      4

.pool

UpdateMakuUpgrade:
    push        {r0-r3}
    ldr         r2, =gTitlescreen
    ldrb        r2, [r2, #6]
    cmp         r2, #1
    bne         @@Return
    mov         r2, #0x2C
    @@Get:
    ldr         r3, =gArchipelago
    ldrb        r0, [r3, r2]
    cmp         r0, #99
    bge         @@Return
    add         r0, #1
    strb        r0, [r3, r2]
    @@Return:
    pop         {r0-r3}
    add         r0, r2
    strb        r1, [r0, #0]
    bx          lr
    .align      4

.pool

ClearForceSpecial:
    push        {r1, r2}
    mov         r1, #0
    mov         r2, #0x96
    lsl         r2, #1
    sub         r2, #1
    strb        r1, [r0, r2]
    pop         {r1, r2}
    add         r0, r2
    strh        r1, [r0, #0]
    bx          lr

ClearForcePichu:
    push        {r1, r2}
    mov         r1, #0
    mov         r2, #0x96
    lsl         r2, #1
    sub         r2, #1
    strb        r1, [r0, r2]
    pop         {r1, r2}
    add         r0, r4
    strh        r1, [r0, #0]
    bx          lr

ShopBlockHelpers:
    add         r0, r1
    ldrh        r0, [r0, #0]
    cmp         r0, #22
    beq         @@MainRuby
    cmp         r0, #23
    bne         @@ReturnQuick
    mov         r3, #1
    @@Main:
    push        {lr}
    bl          CheckHelper
    pop         {r2}
    cmp         r0, #1
    bge         @@Skip
    add         r2, #0x12
    @@Get:
    ldr         r3, =#999
    @@Skip:
    bx          r2
    @@MainRuby:
    mov         r3, #3
    b           @@Main
    @@ReturnQuick:
    bx          lr
    .align      4

.pool

HandleAreas:
    push        {r0-r6}
    nop
    @@Get1:
    ldr         r6, =gCurrentPinballGame
    ldr         r1, [r6, #0] //; gCurrentPinballGame, have to do this here for alignment purposes
    @@Get2:
    ldr         r5, =gMain
    add         r1, #0x32
    ldrb        r0, [r1, #0] //; get current stage
    ldrb        r3, [r5, #4] //; board
    @@Get3:
    ldr         r2, =gArchipelago+0x10
    cmp         r3, #0
    beq         @@Compare
    add         r2, #7
    @@Compare:
    mov         r5, r0
    add         r0, #1
    mov         r3, #0
    mov         r4, #1
    @@CompComp:
    cmp         r0, #6
    blt         @@Loop
    mov         r0, #0
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
    b           @@CompComp
    @@Return:
    pop         {r0-r6}
    bx          lr
    .align 4

.pool

HandleRuinsCardTravel:
    push        {r0-r6}
    nop
    @@Get1:
    ldr         r6, =gCurrentPinballGame
    ldr         r1, [r6, #0] //; gCurrentPinballGame, have to do this here for alignment purposes
    @@Get2:
    ldr         r5, =gMain
    add         r1, #0x32
    mov         r0, #0 //; start at 0 for checking purposes
    ldrb        r3, [r5, #4] //; board
    @@Get3:
    ldr         r2, =gArchipelago+0x10
    cmp         r3, #0
    beq         @@Compare
    add         r2, #7
    @@Compare:
    mov         r5, r0
    mov         r3, #0
    mov         r4, #1
    @@CompComp:
    cmp         r0, #6
    blt         @@Loop
    mov         r0, #0
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
    b           @@CompComp
    @@Return:
    pop         {r0-r6}
    bx          lr
    .align 4

.pool

CheckRuinsAndCard:
//; assume r0 holds the current card status
//; return r0 & ruins status
    push        {r1-r3}
    cmp         r0, #0
    beq         @@Return
    mov         r2, #0
    ldr         r1, =gMain
    ldrb        r1, [r1, #4]
    ldr         r3, =gArchipelago+0x10
    cmp         r1, #0
    beq         @@Check
    mov         r2, #7
    @@Check:
    add         r3, r2
    ldrb        r1, [r3, #6]
    and         r0, r1
    @@Return:
    pop         {r1-r3}
    bx          lr
    .pool

CheckRuinsAndCardEx:
    push        {r0, lr}
    ldrh        r0, [r0, r1]
    bl          CheckRuinsAndCard
    mov         r1, r0
    cmp         r1, #0
    pop         {r0, pc}


CheckRuinsAndCardRoulette:
    push        {lr}
    mov         r1, #4
    strb        r1, [r0, #0]
    mov         r0, #1 //; can only reach this codepath with card enabled
    bl          CheckRuinsAndCard
    pop         {r1}
    cmp         r0, #0
    bne         @@Return
    add         r1, #0x22
    @@Return:
    bx          r1

RingLinkRoulette:
    add         r2, r1
    strb        r0, [r2, #0]
    ldr         r2, =gArchipelago
    mov         r1, #0x2D
    strb        r0, [r2, r1]
    bx          lr

.pool

RingLinkShop:
    sub         r0, r3
    strb        r0, [r1, #0]
    ldr         r2, =gArchipelago
    mov         r0, #0x2E
    strb        r3, [r2, r0]
    bx          lr

.pool

PrepareTextDisplay:
    push            {r0-r3}
    ldr             r3, =gBG0TilemapBuffer
    mov             r0, #0xA0
    lsl             r0, #2
    add             r1, r3, r0
    mov             r2, #0x0
    mov             r0, #0x20
    @@Loop:
    strh            r2, [r1, #0]
    add             r1, #2
    sub             r0, #1
    cmp             r0, #0
    bne             @@Loop
    pop             {r0-r3}
    bx              lr

.pool

CleanTextDisplay:
    push            {r0-r3}
    ldr             r3, =gBG0TilemapBuffer
    mov             r0, #0xA0
    lsl             r0, #2
    add             r1, r3, r0
    ldr             r2, =0x1FF
    mov             r0, #0x20
    @@Loop:
    strh            r2, [r1, #0]
    add             r1, #2
    sub             r0, #1
    cmp             r0, #0
    bne             @@Loop
    @@GetTilemap:
    ldr             r1, =0x040000D4
    str             r3, [r1, #0]
    @@GetAddr:
    ldr             r0, =0x6002000
    str             r0, [r1, #4]
    @@GetSetting:
    ldr             r0, =0x80000400
    str             r0, [r1, #8]
    ldr             r0, [r1, #8]
    pop             {r0-r3}
    bx              lr

.pool

DisplayText:
    //; reuse the debug display for this basically
    //; assume we've already called the tilemap handling, we just want to trigger the display
    ldr             r3, =gBG0TilemapBuffer
    mov             r0, #0xA0
    lsl             r0, #2
    add             r1, r3, r0
    mov             r2, #0xC1
    lsl             r2, #8
    mov             r0, #0x20
    @@Loop:
    ldrh            r4, [r1, #0]
    add             r4, r2
    strh            r4, [r1, #0]
    add             r1, #2
    sub             r0, #1
    cmp             r0, #0
    bne             @@Loop
    @@GetTilemap:
    ldr             r1, =0x040000D4
    str             r3, [r1, #0]
    @@GetAddr:
    ldr             r0, =0x6002000
    str             r0, [r1, #4]
    @@GetSetting:
    ldr             r0, =0x80000400
    str             r0, [r1, #8]
    ldr             r0, [r1, #8]
    bx              lr
    .align          4

.pool

DisplayTextR0:
    push            {r1-r4, lr}
    bl              PrepareTextDisplay
    mov             r1, #10
    mov             r2, #0
    bl              DrawTextToTilemap
    bl              DisplayText
    pop             {r1-r4, lr}

.pool

PopulateItemString:
    push            {r1-r5, lr}
    ldr             r0, =gArchipelagoStrings
    ldr             r1, =ReceivedItemText
    mov             r2, #9
    bl              memcpy
    add             r0, #9
    mov             r4, r0
    ldr             r1, =gArchipelagoStringItem
    ldrh            r0, [r1, #0]
    mov             r2, r0
    lsr             r2, #8
    lsl             r2, #2
    ldr             r1, =ItemTypeTable
    ldr             r2, [r1, r2]
    mov             r1, #0xFF
    and             r0, r1
    lsl             r0, #2
    ldr             r1, [r2, r0]
    mov             r5, r1
    mov             r0, r1
    bl              strlen
    mov             r2, r0
    mov             r0, r4
    mov             r1, r5
    add             r5, r0, r2
    bl              memcpy
    mov             r0, #0
    strb            r0, [r5, #0]
    ldr             r0, =gArchipelagoStrings
    pop             {r1-r5, pc}

.pool

PopulatePlayerString:
    push            {r1-r5, lr}
    ldr             r0, =gArchipelagoStrings
    ldr             r1, =FromText
    mov             r2, #5
    bl              memcpy
    add             r0, #5
    mov             r4, r0
    ldr             r1, =gArchipelagoStringPlayer
    ldr             r0, [r1, #0]
    ldr             r2, =MaxPlayerString
    ldr             r2, [r2, #0]
    cmp             r0, r2
    bgt             @@GenericPlayer
    //; quick special case, if player is negative it's given by server
    ldr             r2, =#-1
    cmp             r0, r2
    beq             @@CheatConsole
    ldr             r2, =#-2
    cmp             r0, r2
    beq             @@Server
    ldr             r2, =PlayerTable
    lsl             r0, #2
    ldr             r5, [r2, r0]
    @@DisplaySpecific:
    mov             r0, r5
    bl              strlen
    mov             r2, r0
    mov             r1, r5
    mov             r0, r4
    add             r4, r2
    bl              memcpy
    mov             r1, #0
    strb            r1, [r4, #0]
    ldr             r0, =gArchipelagoStrings
    b               @@Return
    @@CheatConsole:
    ldr             r5, =Cheat
    b               @@DisplaySpecific
    @@Server:
    ldr             r5, =Server
    b               @@DisplaySpecific

    @@GenericPlayer:
    mov             r5, r0
    mov             r0, r4
    ldr             r1, =PlayerTable
    ldr             r1, [r1, #0] //; player 0 is the generic player
    mov             r2, #7
    bl              memcpy
    add             r0, #7
    mov             r1, r0
    mov             r0, r5
    mov             r2, #0
    mov             r3, #1
    bl              FormatIntToString //; returns pointer to last value of r1
    mov             r1, #0
    strb            r1, [r0, #1]
    ldr             r0, =gArchipelagoStrings
    @@Return:
    pop             {r1-r5, pc}

.pool

PopulateGoalString:
    push            {r1-r4, lr}
    ldr             r4, =GoalClearText
    mov             r0, r4
    bl              strlen
    mov             r1, r4
    mov             r2, r0
    ldr             r0, =gArchipelagoStrings
    add             r4, r0, r2
    bl              memcpy
    mov             r0, #0
    strb            r0, [r4, #0]
    ldr             r0, =gArchipelagoStrings
    pop             {r1-r4, pc}

.pool

StringHandlingMainLoop:
    push            {r0-r7, lr}
    ldr             r7, =gArchipelagoStringEnable
    ldrb            r1, [r7, #0]
    cmp             r1, #0
    beq             @@Return
    @@Item:
    cmp             r1, #1
    bne             @@Player
    ldrh            r2, [r7, #2]
    cmp             r2, #0
    bne             @@DecrementItem
    bl              PopulateItemString
    bl              DisplayTextR0
    mov             r2, #0x96
    strh            r2, [r7, #2]
    b               @@Return
    @@DecrementItem:
    sub             r2, #1
    strh            r2, [r7, #2]
    cmp             r2, #0
    beq             @@MoveToPlayer
    b               @@Return
    @@MoveToPlayer:
    mov             r1, #2
    strb            r1, [r7, #0]
    b               @@Return
    @@Player:
    cmp             r1, #2
    bne             @@Goal
    ldrh            r2, [r7, #2]
    cmp             r2, #0
    bne             @@DecrementPlayer
    bl              PopulatePlayerString
    bl              DisplayTextR0
    mov             r2, #0x96
    strh            r2, [r7, #2]
    b               @@Return
    @@DecrementPlayer:
    sub             r2, #1
    strh            r2, [r7, #2]
    cmp             r2, #0
    beq             @@ClearDisplay
    b               @@Return
    @@Goal:
    cmp             r1, #3
    bne             @@ClearDisplay
    ldrh            r2, [r7, #2]
    cmp             r2, #0
    bne             @@DecrementGoal
    bl              PopulateGoalString
    bl              DisplayTextR0
    mov             r2, #0x96
    lsl             r2, #1
    strh            r2, [r7, #2]
    b               @@Return
    @@DecrementGoal:
    sub             r2, #1
    strh            r2, [r7, #2]
    cmp             r2, #0
    beq             @@ClearDisplay
    b               @@Return
    @@ClearDisplay:
    bl              CleanTextDisplay
    @@ClearInfo:
    mov             r1, #0
    strb            r1, [r7, #0]
    strh            r1, [r7, #2]
    @@Return:
    pop             {r0-r7}
    ldr             r4, =gMain
    ldrb            r1, [r4, #0xF]
    pop             {pc}
.pool

CheckGoal:
    push        {r1-r7, lr}
    mov         r2, #1
    @@GetGoalVal:
    ldr         r1, =GoalValue
    ldrh        r1, [r1, #0]
    @@GetSavePtr1:
    ldr         r5, =gMain
    ldr         r6, =gCurrentPinballGame
    ldr         r6, [r6, #0]
    and         r2, r1
    beq         @@Score
    @@GetGoalDexNum:
    ldr         r2, =GoalDexNum
    ldrh        r2, [r2, #0]
    mov         r7, #0
    mov         r3, #0x74
    add         r3, r5
    mov         r4, #0
    @@LoopDexNum:
    ldrb        r0, [r3, r7]
    cmp         r0, #4
    bne         @@SkipDexNum
    add         r4, #1
    @@SkipDexNum:
    add         r7, #1
    cmp         r7, #0xCD
    ble         @@LoopDexNum
    //; now we're through, r4 has our num
    cmp         r4, r2
    blt         @@ReturnFalse
    @@Score:
    mov         r2, #2
    and         r2, r1
    beq         @@Targets
    mov         r7, r1
    @@GetGoalScore:
    ldr         r2, =GoalScoreLow
    ldr         r4, [r2, #4]
    ldr         r3, [r2, #0]
    mov         r2, #0
    @@HighScoreLoop:
    push        {r2-r4}
    mov         r0, r4
    mov         r1, r3
    bl          GetNewHighScoreIndex
    pop         {r2-r4}
    cmp         r0, #0
    beq         @@TargetsRestore //; if 0 is returned, this is higher than all reported high scores. if any other value is returned, there's a high score greater than this
    add         r2, #1
    cmp         r2, #2
    blt         @@HighScoreLoop
    @@CheckCurrentScore:
    mov         r0, r4
    mov         r1, r3
    mov         r2, #0x44
    ldr         r3, [r6, r2]
    add         r2, #4
    ldr         r2, [r6, r2]
    bl          CompareScores
    cmp         r0, #0
    bgt         @@ReturnFalse
    @@TargetsRestore:
    mov         r1, r7
    @@Targets:
    mov         r2, #4
    and         r2, r1
    beq         @@Medals
    @@GetGoalDexTargets:
    ldr         r7, =GoalDexTarget
    push        {r1}
    mov         r3, #0
    mov         r4, #0x74
    @@TargetLoop:
    ldrb        r2, [r7, r3]
    mov         r1, #0
    @@TargetCheck:
    mov         r0, #1
    lsl         r0, r1
    and         r0, r2
    beq         @@TargetContinue
    ldrb        r0, [r5, r4]
    cmp         r0, #4
    bne         @@ReturnFalseTarget
    @@TargetContinue:
    add         r4, #1
    add         r1, #1
    cmp         r1, #8
    blt         @@TargetCheck
    mov         r1, #0
    add         r3, #1
    cmp         r3, #26
    blt         @@TargetLoop
    pop         {r1}
    b           @@Medals
    @@ReturnFalseTarget:
    pop         {r1}
    b           @@ReturnFalse
    @@Medals:
    mov         r2, #8
    and         r2, r1
    beq         @@ReturnTrue
    nop
    @@GetGoalMedals:
    ldr         r2, =GoalMedals
    ldrb        r2, [r2, #0]
    @@GetGoalAP:
    ldr         r3, =gArchipelago
    ldrb        r3, [r3, #0xF]
    cmp         r3, r2
    blt         @@ReturnFalse
    @@ReturnTrue:
    mov         r0, #1
    b           @@Return
    @@ReturnFalse:
    mov         r0, #0
    @@Return:
    pop         {r1-r7, pc}
    .align      4

.pool

CheckGoalEndOfBall:
    push        {r0-r4, lr}
    bl          ClearDebugTextDisplay
    bl          CheckGoal
    beq         @@Return
    ldr         r1, =GoalTrigger
    ldrb        r1, [r1, #0]
    cmp         r1, #0
    bne         @@Return
    ldr         r1, =gArchipelago
    mov         r2, #0x2F
    strb        r0, [r1, r2]
    ldr         r1, =gArchipelagoStringEnable
    mov         r0, #3
    strb        r0, [r1, #0]
    mov         r0, #0
    strh        r0, [r1, #2]
    @@Return:
    pop         {r0-r4, pc}

.pool

.endarea

.org 0x86BC000
.byte "ARCHIPELAGO_DATA"
.fill 16
//; world version
.byte 0x00, 0x00, 0x00
//; basepatch version (if i remember to update it lol)
.byte 0x00, 0x03, 0x00
//; slot data at 0x6BC030
.org 0x86BC030
GoalValue:
.hword 0x01
GoalDexNum:
.hword 0x01
GoalScoreLow:
.word 0x0
GoalScoreHigh:
.word 0x0
GoalDexTarget:
.fill 26
GoalMedals:
.byte 0x00
GoalTrigger:
.byte 0x00
.org 0x86BC080
EggTableRuby:
.byte 0x00, 0x02, 0x03, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0F, 0x10, 0x11, 0x12, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1D, 0x1E, 0x1F
.align 32
EggTableSapphire:
.byte 0x00, 0x01, 0x03, 0x04, 0x06, 0x07, 0x09, 0x0A, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F
.align 32
.org 0x86BC100
GoalClearText:
.byte "GOAL COMPLETE!", 0x00
ReceivedItemText:
.byte "RECEIVED ", 0x00
FromText:
.byte "FROM ", 0x00
.align 4
ItemTypeTable:
.word StandardItemStrTable, AreaItemStrTable, FillerItemStrTable, 0x0, EvolutionItemStrTable, 0x0, 0x0, 0x0, HelperItemStrTable, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0
StandardItemStrTable: //; have to offset by 1 because 0 index is reserved
.word 0x0, RubyBoard, SapphireBoard, StartingBall, StartingCoins, StartingModifier, PermPichu
.word SpecialGuests, EncounterRate, RuinsAreaCard, GetArrow, EvoArrow, EvoMode, ChikoritaDex
.word CyndaquilDex, TotodileDex, AerodactylDex, EggForest, EggCave, EggMountain, EggDesert, EggSea
.word EggRuby, EggSapphire, CoinArrow, CoinModifier, PokedexMedal
AreaItemStrTable:
.word ForestRuby, VolcanoRuby, PlainsRuby, OceanRuby, SafariZoneRuby, CaveRuby, RuinsRuby
.word ForestSapphire, LakeSapphire, PlainsSapphire, WildernessSapphire, OceanSapphire, CaveSapphire, RuinsSapphire
FillerItemStrTable:
.word ExtraBall, Big, Small, BallSaver
EvolutionItemStrTable:
.word RareCandy, RareCandy, LeafStone, FireStone, LinkCable, MoonStone, WaterStone, ThunderStone, SunStone, SootheBell, DryPokeblock
HelperItemStrTable:
.word HelperZigzagoon, HelperPelipper, HelperMakuhita, HelperWhiscash
StartingBall:
.byte "+1 STARTING LIFE", 0x00
StartingModifier:
.byte "+1 STARTING MODIFIER", 0x00
StartingCoins:
.byte "+10 STARTING COINS", 0x00
PermPichu:
.byte "PERMANENT PICHU", 0x00
SpecialGuests:
.byte "SPECIAL GUESTS CARD", 0x00
EncounterRate:
.byte "ENCOUNTER RATE UP CARD", 0x00
RuinsAreaCard:
.byte "RUINS AREA CARD", 0x00
RubyBoard:
.byte "RUBY BOARD", 0x00
SapphireBoard:
.byte "SAPPHIRE BOARD", 0x00
EvoArrow:
.byte "EVO ARROW", 0x00
GetArrow:
.byte "GET ARROW", 0x00
CoinArrow:
.byte "COIN ARROW", 0x00
CoinModifier:
.byte "DOUBLE COINS", 0x00
PokedexMedal:
.byte "POKEDEX MEDAL ", 0x00 //; extend in code to show counts
EvoMode:
.byte "EVO MODE", 0x00
ChikoritaDex:
.byte "CHIKORITA DEX ENTRY", 0x00
CyndaquilDex:
.byte "CYNDAQUIL DEX ENTRY", 0x00
TotodileDex:
.byte "TOTODILE DEX ENTRY", 0x00
AerodactylDex:
.byte "AERODACTYL DEX ENTRY", 0x00
EggForest:
.byte "EGG BUNCH (FOREST)", 0x00
EggCave:
.byte "EGG BUNCH (CAVE)", 0x00
EggMountain:
.byte "EGG BUNCH (MOUNTAIN)", 0x00
EggDesert:
.byte "EGG BUNCH (DESERT)", 0x00
EggSea:
.byte "EGG BUNCH (SEA)", 0x00
EggRuby:
.byte "EGG BUNCH (RUBY)", 0x00
EggSapphire:
.byte "EGG BUNCH (SAPPHIRE)", 0x00
RareCandy:
.byte "RARE CANDY", 0x00
LeafStone:
.byte "LEAF STONE", 0x00
FireStone:
.byte "FIRE STONE", 0x00
LinkCable:
.byte "LINK CABLE", 0x00
MoonStone:
.byte "MOON STONE", 0x00
WaterStone:
.byte "WATER STONE", 0x00
ThunderStone:
.byte "THUNDER STONE", 0x00
SunStone:
.byte "SUN STONE", 0x00
SootheBell:
.byte "SOOTHE BELL", 0x00
DryPokeblock:
.byte "DRY POKEBLOCKS", 0x00
ForestRuby:
.byte "FOREST (RUBY)", 0x00
VolcanoRuby:
.byte "VOLCANO (RUBY)", 0x00
PlainsRuby:
.byte "PLAINS (RUBY)", 0x00
OceanRuby:
.byte "OCEAN (RUBY)", 0x00
SafariZoneRuby:
.byte "SAFARI ZONE (RUBY)", 0x00
CaveRuby:
.byte "CAVE (RUBY)", 0x00
RuinsRuby:
.byte "RUINS (RUBY)", 0x00
ForestSapphire:
.byte "FOREST (SAPPHIRE)", 0x00
LakeSapphire:
.byte "LAKE (SAPPHIRE)", 0x00
PlainsSapphire:
.byte "PLAINS (SAPPHIRE)", 0x00
OceanSapphire:
.byte "OCEAN (SAPPHIRE)", 0x00
WildernessSapphire:
.byte "WILDERNESS (SAPPHIRE)", 0x00
CaveSapphire:
.byte "CAVE (SAPPHIRE)", 0x00
RuinsSapphire:
.byte "RUINS (SAPPHIRE)", 0x00
HelperZigzagoon:
.byte "HELPER ZIGZAGOON", 0x00
HelperMakuhita:
.byte "HELPER MAKUHITA", 0x00
HelperWhiscash:
.byte "HELPER WHISCASH", 0x00
HelperPelipper:
.byte "HELPER PELIPPER", 0x00
ExtraBall:
.byte "EXTRA BALL", 0x00
Big:
.byte "BIG", 0x00
Small:
.byte "SMALL", 0x00
BallSaver:
.byte "30 SEC. BALL SAVER", 0x00
Server:
.byte "ARCHIPELAGO", 0x00
Cheat:
.byte "CHEAT CONSOLE", 0x00
.align 4
MaxPlayerString:
.word 0x00
PlayerTable:
.word Player0
.fill 254*4 //; this is gonna be flexible, since we have the entire rest of the rom to work with currently
//; we allocate 255 initially, but we rewrite the entire table on generation
Player0:
.byte "PLAYER ", 0x00 //; generic player, manually place the number following (special case)

.notice "Max Player: " + orga(MaxPlayerString)
.close