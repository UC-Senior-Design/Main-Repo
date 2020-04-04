import random, requests

instrument_id = 'FLX0122030515'

def home():
    json = {
        'jsonrpc': '2.0',
        'method': 'instrument.head.homeCustom',
        'params': {
            'instrument_id': instrument_id
        },
        'id': 0
    }
    requests.post('http://localhost:55555/api', json=json)

def move_to(point):
    json = {
        'jsonrpc': '2.0',
        'method': 'instrument.head.moveToCustom',
        'params': {
            'instrument_id': instrument_id,
            'target': {
                'left_right': point[0],
                'front_rear': point[1],
                'up_down': point[2]
            }
        },
        'id': 0
    }
    requests.post('http://localhost:55555/api', json=json)

def get_random_nearby_point(point, offset):
    new_point = tuple(map(lambda comp: comp + random.randint(-offset, offset), point))
    if in_bounds(new_point):
        return new_point
    return get_random_nearby_point(point, offset)

def get_random_point_in_bounds():
    return [random.randint(0, 7000), random.randint(0, 1300), random.randint(0, 1300)]

def in_bounds(point):
    if (point[0] < 0 or point[1] < 0 or point[2] < 0):
        return False
    if (point[0] > 7000 or point[1] > 1300 or point[2] > 1300):
        return False
    return True