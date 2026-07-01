from memorine import Mind
import random
import string
import mpire
import multiprocessing 
from mpire import WorkerPool
from pprint import pprint
import itertools
num_cores =max(multiprocessing.cpu_count()//2,1)
import shutil
import random
from multiprocessing import Manager
from pprint import pprint
def smart_parallel_learn(agi_name,fid_to_correct,task):
    brain = Mind(agi_name)
    brain.correct(fid_to_correct, task)
    # print(f"Corrected memory ID: {fid_to_correct}")
    return {"fid_to_correct": fid_to_correct, "task": task}

def create_agi(tasks, agi_name):
    brain = Mind(agi_name)

    all_jobs = []

    for task in tasks:
        fid, contradictions = brain.learn(task)

        if contradictions:
            all_jobs.extend(
                {
                    "agi_name": agi_name,
                    "fid_to_correct": c["id"],
                    "task": task,
                }
                for c in contradictions
            )

    with WorkerPool(n_jobs=num_cores, daemon=False) as pool:
        pool.map(smart_parallel_learn, all_jobs)

    return brain

def ask_agi(brain, query):
    correct_response = brain.recall(query)
    results = []
    for resp in correct_response:
        if resp.get("fact"):
            results.append(resp.get("fact"))
    return list(set(results))  # Return unique responses


if __name__ == "__main__":
    agi_name = ''.join(
        random.choices(string.ascii_letters + string.digits, k=100)
    )

    tasks = [
        "Tony Stark is not Iron Man",
        "Tony Stark is Iron Man",
        "Rhodey James is also Iron Man"
    ]

    agi_system = create_agi(tasks, agi_name)
    print("\AGI created successfully.")

    query = "Who wears Iron Man Armour?"
    print(f"\nQuery: {query}")
    response = ask_agi(agi_system, query)
    print(f"Response:")
    pprint(response)
