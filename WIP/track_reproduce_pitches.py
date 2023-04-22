import _dolphin_memory_engine as dme
import memory_engine as me

# hook into dme
dme.hook()


# var to update with current frame/input
active_curve = None
active_frame = None

# store inputs
input_list = []

# used when I didn't want to save in real time - wrote to file and saved it there, but should be equally doable from input_list
# append values to list
with open('test.txt', 'r') as p_file:
    vals = p_file.readlines()
    for v in vals:
        input_list.append(float(v))

# ignore
# test = []

while True:
    # assign variables - this measures current curve control input for frame
    curve_control = me.read_float(0x80890A24)

    # pitch frames - countdown of pitch, pitch = total duration of pitch / check for pitching or not
    pitch_frames = me.read_half_word(0x80890AF2)
    pitch = me.read_half_word(0x80890AF4)

    # if a pitch is actively occurring
    if pitch_frames != active_frame:
        # print(pitch_frames)

        # write float from list to current frame of pitch (len used to evaluate total length of pitch / what index of list to pull from)
        pitch_rewrite = me.write_float(0x80890A24, input_list[len(input_list) - 1 - pitch_frames])

        # update active_frame
        active_frame = pitch_frames

        # ignore
        # test.append(pitch_rewrite)






    #
    #     if curve_control != active_frame:
    #         print(curve_control)
    #         input_list.append(curve_control)
    #         active_curve = curve_control
    #         print(input_list)
    #
    #     if pitch_frames == 0:
    #         with open('test.txt', 'w') as f:
    #             for i in input_list:
    #                 f.write(str(i) + "\n")


