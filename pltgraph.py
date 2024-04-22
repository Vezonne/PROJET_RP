import matplotlib.pyplot as plt

n = [8, 10, 12, 14, 16]
dd_time = [0.0011, 0.0012, 0.00151, 0.00151, 0.00171]
dd_res = [3.4, 2.4, 3, 3.7, 3.4]
md_time = [1.74, 2.01, 3.79, 2.6, 0.825]
md_res = [3.4, 3, 2, 3.5, 3.4]
ash1_time = [0.0014, 0.00499, 0.00367, 0.00501, 0.00378]
ash1_res = [3.4, 3, 3, 3.7, 3.4]
ash2_time = [4.55, 27.7, 56.4, 1.17, 126]
ash2_res = [1.9,1.8, 2.1, 2.2, 2.4]
asm_time = [2.53, 7.11, 0.187, 2.06, 6.01]
asm_res = [3.4, 3, 2, 3.5, 3.4]

k=[1, 2, 3, 4, 5]
dd_robot_res=[3.2, 2.5, 3.0, 2.8, 2.6]
dd_robot_time=[0.000649, 0.00055, 0.0003, 0.000552, 0.000602]
md_robot_res=[3.2, 2.6, 3.0, 2.7, 2.6]
md_robot_time=[0.00165, 0.0186, 0.0789, 0.294, 0.359]
ash1_robot_res=[3.2, 2.5, 3.0, 2.8, 2.6]
ash1_robot_time=[0.00045, 0.0003, 0.000398, 0.000351, 0.000349]

plt.figure()
plt.plot(n, dd_time, label="DD")
plt.plot(n, md_time, label="MD")
plt.plot(n, ash1_time, label="ASH1")
plt.plot(n, ash2_time, label="ASH2")
plt.plot(n, asm_time, label="ASM")

plt.xlabel("n")
plt.ylabel("Time (s)")
plt.legend()
plt.grid()
plt.savefig(".\img\pltgraph_time.png")

plt.figure()
plt.plot(n, dd_res, label="DD")
plt.plot(n, md_res, label="MD")
plt.plot(n, ash1_res, label="ASH1")
plt.plot(n, ash2_res, label="ASH2")
plt.plot(n, asm_res, label="ASM")

plt.xlabel("n")
plt.ylabel("OPT")
plt.legend()
plt.grid()
plt.savefig(".\img\pltgraph_res.png")



plt.figure()
plt.plot(k, dd_robot_time, label="DD")
plt.plot(k, md_robot_time, label="MD")
plt.plot(k, ash1_robot_time, label="ASH1")


plt.xlabel("k")
plt.ylabel("Time (s)")
plt.legend()
plt.grid()
plt.savefig(".\img\pltgraph_robot_time.png")

plt.figure()
plt.plot(k, dd_robot_res, label="DD")
plt.plot(k, md_robot_res, label="MD")
plt.plot(k, ash1_robot_res, label="ASH1")

plt.xlabel("k")
plt.ylabel("OPT")
plt.legend()
plt.grid()
plt.savefig(".\img\pltgraph_robot_res.png")