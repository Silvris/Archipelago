# Pokémon Pinball Ruby & Sapphire

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What does randomization do to this game?

Board features such as Hatch Mode and Evo Mode are locked behind progression in the multiworld, as well as starting lives and coins.
Areas that can be traveled to are also locked behind multiworld progression, as well as one of the two boards.
E-reader cards can be received and activated to skip progression usually locked behind very long pinball games.

## What Pokémon Pinball Ruby & Sapphire items can appear in other players' worlds?
- Ruby Board
- Sapphire Board
- Extra Starting Ball
- +10 Starting Coins
- Starting Ball Modifier
- Permanent Pichu Upgrade
- e-Reader Card - Special Guests
  - Forces the next Catch'em Mode to be one of Chikorita/Cyndaquil/Totodile/Aerodactyl
- e-Reader Card - Encounter Rate Up
  - Doubles the appearance rate of rare Pokémon
- e-Reader Card - Ruins Area
  - Start the game in the Ruins area (if unlocked), and set the first bonus stage to be Rayquaza
- Get Arrow
- Evo Arrow
- Egg Bunches
- Chikorita/Cyndaquil/Totodile/Aerodactyl Pokédex Entries
- BIG (score bonus)
- Small (score bonus)
- Extra Ball
- 30 Sec. Ball Saver

## What is considered a location check in Pokémon Pinball Ruby & Sapphire?
- Catching a Pokémon and registering it in the Pokédex.
- Completing a bonus stage for the first time

## When the player receives an item, what happens?
A sound effect will play based on the type of item received, and the effects of the item will be immediately applied.
Some items may only be applied the next time they are relevant, such as starting a new game.

## Unique Local Commands
- `/ereader` Used to activate E-reader Card effects. Valid entries are `Special Guests`, `Encounter Rate Up`, and 
`Ruins Area`. These effects are toggleable. `Encounter Rate Up` will be toggled on naturally by the game when Rayquaza 
is defeated for the first time in a play session.