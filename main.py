from src.UiClass import tictactoe
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #it first calls the player factory (IPlayerFacotory) to get an instance of IPlayer for the current user
    #it calls the UI Factory to generate a UI for the game
    #Then it will run the UI
    # it should run the application factory (IGFactory) based on the parameters coming form user
    #The application factory will return an object of IGameApp class
    #finaly set(IGameApp) the application factory to the gui.

    window = tictactoe()
    window.geometry("650x650")
    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
