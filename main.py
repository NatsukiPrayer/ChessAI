import itertools
import signal
from time import sleep
import time
from Field import Field
from random import randint
import multiprocessing as mp
import worker
from AIPlayer import AI
import torch
from itertools import permutations, product
from os import cpu_count


def test(players, cond):
    player1, player2 = players
    start = time.time()
    t = randint(5, 10)
    print(f"Playing game between {player1.ID} and {player2.ID} for {t} seconds")
    # ...
    # Play the game logic here
    # ...
    sleep(t)  # Simulating game time
    print(f"Finishing game between {player1.ID} and {player2.ID}")
    return (start, (player1.ID, player2.ID))


def main():
    epoch = 0
    while True:
        print("Noew playing epoch: ", epoch)
        ghostMain(64, epoch)

        epoch += 1


def ghostMain(numOfPlayers, epoch):
    players = [AI(id) for id in range(numOfPlayers)]

    matches = {p.ID: {p1.ID: -1 for p1 in players if p.ID != p1.ID} for p in players}

    playingNow = []

    def forCallback(res):
        # player1 = res[2]
        # player2 = res[3]
        # id1, id2 = res[1]
        # players[id1] = player1
        # players[id2] = player2
        id0 = res[0].ID
        id1 = res[1].ID
        matches[id0][id1] = 1
        if id0 in playingNow:
            playingNow.pop(playingNow.index(id0))
        if id1 in playingNow:
            playingNow.pop(playingNow.index(id1))

    def wait_for(async_results):
        for idx, ar in enumerate(async_results):
            try:
                if not ar.ready():
                    continue
                newPlayers = ar.get()
            except mp.TimeoutError:
                raise TimeoutError
            else:
                for pl in newPlayers:
                    players[pl.ID].score = pl.score
                    players[pl.ID].memory = pl.memory
                async_results.pop(async_results.index(ar))

    workers = 8  # cpu_count()

    workers = min(workers, int(len(players) / 2))

    semaphores = mp.BoundedSemaphore(workers)  # type: ignore

    pool = mp.Pool(workers, worker.initialize, [semaphores])
    async_results = []
    while True:
        end = True
        for k1 in matches:
            for k2 in matches[k1]:
                if (
                    matches[k1][k2] == -1
                    and k1 not in playingNow
                    and k2 not in playingNow
                ):
                    end = False
                    async_results.append(
                        pool.apply_async(
                            worker.execute,
                            args=[(players[k1], players[k2]), False],
                            callback=forCallback,
                        )
                    )
                    playingNow.append(k1)
                    playingNow.append(k2)
        if end and playingNow == []:
            break
        try:
            wait_for(async_results)
        except:
            pool.terminate()
            raise

    pool.close()
    pool.join()
    bestScore = 0
    bestIdx = 0
    for player in players:
        print(f"Player {player.ID} score is {player.score}")
        if player.score > bestScore:
            bestScore = player.score
            bestIdx = player.ID

    if epoch % 10 == 0:
        torch.save(players[bestIdx].net, f"BESTBOYES/BESTBOYBITCH{epoch}.pt")


if __name__ == "__main__":
    main()

    # _parallelism_semaphores = None

    # def callback():
    #     return "A KAKOgo hUYA??"

    # def wait_for(async_results):
    #     for idx, ar in enumerate(async_results):
    #         try:
    #             test = ar.get(600)
    #         except mp.TimeoutError:
    #             raise TimeoutError
    #         else:
    #             print(test)
    #             if test[0] == "draw":
    #                 players[test[1][0]].changeScore(0.5)
    #                 players[test[1][1]].changeScore(0.5)
    #             else:
    #                 players[test[1][int(test[0] == "black lost")]].changeScore(1)

    # workers = 1  # cpu_count()
    # players = [AI(id) for id in range(2)]

    # matches = product(players, repeat=2)

    # semaphores = mp.BoundedSemaphore(workers)  # type: ignore
    # pool = mp.Pool(workers, worker.initialize, [semaphores])
    # async_results = [
    #     pool.apply_async(worker.execute, args=[match, False])
    #     for match in matches
    #     if match[0].ID != match[1].ID
    # ]
    # pool.close()

    # try:
    #     wait_for(async_results)
    # except:
    #     pool.terminate()
    #     raise
    # finally:
    #     pool.join()
    # for player in players:
    #     print(f"Player {player.ID} score is {player.score}")
