
from redis.client import Redis

database = Redis("37.114.63.21", 6379, 0)
with open("questions.csv", "r") as f:
    questions = f.readlines()

for q in questions:
    q = q.strip()
    question = q.split(":")[0]
    answer = q.split(":")[1]
    print(question + " -> " + answer)
    database.set(question, answer)