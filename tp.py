#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # ATTENTION: test_tp modifie la valeur de END

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')


############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert (len(char) <= 1)
    # RMQ: on n'utilise pas 1 <= int(char) <= 9 car cela échoue sur la chaîne vide
    return '1' <= char <= '9'

def digit(char):
    assert (len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur

def integer_Q2():
    init_char()
    return integer_Q2_state_0()


def integer_Q2_state_0():
    ch = next_char()
    if ch == "0":
        return integer_Q2_state_1()
    elif nonzerodigit(ch):
        return integer_Q2_state_2()
    return False

def integer_Q2_state_1():
    ch = next_char()
    if ch == "0":
        return integer_Q2_state_1()
    elif ch == END:
        return True
    return False

def integer_Q2_state_2():
    ch = next_char()
    if digit(ch):
        return integer_Q2_state_2()
    elif ch == END:
        return True
    return False

def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

def pointfloat_Q2_state_0():
    ch = next_char()
    if ch == ".":
        return pointfloat_Q2_state_1()
    elif digit(ch):
        return pointfloat_Q2_state_2()
    return False

def pointfloat_Q2_state_1():
    
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    return False

def pointfloat_Q2_state_2():
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch == ".":
        return pointfloat_Q2_state_3()
    return False

def pointfloat_Q2_state_3():
    ch = next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    elif ch == END:
        return True
    return False



############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0

def integer():
    init_char()
    return integer_state_0()


def integer_state_0():
    global int_value
    ch = next_char()
    if ch == "0":
        int_value = 0
        return integer_state_1()
    elif nonzerodigit(ch):
        int_value = int(ch)
        return integer_state_2()
    return (False, None)

def integer_state_1():
    global int_value
    ch = next_char()
    if ch == "0":
        return integer_state_1()
    elif ch == END:
        return (True, int_value)
    return (False, None)

def integer_state_2():
    global int_value
    ch = next_char()
    if digit(ch):
        int_value = int_value*10 + int(ch)
        return integer_state_2()
    elif ch == END:
        return (True, int_value)
    return (False, None)


############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0.
    exp_value = 0
    return pointfloat_state_0()

def pointfloat_state_0():
    global int_value
    global exp_value
    ch = next_char()
    if ch == ".":
        exp_value = 0
        return pointfloat_state_1()
    elif digit(ch):
        int_value = int(ch)
        return pointfloat_state_2()
    return (False, None)

def pointfloat_state_1():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        exp_value += 1
        int_value = int_value*10 + int(ch)
        return pointfloat_state_3()
    return (False, None)

def pointfloat_state_2():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        int_value = int_value*10 + int(ch)
        return pointfloat_state_2()
    elif ch == ".":
        exp_value = 0
        return pointfloat_state_3()
    return (False, None)

def pointfloat_state_3():
    global int_value
    global exp_value
    ch = next_char()
    if digit(ch):
        exp_value += 1
        int_value = int_value*10 + int(ch)
        return pointfloat_state_3()
    elif ch == END:
        return (True, int_value* (10**(-exp_value)))
    return (False, None)



############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value = 0


def exponent():
    global exp_value
    init_char()
    exp_value = 0
    return exponent_state_0()


def exponent_state_0():
    global exp_value
    ch = next_char()
    if ch == "e" or ch == "E":
        return exponent_state_1()
    return (False, None)


def exponent_state_1():
    global sign_value
    global exp_value
    ch = next_char()
    if ch == "+":
        sign_value = 1
        return exponent_state_2()
    
    elif ch == "-":
        sign_value = -1
        return exponent_state_2()

    elif digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return exponent_state_3()
    return (False, None)


def exponent_state_2():
    global exp_value
    ch = next_char()
    if digit(ch):
        exp_value = int(ch)
        return exponent_state_3()
    return (False, None)


def exponent_state_3():
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = 10*exp_value + int(ch)
        return exponent_state_3()
    elif ch == END:
        return (True, exp_value*sign_value)
    return (False, None)




def exponentfloat():
    global int_value
    global exp_value
    global sign_value
    init_char()
    exp_value = 0
    int_value = 0
    return exponentfloat_state_0()

def exponentfloat_state_0():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if ch == ".":
        return exponentfloat_state_2()
    elif digit(ch):
        int_value = int(ch)
        return exponentfloat_state_1()
 
    return (False, None)

def exponentfloat_state_1():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        int_value = int_value*10+int(ch)
        return exponentfloat_state_1()
    elif ch == ".":
        return exponentfloat_state_2()
    elif ch == "e" or ch == "E":
        return exponentfloat_state_3()
        
    return (False, None)


def exponentfloat_state_2():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value += 1
        int_value = int_value*10+int(ch)
        return exponentfloat_state_2()
    elif ch == "e" or ch == "E":
        int_value = int_value* (10**(-exp_value))
        return exponentfloat_state_3()
    return (False, None)
    
def exponentfloat_state_3():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if ch == "+":
        sign_value = 1
        return exponentfloat_state_4()
    
    elif ch == "-":
        sign_value = -1
        return exponentfloat_state_4()

    elif digit(ch):
        sign_value = 1
        exp_value = int(ch)
        return exponentfloat_state_5()
    return (False, None)


def exponentfloat_state_4():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = int(ch)
        return exponentfloat_state_5()
    return (False, None)


def exponentfloat_state_5():
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch):
        exp_value = 10*exp_value + int(ch)
        return exponentfloat_state_5()
    elif ch == END:
        return (True, int_value*(10**(exp_value*sign_value)))
    return (False, None)


def number():
    global int_value
    global exp_value
    global sign_value
    int_value = 0
    exp_value = 0
    sign_value = 0
    init_char()
    return number_state_0()

def number_state_0() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if ch == '0' :
        return number_state_1()
    elif nonzerodigit(ch) :
        int_value = int(ch)
        return number_state_2()
    elif ch == '.' :
        return number_state_3()
    return (False, None)

def number_state_1() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if ch == '0' :
        return number_state_1()
    elif ch == 'E' or ch == 'e' :
        return number_state_6()
    elif nonzerodigit(ch) :
        int_value = int(ch)
        return number_state_5()
    elif ch == '.' :
        return number_state_4()
    elif ch == END or ch == " ":
        return (True, int_value)
    return (False, None)

def number_state_2() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        int_value = int_value * 10 + int(ch)
        return number_state_2()
    elif ch == '.' :
        return number_state_4()
    elif ch == 'E' or ch == 'e' :
        return number_state_6()
    elif ch == END or ch == " ":
        return (True, int_value)
    return (False, None)

def number_state_3() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        exp_value += 1
        int_value = int_value * 10 + int(ch)
        return number_state_4()
    return (False, None)

def number_state_4() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        exp_value += 1
        int_value = int_value * 10 + int(ch)
        return number_state_4()
    elif ch == 'E' or ch == 'e' :
        int_value = int_value * (10**(-exp_value))
        return number_state_6()
    elif ch == END or ch == " ":
        return (True, int_value * (10**(-exp_value)))
    return (False, None)

def number_state_5() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        int_value = 10 * int_value + int(ch)
        return number_state_5()
    elif ch == '.' :
        return number_state_4()
    elif ch == 'E' or ch == 'e' :
        return number_state_6()
    return (False, None)

def number_state_6() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        sign_value = 1
        exp_value = int(ch)
        return number_state_8()
    elif ch == '+' :
        sign_value = 1
        return number_state_7()
    elif ch == '-' :
        sign_value = -1
        return number_state_7()
    return (False, None)

def number_state_7() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        exp_value = int(ch)
        return number_state_8()
    return (False, None)

def number_state_8() :
    global int_value
    global exp_value
    global sign_value
    ch = next_char()
    if digit(ch) :
        exp_value = 10* exp_value + int(ch)
        return number_state_8()
    elif ch == END or ch == " ":
        return (True, int_value*(10** (exp_value*sign_value)))
    return (False, None)



########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    elif ch == "-":
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 - n2
    elif ch == "*":
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 * n2
    elif ch == "/":
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 / n2
    else: 
        return number()[1]

############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''


def number_v2():
    global int_value
    global exp_value
    global sign_value
    int_value = 0
    exp_value = 0
    sign_value = 0
    init_char()
    return number_v2_state_0()

def number_v2_state_0() :
    global int_value
    global exp_value
    global sign_value
    ch = peek_char()
    if ch == '0' :
        return number_v2_state_1()
    elif nonzerodigit(ch) :
        int_value = int(ch)
        return number_v2_state_2()
    elif ch == '.' :
        return number_v2_state_3()
    return (False, None)

def number_v2_state_1() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if ch == '0' :
        return number_v2_state_1()
    elif ch == 'E' or ch == 'e' :
        return number_v2_state_6()
    elif nonzerodigit(ch) :
        int_value = int(ch)
        return number_v2_state_5()
    elif ch == '.' :
        return number_v2_state_4()
    elif ch == END or ch == " ":
        return (True, int_value)
    return (False, None)

def number_v2_state_2() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        int_value = int_value * 10 + int(ch)
        return number_v2_state_2()
    elif ch == '.' :
        return number_v2_state_4()
    elif ch == 'E' or ch == 'e' :
        return number_v2_state_6()
    elif ch == END or ch == " ":
        return (True, int_value)
    return (False, None)

def number_v2_state_3() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    print(ch)
    if digit(ch) :
        exp_value += 1
        int_value = int_value * 10 + int(ch)
        return number_v2_state_4()
    return (False, None)

def number_v2_state_4() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        exp_value += 1
        int_value = int_value * 10 + int(ch)
        return number_v2_state_4()
    elif ch == 'E' or ch == 'e' :
        int_value = int_value * (10**(-exp_value))
        return number_v2_state_6()
    elif ch == END or ch == " ":
        return (True, int_value * (10**(-exp_value)))
    return (False, None)

def number_v2_state_5() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        int_value = 10 * int_value + int(ch)
        return number_v2_state_5()
    elif ch == '.' :
        return number_v2_state_4()
    elif ch == 'E' or ch == 'e' :
        return number_v2_state_6()
    return (False, None)

def number_v2_state_6() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        sign_value = 1
        exp_value = int(ch)
        return number_v2_state_8()
    elif ch == '+' :
        sign_value = 1
        return number_v2_state_7()
    elif ch == '-' :
        sign_value = -1
        return number_v2_state_7()
    return (False, None)

def number_v2_state_7() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        exp_value = int(ch)
        return number_v2_state_8()
    return (False, None)

def number_v2_state_8() :
    global int_value
    global exp_value
    global sign_value
    consume_char()
    ch = peek_char()
    if digit(ch) :
        exp_value = 10* exp_value + int(ch)
        return number_v2_state_8()
    elif ch == END or ch == " ":
        return (True, int_value*(10** (exp_value*sign_value)))
    return (False, None)


def eval_exp_v2():
    ch = peek_char()
    if ch == '+':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 + n2
    elif ch == "-":
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 - n2
    elif ch == "*":
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 * n2
    elif ch == "/":
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 / n2
    else: 
        consume_char()
        return number_v2()[1]


############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    init_char()
    ch = peek_char()
    if ch == "(" or ch == ")" or ch in operator:
        consume_char()
        return True
    return number_v2()[0]




############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0


def FA_Lex_w_token():
    global token_value
    init_char()
    ch = peek_char()
    if ch == "(" or ch == ")":
        consume_char()
        return (True, OPAR)
    elif ch == ")":
        consume_char()
        return (True, FPAR)
    elif ch == "+":
        consume_char()
        return (True, ADD)
    elif ch == "-":
        consume_char()
        return (True, SOUS)
    elif ch == "*":
        consume_char()
        return (True, MUL)
    elif ch == "/":
        consume_char()
        return (True, DIV)
    valide, nombre = number_v2()
    if valide:
        token_value = nombre
        return (True, NUM)
    return (False, None)



# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        #ok = integer_Q2() # changer ici pour tester un autre automate sans valeur
        # ok, val = number() # changer ici pour tester un autre automate avec valeur
        # ok, val = True, eval_exp_v2() # changer ici pour tester eval_exp et eval_exp_v2
        # ok = FA_Lex()
        ok, token = FA_Lex_w_token()
        if ok:
            print("Accepted!")
            # print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
            print(f"Valeur de retour du programme: {ok, token}")
            if token == 0 :
                print(f"Valeur du token {token_value}")
        else:
            print("Rejected!")
            # print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
