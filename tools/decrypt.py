import httpx, json

def decrypt(data: str) -> str:
    url = "http://solver.dexv.lol:1500/decrypt"
    json = {"data": data, "key": "88de30e1c0d0e89d"}
    return httpx.post(url, json=json).text

decrypted = decrypt("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")

try:
    decrypted_json = json.loads(decrypted)
    print(json.dumps(decrypted_json, indent=4))
except json.JSONDecodeError:
    print("yeah")