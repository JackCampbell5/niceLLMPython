from chat import Chat


def loop_through(message_loc, arr):
    total = 0
    correct = 0
    correct_fixed = 0
    print("\n\n", message_loc, "\n")
    for total in range(size):
        print(total)
        try:
            result = chat.send_message(message=message_loc)
            print(result)
            if result.find("{") != -1:
                if len(result) > 25:
                    print(result[:25])
                correct += 1
            else:
                print("\n", result, "\n")
                result = chat.send_message("Those details are correct")
                if result.find("{") != -1:
                    if len(result) > 25:
                        print("2", result[:25])
                    correct_fixed += 1
                    correct += 1
                else:
                    print("\n", result, "\n")
            chat.clear_chat()
            print(f"Total:{total + 1} Correct:{correct} Correct After 2:{correct_fixed}\n")
        except Exception as e:
            print(e.with_traceback())
    arr[0] += total + 1
    arr[1] += correct
    arr[2] += correct_fixed
    return f"Total:{total + 1} Correct:{correct} Correct After 2:{correct_fixed}\n\n"


# Params
size = 25
arr = [0] * 3
# Actual program

print("Program has started:")
result_str = ""

chat = Chat()

message = ("Create a json trajectory with prefix angleChecks with description “this is a file that checks angle” that "
           "loop through sample angle from 1 to 1.96 with a step of 0.08 and detector angle from 2 to 3.92 with a "
           "step of 0.16. “init” section should contain a count against TIME and time and monitor counters at 40 and "
           "nothing else.")
result_str += message + "\n " + loop_through(message_loc=message, arr=arr)

message = ("Create a json trajectory with prefix apertureChecks with description “this loops through apertures” that "
           "loop through sample angle from 2 to 4 with a step of 0.1 that sets slitAperture1 to 0.4 times the sample "
           "angle. “init” section should contain a count against TIME and set prefac to 2 and nothing else.")
result_str += message + "\n " + loop_through(message_loc=message, arr=arr)

message = ("Create a json trajectory with prefix mb111 with description “5.4kG mq PSD” that loop through detector "
           "angle from 0.8 to 2 with a step of 0.1 as well as looping through slitAperture1 from 1 to 1 with step of "
           "0. “init” section should contain down set to down and up set to up and a count against TIME.")
result_str += message + "\n " + loop_through(message_loc=message, arr=arr)

message = ("Create a json trajectory with prefix live.sample.name with description “'transverse 5+5um stripes'” that "
           "loops through sampleAngle from -1 to 2 with step of 0.0075. “init” section should contain detector angle "
           "set to 1.24 and a count against TIME.")
result_str += message + "\n " + loop_through(message_loc=message, arr=arr)

print(result_str)
print(f"nTotal:{arr[0]} Correct:{arr[1]} Correct After 2:{arr[2]}\n\n")
print("Program Complete")
