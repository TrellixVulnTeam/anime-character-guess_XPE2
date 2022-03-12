from game import play

if __name__ == '__main__':
    if not play():
        print('Something went wrong, please try again')
    
    print('Thanks for playing the game...')
    input()