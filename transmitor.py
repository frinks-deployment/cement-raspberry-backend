import sys
import time
import shlex
import imagezmq
import numpy as np
import subprocess as sp

rpi_name = sys.argv[1]  # send RPi hostname with each image
video_path = sys.argv[2]
tcp_port = sys.argv[3]
height = int(sys.argv[4])
width = int(sys.argv[5])
testing = int(sys.argv[6])

gstreamer_exe = 'gst-launch-1.0'  # '/usr/bin/gst-launch-1.0'
gstreamer_source = 'rtspsrc' if testing == 0 else 'filesrc'
gstreamer_latency = 'latency=0' if testing == 0 else ''

p = sp.Popen(shlex.split(
    f'{gstreamer_exe} --quiet {gstreamer_source} location={video_path} {gstreamer_latency} ! decodebin ! videoconvert ! video/x-raw,format=BGR ! fdsink'), stdout=sp.PIPE)

sender = imagezmq.ImageSender(connect_to=f'tcp://127.0.0.1:{tcp_port}')

while True:
    try:
        raw_image = p.stdout.read(width * height * 3)
        print(len(raw_image))
        if len(raw_image) < width*height*3:
            print(f"RTSP broken----{rpi_name}")
            p.terminate()
            p.stdout.close()
            p = sp.Popen(shlex.split(
                f'{gstreamer_exe} --quiet {gstreamer_source} location={video_path} {gstreamer_latency} ! decodebin ! videoconvert ! video/x-raw,format=BGR ! fdsink'), stdout=sp.PIPE)
            continue

        image = np.frombuffer(raw_image, np.uint8).reshape((height, width, 3))
        sender.send_image(rpi_name, image)

    except KeyboardInterrupt:
        p.stdout.close()
        p.terminate()
        p.wait()
        print("\nEXITING...")
        break