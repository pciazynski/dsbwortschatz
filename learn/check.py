ff = {}

with open("falsefriends.txt", "r", encoding="utf8") as inf:
    for line in inf:
        ff[line.strip()] = 1
        
with open("deu_found.txt", "r", encoding="utf8") as inf:
    for line in inf:
        if line.strip() in ff:
            print(line)
            
