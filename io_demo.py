
with open('G:/logs/老TPP/tpp-transfer/thirdpp-transfer.log', 'r+', encoding='UTF-8', errors='ignore') as f:
    for line in f.readlines():
        print(line.strip())  # 把末尾的'\n'删掉
    f.write('Hello, worl d!')