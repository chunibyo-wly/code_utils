from argparse import ArgumentParser
import csv
import numpy as np
from matplotlib import pyplot as plt

file = 'data.csv'


def skew(w):
    temp = np.array([
        [0, -w[2], w[1]],
        [w[2], 0, -w[0]],
        [-w[1], w[0], 0]
    ])
    return temp


class ImuData(object):
    def __init__(self, acc, gyro, timestamp):
        self.acc = acc
        self.gyro = gyro
        self.timestamp = timestamp


class Integrate(object):
    def __init__(self):
        self.position = np.zeros((3, 1))
        self.velocity = np.zeros((3, 1))
        self.rotation = np.eye(3)

        self.positions = []
        self.velocities = []

    def update(self, acc, gyro, timestep):
        self.position = self.position + self.velocity * timestep + 0.5 * acc * timestep * timestep
        self.velocity = self.velocity + acc * timestep
        self.rotation = self.rotation * np.exp(skew*gyro * timestep)

        self.positions.append(np.mean(self.position))
        self.velocities.append(np.mean(self.velocity))


def get_imu_data(file_path):
    # timestamp [ns]
    # w_RS_S_x [rad s^-1], w_RS_S_y [rad s^-1], w_RS_S_z [rad s^-1]
    # a_RS_S_x [m s^-2], a_RS_S_y [m s^-2], a_RS_S_z [m s^-2]
    imuDatas = []
    with open(file_path) as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if row[0][0] == '#':
                continue
            imuDatas.append(ImuData(
                acc=np.array([float(row[4]),  float(row[5]),  float(row[6])]).reshape(3, 1),
                gyro=np.array([float(row[1]),  float(row[2]),  float(row[3])]).reshape(3, 1),
                timestamp=float(row[0]) / 1e9
            ))
    return imuDatas


if __name__ == "__main__":
    imuDatas = get_imu_data(file)
    integration = Integrate()
    '''
    for i in range(0, len(imuDatas)-1):
        integration.update(
            (imuDatas[i].acc + imuDatas[i+1].acc)/2,
            (imuDatas[i].gyro + imuDatas[i+1].gyro)/2,
            imuDatas[i+1].timestamp - imuDatas[i].timestamp
        )
    '''

    length = len(imuDatas)
    fig, ax = plt.subplots()
    for i in range(3):
        plt.subplot(3, 2, i*2+1)
        plt.plot(np.arange(length), np.array([x.acc[i] for x in imuDatas[:length]]))

        plt.subplot(3, 2, (i+1)*2)
        plt.plot(np.arange(length), np.array([x.gyro[i] for x in imuDatas[:length]]))
    plt.show()
