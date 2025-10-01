import menuManager

def main():
    while True:
        # Display the main menu and handle user input
        menuManager.PrintMenu()
        choice = menuManager.CatchInput()
        menuManager.InputManager(choice)



if __name__ == "__main__":
    main()