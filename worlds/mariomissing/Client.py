import logging
import struct
import typing
import time
import random
from struct import pack
from .community_questions import (question_mapping, answer_addrs,
                                  correct_answer, incorrect_answer_1,
                                  incorrect_answer_2, incorrect_answer_3,
                                  supported_categories, categories_with_questions,
                                  question_test)

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext
else:
    SNIContext = typing.Any

snes_logger = logging.getLogger("SNES")

GAME_MIM = "Mario is Missing"

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

MIM_ROMHASH_START = 0x007FC0
ROMHASH_SIZE = 0x0F

ITEM_RECEIVED = WRAM_START + 0x1550
ITEM_LIST = WRAM_START + 0x1551
DEATH_RECEIVED = WRAM_START + 0x1554
GOAL_FLAG = WRAM_START + 0x1543
VALIDATION_CHECK = WRAM_START + 0x1545
VALIDATION_CHECK_2 = WRAM_START + 0x1546
MIM_DEATHLINK_ENABLED = ROM_START + 0x0FFF11
IS_IN_QUIZ = WRAM_START + 0x154B
QUIZ_MODE = 0x0FFF13
QUESTION_DEBUG = WRAM_START + 0x1544

class MIMSNIClient(SNIClient):
    game = "Mario is Missing"

    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        validation_check_low = await snes_read(ctx, VALIDATION_CHECK, 0x1)
        if validation_check_low[0] != 0x69:
            return

        validation_check_high = await snes_read(ctx, VALIDATION_CHECK_2, 0x1)
        if validation_check_high[0] != 0x42:
            return

        snes_buffered_write(ctx, WRAM_START + 0x0565, bytes([0x84]))
        snes_buffered_write(ctx, WRAM_START + 0x0566, bytes([0x03]))
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def validate_rom(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read, snes_write

        rom_name = await snes_read(ctx, MIM_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name == bytes([0] * ROMHASH_SIZE) or rom_name[:5] != b"MiMAP":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_name

        death_link = await snes_read(ctx, MIM_DEATHLINK_ENABLED, 1)
        if death_link:
            await ctx.update_death_link(bool(death_link[0] & 0b1))
        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read


        validation_check_low = await snes_read(ctx, VALIDATION_CHECK, 0x1)
        validation_check_high = await snes_read(ctx, VALIDATION_CHECK_2, 0x1)
        goal_done = await snes_read(ctx, GOAL_FLAG, 0x1)
        current_item = await snes_read(ctx, ITEM_RECEIVED, 0x1)
        is_dead = await snes_read(ctx, DEATH_RECEIVED, 0x1)
        init_comm_quiz = await snes_read(ctx, IS_IN_QUIZ, 0x1)
        quiz_mode = await snes_read(ctx, QUIZ_MODE, 0x1)
        question_debug = await snes_read(ctx, QUESTION_DEBUG, 0x1)

        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            currently_dead = is_dead[0] == 0x01
            await ctx.handle_deathlink_state(currently_dead,
                                             ctx.player_names[ctx.slot] + " is bad at trivia!" if ctx.slot else "")
            if is_dead[0] != 0x00:
                snes_buffered_write(ctx, WRAM_START + 0x1554, bytes([0x00]))
        if validation_check_low is None:
            return

        if validation_check_high is None:
            return
        if validation_check_low[0] != 0x69:
            return
        if validation_check_high[0] != 0x42:
            return
        if current_item[0] > 0x00:
            return
        if goal_done[0] == 0x69:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        rom = await snes_read(ctx, MIM_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if 'active_categories' not in globals(): #only create categories once
            active_categories = []
            if quiz_mode[0] == 0x02:
                active_categories.extend(supported_categories)
            elif quiz_mode[0] == 0x01:
                for i in range(len(ctx.slot_info)):
                    active_categories.append(ctx.slot_info[i + 1].game)
            active_categories.append('General')

        if init_comm_quiz[0] != 0x00:
            question_repeat = True
            loaded_question = await snes_read(ctx, SRAM_START + 0x0012, 0x40)
            loaded_question_raw = loaded_question.decode('ascii')
            current_category = random.choice(active_categories)
            while question_repeat is True:
                if current_category not in categories_with_questions:
                    current_category = 'General'
                var_answ_values = [0, 1, 2, 3]
                var_answ = random.choice(var_answ_values)
                if question_debug[0] != 0x00:
                    question_text = question_test[question_debug[0]]
                else:
                    question_text = random.choice(question_mapping[current_category])
                    if question_text == loaded_question_raw:
                        question_repeat = True
                    else:
                        question_repeat = False
            snes_buffered_write(ctx, SRAM_START + 0x0010, bytes([0x04])) #Number of answers
            snes_buffered_write(ctx, SRAM_START + 0x0012, question_text)
            answer_lookup = {
                0: incorrect_answer_1,
                1: incorrect_answer_2,
                2: incorrect_answer_3
            }
            for i in range(3):
                current_answer = answer_lookup[i][question_text]
                snes_buffered_write(ctx, SRAM_START + answer_addrs[var_answ], current_answer)
                var_answ_values.remove(var_answ)
                var_answ = random.choice(var_answ_values)
            var_answ = var_answ_values[0]
            snes_buffered_write(ctx, SRAM_START + answer_addrs[var_answ], correct_answer[question_text])

            snes_buffered_write(ctx, SRAM_START + 0x0052, bytes([0x00])) #Question terminator
            snes_buffered_write(ctx, SRAM_START + 0x0074, bytes([0x00])) #Answer terminator
            snes_buffered_write(ctx, SRAM_START + 0x0096, bytes([0x00])) #Answer terminator
            snes_buffered_write(ctx, SRAM_START + 0x00B8, bytes([0x00])) #Answer terminator
            snes_buffered_write(ctx, SRAM_START + 0x00DA, bytes([0x00])) #Answer terminator
            snes_buffered_write(ctx, SRAM_START + 0x0011, bytes([var_answ + 1])) #Correct Answer
            snes_buffered_write(ctx, WRAM_START + 0x154B, bytes([0x00])) #End quiz logic
            #print(active_slots)

        new_checks = []
        from .Rom import location_table, item_values

        location_ram_data = await snes_read(ctx, WRAM_START + 0x1555, 0x80)
        for loc_id, loc_data in location_table.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0] - 0x1555]
                masked_data = data & (1 << loc_data[1])
                bit_set = (masked_data != 0)
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names[new_check_id]
            snes_logger.info(
                f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, ITEM_LIST, 2)
        recv_index = struct.unpack("H", recv_count)[0]
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names[item.item], 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names[item.location], recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, ITEM_LIST, pack("H", recv_index))
            if item.item in item_values:
                item_count = await snes_read(ctx, WRAM_START + item_values[item.item][0], 0x1)
                increment = item_values[item.item][1]
                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                snes_buffered_write(ctx, WRAM_START + item_values[item.item][0], bytes([new_item_count]))
        await snes_flush_writes(ctx)
