# Mega Man 11 Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- [Mega Man 11](https://store.steampowered.com/app/742300/Mega_Man_11/)
- [Mega Man 11 Archipelago Client](https://github.com/Silvris/MegaMan11Archipelago)

## Generating a Game

1. Create your options file (YAML). You can make one using the Options Creator within the Archipelago Launcher.
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you.

## Installing the Client
1. Navigate to your Mega Man 11 installation folder (can easily access by right-clicking Mega Man 11 in Steam,
and then selecting "Manage -> Browse local files").
2. Extract `dinput8.dll` and `APCpp.dll` from the Mega Man 11 Archipelago Client zip into the Mega Man 11 installation 
folder.
3. (Linux only) Add the following launch args to Mega Man 11 in Steam: `-WINEDLLOVERRIDES=dinput8=n,b %command%`

## Uninstalling the Client
If you ever want to uninstall the client, delete the following files:
- dinput8.dll
- APCpp.dll
- imgui.ini
- mm11_archipelago.log
- /.datapkg-cache/

## Connecting to a Server

1. As the game opens, you should notice the Mega Man 11 Archipelago client in the corner.
2. Press the Connect button under the Server tab to open the connect menu.
3. Input the connection info into the relevant fields, then press Connect.
4. If connection is successful, messages should begin displaying in the client. The Goal and EnergyLink tabs should now 
show correctly.
5. The client can be toggled visible by pressing F1.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect.
