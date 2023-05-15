from persistence import *

import sys

def main(args : list):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if poss
        
            
            
            cur_quantity = repo.products.find(splittedline[0]).quantity
            if(int(splittedline[1]) < 0 ): # its a sale
                
                # if(the quantity i have + splittedline[1] >= 0) only then do stuff
                
                splittedline[0] #product
                splittedline[2] #id of the saler\supplier
                splittedline[3] #date
                

                if(cur_quantity + int(splittedline[1]) >= 0):
                    new_quantity =  cur_quantity + int(splittedline[1])
                    repo.products.updateQuantity(splittedline[0], new_quantity)
                    repo.activities.insert(Activitie(splittedline[0],splittedline[1],splittedline[2],splittedline[3]))
                
                
            else: # its a supply arrival!
                new_quantity =  cur_quantity + int(splittedline[1])
                repo.products.updateQuantity(splittedline[0], new_quantity)
                repo.activities.insert(Activitie(splittedline[0],splittedline[1],splittedline[2],splittedline[3]))
                
            
if __name__ == '__main__':
    main(sys.argv)