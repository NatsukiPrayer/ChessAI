import signal
from Field import Field
from random import randint
import multiprocessing as mp
import worker
from AIPlayer import AI
from itertools import permutations, product
from os import cpu_count

if __name__ == "__main__":
    _parallelism_semaphores = None

    def initialize(parallelism_semaphores):
        global _parallelism_semaphores
        _parallelism_semaphores = parallelism_semaphores

        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def callback():
        return "A KAKOgo hUYA??"

    def wait_for(async_results):
        for idx, ar in enumerate(async_results):
            try:
                test = ar.get(600)
            except mp.TimeoutError:
                raise TimeoutError
            else:
                print(test)
                if test[0] == "draw":
                    players[test[1][0]].changeScore(0.5)
                    players[test[1][1]].changeScore(0.5)
                else:
                    players[test[1][int(test[0] == "black lost")]].changeScore(1)

    workers = cpu_count()
    players = [AI(id) for id in range(16)]
    matches = product(players, repeat=2)
    semaphores = mp.BoundedSemaphore(workers)  # type: ignore
    pool = mp.Pool(workers, worker.initialize, [semaphores])
    async_results = [
        pool.apply_async(worker.execute, args=[match, False])
        for match in matches
        if match[0].ID != match[1].ID
    ]
    pool.close()

    try:
        wait_for(async_results)
    except:
        pool.terminate()
        raise
    finally:
        pool.join()
    for player in players:
        print(f"Player {player.ID} score is {player.score}")
