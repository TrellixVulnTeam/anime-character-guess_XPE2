from hashlib import new
import easygui as gui
import os, random, shutil
from api import GET, Character, Anime
from PIL import Image
import questionary
from rich.console import Console
console = Console()

K = 4 # Şık sayısı

def clean():
    console.clear()
    console.rule('WHO AM I | Anime character guess game')

def main():
    clean()
    input_name = questionary.text('Enter name of anime:').ask()
    anime = GET.media_anime(input_name)
    difficulty = questionary.select('Select the difficulty', choices=['Easy', 'Medium', 'Hard', 'Impossible']).ask()
    if difficulty == 'Easy':
        factor = 1
    elif difficulty == 'Medium':
        factor = 2
    elif difficulty == 'Hard':
        factor = 3
    else:
        factor = 5
    character_count = 50 * factor
    characters = GET.charaterlist_from_anime(anime.id, character_count)

    wins = 0
    loses = 0
    
    while True:
        if wins >= character_count * 75/100:
            shutil.rmtree('./temp')
            break
        elif loses >= character_count * 25/100:
            shutil.rmtree('./temp')
            break
        quiz = random.choices(characters, k = K)
        # 0 the winner
        msg = 'Select the name of this character'
        winner = quiz[0]
        characters.remove(winner)
        random.shuffle(quiz)
        try:
            path = f'./temp/{winner.id}.jpg'
            winner.download_picture(path)
        except FileNotFoundError:
            os.mkdir('./temp')
            winner.download_picture(path)
        image = Image.open(path)
        new_path = f'./temp/{winner.id}.png'
        image.save(new_path)
        choices = [x.name for x in quiz]
        reply = gui.buttonbox(msg,image = new_path, choices = choices)

        if reply == winner.name:
            wins += 1
        else:
            loses += 1
        
        clean()
        console.print(f'[i][white]Number of wins: [blue] {wins}\n[white]Number of loses: [red] {loses} ')

    clean()
    console.print(f'[i][white]Number of wins: [blue] {wins}\n[white]Number of loses: [red] {loses} ')
    console.print(f'Winrate {wins / (wins + loses) * 100}% at difficulty {difficulty}')
    






if __name__ == '__main__':
    main()