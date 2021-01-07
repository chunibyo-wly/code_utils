# /usr/bin/python2

import os
import cv2
import shutil
import argparse

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

parser = argparse.ArgumentParser(description="Change a ROS bag to euroc format.")
parser.add_argument('bag',  help="Input ROS bag.")
parser.add_argument('output',  help="Output directory.")
parser.add_argument("-p", "--picture", help="Image topic.", nargs="+", type=str)
parser.add_argument("-i", "--imu", help="Imu topic.", nargs="+", type=str)

args = parser.parse_args()


def msg2txt(bag, topic):
    data_csv = "#timestamp [ns],w_RS_S_x [rad s^-1],w_RS_S_y [rad s^-1],w_RS_S_z [rad s^-1],a_RS_S_x [m s^-2],a_RS_S_y [m s^-2],a_RS_S_z [m s^-2]\n"
    out_folder = os.path.join(args.output, topic[1:])

    '/imu'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for topic, msg, timestamp in bag.read_messages(topics=[topic]):

        wx = msg.angular_velocity.x
        wy = msg.angular_velocity.y
        wz = msg.angular_velocity.z

        ax = msg.linear_acceleration.x
        ay = msg.linear_acceleration.y
        az = msg.linear_acceleration.z

        line = "{},{},{},{},{},{},{}\n".format(timestamp, wx, wy, wz, ax, ay, az)
        data_csv += line

    with open(os.path.join(out_folder, 'data.csv'), 'w') as file:
        file.write(data_csv)


def msg2image(bag, topic):

    bridge = CvBridge()
    cnt = 0
    data_csv = '#timestamp [ns],filename\n'
    out_folder = os.path.join(args.output, topic[1:], 'data')

    # '/camera/left/image_raw/data'
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for topic, msg, timestamp in bag.read_messages(topics=[topic]):
        cnt = cnt + 1
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
        t = str(cnt).zfill(4)
        cv2.imwrite(os.path.join(out_folder, t+'.png'), cv_image)

        data_csv += '{},{}.png\n'.format(timestamp, t)

    with open(os.path.join(out_folder, '..', 'data.csv'), 'w') as file:
        file.write(data_csv)


def main():

    # shutil.rmtree(args.output)

    bag = rosbag.Bag(args.bag, "r")
    # Extract picture
    if args.picture != None:
        for topic in args.picture:
            msg2image(bag, topic)
            
    # Extract txt
    if args.imu != None:
        for topic in args.imu:
            msg2txt(bag, topic)

    bag.close()


if __name__ == "__main__":
    main()
