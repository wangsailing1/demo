def hanshu(x,y,s):
    n = 0
    for i in s:
        if i == 'p' or i == 'P':
            n+=1
        elif i == 'm' or i == 'M':
            x += 100
        elif i == 'l' or i == 'L':
            if n % 2:
                y += 100
            else:
                y -= 100
        elif i == 'r' or i == 'R':
            if n % 2:
                y -= 100
            else:
                y += 100
        else:
            print("test OK")
    return x,y

print(hanshu(11,39,'MTMPRPMTMLMRPRMTPLMTLMRRMP'))







