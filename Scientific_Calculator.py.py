from math import *
def hazra():
    print("          \n                              ()<>---] SCIENTIFIC CALCULATOR [---<>()")
    print("                                      ___________x___________\n\n")
    print(" :--:   ADDITION(+)    :--:           :--: SUBSTRACTION(-):--:           :--:   asin_acos_atan   :--:")
    print(" :--:MULTIPLICATION(*) :--:           :--:   DEVISION(/)  :--:           :--:   sinh_cosh_tanh   :--:")
    print(" :--:FLOOR DIVISION(//):--:           :--:   MODULUS(%)   :--:           :--:  asinh_acosh_atanh :--:")
    print(" :--:EXPONENTIATION()  :--:           :--:    LOG(log)    :--:           :--:   log10_exp_sqrt   :--:")
    print(" :--:   sin_cos_tan    :--:           :--:FACTORIAL(fact) :--:")         
    print("\n\n/></..........")
    print("        ____________________________________________________________________________________")
    print("        ____________________________________________________________________________________\n")
    palash=['1','2','3','4','5','6','7','8','9','0','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100']
    a = float(input("\n                              []--Enter The First value--('a')  :- "))
    operator = input("\n                              []----Enter your operator----[] \n                              []'+','-','*','/','//','%'...[]   :- ")
    if operator in ['sin','cos','tan','log','log10','exp','fact','sqrt','asin','acos','atan','sinh','cosh','tanh','asinh','acosh','atanh']:
        b=None
        print("\n     + - + - + - + - + - + - + - + - + - + - + - >+< - + - + - + - + - + - + - + - + - + - + - +")
    elif operator in palash:
        b=None
        print("\n     + - + - + - + - + - + - + - + - + - + - + - >+< - + - + - + - + - + - + - + - + - + - + - +")
    else:
        b = float(input("\n                              []--Enter The Second value--('b') :-  "))
        print("\n     + - + - + - + - + - + - + - + - + - + - + - >+< - + - + - + - + - + - + - + - + - + - + - +")
    if operator == "+": 
        print("\n                            [()]--- FINAL ADDITION IS---[()]  :--->",a + b)
    elif operator == "-":
        print("\n                         [()]---FINAL SUBSTRACTION IS--[()]   :--->",a - b)
    elif operator in palash:
        print("\n                                [(+)]---INVALID OPERATOR---[(+)]")
    elif operator == "*":
        print("\n                         [()]---FINAL MULTIPLICATION IS[()]   :--->",a * b)
    elif operator == "/":
        print("\n                            [()]---FINAL DEVISION IS---[()]   :--->",a / b)
    elif operator == "//":
        print("\n                         [()]---FINAL FLOOR DIVISION IS[()]   :--->",a // b)
    elif operator == "%":
        print("\n                            [()]---FINAL MODULUS IS---[()]    :--->",a % b)
    elif operator == "**":
        print("\n                         [()]---AL EXPONENTIATION IS---[()]   :--->",a ** b)
    elif operator =="sqrt":
        print("\n                         [()]---FINAL SQUAR ROOT IS---[()]    :--->",sqrt(a))
    elif operator == "sin":
        print("\n                            [()]---FINAL SIN IS---[()]        :--->",sin(radians(a)))
    elif operator == "cos":
        print("\n                            [()]---FINAL COS IS---[()]        :--->",cos(radians(a)))
    elif operator == "tan":
        print("\n                            [()]---FINAL TAN IS---[()]        :--->",tan(radians(a)))
    elif operator == "log":
        print("\n                        [()]---] THE VALUE OF LOG IS---[()]   :--->",log(a))
    elif operator == "log10":
        print("\n                          [()]---THE VALUE OF LOG10 IS---[()] :--->",log10(a))
    elif operator == "exp":
        print("\n                            [()]--FINAL EXP IS---[()]         :--->",exp(a))
    elif operator == "fact":
        print("\n                         [()]---YOUR FINAL FACTORIAL IS---[()]:--->",factorial(int(a)))
    elif operator == "asin":
        print("\n                          [()]---] THE FINAL ASIN IS---[()]   :--->", degrees(asin(a)))
    elif operator == "acos":
        print("\n                          [()]---] THE FINAL ACOS IS---[()]   :--->", degrees(acos(a)))
    elif operator == "atan":
        print("\n                          [()]---] THE FINAL ATAN IS---[()]   :--->", degrees(atan(a)))
    elif operator == "sinh":
        print("\n                          [()]---] THE FINAL SINH IS---[()]   :--->", sinh(a))
    elif operator == "cosh":
        print("\n                          [()]---] THE FINAL COSH IS---[()]   :--->", cosh(a))
    elif operator == "tanh":
        print("\n                          [()]---] THE FINAL TANH IS---[()]   :--->", tanh(a))
    elif operator == "asinh":
        print("\n                         [()]---] THE FINAL ASINH IS---[()]   :--->", asinh(a))
    elif operator == "acosh":
        print("\n                         [()]---] THE FINAL ACOSH IS---[()]   :--->", acosh(a))
    elif operator == "atanh":
        print("\n                         [()]---] THE FINAL ATANH IS---[()]   :--->", atanh(a))
    else:
         print("\n     + - + - + - + - + - + - + - + - + - + - + - >+< - + - + - + - + - + - + - + - + - + - + - +\n")
         print("        ____________________________________________________________________________________")
         print("        ____________________________________________________________________________________\n")
         print("                                                                                       ........../></  ")
         print("\n                          ---<>---] YOUR TYPING OPERATOR IS WRONG [----<>---    \n\n\n")
         hazra()
         exit()
    print("\n     + - + - + - + - + - + - + - + - + - + - + - >+< - + - + - + - + - + - + - + - + - + - + - +\n")
    print("        ____________________________________________________________________________________")
    print("        ____________________________________________________________________________________\n")
    print("                                                                                      ........../></  ")                   
    print("\n                             ---<>---] THANK YOU FOR COMING [---<>---     \n\n\n")
    hazra()
hazra()