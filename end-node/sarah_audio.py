from multiprocessing import Process, Queue # Used for multiprocessing
from time import strftime, localtime
import json
import queue

def add_audio(audio):
    new_data = {"filename": audio, "title": f"Base Message {strftime('%H:%M', localtime())}", "length":10,"lat":0,"long":0}
    with open("./audio/tracklist.json", "r+") as file:
        data = list(json.load(file))
        data.append(new_data)
        print(data)
        file.seek(0)
        json.dump(data, file)
        file.truncate()        


def get_audio():
    result = ""
    with open("./audio/audio_out/outlist.json", "r+") as file:
        data = list(json.load(file))
        for i in range(len(data)):
            if not data[i]["is_sent"]:
                result = data[i]["filename"]
                data[i]["is_sent"] = True
                file.seek(0)
                json.dump(data, file)
                file.truncate()
                return result
    return False

def main(audio_queue_in, audio_queue_out):
    print('Begin audio')
    while(True):
        try:
            audio = audio_queue_in.get(block=False)
            if audio != None:
                print('Got audio off queue')
                add_audio(audio)
        except queue.Empty:
            pass

        out_audio = get_audio()
        if out_audio:
            print('Putting Audio on queue from PI: {0:}'.format(out_audio))
            audio_queue_out.put(out_audio)

    print('End audio')
