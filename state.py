import urllib.request
from obswebsocket import obsws, requests  # noqa: E402
import mido

slide_target = []

obs_host = "localhost"
obs_port = 4444
obs_password = "secret"

obs_ws = obsws(obs_host, obs_port, obs_password)
obs_ws.connect()
obs_scenes = {}
last_scene = ""
last_preset = []

# cleanup at end???
# ws.disconnect()

def my_int(str):
    if str == '':
        return -1
    return int(str)

def init(rows):
    global obs_scenes
    global last_scene
    global last_preset

    last_scene = "none"
    last_preset = [-1, -1, -1]
    obs_scenes = obs_ws.call(requests.GetSceneList())
    for s in obs_scenes.getScenes():
        print(s['name'])
    global slide_target
    for row in rows:
        nRowsToAdd = int(row['Slide']) - 1 - len(slide_target)
        while nRowsToAdd > 0:
            new_row = slide_target[len(slide_target) - 1].copy()
            slide_target.append(new_row)
            nRowsToAdd = nRowsToAdd - 1

        new_row = {}
        new_row['desc'] = row['Description']
        new_row['scene'] = row['Scene']
        new_row['cams'] = [my_int(row['Cam1']), my_int(row['Cam2']), my_int(row['Cam3'])]
        new_row['mics'] = [0, my_int(row['Lectern']), my_int(row['Vocal']), my_int(row['Ac Guit']), my_int(row['KeyBd']), my_int(row['Cong']), my_int(row['Media L']), my_int(row['Media R']), my_int(row['Stream L']), my_int(row['Stream R']), my_int(row['Pr Ely']), my_int(row['Pr Ed'])]
        slide_target.append(new_row)

    # fill out defaults that extend down
    mics = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for row in slide_target:
        new_mics = row['mics'].copy()
        for i in range(0, 12):
            if new_mics[i] < 0:
                new_mics[i] = mics[i]
        row['mics'] = new_mics
        mics = new_mics

    # fill out defaults that extend up
    cams = [1, 1, 1]
    for ix in range(len(slide_target) - 1, 0, -1):
        row = slide_target[ix]
        new_cams = row['cams'].copy()
        for i in range(0, 3):
            if new_cams[i] < 0:
                new_cams[i] = cams[i]
        row['cams'] = new_cams
        cams = new_cams


    slide = 1
    for row in slide_target:
        print(slide, row)
        slide = slide + 1



def set_camera(camera_ix, preset):
    if camera_ix < 0 or camera_ix > 2:
        return
    if last_preset[camera_ix] == preset:
        return

    last_preset[camera_ix] = preset
    print("set camera", camera_ix, "to", preset)
    url_base = ["192.168.89.210", "192.168.89.212", "192.168.89.213"]
    url = "http://" + url_base[camera_ix] + "/cgi-bin/ptzctrl.cgi?ptzcmd&poscall&" + str(preset)
    web_url = urllib.request.urlopen(url)
    print("result code:", str(web_url.getcode()))



def set_scene(scene_name):
    global obs_scenes
    global last_scene

    if last_scene == scene_name:
        return
    last_scene = scene_name
    print(u"Switching to {}".format(scene_name))
    obs_ws.call(requests.SetCurrentScene(scene_name))


def set_mics(mics):
    print("SET MICS:", mics)
    with mido.open_output('USB Midi  1') as port:
        for i in range(0, 12):
            num = i + 1
            if mics[i] == 0:
                my_value = 127
            else:
                my_value = 0

            msg = mido.Message('control_change', channel=1, control=i, value=my_value)
            print(msg)
            port.send(msg)


def set_slide(current):
    if current < 1 or current > len(slide_target):
        print("illegal slide number", current)
        return

    new_set = slide_target[current - 1]

    for i in range(0, 3):
        set_camera(i, new_set['cams'][i])

    set_scene(new_set['scene'])
    set_mics(new_set['mics'])



