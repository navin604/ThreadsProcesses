import random
import string
import time
import hashlib
import multiprocessing
import sys

global q
q = multiprocessing.Queue()
times = []

def setup(num):
    """Sets up workers"""
    count = 1
    processes = []

    total_time = 0
    while count <= int(num):
        process = multiprocessing.Process(target=math_function)
        processes.append(process)
        count += 1
    for i in processes:
        i.start()
    for j in processes:
        j.join()
    for i in range(int(num)):
        val = q.get()
        times.append(val)
    for i in times:
        total_time = total_time + i
        with open("Processing.txt", "a") as file:
            file.write(str(i) + "\n")
    total_time = total_time/int(num)
    print(f"Average worker run time: {round(total_time,3)}")


def math_function():
    """Performs system intensive operation"""
    count = 0
    arr = []
    start = time.time()
    while count < 10000:
        hash_string = ''.join(random.choices(string.ascii_letters +
                                             string.digits, k=100))
        hash_object = hashlib.sha3_256(str.encode(hash_string))
        with open("Processing.txt", "a") as file:
            file.write(hash_object.hexdigest() +"\n")
        arr.append(hash_object.hexdigest())
        count +=1
    end = time.time()
    q.put(round(end - start, 3))


if __name__ == "__main__":
    try:
        val = int(sys.argv[1])
    except:
        sys.exit('Must enter valid amount of workers')
    setup(val)
