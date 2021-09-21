from pushbullet import Pushbullet
import random ,string

api_key = "o.idxqQ5Q6C3VM4vXLGqWQc2Ep7yuBZGFu"

pb= Pushbullet(api_key)
def specific_string(length):  
     
    letters = string.ascii_lowercase # define the lower case string  
     # define the condition for random.choice() method  
    result = ''.join((random.choice(letters)) for x in range(length))  
    print(" Random generated string with repetition: ", result)  
    return result
push = pb.push_note("Title",specific_string(13))