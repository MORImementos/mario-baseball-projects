"""not my file - credit to MattGree"""

def return_and_error_message(key, dictionary):
    if key in dictionary.keys():
        return dictionary[key]
    else:
        return "Bad ID" + str(key)


def char_id(val):
    char_name_dict = {
        0: "Mario",
        1: "Luigi",
        2: "DK",
        3: "Diddy",
        4: "Peach",
        5: "Daisy",
        6: "Yoshi",
        7: "Baby Mario",
        8: "Baby Luigi",
        9: "Bowser",
        10: "Wario",
        11: "Waluigi",
        12: "Koopa(G)",
        13: "Toad(R)",
        14: "Boo",
        15: "Toadette",
        16: "Shy Guy(R)",
        17: "Birdo",
        18: "Monty",
        19: "Bowser Jr",
        20: "Paratroopa(R)",
        21: "Pianta(B)",
        22: "Pianta(R)",
        23: "Pianta(Y)",
        24: "Noki(B)",
        25: "Noki(R)",
        26: "Noki(G)",
        27: "Bro(H)",
        28: "Toadsworth",
        29: "Toad(B)",
        30: "Toad(Y)",
        31: "Toad(G)",
        32: "Toad(P)",
        33: "Magikoopa(B)",
        34: "Magikoopa(R)",
        35: "Magikoopa(G)",
        36: "Magikoopa(Y)",
        37: "King Boo",
        38: "Petey",
        39: "Dixie",
        40: "Goomba",
        41: "Paragoomba",
        42: "Koopa(R)",
        43: "Paratroopa(G)",
        44: "Shy Guy(B)",
        45: "Shy Guy(Y)",
        46: "Shy Guy(G)",
        47: "Shy Guy(Bk)",
        48: "Dry Bones(Gy)",
        49: "Dry Bones(G)",
        50: "Dry Bones(B)",
        51: "Bro(B)",
        52: "Dry Bones(R)",
        53: "Bro(F)"
    }
    return return_and_error_message(val, char_name_dict)


def stadium_id(val):
    stadium_id_dict = {
        0: "Mario Stadium",
        1: "Bowser's Castle",
        2: "Wario's Palace",
        3: "Yoshi's Island",
        4: "Peach's Garden",
        5: "DK's Jungle",
        6: "Toy Field"
    }
    return return_and_error_message(val, stadium_id_dict)


def contact_id(val):
    contact_id_dict = {
        255: "Miss",
        0: "Sour - Left",
        1: "Nice - Left",
        2: "Perfect",
        3: "Nice - Right",
        4: "Sour - Right"
    }
    return return_and_error_message(val, contact_id_dict)


def hand_id(val):
    hand_id_dict = {
        0: "Left",
        1: "Right"
    }
    return return_and_error_message(val, hand_id_dict)


def hand_bool(bool):
    hand_bool_dict = {
        True: "Left",
        False: "Right"
    }
    return return_and_error_message(bool, hand_bool_dict)


def input_direction_id(val):
    input_direction_dict = {
        0: "None",
        1: "Left",
        2: "Right",
        4: "Down",
        5: "Down and Left",
        6: "Down and Right",
        8: "Up",
        9: "Up and Left",
        10: "Up and Right"
    }
    return return_and_error_message(val, input_direction_dict)


def pitch_type_id(val):
    pitch_type_dict = {
        0: "Curve",
        1: "Charge",
        2: "ChangeUp"
    }
    return return_and_error_message(val, pitch_type_dict)


def charge_pitch_id(val):
    charge_type_dict = {
        0: "N/A",
        2: "Slider",
        3: "Perfect"
    }
    return return_and_error_message(val, charge_type_dict)


def type_of_swing_id(val):
    type_of_swing_dict = {
        0: "None",
        1: "Slap",
        2: "Charge",
        3: "Star",
        4: "Bunt"
    }
    return return_and_error_message(val, type_of_swing_dict)


def position_id(val):
    position_id_dict = {
        0: "P",
        1: "C",
        2: "1B",
        3: "2B",
        4: "3B",
        5: "SS",
        6: "LF",
        7: "CF",
        8: "RF",
        255: "Inv",
        None: "None"
    }
    return return_and_error_message(val, position_id_dict)


def fielder_actions_id(val):
    fielder_actions_dict = {
        0: "None",
        2: "Sliding",
        3: "Walljump",
    }
    return return_and_error_message(val, fielder_actions_dict)


def fielder_bobbles_id(val):
    fielder_bobbles_dict = {
        0: "None",
        1: "Slide/stun lock",
        2: "Fumble",
        3: "Bobble",
        4: "Fireball",
        16: "Garlic knockout",
        255: "None"
    }
    return return_and_error_message(val, fielder_bobbles_dict)


def steal_type_id(val):
    steal_type_dict = {
        0: "None",
        1: "Ready",
        2: "Normal",
        3: "Perfect",
        55: "None"
    }
    return return_and_error_message(val, steal_type_dict)


def out_type_id(val):
    out_type_dict = {
        0: "None",
        1: "Caught",
        2: "Force",
        3: "Tag",
        4: "Force Back",
        16: "Strike-out",
    }
    return return_and_error_message(val, out_type_dict)


def pitch_result_id(val):
    pitch_result_dict = {
        0: "HBP",
        1: "BB",
        2: "Ball",
        3: "Strike-looking",
        4: "Strike-swing",
        5: "Strike-bunting",
        6: "Contact",
        7: "Unknown"
    }
    return return_and_error_message(val, pitch_result_dict)


def primary_contact_result_id(val):
    primary_contact_result_dict = {
        0: "Out",
        1: "Foul",
        2: "Fair",
        3: "Fielded",
        4: "Unknown"
    }
    return return_and_error_message(val, primary_contact_result_dict)


def secondary_contact_result_id(val):
    secondary_contact_result_dict = {
        0: "Out-caught",
        1: "Out-force",
        2: "Out-tag",
        3: "foul",
        7: "Single",
        8: "Double",
        9: "Triple",
        10: "HR",
        11: "Error - Input",
        12: "Error - Chem",
        13: "Bunt",
        14: "SacFly",
        15: "Ground Ball Double Play",
        16: "Foul catch",
    }
    return return_and_error_message(val, secondary_contact_result_dict)


def final_result_id(val):
    final_result_id_dict = {
        0: "None",
        1: "Strikeout",
        2: "Walk (BB)",
        3: "Walk HBP",
        4: "Out",
        5: "Caught (Anything Else)",
        6: "Caught (Line Drive)",
        7: "Single",
        8: "Double",
        9: "Triple",
        10: "HR",
        11: "Error Input",
        12: "Error Chem",
        13: "Bunt",
        14: "Sac Fly",
        15: "Ground Ball Double Play",
        16: "Foul Catch"
    }
    return return_and_error_message(val, final_result_id_dict)


def pitch_result(val):
    pitch_result_id_dict = {
        0: "HBP",
        1: "BB",
        2: "Ball",
        3: "Strike-looking",
        4: "Strike-swing",
        5: "Strike-bunting",
        6: "Contact",
        7: "Unknown"
    }
    return return_and_error_message(val, pitch_result_id_dict)


def manual_select_id(val):
    manual_select_dict = {
        0: "No Selected Char",
        1: "Selected Other Char",
        2: "Selected This Char",
        None: "None"
    }
    return return_and_error_message(val, manual_select_dict)