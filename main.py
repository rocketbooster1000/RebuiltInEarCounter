from ntcore import NetworkTableInstance
import pygame
import time

def getShift(seconds):
    if (seconds < 10):
        return "Transition"
    elif (seconds < 10 + 25):
        return "Shift 1"
    elif (seconds < 10 + 25 + 25):
        return "Shift 2"
    elif (seconds < 10 + 25 + 25 + 25):
        return "Shift 3"
    elif (seconds < 10 + 25 + 25 + 25 + 25):
        return "Shift 4"
    elif (seconds < 140):
        return "Endgame"
    else:
        return "Disabled"
    
def getShiftTimeRemaining(seconds):
    if (seconds <= 10):
        return 10 - seconds
    elif (seconds <= 10 + 25):
        return 10 + 25 - seconds
    elif (seconds <= 10 + 25 + 25):
        return 10 + 25 + 25 - seconds
    elif (seconds <= 10 + 25 + 25 + 25):
        return 10 + 25 + 25 + 25 - seconds
    elif (seconds <= 10 + 25 + 25 + 25 + 25):
        return 10 + 25 + 25 + 25 + 25 - seconds
    elif (seconds <= 140):
        return 140 - seconds
    else:
        return 0
    
def main():
    # seconds_sounds_root = "media/seconds/s"
    seconds_sounds_root = "media/altseconds/s"
    shift_sounds_root = "media/shifts/"
    pygame.mixer.init()

    shift_change_sound = pygame.mixer.Sound('media/jason.mp3')
    time_count_sound = pygame.mixer.Sound('media/balls2.mp3')

    seconds_sounds = []
    win_shift_sounds = {}
    lose_shift_sounds = {}

    print("Initializing sounds")

    for i in range(30):
        seconds_sounds.append(pygame.mixer.Sound(seconds_sounds_root + str(i) + ".mp3"))

    win_shift_sounds["Transition"] = pygame.mixer.Sound(shift_sounds_root + "auto_won.mp3")
    win_shift_sounds["Shift 1"] = pygame.mixer.Sound(shift_sounds_root + "lob.mp3")
    win_shift_sounds["Shift 2"] = pygame.mixer.Sound(shift_sounds_root + "scoring.mp3")
    win_shift_sounds["Shift 3"] = pygame.mixer.Sound(shift_sounds_root + "lob.mp3")
    win_shift_sounds["Shift 4"] = pygame.mixer.Sound(shift_sounds_root + "scoring.mp3")
    win_shift_sounds["Endgame"] = pygame.mixer.Sound(shift_sounds_root + "endgame.mp3")
    
    lose_shift_sounds["Transition"] = pygame.mixer.Sound(shift_sounds_root + "auto_lost.mp3")
    lose_shift_sounds["Shift 1"] = pygame.mixer.Sound(shift_sounds_root + "scoring.mp3")
    lose_shift_sounds["Shift 2"] = pygame.mixer.Sound(shift_sounds_root + "lob.mp3")
    lose_shift_sounds["Shift 3"] = pygame.mixer.Sound(shift_sounds_root + "scoring.mp3")
    lose_shift_sounds["Shift 4"] = pygame.mixer.Sound(shift_sounds_root + "lob.mp3")
    lose_shift_sounds["Endgame"] = pygame.mixer.Sound(shift_sounds_root + "endgame.mp3")
    
    bootup_sound = pygame.mixer.Sound('media/utils/bootup.mp3')

    print("Sounds initialized")

    ntInst = NetworkTableInstance.getDefault()
    ntInst.startClient4("my-dashboard")
    # ntInst.setServerTeam(3006)
    ntInst.setServer("127.0.0.1")
    print("Connecting to NetworkTables...")
        
    while not ntInst.isConnected():
        time.sleep(0.1)

    smartdashboard = ntInst.getTable("SmartDashboard")
    
    nt_prefix = "Match Timer/Headphone Counter/"

    # subscriber = smartdashboard.getDoubleTopic(nt_prefix + "shift-time-int").subscribe(0.0)

    # shift = smartdashboard.getStringTopic(nt_prefix + "Match state").subscribe("")

    disabled = smartdashboard.getBooleanTopic(nt_prefix + "disabled").subscribe(True)

    auto_won = smartdashboard.getBooleanTopic(nt_prefix + "auto won").subscribe(False)

    print("Smartdashboard connected")

    last_floor_val = 0
    last_shift = ""
    second_counter = 0
    switch_shift = False
    match_counter = 140
    
    last_disabled = True
    
    start = 0
    
    print("Ready")
    
    bootup_sound.play()
    
    while True:
        if disabled.get():
            match_counter = 140
            last_disabled = True
            continue
        
        elif not disabled.get() and last_disabled:
            print("Match started")
            last_disabled = False
            start = time.time()
            
        
        # shift_val = shift.get()
        # if (shift_val != last_shift):
        #     print("Received shift:", shift_val)
        #     print("\n")
        #     last_shift = shift_val
        #     playsound('media/jason.mp3', block=False)
        #     if (shift_val == "SHIFT_1" or shift_val == "SHIFT_2" or shift_val == "SHIFT_3" or shift_val == "SHIFT_4"):
        #         second_counter = 24
        #         # playsound('media/balls2.mp3', block=False)
        # else:
        #     if (second_counter >= 0):
        #         playsound("media/balls2.mp3", block=False)
        #         second_counter -= 1
        
        # time.sleep(1)
        
        # print("Received value:", subscriber.get())
        
        
        
        
        
        
        
        # val = subscriber.get()
        # floored_val = int(val)
        # if (last_floor_val != floored_val):
        #     match_counter = match_counter - 1
        #     print("Shift Remaining:", getShiftTimeRemaining(140 - match_counter)) 
        #     print(match_counter)
        #     # if (last_shift != shift_val):
        #     if (last_floor_val == 0 or match_counter == 139):
        #         predicted_shift = getShift(140 - match_counter)
        #         print("Received shift:", shift_val)
        #         print("Predicted shift:", predicted_shift)
        #         print("\n")
        #         last_shift = shift_val
        #         # shift_change_sound.play()
        #         if (auto_won.get()):
        #             win_shift_sounds[predicted_shift].play()
        #         else:
        #             lose_shift_sounds[predicted_shift].play()
        #     else:
        #         print("Received floor:", floored_val)
        #         print("Received value:", val)
        #         print("\n")
        #         # time_count_sound.play()
        #         seconds_sounds[floored_val].play()
        #     last_floor_val = floored_val
            
        val = 140 - (time.time() - start)
        floored_val = getShiftTimeRemaining(140 - int(val))
        if (last_floor_val != floored_val):
            match_counter = match_counter - 1
            print(match_counter)
            # if (last_shift != shift_val):
            if (last_floor_val == 0 or val == 139):
                predicted_shift = getShift(140 - match_counter)
                print("Predicted shift:", predicted_shift)
                print("\n")
                if (auto_won.get()):
                    win_shift_sounds[predicted_shift].play()
                else:
                    lose_shift_sounds[predicted_shift].play()
            else:
                if (val < 0):
                    continue
                print("Received floor:", floored_val)
                print("Received value:", val)
                print("\n")
                # time_count_sound.play()
                seconds_sounds[floored_val].play()
            last_floor_val = floored_val
            
            
            
        # if (last_shift != shift_val):
        #     print("Received shift:", shift_val)
        #     print("\n")
        #     last_shift = shift_val
        #     shift_change_sound.play()
        #     last_floor_val = floored_val
        #     switch_shift = True
        # elif switch_shift:
        #     last_floor_val = floored_val
        #     switch_shift = False
        # elif (last_floor_val != floored_val):
        #     print("Received floor:", floored_val)
        #     print("Received value:", val)
        #     print("\n")
        #     last_floor_val = floored_val
        #     time_count_sound.play()
        # playsound("media/balls2.mp3", block=False)
        # time.sleep(1)
        
print(__name__)
        
if __name__ == "__main__":
    main()