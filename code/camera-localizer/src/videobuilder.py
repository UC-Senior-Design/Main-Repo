import ioutils, cv2, numpy as np, time, matplotlib.pyplot as plt
from itertools import product, combinations

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def load_data(drone_image_path, drone_inference_path):
    drone_image_info = ioutils.get_all_file_info('./drone')
    drone_inference_info = ioutils.load_results_csv(drone_inference_path)
    snap_indices = sorted(list(set(map(lambda image: int(image['snapIndex']), drone_image_info))))

    def get_drone_image_info(snap_index):
        out = {}
        for info in drone_image_info:
            if int(info['snapIndex']) == snap_index:
                out[info['camera']] = {
                    "path": info['path'],
                    "time": info['snapTime']
                }
        return out

    def get_inference_info(snap_index):
        for info in drone_inference_info:
            if int(info['snapIndex']) == snap_index:
                return info
        return None

    out = []
    last_snap_index = None
    for snap_index in snap_indices:
        image_info = get_drone_image_info(snap_index)
        inference_info = get_inference_info(snap_index)
        velocity = None
        if inference_info != None and last_snap_index != None and last_snap_index == snap_index - 1 and get_inference_info(last_snap_index) != None:
            last_inference_info = get_inference_info(last_snap_index)
            # Compute velocity
            velocity = {
                "x": (inference_info['x'] - last_inference_info['x'])/0.1,
                "y": (inference_info['y'] - last_inference_info['y'])/0.1,
                "z": (inference_info['z'] - last_inference_info['z'])/0.1,
            }

        out.append({
            "snapIndex": snap_index,
            "images": image_info,
            "inference": inference_info,
            "velocity": velocity
        })
        last_snap_index = snap_index
    return out


def render_frame(frame_info, image_base_path):
    output = np.zeros((1080, 1920, 3), np.uint8)
    if frame_info["inference"] == None:
        d_pos = None
    else:
        d_pos = {
            "x": float(frame_info['inference']['x']),
            "y": float(frame_info['inference']['y']),
            "z": float(frame_info['inference']['z']) + 0.4531943,
        }
    if frame_info["velocity"] == None:
        d_vel = None
    else:
        d_vel = {
            "x": float(frame_info['velocity']['x']),
            "y": float(frame_info['velocity']['y']),
            "z": float(frame_info['velocity']['z']),
        }
        

    def get_data_image():
        image = np.zeros((640, 480, 3), np.uint8)
        if d_pos == None:
            pos_string = "?"
        else:
            pos_string = "{:.2f}, {:.2f}, {:.2f}".format(d_pos['x'], d_pos['y'], d_pos['z'])

        if d_vel == None:
            vel_string = "?"
        else:
            vel_string = "{:.2f}, {:.2f}, {:.2f}".format(d_vel['x'], d_vel['y'], d_vel['z'])
        rows = [
            "Time (seconds): {}".format(frame_info['snapIndex'] / 10.0),
            "",
            "Position (meters):",
            pos_string,
            "",
            "Velocity (meters/s):",
            vel_string
        ]
        for row_index in range(len(rows)):
            cv2.putText(
                image,
                rows[row_index],
                (25, 50 + 75 * row_index),
                cv2.FONT_HERSHEY_TRIPLEX,
                1,
                (255, 200, 200),
                2
            )
        return image

    def get_virtual_drone():
        fig_scale = 1
        fig = Figure(figsize=(4*fig_scale, 3*fig_scale), dpi=200)
        canvas = FigureCanvas(fig)
        ax = fig.gca(projection='3d')
        ax.set_title("Drone Position (meters)")
        ax.set_ylim([-0.7, 0.7])
        ax.set_xlim([-0.7, 0.7])
        ax.set_zlim([0, 1])

        color = "#00ff00"
        quiver_color = "#0055ff"
        if d_pos != None:
            ax.scatter([d_pos['x']], [d_pos['y']], [d_pos['z']], color=color)
            if d_vel != None:
                ax.quiver(d_pos['x'], d_pos['y'], d_pos['z'], d_vel['x'], d_vel['y'], d_vel['z'], length=0.2, color=quiver_color)

        canvas.draw()
        width, height = fig.get_size_inches() * fig.get_dpi()
        image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
        return image

    def get_camera_image(camera):
        image = cv2.imread(image_base_path + frame_info['images'][camera]['path'])
        if frame_info['inference'] != None:
            drone_center = frame_info['inference']['cameras'][camera]
            cv2.circle(image, (int(drone_center['x']*320), int(drone_center['y']*240)), 4, (64, 255, 0), -1)
        return image

    def place_image(image, pos):
        resized = cv2.resize(image, (640, 480))
        ioutils.overlay_image_alpha(output, resized, (pos[0]*640, pos[1]*480))     
    
    people = cv2.imread('../../data/people.png')

    place_image(get_camera_image("1"), (0, 0))
    place_image(get_camera_image("2"), (1, 0))
    place_image(get_camera_image("3"), (2, 0))
    place_image(get_virtual_drone(), (0, 1))
    place_image(get_data_image(), (1, 1))
    place_image(people, (2, 1))
    return output


data = load_data('./drone', '../../data/result.csv')
out = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc(*"mp4v"), 10, (1920, 1080))
for line in data:
    frame = render_frame(line, './drone/')

    out.write(frame)
    # cv2.imshow('frame', frame)
    # cv2.waitKey(10)
    pass
out.release()

