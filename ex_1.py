from datetime import timedelta, date,datetime

days_dict = {1:"Lundi",2:"mardi",3:"Mercredi",4:"Jeudi",5:"Vendredi"}


def days_time(inp:list)->list:
    """
    
    """
    days = [[] for i in range(5)]
    if inp == []:
        return days
    N = int(inp[0])
    tmp = inp[1:]
    for time_slot in tmp:
        day, slots = time_slot.split()
        if int(day)<=5:
            days[int(day)-1].append(slots)
    return days


def __sort_slot_of_day(day:list):
    starts_slots = []
    for slot in day:
        from_time, to_time = slot.split('-')
        from_time = datetime.strptime(from_time, "%H:%M").time()
        to_time = datetime.strptime(to_time, "%H:%M").time()
        starts_slots.append((from_time,to_time))
        
    return sorted(starts_slots)

def calculate_difference(f,t):
    return (datetime.combine(date.min, t) - datetime.combine(date.min, f)).total_seconds()/60 + 1

def add_hour(t):
    return (datetime.combine(date.min, t) + timedelta(minutes=59)).time()

def find_slot(day:list):
    slots_day = []
    if(len(day) == 0):
        return datetime.strptime("08:00", "%H:%M").time(), datetime.strptime("08:59", "%H:%M").time()
    starts_slots = __sort_slot_of_day(day)
    start_of_day = datetime.strptime("08:00", "%H:%M").time()
    end_of_day = datetime.strptime("18:00", "%H:%M").time()
    f,t = starts_slots[0]
    difference = calculate_difference(start_of_day,f)
    if difference >= 60:
        return start_of_day,add_hour(start_of_day)
    else:
        slots_day.append(start_of_day)
        slots_day.append(f)
        slots_day.append(f)
        slots_day.append(t)
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
    sorted_days = sorted(days, key=lambda d: len(d))
    for day in sorted_days:
        from_t, to_t = find_slot(day)
        if from_t != -1 and to_t != -1:
            print(days_dict[days.index(day)+1],"de",from_t,"à",to_t)
            break

if __name__ == '__main__':
    main()
