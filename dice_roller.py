from random import randint
import re

"""
Roll queries are made by space separated blocks
Accepted blocks:

<n>d<s>         (n = number, s = size; example 4d12)
<n>d<s>+<o>     (o = offset; example 1d20+5)
<n>d<s>-<o>     (example 2d10-3)
adv             All other dice are rolled with advantage
disadv          All other dice are rolled with disadvantage
sum             Total sum off all dice blocks will be shown

"""

dice_sizes = [2, 4, 6, 8, 12, 20]
max_die_quant = 50
max_dice_blocks = 10
max_offset = 100
adv_key = "adv"
disadv_key = "disadv"
sum_key = "sum"
search_pattern = r"^(\d*)d(\d+)(?:([+-])(\d+))?$"
no_arg_default = "1d20"



def handle_roll_query(query_args):
    query_args = [simplify_str(arg) for arg in query_args]
    if len(query_args) == 0:
        query_args = [no_arg_default]
    adv_flag = 0
    sum_flag = 0
    roll_results = []
    output_str = ""

    if adv_key in query_args:
        adv_flag = 1
        query_args.remove(adv_key)
    elif disadv_key in query_args:
        adv_flag = -1
        query_args.remove(disadv_key)
    if sum_key in query_args:
        sum_flag = 1
        query_args.remove(sum_key)
    if len(query_args) > max_dice_blocks:
        return f"**Error**: too many arguments, maximum number of dice blocks: {max_dice_blocks}"
    try:
        for roll_block in query_args:
            block_total, block_msg = handle_roll_block(roll_block, adv_flag=adv_flag)
            output_str += f"\nRolling {roll_block}:\n{block_msg}"
            roll_results.append(block_total)
        if sum_flag == 1:
            output_str += f"\n\n**Total**:\n{" + ".join([str(i) for i in roll_results])} = **{sum(roll_results)}**"
        return output_str
    except Exception as e:
        return f"**Error**: {e}"

    

def handle_roll_block(block, adv_flag):
    match_result = re.match(search_pattern, block)
    if match_result:
        total = 0
        roll_strs = []
        dice_quant = int(match_result.group(1)) if match_result.group(1) else 1
        dice_size = int(match_result.group(2))
        operator = match_result.group(3)
        offset_value = int(match_result.group(4)) if match_result.group(4) else 0
        offset = offset_value if operator == "+" else -offset_value

        if dice_size not in dice_sizes:
            raise Exception(f"Invalid dice size in {block}, size can be {", ".join([str(i) for i in dice_sizes])}")
        if dice_quant < 1 or dice_quant > max_die_quant:
            raise Exception(f"Invalid dice quantity in {block}, quantity must be between 1 and {max_die_quant}")
        if offset_value > max_offset:
            raise Exception(f"Invalid offset in {block}, offset cannot be larger than {max_offset}")

        for i in range(dice_quant):
            roll, roll_str = get_roll_string(dice_size=dice_size, adv_flag=adv_flag)
            roll_strs.append(roll_str)
            total += roll
        if offset == 0:
            if dice_quant == 1:
                block_str = f"{bolden_last_word(roll_strs[0])}"
            else:
                block_str = f"{" + ".join(roll_strs)} = **{total}**"
            return total, block_str
        total += offset
        return total, f"[{" + ".join(roll_strs)}] {operator} {offset_value} = **{total}**"
    else:
        raise Exception(f"invalid roll block {block}")

def get_roll_string(dice_size, adv_flag):
    roll = roll_dice(dice_size)
    if adv_flag == 0:
        return roll, str(roll)
    extra_roll = roll_dice(dice_size)
    roll_return = max(roll, extra_roll) if adv_flag == 1 else min(roll, extra_roll)
    if (roll > extra_roll and adv_flag == 1) or (roll < extra_roll and adv_flag == -1):
        return roll_return, f"({roll}, *{extra_roll}*) → {roll_return}"
    return roll_return, f"(*{roll}*, {extra_roll}) → {roll_return}"

def roll_dice(size):
    return randint(1, size)

def bolden_last_word(string):
    string = string.split(" ")
    string.extend(["**", "**"])
    string[len(string)-2], string[len(string)-3] = string[len(string)-3], string[len(string)-2]
    return " ".join(string)

def simplify_str(input_string):
    simplified = re.sub(r'[^a-zA-Z0-9+-]', '', input_string).lower()
    return simplified

