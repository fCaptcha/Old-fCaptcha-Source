import multiprocessing

from tools.DiscordGen import proc

if __name__ == '__main__':
    for i in range(2):
        multiprocessing.Process(target=proc).start()
