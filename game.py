from hashlib import new
import easygui as gui
import os, random, tempfile
from api import GET
from PIL import Image
import questionary
from rich.console import Console
console = Console()

K = 4 # Şık sayısı

def clean():
    console.clear()
    console.rule('WHO AM I | Anime character guess game')

def play():
    clean()
    input_name = questionary.text('Enter name of anime:').ask()
    anime = GET.media_anime(input_name)
    console.print(f'Selected anime [b][red]{anime.title_romaji} | {anime.title_english}')
    console.print('Easy         => top[b][green] 50 [default] \n'
                + 'Medium       => top[b][green] 100 [default] \n'
                + 'Hard         => top[b][green] 150 [default] \n'
                + '[red]Impossible [default]  => top[b][green] 250 [default]')
    difficulty = questionary.select('Select the difficulty', choices=['Easy', 'Medium', 'Hard', 'Impossible']).ask()
    if difficulty == 'Easy':
        factor = 1
    elif difficulty == 'Medium':
        factor = 2
    elif difficulty == 'Hard':
        factor = 3
    elif difficulty == 'Impossible':
        factor = 5
    else:
        return False
    character_count = 50 * factor
    characters = GET.charaterlist_from_anime(anime.id, character_count)
    characters_other = GET.charaterlist_from_anime(anime.id, character_count)

    wins = 0
    loses = 0
    
    while True:

        if len(characters) <= 0:
            break
        
        winner = random.choice(characters)
        characters.remove(winner)
        quiz = [winner]
        while winner in quiz:
            quiz = random.sample(characters_other, k = K - 1)
        quiz.append(winner)
        random.shuffle(quiz)

        with tempfile.TemporaryDirectory() as temp_dir:
            with open(f'{temp_dir}/{winner.id}.jpg','wb') as f:
                f.write(winner.picture_data())
            img = Image.open(f'{temp_dir}/{winner.id}.jpg')
            img.save(f'{temp_dir}/{winner.id}.png')
            choices = [x.name for x in quiz]
            reply = gui.buttonbox(image = f'{temp_dir}/{winner.id}.png', choices = choices, cancel_choice=False)
        
        clean()
        if not reply:
            break
        elif reply == winner.name:
            wins += 1
            console.print('TRUE', style='bold green')
        else:
            loses += 1
            console.print('FALSE', style ='bold red')
        
        console.print(f'[i][white]Number of wins: [blue] {wins}\n[white]Number of loses: [red] {loses}\n'
                    + f'[default]Remaining characters [green]{len(characters)}')

    clean()
    console.print(f'[i][white]Number of wins: [blue] {wins}\n[white]Number of loses: [red] {loses} ')
    console.print(f'Winrate { (wins / (wins + loses) * 100) if wins != 0 else 0 }% at difficulty {difficulty}')

    return True


if __name__ == '__main__':
    console.print_exception('You are trying to run wrong app')