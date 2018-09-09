from os import system, name
import requests
import getpass

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

token = ""

def user_menu():
    f = open("user", "r")
    token = f.readline()
    f.close()
    while(True):
        print("\n1. Create a new todo")
        print("2. View all todos")
        print("3. Delete a todo")
        print("4. Logout")
        print("5. Exit")
        ch = input("\n[?]: ")
        if ch == "5":
            return
        elif ch == "4":
            requests.post("https://sdabhi23.pythonanywhere.com/logout", json={"token": token})
            print("\nLogged out successfully...!")
            f = open("user", "w+")
            f.truncate()
            f.close()
            break
        elif ch == "3":
            print("\nProvide the \"id\" of the todo to be deleted at the next prompt.")
            print("Hint: the ids can be viewed using option 2")
            todo_id = input("\n[?]: ")
            r = requests.post("https://sdabhi23.pythonanywhere.com/delete_todo", json={"token": token, "todo_id": todo_id})
            response = r.json()
            try:
                if response["202"] == "Success":
                    print("\nThe following todo hass been deleted successfully:")
                    print("\n\t| id:", response["deleted"]["id"])
                    print("\t| title:", response["deleted"]["title"])
                    print("\t| message:", response["deleted"]["message"])
            except:
                print(list(response.values())[0])
        elif ch == "2":
            r = requests.post("https://sdabhi23.pythonanywhere.com/view_todos", json={"token": token})
            response = r.json()
            print()
            for todo in response["todos"]:
                print("-----")
                print("id:", todo["id"])
                print("title:", todo["title"])
                print("message:", todo["message"])
            print("-----")
        elif ch == "1":
            title = input("\nTitle: ")
            message = input("Message: ")
            r = requests.post("https://sdabhi23.pythonanywhere.com/new_todo", json={"token": token, "title": title, "message": message})
            response = r.json()
            try:
                if response["202"] == "Success":
                    print("\nTodo added successfully...!")
                else:
                    print(list(response.values())[0])
            except:
                print(list(response.values())[0])
        else:
            print("\nSorry I cannot understand your request...!")

def cred():
    clear()
    print("\n=== Welcome to PyTodo ===")
    with open("user", "r+") as f:
        token = f.readline()
        if(token == ""):
            while(True):
                print("\n1. Signup")
                print("2. Login")
                print("3. Exit")
                ch = input("\n[?]: ")
                if ch == "3":
                    return
                elif ch == "2":
                    uname = input("\nUsername: ")
                    paswd = getpass.getpass()
                    r = requests.post("https://sdabhi23.pythonanywhere.com/login", json={"name": uname, "password": paswd})
                    response = r.json()
                    try:
                        if response["202"] == "Success":
                            print("\n==", "Welcome", uname, "==")
                            token = response["token"]
                            f.write(response["token"])
                            f.close()
                            break
                    except:
                        print("\n"+list(response.values())[0])
                elif ch == "1":
                    uname = input("\nUsername: ")
                    paswd = getpass.getpass()
                    r = requests.post("https://sdabhi23.pythonanywhere.com/signup", json={"name": uname, "password": paswd})
                    response = r.json()
                    try:
                        if response["202"] == "Success":
                            print("\nAccount created successfully!")
                            print("Now you can login using your username and password...")
                    except:
                        print("\n"+list(response.values())[0])
                else:
                    print("\nSorry I cannot understand your resquest...!")
        else:
            r = requests.post("https://sdabhi23.pythonanywhere.com/user", json={"token": token})
            response = r.json()
            print("\n==", "Welcome", response["name"], "==")
    user_menu()

if __name__ == "__main__":
    cred()