def capture_all(cameras):
    success = map(lambda cam: cam.grab(), cameras)
    decoded = map(lambda cam: cam.retrieve()[1], cameras)
    return decoded

def capture_all_slow(cameras):
    decoded = map(lambda cam: cam.read()[1], cameras)
    return decoded