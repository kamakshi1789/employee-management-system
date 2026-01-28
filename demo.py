import os
import msvcrt

# ======================= LOGIN SYSTEM =======================

def loginMenu():
    os.system('cls')
    print("===== LOGIN MENU =====")
    print("1. Admin Login")
    print("2. Employee Login")
    print("3. Exit")

    ch = msvcrt.getch().decode()

    if ch == '1':
        adminLogin()
    elif ch == '2':
        employeeLogin()
    elif ch == '3':
        exit()
    else:
        loginMenu()

def adminLogin():
    os.system('cls')
    u = input("Admin Username: ")
    p = input("Admin Password: ")
    if u == "admin" and p == "admin123":
        adminMenu()
    else:
        print("Invalid Login")
        msvcrt.getch()
        loginMenu()

def employeeLogin():
    os.system('cls')
    empid = input("Enter Employee ID: ")
    employeeMenu(empid)

# ======================= EMPLOYEE MENU =======================

def employeeMenu(empid):
    os.system('cls')
    print("===== EMPLOYEE PANEL =====")
    print("1. My Dashboard")
    print("2. View My Profile")
    print("3. View Salary History")
    print("4. Logout")

    ch = msvcrt.getch().decode()

    if ch == '1':
        employeeDashboard(empid)
    elif ch == '2':
        viewMyDetails(empid)
    elif ch == '3':
        viewMySalary(empid)
    elif ch == '4':
        loginMenu()

    msvcrt.getch()
    employeeMenu(empid)


def viewMyDetails(empid):
    os.system('cls')

    if not os.path.exists("employee.xls"):
        print("No Records Found")
        return

    found = False
    with open("employee.xls", "r") as fp:
        for line in fp:
            data = line.strip().split("\t")
            if data[0] == empid:
                found = True
                print("===== EMPLOYEE PROFILE =====\n")
                print("{:<15}: {}".format("Employee ID", data[0]))
                print("{:<15}: {}".format("Name", data[1]))
                print("{:<15}: {}".format("Department", data[2]))
                print("{:<15}: {}".format("City", data[3]))
                print("{:<15}: {}".format("Salary", data[4]))
                break

    if not found:
        print("Employee Record Not Found")

def viewMySalary(empid):
    os.system('cls')

    if not os.path.exists("salary.xls"):
        print("No Salary Records Found")
        return

    print("===== SALARY HISTORY =====\n")
    print("{:<10} {:>10}".format("Emp ID", "Salary"))
    print("-" * 25)

    total = 0
    found = False

    with open("salary.xls", "r") as fp:
        for line in fp:
            data = line.strip().split("\t")
            if data[0] == empid:
                found = True
                print("{:<10} {:>10}".format(data[0], data[1]))
                total += int(data[1])

    if found:
        print("-" * 25)
        print("{:<10} {:>10}".format("Total", total))
    else:
        print("No Salary Data Found")


def employeeDashboard(empid):
    os.system('cls')

    if not os.path.exists("employee.xls"):
        print("No Employee Data Found")
        return

    name = dept = city = salary = ""
    found = False

    # Fetch employee details
    with open("employee.xls", "r") as fp:
        for line in fp:
            data = line.strip().split("\t")
            if data[0] == empid:
                name = data[1]
                dept = data[2]
                city = data[3]
                salary = data[4]
                found = True
                break

    if not found:
        print("Employee Record Not Found")
        return

    # Calculate total salary paid
    total_paid = 0
    if os.path.exists("salary.xls"):
        with open("salary.xls", "r") as sp:
            for line in sp:
                sdata = line.strip().split("\t")
                if sdata[0] == empid:
                    total_paid += int(sdata[1])

    # Dashboard display
    print("=" * 40)
    print(f" Welcome, {name}")
    print("=" * 40)
    print(f"Employee ID : {empid}")
    print(f"Department  : {dept}")
    print(f"City        : {city}")
    print(f"Salary      : {salary}")
    print(f"Total Paid  : {total_paid}")



# ======================= ADMIN FUNCTIONS =======================

def autoID():
    if not os.path.exists("employee.xls"):
        return 1001

    with open("employee.xls", "r") as fp:
        ids = []
        for line in fp:
            parts = line.strip().split("\t")
            if parts[0].isdigit():
                ids.append(int(parts[0]))

    if not ids:
        return 1001

    return max(ids) + 1

def AddEmployee():
    os.system('cls')
    eid = autoID()
    print("Employee ID:", eid)
    ename = input("Name: ")
    edept = input("Department: ")
    ecity = input("City: ")
    esal = input("Salary: ")

    with open("employee.xls", "a+") as fp:
        fp.write(f"{eid}\t{ename}\t{edept}\t{ecity}\t{esal}\n")

    print("Employee Added Successfully")

def showEmployee():
    os.system('cls')

    if not os.path.exists("employee.xls"):
        print("No Records Found")
        return

    with open("employee.xls", "r") as fp:
        records = []
        for line in fp:
            parts = line.strip().split("\t")
            if len(parts) == 5 and parts[0].isdigit():
                records.append(parts)

    if not records:
        print("No Records Found")
        return

    # sort by Employee ID
    records.sort(key=lambda x: int(x[0]))

    # table header
    print("{:<6} {:<18} {:<14} {:<14} {:>8}".format(
        "ID", "Name", "Department", "City", "Salary"))
    print("-" * 65)

    # table rows
    for r in records:
        print("{:<6} {:<18} {:<14} {:<14} {:>8}".format(
            r[0], r[1], r[2], r[3], r[4]))


def searchEmployee():
    os.system('cls')
    empid = input("Enter Employee ID: ")
    found = False
    with open("employee.xls", "r") as fp:
        for i in fp:
            if i.split("\t")[0] == empid:
                print(i)
                found = True
                break
    if not found:
        print("Record Not Found")

def modifyEmployee():
    os.system('cls')
    empid = input("Employee ID to Modify: ")
    found = False

    with open("employee.xls", "r") as fp, open("temp.xls", "w") as tp:
        for i in fp:
            data = i.strip().split("\t")
            if data[0] == empid:
                found = True
                data[1] = input("New Name: ")
                data[2] = input("New Department: ")
                data[3] = input("New City: ")
                data[4] = input("New Salary: ")
                tp.write("\t".join(data) + "\n")
            else:
                tp.write(i)

    if found:
        os.replace("temp.xls", "employee.xls")
        print("Record Modified Successfully")
    else:
        os.remove("temp.xls")
        print("Record Not Found")

def deleteEmployee():
    os.system('cls')
    empid = input("Employee ID to Delete: ")
    found = False

    with open("employee.xls", "r") as fp, open("temp.xls", "w") as tp:
        for i in fp:
            if i.split("\t")[0] == empid:
                found = True
            else:
                tp.write(i)

    if found:
        os.replace("temp.xls", "employee.xls")
        print("Record Deleted Successfully")
    else:
        os.remove("temp.xls")
        print("Record Not Found")

def addSalary():
    os.system('cls')
    empid = input("Employee ID: ")
    sal = input("Salary: ")
    with open("salary.xls", "a+") as fp:
        fp.write(f"{empid}\t{sal}\n")
    print("Salary Added Successfully")

def totalEmployees():
    os.system('cls')
    if not os.path.exists("employee.xls"):
        print("Total Employees: 0")
        return
    with open("employee.xls", "r") as fp:
        print("Total Employees:", len(fp.readlines()))

def backupEmployee():
    os.system('cls')
    if not os.path.exists("employee.xls"):
        print("No Data Available for Backup")
        return
    with open("employee.xls", "r") as fp, open("employee_backup.xls", "w") as bp:
        bp.write(fp.read())
    print("Backup Created Successfully")

# ======================= ADMIN MENU =======================

def adminMenu():
    os.system('cls')
    print("===== ADMIN MENU =====")
    print("1. Add Employee")
    print("2. Show Employee")
    print("3. Search Employee")
    print("4. Modify Employee")
    print("5. Delete Employee")
    print("6. Add Salary")
    print("7. Total Employees")
    print("8. Backup Data")
    print("9. Logout")

    ch = msvcrt.getch().decode()

    if ch == '1':
        AddEmployee()
    elif ch == '2':
        showEmployee()
    elif ch == '3':
        searchEmployee()
    elif ch == '4':
        modifyEmployee()
    elif ch == '5':
        deleteEmployee()
    elif ch == '6':
        addSalary()
    elif ch == '7':
        totalEmployees()
    elif ch == '8':
        backupEmployee()
    elif ch == '9':
        loginMenu()

    msvcrt.getch()
    adminMenu()

# ======================= PROGRAM START =======================

loginMenu()
