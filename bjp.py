
with open("config.txt", 'r') as f:
    cleaned = [line for line in f.readlines() if line != '\n']
    path = cleaned[1].split('"', 1)[1].replace('"', "")
    print(path)