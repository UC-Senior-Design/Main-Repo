import ioutils, time

metersPerStep = 0.0001495806
robot_data = ioutils.ndjsonToDictArray('../../data/training/run_1585442818.411675__flex_points.ndjson')
led_data = ioutils.ndjsonToDictArray('../../data/training/leds.ndjson')

snap_indices = map(lambda d: int(d['capture_index']), robot_data)
out = []
out.append('cam0x,cam0y,cam1x,cam1y,cam3x,camy3,robx,roby,robz')
for i in snap_indices:
    try:
        robot = next(r for r in robot_data if int(r['capture_index']) == i)
        led = next(l for l in led_data if int(l['capture_index']) == i)
    except:
        continue
    if robot['pos'][0] == 0 and robot['pos'][1] == 0 and robot['pos'][2] == 0:
        continue
    line = '{},{},{},{},{},{},{},{},{}'.format(
        led['cams']['0'][0]/320,
        led['cams']['0'][1]/240,
        led['cams']['1'][0]/320,
        led['cams']['1'][1]/240,
        led['cams']['3'][0]/320,
        led['cams']['3'][1]/240,
        (robot['pos'][0]-3500)*metersPerStep,
        (robot['pos'][1]-650)*metersPerStep,
        (-robot['pos'][2]+650)*metersPerStep
    )
    out.append(line)

with open('./cleaned.csv', 'w') as f:
    for line in out:
        f.write(line + '\n')

print('wrote {} lines to csv'.format(len(out)))

drone_data = ioutils.ndjsonToDictArray('../../data/detection/drones.ndjson')
snap_indices = map(lambda d: int(d['capture_index']), drone_data)
out = []
out.append('snap_index,cam0x,cam0y,cam1x,cam1y,cam3x,camy3')
for i in snap_indices:
    def is_empty(rect):
        return int(rect[0]) == 0 and int(rect[1]) == 0 and int(rect[2]) == 0 and int(rect[3]) == 0
    try:
        drone = next(l for l in drone_data if int(l['capture_index']) == i)
    except:
        continue
    c1 = drone['cams']['1']
    c2 = drone['cams']['2']
    c3 = drone['cams']['3']
    if is_empty(c1) or is_empty(c2) or is_empty(c3):
        print('empty detected')
        continue
    line = '{},{},{},{},{},{},{}'.format(
        i,
        (int(c1[0]) + (int(c1[2]) * 0.5))/320,
        (int(c1[1]) + (int(c1[3]) * 0.5))/240,
        (int(c2[0]) + (int(c2[2]) * 0.5))/320,
        (int(c2[1]) + (int(c2[3]) * 0.5))/240,
        (int(c3[0]) + (int(c3[2]) * 0.5))/320, 
        (int(c3[1]) + (int(c3[3]) * 0.5))/240
    )
    out.append(line)

with open('./drone_cleaned.csv', 'w') as f:
    for line in out:
        f.write(line + '\n')

print('wrote {} lines to csv'.format(len(out)))

