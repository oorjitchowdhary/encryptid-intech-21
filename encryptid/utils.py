from datetime import datetime
import pytz

def readable_date(timestamp):
    t = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('Asia/Kolkata'))
    return t.strftime("%I:%M %p, %b %d")

def paginate(iterable):
    paginated = []

    for i in iterable:
        if iterable.index(i) % 2 == 0:
            if len(iterable) % 2 != 0 and iterable.index(i) == len(iterable) - 1:
                l = []
                l.append(i)
                paginated.append(tuple(l))
            else:
                paginated.append((i, iterable[iterable.index(i) + 1]))

    return paginated

def is_valid_host(request):
    trusted = ['intech.encryptid.live', 'localhost:5000']

    if request.host not in trusted:
        return False

    return True