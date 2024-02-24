def remove_dupes():
    counts = {}

    with open("scraped.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line in counts:
            counts[line] += 1
        else:
            counts[line] = 1

    dupes = [line for line, count in counts.items() if count > 1]
    non = [line for line, count in counts.items() if count == 1]

    for line in dupes:
        print(line)

    with open("questions.txt", 'w', encoding="utf-8") as f:
        for line in non:
            if '>>' in line and (line.lower().endswith('ja\n') or line.lower().endswith('nej\n')):
                f.write(line)

    print(f"non dupes: {len(non)} / dupes: {len(lines) - len(non)}")

remove_dupes()
input()