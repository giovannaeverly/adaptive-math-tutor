"""UI-independent adaptive exercise engine."""
from dataclasses import dataclass
import random

LEVELS = ('easy', 'medium', 'hard')
LEVEL_NAMES = {'easy': 'Explorer', 'medium': 'Adventurer', 'hard': 'Math Master'}
WORLDS = {
 '1': ('Ocean', '🌊', 'shells'), '2': ('Space', '🚀', 'stars'),
 '3': ('Dinosaurs', '🦖', 'eggs'), '4': ('Sports', '⚽', 'balls'),
 '5': ('Magic', '🪄', 'crystals'), '6': ('Racing', '🏎️', 'cars')
}

@dataclass(frozen=True)
class Exercise:
    question: str
    answer: int
    hint: str
    skill: str
    expression: str


def starting_level(age: int) -> str:
    return 'easy' if age <= 6 else 'medium' if age <= 8 else 'hard'


def change_level(level: str, direction: int) -> str:
    index = LEVELS.index(level)
    return LEVELS[max(0, min(len(LEVELS)-1, index+direction))]


def generate_exercise(world: str, level: str, rng=None) -> Exercise:
    if world not in WORLDS or level not in LEVELS:
        raise ValueError('Invalid world or difficulty')
    rng = rng or random
    item = WORLDS[world][2]
    skills = {'easy': ['add', 'sub'], 'medium': ['add', 'sub', 'mul'], 'hard': ['add', 'sub', 'mul', 'div']}[level]
    skill = rng.choice(skills)
    if skill == 'add':
        a, b = (rng.randint(1, 9), rng.randint(1, 9)) if level == 'easy' else (rng.randint(8, 35), rng.randint(3, 29))
        answer, expr = a+b, f'{a} + {b}'
        question = f'You have {a} {item} and find {b} more. How many {item} do you have now?'
        hint = f'Add {a} and {b}. Count up from {a}.'
        label = 'Addition'
    elif skill == 'sub':
        a = rng.randint(5, 18) if level == 'easy' else rng.randint(20, 70)
        b = rng.randint(1, min(a, 9 if level == 'easy' else 35))
        answer, expr = a-b, f'{a} − {b}'
        question = f'You had {a} {item} and gave away {b}. How many are left?'
        hint = f'Start with {a} and take away {b}.'
        label = 'Subtraction'
    elif skill == 'mul':
        a = rng.randint(2, 5) if level == 'medium' else rng.randint(3, 10)
        b = rng.randint(2, 6) if level == 'medium' else rng.randint(3, 10)
        answer, expr = a*b, f'{a} × {b}'
        question = f'There are {a} groups of {b} {item}. How many are there in total?'
        hint = f'Add {b}, {a} times.'
        label = 'Multiplication'
    else:
        answer = rng.randint(2, 10)
        b = rng.randint(2, 9)
        a, expr = answer*b, f'{answer*b} ÷ {b}'
        question = f'You split {a} {item} equally into {b} groups. How many are in each group?'
        hint = f'What number multiplied by {b} gives {a}?'
        label = 'Division'
    return Exercise(question, answer, hint, label, expr)


def parse_answer(value: str) -> int | None:
    value = value.strip()
    if not value or len(value) > 12:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def next_level(level: str, correct_first: bool, correct_second: bool) -> str:
    if correct_first:
        return change_level(level, 1)
    if correct_second:
        return level
    return change_level(level, -1)
