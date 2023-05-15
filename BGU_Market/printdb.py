from persistence import *


def printActivities():
    print("Activities")

    for a in repo.activities.find_all():
        print(a)

def printBranches():
    print("Branches")
    
    for b in repo.branches.find_all():
        print(b)

def printEmployees():
    print("Employees")
    for e in repo.employees.find_all():
        print(e)

def printProducts():
    print("Products")
    for p in repo.products.find_all():
        print(p)

def printSuppliers(): 
    print("Suppliers")
    for s in repo.suppliers.find_all():
        print(s)

def printEmployees_report():
    print("Employees report")
    for er in repo.get_employees_report():
        print('{} {} {} {}'.format(er.name, er.salary, er.working_location, er.total_sales_income))


def printActivities_report():
    print("Activities report")
    for ar in repo.get_activities_report():
        print(ar)


def main():
    #TODO: implement
    printActivities()
    printBranches()
    printEmployees()
    printProducts()
    printSuppliers()
    print()
    printEmployees_report()
    print()
    printActivities_report()
    


if __name__ == '__main__':
    main()