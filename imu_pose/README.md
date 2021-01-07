# measure pose from imu sensor

## 1. IMU motion model

### posiiton and velocity
$$
\frac{dp}{dt} = v
$$

$$
v_{W}^{i+1} = v_{W}^i + a_{W}*\Delta t
$$

$$
\frac{dv}{dt} = a
$$

$$
p_{W}^{i+1} = p_{W}^i + v_{W}^{i}*\Delta t + \frac{1}{2}a_{W} \Delta t^2
$$

### rotation
![](https://img-blog.csdnimg.cn/20200608220033626.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM0MjEzMjYw,size_16,color_FFFFFF,t_70)

$$
\frac{dr}{dt} = w_{B} \times r = w_{B} \hat{} \cdot r
$$

$$
w_{B} \hat{} = 
\begin{bmatrix}
0 & -w_3 & w_2 \\
w_3 & 0 & -w_1 \\
-w_2 & w_1 & 0
\end{bmatrix}
$$

$$
w_{B} = R_B^W w_W
$$