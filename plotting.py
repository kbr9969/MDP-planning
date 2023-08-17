import matplotlib.pyplot as plt
import numpy as np
import random
import argparse
import sys
import subprocess
import os
parser = argparse.ArgumentParser()

random.seed(0)


def encode_pol_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()
    S = len(lines)
    actions = [0, 1, 2, 4, 6]
    actions_idx = {0: 0, 1: 1, 2: 2, 4: 3, 6: 4}
    policy = []
    for line in lines:
        action = int(line.strip().split()[-1])
        policy.append(actions_idx[action])
    for x in range(S+2):
        policy.append(0)
    for a in policy:
        print(a)


def plot1():
    diff = 20
    balls = 15
    runs = 30
    Q = np.array(list(range(0, diff)))
    p1_parameter = "./data/cricket/sample-p1.txt"
    opt_probs, rand_probs = [], []
    for q in Q:
        q /= diff
        q = str(q)
        cmd_encoder = "python", "cricket_states.py", "--balls", str(
        balls), "--runs", str(runs)
        # print("\n","Generating the MDP encoding using encoder.py")
        f = open('states', 'w')
        subprocess.call(cmd_encoder, stdout=f)
        f.close()
        cmd_encoder = "python", "encoder.py", "--parameters", p1_parameter, "--q", q, "--states", "states"
        # print("\n","Generating the MDP encoding using encoder.py")
        f = open('verify_attt_mdp', 'w')
        subprocess.call(cmd_encoder, stdout=f)
        f.close()

        cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp"
        # print("\n","Generating the value policy file using planner.py using default algorithm")
        f = open('policy', 'w')
        subprocess.call(cmd_planner, stdout=f)
        f.close()
        with open("policy", "r") as f:
            lines = f.readlines()
        opt_prob = float(lines[0].strip().split()[0])
        os.remove('verify_attt_mdp')
        os.remove("policy")

        cmd_encoder = "python", "encoder.py", "--parameters", p1_parameter, "--q", q, "--states", "states"
        # print("\n","Generating the MDP encoding using encoder.py")
        f = open('verify_attt_mdp', 'w')
        subprocess.call(cmd_encoder, stdout=f)
        f.close()

        cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp", "--policy", "encoded_pol.txt"
        # print("\n","Generating the value policy file using planner.py using default algorithm")
        f = open('policy2', 'w')
        subprocess.call(cmd_planner, stdout=f)
        f.close()
        with open("policy2", "r") as f:
            lines = f.readlines()
        rand_prob = float(lines[0].strip().split()[0])
        opt_probs.append(opt_prob)
        rand_probs.append(rand_prob)
        os.remove('verify_attt_mdp')
        os.remove('policy2')
        # cmd_decoder = "python","decoder.py","--value-policy","verify_attt_planner","--states",states
        # #print("\n","Generating the decoded policy file using decoder.py")
        # cmd_output = subprocess.check_output(cmd_decoder,universal_newlines=True)

    fig, ax = plt.subplots()
    ax.plot(Q/diff, rand_probs, label="random policy")
    ax.plot(Q/diff, opt_probs, label="optimal policy")
    plt.legend()
    plt.show()
    plt.savefig("plot1.png")


def plot2():
    balls = 15
    q = 0.25
    runs = 30
    p1_parameter = "./data/cricket/sample-p1.txt"
    opt_probs, rand_probs = [], []
    cmd_encoder = "python", "cricket_states.py", "--balls", str(
        balls), "--runs", str(runs)
    # print("\n","Generating the MDP encoding using encoder.py")
    f = open('states', 'w')
    subprocess.call(cmd_encoder, stdout=f)
    f.close()

    cmd_encoder = "python", "encoder.py", "--parameters", p1_parameter, "--q", str(
        q), "--states", "states"
    # print("\n","Generating the MDP encoding using encoder.py")
    f = open('verify_attt_mdp', 'w')
    subprocess.call(cmd_encoder, stdout=f)
    f.close()

    cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp"
    # print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('policy', 'w')
    subprocess.call(cmd_planner, stdout=f)
    f.close()
    with open("policy", "r") as f:
        lines = f.readlines()
    for i in range(160, 180):
        opt_probs.append(float(lines[i].strip().split()[0]))

    cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp", "--policy", "encoded_pol.txt"
    # print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('policy2', 'w')
    subprocess.call(cmd_planner, stdout=f)
    f.close()
    with open("policy2", "r") as f:
        lines = f.readlines()
    for i in range(160, 180):
        rand_probs.append(float(lines[i].strip().split()[0]))
    opt_probs = list(reversed(opt_probs))
    rand_probs = list(reversed(rand_probs))
    os.remove("states")
    os.remove('verify_attt_mdp')
    os.remove('policy2')
    os.remove("policy")

    fig, ax = plt.subplots()
    X = np.array(list(range(1, 21)))
    ax.plot(X, np.array(rand_probs), label="random policy")
    ax.plot(X, np.array(opt_probs), label="optimal policy")
    ax.set(xlim=(0, 22))
    plt.xticks(list(range(1, 21)))
    plt.legend()
    plt.show()
    plt.savefig("plot2.png")


def plot3():
    balls = 15
    q = 0.25
    runs = 30
    p1_parameter = "./data/cricket/sample-p1.txt"
    opt_probs, rand_probs = [], []
    cmd_encoder = "python", "cricket_states.py", "--balls", str(balls), "--runs", str(runs)
    # print("\n","Generating the MDP encoding using encoder.py")
    f = open('states', 'w')
    subprocess.call(cmd_encoder, stdout=f)
    f.close()

    cmd_encoder = "python", "encoder.py", "--parameters", p1_parameter, "--q", str(q), "--states", "states"
    # print("\n","Generating the MDP encoding using encoder.py")
    f = open('verify_attt_mdp', 'w')
    subprocess.call(cmd_encoder, stdout=f)
    f.close()

    cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp"
    # print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('policy', 'w')
    subprocess.call(cmd_planner, stdout=f)
    f.close()
    with open("policy", "r") as f:
        lines = f.readlines()
    for i in range(20,(len(lines)-2)//2,runs):
        opt_probs.append(float(lines[i].strip().split()[0]))

    cmd_planner = "python", "planner.py", "--mdp", "verify_attt_mdp", "--policy", "encoded_pol.txt"
        # print("\n","Generating the value policy file using planner.py using default algorithm")
    f = open('policy2', 'w')
    subprocess.call(cmd_planner, stdout=f)
    f.close()
    with open("policy2", "r") as f:
        lines = f.readlines()
    for i in range(20,(len(lines)-2)//2,runs):
        rand_probs.append(float(lines[i].strip().split()[0]))
    
    opt_probs = list(reversed(opt_probs))
    rand_probs = list(reversed(rand_probs))
    os.remove("states")
    os.remove('verify_attt_mdp')
    os.remove('policy2')
    os.remove("policy")

    fig, ax = plt.subplots()
    X = np.array(list(range(1, 16)))
    ax.plot(X, np.array(rand_probs), label="random policy")
    ax.plot(X, np.array(opt_probs), label="optimal policy")
    ax.set(xlim=(0, 18))
    plt.xticks(list(range(1, 16)))
    plt.legend()
    plt.show()
    plt.savefig("plot3.png")


if __name__ == "__main__":
    #encode_pol_file("./data/cricket/rand_pol.txt")
    plot1()
    plot2()
    plot3()
