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
    StartThing = 'Starting Benchmark...\n'

    def __init__(self, t):
        self.t = t
    # Score

    def Score(self):
        ScoreText = f"Average completion time: {round(self.t, 3)} s"
        hashes = "\n"+len(ScoreText)*"#"+"\n"
        print(hashes + ScoreText + hashes)

    def __str__(self):
        return

# Gets the system specifications


class Specs:
    def __init__(self, System):
        self.System = System
        # OS and build version
        self.sys = f'{self.System} {release()}, Build {version()}'
        # CPU model name
        self.cpu = check_output('wmic cpu get name /format:list').strip().decode()[5:]
        # CPU Clock base clock speed
        self.clock = float(check_output('wmic cpu get currentclockspeed').strip().decode()[22:]) / 1000
        # Total ram installed
        self.ram = round(float(check_output('wmic OS get TotalVisibleMemorySize /Value').strip().decode()[23:]) / 1048576, 1)

    def system_info(self):
        return f'OS: {self.sys}\n' \
               f'CPU: {self.cpu}\n' \
               f'CPU Base Clock Speed: {self.clock} GHz\n' \
               f'Total RAM installed: {self.ram} GB\n'

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

# Executes the main algorithm and calculates the elapsed time using the QPC timer


def main():
    kernel32.QueryPerformanceFrequency(byref(frequency))
    kernel32.QueryPerformanceCounter(byref(starting_time))
    Benchmark(pr)
    kernel32.QueryPerformanceCounter(byref(ending_time))

    elapesed_time = ending_time.value - starting_time.value
    elapesed_time /= frequency.value

    Runs.append(elapesed_time)


System = Specs(OS)
print(UI.Title + System.system_info() + UI.Description)
input(UI.UserInput)
print(UI.StartThing)

# Runs the benchmark 5 times and then calculates the average completion time
for i in range(5):
    main()
    print(f"Completed run {i + 1}/5")

CurrentScore = UI(sum(Runs) / len(Runs))
CurrentScore.Score()

# Asks for input to close the program, otherwise the window would close instantly after finishing the benchmark
input(UI.ExitPrompt)
