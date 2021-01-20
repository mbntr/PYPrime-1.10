import math
from platform import system, release, version
from subprocess import check_output
from ctypes import WinDLL, wintypes, byref


# Imports kernel32.dll
kernel32 = WinDLL('kernel32', use_last_error=True)

starting_time = wintypes.LARGE_INTEGER()
ending_time = wintypes.LARGE_INTEGER()
elapsed_time = wintypes.LARGE_INTEGER()
frequency = wintypes.LARGE_INTEGER()

QueryPerformanceFrequency = kernel32.QueryPerformanceFrequency(byref(frequency))

# Upper limit for primes
pr = 8000000
OS = system()
Runs = []


# Main UI

class UI:
    Title = f"{85 * '-'}\n{35 * ' '}PYPrime 1.10 Windows{35 * ' '}\n{85 * '-'}\n\n"
    Description = '\nThis is a strictly single core benchmark. Please close all applications running in background to get the most reliable result\n'
    UserInput = f'{34 * "*"}\nPress ENTER to start the benchmark'
    ExitPrompt = 'Press ENTER to exit'
    InvalidExitPrompt = '\nInvalid run detected, press ENTER to exit'
    StartThing = 'Starting Benchmark...\n'

    def __init__(self, t):
        self.t = t

    # Score

    def Score(self):
        ScoreText = f"Average completion time: {round(self.t, 3)} s"
        hashes = "\n" + len(ScoreText) * "#" + "\n"
        print(hashes + ScoreText + hashes)


# Gets the system specifications

class Specs:
    def __init__(self, Sys):
        # OS and build version
        self.System = Sys
        self.sys = f'{self.System} {release()}, Build {version()}'
        self.timer = frequency.value / 1000000

    def system_info(self):
        return f'OS: {self.sys}\n' \
               f'Timer: {self.timer} MHz\n'


# Prime Calculation


def Benchmark(limit):
    P = [2, 3]
    sieve = [False] * (limit + 1)
    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):
            n = 4 * x ** 2 + y ** 2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                sieve[n] = not sieve[n]
            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7:
                sieve[n] = not sieve[n]
            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11:
                sieve[n] = not sieve[n]
    for x in range(5, int(math.sqrt(limit))):
        if sieve[x]:
            for y in range(x ** 2, limit + 1, x ** 2):
                sieve[y] = False
    for p in range(5, limit):
        if sieve[p]:
            P.append(p)

    return P[-1]


# Executes the main algorithm and calculates the elapsed time using the QPC timer


def main(QPF):
    valid = False
    kernel32.QueryPerformanceCounter(byref(starting_time))
    if Benchmark(pr) == 7999993:
        valid = True
    kernel32.QueryPerformanceCounter(byref(ending_time))
    elapesed_time = ending_time.value - starting_time.value
    elapesed_time /= QPF

    Runs.append(elapesed_time)
    return [valid, elapesed_time]


System = Specs(OS)


print(UI.Title + System.system_info() + UI.Description)
input(UI.UserInput)
print(UI.StartThing)

# Runs the benchmark 5 times and then calculates the average completion time
while True:
    for i in range(5):
        results = main(frequency.value)
        print(f"Completed run {i + 1}/5 in {round(results[1], 3)}s {'VALID' if results[0] == True else 'INVALID'}")
        if not results[0]:
            break
    else:
        CurrentScore = UI(sum(sorted(Runs)[1:4]) / 3)
        CurrentScore.Score()

        # Asks for input to close the program, otherwise the window would close instantly after finishing the benchmark
        input(UI.ExitPrompt)
        break
    input(UI.InvalidExitPrompt)
    break
