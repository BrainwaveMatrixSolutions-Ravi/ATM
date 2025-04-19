import time
class InvalidLoginException(Exception):
    def __init__(self,msg):
      self.msg=msg
      
class InSufficientFundsException(Exception):
     def __init__(self,msg):
         self.msg=msg
         
class InvalidPinException(Exception):
       def __init__(self,msg):
          self.msg=msg
          
ATMLOGINPIN=int(input("Enter your ATM LOGIN PIN:"))
LOGINPIN=995566

try:
    if ATMLOGINPIN !=LOGINPIN:
       raise InvalidLoginException("Enter invalid Login Pin")
    else:
        print("Enter valid ATM LOGIN PIN\n")
        
        Accbal=100000
        
        while True:
           print("ATM Menu:")
           print("1.Withdraw")
           print("2.Deposit")
           print("3.Check Balance")
           print("4.Exit")
           choice = int(input("Enter your Choice:"))
           
           
           if choice==4:
              print("Exiting ATM> Thank You!")
              break
              
           ATMPIN=int(input("Enter your ATM PIN:"))
           PIN=989898

           try:
               if ATMPIN !=PIN:
                 raise InvalidPinException("Enter invalid ATM PIN")
                 
               if choice==1:
                  Wamt=int(input("Withdraw amount:"))
                  if Wamt>Accbal:
                    raise InSufficientFundsException("InSufficient Funds in Account.")
                  else:
                     Accbal -=Wamt
                     print("Transaction Successful!\n\nBAlance After transaction:",Accbal)
               elif choice==2:
                  Damt=int(input("Enter Deposit amount:"))
                  Accbal +=Damt
                  print("Deposit Successful!\n\nBAlance After Deposit:", Accbal)
                  
               elif choice==3:
                  print("Your Account Balance is:", Accbal)
               else:
                   print("Invalid choive! Please Select a valid Option.")
                
           except InvalidPinException as msg:
                 print(msg)
                 print("Please enter a valid ATM PIN!")
                         
           except InSufficientFundsException as msg:
               print(msg)
               print("Transaction Not Possible!")
               
except InvalidLoginException as msg:
    print(msg)
    print("Please enter a valid ATM LOGIN PIN!")


