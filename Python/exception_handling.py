#try-except-else-finally

try:
    x = int(input("Enter number: "))
    result = 10 / x
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
else:
    print("Result:", result)
finally:
    print("Execution completed")


#functions
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Division by zero is not allowed"


#flies
try:
    filename = input("Enter filename: ")
    with open(filename) as f:
        data = int(f.read())
        print(100 / data)
except FileNotFoundError:
    print("File not found")
except ValueError:
    print("File does not contain number")
except ZeroDivisionError:
    print("Division by zero")
except Exception as e:
    print("Unexpected error:", e)
finally:
    print("Program finished")
