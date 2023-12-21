#!/usr/bin/env python3
# This file is part of Handheld Game Console Controller System (HandyGCCS)
# Copyright 2023 Philip Müller <philm@manjaro.org>
# Copyright 2022-2023 Derek J. Clark <derekjohn.clark@gmail.com>

######### NOTE #########
# This is a prototype and may change in production
#
# There are 4 extra buttons available via AT Translated Set 2 keyboard
# LC = MSC_SCAN 68
# RC = MSC_SCAN 69
# Lower_Left_2 = MSC_SCAN 67
# Lower_Right_1 = MSC_SCAN 66
#
# Other buttons are available via Microsoft X-Box 360 pad from the
# SHANWAN Android Gamepad
#
# Top buttons: LB, LT (trigger), Power, Volume rocker, RB, RT (trigger)
# Front buttons: D-Pad, X-Y-A-B buttons, Lower_Left_1, Lower_Right_2, 2 Analog Sticks
#
########################


from evdev import InputDevice, InputEvent, UInput, ecodes as e, list_devices, ff

handycon = None

def init_handheld(handheld_controller):
    global handycon
    handycon = handheld_controller
    handycon.BUTTON_DELAY = 0.11
    handycon.CAPTURE_CONTROLLER = True
    handycon.CAPTURE_KEYBOARD = True
    handycon.CAPTURE_POWER = True
    handycon.GAMEPAD_ADDRESS = 'usb-0000:c3:00.3-5/input0'
    handycon.GAMEPAD_NAME = 'Microsoft X-Box 360 pad'
    handycon.KEYBOARD_ADDRESS = 'isa0060/serio0/input0'
    handycon.KEYBOARD_NAME = 'AT Translated Set 2 keyboard'


# Captures keyboard events and translates them to virtual device events.
async def process_event(seed_event, active_keys):
    global handycon

######### Note #########
# button1 SCR
# button2 QAM
# button3 ESC
# button4 OSK
# button5 MODE
# button6 OPEN_CHIMERA
# button7 TOGGLE_PERFORMANCE
# button8 MODE
# button9 TOGGLE_MOUSE
# button10 ALT_TAB
# button11 KILL
# button12 TOGGLE_GYRO
# power_button SUSPEND
#########################

    # Button map shortcuts for easy reference.
    button1 = handycon.button_map["button1"]  # Default Screenshot
    button2 = handycon.button_map["button2"]  # Default QAM
    button3 = handycon.button_map["button3"]  # Default ESC
    button4 = handycon.button_map["button4"]  # Default OSK
    button5 = handycon.button_map["button5"]  # Default MODE

    ## Loop variables
    button_on = seed_event.value

    # Automatically pass default keycodes we dont intend to replace.
    if seed_event.code in [e.KEY_VOLUMEDOWN, e.KEY_VOLUMEUP]:
        handycon.emit_event(seed_event)

    # BUTTON 1 (Default: Screenshot/Launch Chiumera) LC Button
    if active_keys == [] and button_on == 1 and button1 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button1)
    elif active_keys == [] and seed_event.code in [] and button_on == 0 and button1 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button1)

    # BUTTON 2 (Default: QAM) Lower_Right_1
    if active_keys == [] and button_on == 1 and button2 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button2)
    elif active_keys == [] and seed_event.code in [] and button_on == 0 and button2 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button2)

    # BUTTON 4 (Default: OSK) RC Button
    if active_keys == [] and button_on == 1 and button4 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button4)
    elif active_keys == [] and seed_event.code in [] and button_on == 0 and button4 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button4)

    # BUTTON 5 (Default: MODE) Lower_Left_2
    if active_keys == [] and button_on == 1 and button5 not in handycon.event_queue:
        await handycon.handle_key_down(seed_event, button5)
    elif active_keys == [] and seed_event.code in [] and button_on == 0 and button5 in handycon.event_queue:
        await handycon.handle_key_up(seed_event, button5)

    # Handle L_META from power button
    elif active_keys == [] and seed_event.code == 125 and button_on == 0 and handycon.event_queue == [] and handycon.shutdown == True:
        handycon.shutdown = False

    if handycon.last_button:
        await handycon.handle_key_up(seed_event, handycon.last_button)
