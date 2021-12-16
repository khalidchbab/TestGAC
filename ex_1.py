from datetime import timedelta, date,datetime, time

days_dict = {1:"Lundi",2:"mardi",3:"Mercredi",4:"Jeudi",5:"Vendredi"}


def days_time(input_list:list)->list:
    """
    Takes the list of impossible time slots and orginize it to a list of 5 list coresponding to the working day of the week
    Example :
        input_list = ['6', '2 08:39-09:48', '2 08:12-11:08', '1 13:09-16:27', '4 15:18-15:23', '3 14:05-17:51', '2 13:19-17:18']
        returns [['13:09-16:27'], ['08:39-09:48', '08:12-11:08', '13:19-17:18'], ['14:05-17:51'], ['15:18-15:23'], []]
        Where the last list is empty because the whole day is empty
    Parameters:
        input_list(list) : list of impossible time slots
    returns
        days(list) : list of 5 arrays coresponding to the working day of the week
    """
    days = [[] for i in range(5)]
    if input_list == []:
        return days
    tmp = input_list[1:]
    for time_slot in tmp:
        day, slots = time_slot.split()
        if int(day)<=5:
            days[int(day)-1].append(slots)
    return days


def __sort_slot_of_day(day:list) -> list:
    """
        Change the string of time to time and then sort the impossible slots of the day based on the start date. this function is a helper function and should not be called on it own.
        Parameters:
            day(list) : list of impossible time slots in this day
        returns
            _(list) : sorted list of day
    """
    starts_slots = []
    for slot in day:
        from_time, to_time = slot.split('-')
        from_time = datetime.strptime(from_time, "%H:%M").time()
        to_time = datetime.strptime(to_time, "%H:%M").time()
        starts_slots.append((from_time,to_time))
        
    return sorted(starts_slots)

def calculate_difference(from_time:time,to_time:time) -> float:
    """
        calculate difference between two times 
        Parameters:
            from_time(datetime.time) : the time from to calculate difference
            to_time(datetime.time) : the time to which calculate difference
        returns
            _(float) : difference between the two times as float
    """
    return (datetime.combine(date.min, to_time) - datetime.combine(date.min, from_time)).total_seconds()/60 + 1

def add_hour(t):
    return (datetime.combine(date.min, t) + timedelta(minutes=59)).time()

def find_slot(day:list) ->tuple:
    """
        Find the slot of time to schedule the meeting 
        Parameters:
            day(list) : the impossible time slots of the day
        returns
            _(tupple(datetime.time, datetime.time) | (-1,-1)) : time slot if found any otherwise (-1,-1)
    """

    if(len(day) == 0): ## check if the day has any 
        return datetime.strptime("08:00", "%H:%M").time(), datetime.strptime("08:59", "%H:%M").time()
    slots_day = [] ## declare all day possible

    start_of_day = datetime.strptime("08:00", "%H:%M").time() # 08:00
    end_of_day = datetime.strptime("18:00", "%H:%M").time() # 18:00

    starts_slots = __sort_slot_of_day(day) # sort the impossible slots of the day from early to late based on start time
    f,t = starts_slots[0] # Take the first impossible time to compare it with the start of the day
    difference = calculate_difference(start_of_day,f)
    if difference >= 60:
        return start_of_day,add_hour(start_of_day) # return 08:00-08:59
    else:
        ## The idea from here on is to create a representation of the day
        ## Example starts_slots = [] at first and since 8:00-8:59 isn't avaible we add it to the starts_slots = ['08:00','08:59']
        ## and so on until we have a list of impossible times
        ## then we can compare every second element in the list with the start next impossible slot  and check if difference is more than hour
        slots_day.append(start_of_day) # Add 08:00
        slots_day.append(f) # add first impossible time slot
        slots_day.append(f) # add first impossible time slot
        slots_day.append(t) # add first impossible time slot
        for f,t in starts_slots[1:]:
            if calculate_difference(slots_day[-1],f) <= 0:
                if calculate_difference(slots_day[-1],t) > 0:
                    slots_day[-1] = t
            else:
                slots_day.append(f)
                slots_day.append(t)
        print("slots of day : ", slots_day)
        for i in range(1,len(slots_day)-1,2):
            diff = calculate_difference(slots_day[i],slots_day[i+1])
            if diff >= 60:
                return slots_day[i],slots_day[i+1]
        if calculate_difference(slots_day[-1],end_of_day)>=60:
            return slots_day[-1],add_hour(slots_day[-1])
    return -1,-1




def main():
    impo_time_slots = ['6', '2 08:39-09:48', '2 08:12-11:08', '1 13:09-16:27', '4 15:18-15:23', '3 14:05-17:51', '2 13:19-17:18']
    days = days_time(impo_time_slots)
    sorted_days = sorted(days, key=lambda d: len(d)) ## we sort the days based on the number of impossible timeslots in that day thus if we have an empty day as in the example Vendredi/Friday we return it first
    for day in sorted_days:
        from_t, to_t = find_slot(day)
        print(type(from_t))
        if from_t != -1 and to_t != -1:
            print(days_dict[days.index(day)+1],"de",from_t,"à",to_t)
            break
        
if __name__ == '__main__':
    main()
