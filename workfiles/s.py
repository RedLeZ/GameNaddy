operateur = '+-*/' # les operateur 

x = int(input("Saisir X : ")) # hot X
y = int(input("Saisir Y : ")) # hot Y
op = input('Choisissez un opérateur (+, -, * ou /)') # 5taR operateur

if len(op) == 1 : # kan fama op barka (mich (+-) wala (*/) mithal, ya3ni fih harif barka)
    if op in operateur: # kan el op majoud fil lista 'operateur'
        if op == '+': # kan el operateur ='+' 
            print(x + y) # 3melna X + y
        elif op == '-': # kan el operateur = '-'
            print(x - y) # 3melna X - y
        elif op == '*' : # kan el operateur = '*'
            print(x * y) # 3melna X * y
        elif op == '/' : # 3melna X / y
            if y != 0 : # kan y mahish 0
                print(x / y) # 3melna X / y
            else :
                print("Erreur division par zero") # kan y == 0
    else :
        print ("Opérateur incorrect") #kan el op mahoush fil lista 'operateur'
else :
    print("Erreur") # kan op fiha akter min kelma