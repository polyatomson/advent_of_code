with open("15/input.txt", 'r') as f:
    dat = f.read()

dat.replace('\n', '')
dat = dat.split(',')

def hash(line: str):
    current = 0
    for char in line:
        current += ord(char)
        current *= 17
        current = current%256
    return(current)


res = [hash(record) for record in dat]
print("Result", sum(res))

