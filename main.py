from Application.GAppFactory import GameAppBuilder
from src.UiClass import tictactoe

if __name__ == '__main__':

    #it generates a UI for the game
    #Then it will run the UI

    app_builder : GameAppBuilder = GameAppBuilder()

    window = tictactoe(app_builder)
    #window.setGameApp(game_app)


    window.geometry("650x650")
    window.mainloop()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
