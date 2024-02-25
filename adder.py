from redis.client import Redis

database = Redis("147.189.168.82", 6379, 0, "4wHQaoenQxqk4E@FC8")
with open("questions.csv", "r") as f:
    questions = f.readlines()

for q in questions:
    q = q.strip()
    question = q.split(":")[0]
    answer = q.split(":")[1]
    print(question + " -> " + answer)
    database.set(question, answer)