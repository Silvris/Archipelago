# Monster Hunter Freedom Unite Randomizer Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases).
- [The newest nightly build of PPSSPP](https://www.ppsspp.org/devbuilds/). Build must be equal or newer than devbuild v1.19.3-725.
- Monster Hunter Freedom Unite (`ULUS10391`, `ULES01213`) or Monster Hunter Portable 2nd (`ULJM05500`)

## Installation Procedures

1. Download and install Archipelago from the link above, making sure to install the most recent version.
   **The installer file is located in the assets section at the bottom of the version information**.
    - During generation/patching, you will be asked to locate your base ROM file. This is your Kirby's Dream Land 3 ROM file.

2. Download and setup PPSSPP from the link above. In PPSSPP's settings, navigate to Tools -> Developer tools and enable "Allow remote debugger".
You may get a firewall prompt here, allow PPSSPP.

## Create a Config (.yaml) File

### What is a config file and why do I need one?

Your config file contains a set of configuration options which provide the generator with information about how it
should generate your game. Each player of a multiworld will provide their own config file. This setup allows each player
to enjoy an experience customized for their taste, and different players in the same multiworld can all have different
options.

See the guide on setting up a basic YAML at the Archipelago setup
guide: [Basic Multiworld Setup Guide](/tutorial/Archipelago/setup/en)

### Where do I get a config file?

The [Player Options](/games/Monster%20Hunter%20Freedom%20Unite/player-options) page on the website allows you to configure
your personal options and export a config file from them.

### Verifying your config file

If you would like to validate your config file to make sure it works, you may do so on the
[YAML Validator](/mysterycheck) page.

## Generating a Single-Player Game

1. Navigate to the [Player Options](/games/Monster%20Hunter%20Freedom%20Unite/player-options) page, configure your options,
   and click the "Generate Game" button.
2. You will be presented with a "Seed Info" page.
3. Click the "Create New Room" link.
4. You will be presented with a server page.
5. Double-click on your player name, and AP will open the client and connect you to the server.
6. If the client does not automatically connect to PPSSPP while it is opened, run `/psp` in the client to connect.

## Joining a MultiWorld Game
### Basic Concept

When you join a multiworld game, you will be asked to provide your config file to whoever is hosting. Once that is done,
the host will provide you with the link to the room. From there, just follow step 4+ in the single player guide.

## Hosting a MultiWorld game

The recommended way to host a game is to use our [hosting service](/generate). The process is relatively simple:

1. Collect config files from your players.
2. Create a zip file containing your players' config files.
3. Upload that zip file to the website linked above.
4. Wait a moment while the seed is generated.
5. When the seed is generated, you will be redirected to a "Seed Info" page.
6. Click "Create New Room". This will take you to the server page. Provide the link to this page to your players, so
   they may download their patch files from there.
7. Note that a link to a MultiWorld Tracker is at the top of the room page. The tracker shows the progress of all
   players in the game. Any observers may also be given the link to this page.
8. Once all players have joined, you may begin playing.
