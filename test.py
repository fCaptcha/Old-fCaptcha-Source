import g4f

g4f.debug.logging = False
g4f.debug.version_check = False

response = g4f.ChatCompletion.create(
    model=g4f.models.llama2_70b,
    messages=[{"role": "user", "content": "srictly respond to the following question with only a single word, number, or phrase : What legendary beast bears a horn?"}],
)

print(response)
