from question_bank import questions, worlds
print("Hi! I'm your math tutor!")

name = input("What's your name? ")

print()
print(f"Nice to meet you, {name}!")

print()
age = int(input("How old are you? "))

print()
print("What would you like to do today?")
print("1. Homework Help 📚")
print("2. Practice & Play 🎮")

print()
mode = input("Choose 1 or 2: ")

while mode not in ["1", "2"]:
    print()
    print("Oops! Please choose 1 or 2.")
    mode = input("Choose 1 or 2: ")


# HOMEWORK HELP
if mode == "1":
    print()
    print("📚 Let's work on your homework together!")
    print("Homework Help is coming soon! 🌟")


# PRACTICE & PLAY
elif mode == "2":
    print()
    print("Let's practice and play! 🎮")

    print()
    print("What do you like the most?")
    print("1. Ocean Adventure 🦈")
    print("2. Space Adventure 🚀")
    print("3. Dinosaur World 🦖")
    print("4. Sports Challenge ⚽")
    print("5. Magic & Fantasy 🪄")
    print("6. Cars & Racing 🏎️")

    print()
    choice = input("Choose a number from 1 to 6: ")

    while choice not in ["1", "2", "3", "4", "5", "6"]:
        print()
        print("Oops! Please choose a number from 1 to 6.")
        choice = input("Choose a number from 1 to 6: ")


    # OCEAN AND SPACE ARE READY
    if choice in ["1", "2", "3", "4", "5", "6"]:

        world_name = worlds[choice][0]
        world_emoji = worlds[choice][1]

        print()
        print(f"{world_emoji} Your {world_name} begins, {name}!")
        print("Complete the challenges and collect stars! ⭐")


        # CHOOSE STARTING LEVEL FROM AGE
        if age <= 6:
            level = "easy"
        elif age <= 8:
            level = "medium"
        else:
            level = "hard"


        stars = 0


       # PLAY THE 3 CHALLENGES

level_order = ["easy", "medium", "hard"]

level_names = {
    "easy": "Explorer 🌱",
    "medium": "Adventurer 🚀",
    "hard": "Math Master ⭐"
}

for challenge_number in range(3):

    question, correct_answer, hint = questions[choice][level][challenge_number]

    print()
    print(f"🎯 Challenge {challenge_number + 1} of 3")
    print(f"Level: {level_names[level]}")
    print()
    print(question)

    answer = input("Your answer: ")

    # CORRECT ON THE FIRST TRY
    if answer == correct_answer:
        stars = stars + 1

        print()
        print("🌟 Amazing job!")
        print("You earned a star! ⭐")
        print(f"Stars: {stars} ⭐")

        # Level up
        if level != "hard":
            current_level = level_order.index(level)
            level = level_order[current_level + 1]

            print()
            print("🚀 You're doing great!")
            print("Your next challenge is leveling up!")

    # WRONG ON THE FIRST TRY
    else:
        print()
        print("💡 Oops! Not quite.")
        print(hint)

        print()
        answer = input("Want to try again? 🌟 ")

        # CORRECT AFTER THE HINT
        if answer == correct_answer:
            stars = stars + 1

            print()
            print("🎉 You got it!")
            print("Great thinking! You earned a star! ⭐")
            print(f"Stars: {stars} ⭐")

            print()
            print("✨ We'll stay at this level for the next challenge.")

        # WRONG EVEN AFTER THE HINT
        else:
            print()
            print("🌱 Nice try!")
            print(f"The answer was {correct_answer}.")
            print("We'll keep learning together!")

            # Level down
            if level != "easy":
                current_level = level_order.index(level)
                level = level_order[current_level - 1]

                print()
                print("💚 Let's make the next challenge a little easier.")

        # END OF ADVENTURE
        print()
        print(f"🏆 {world_name} Complete!")
        print(f"You collected {stars} out of 3 stars! ⭐")


        # FINAL FEEDBACK
        if stars == 3:
            print("🌟 Perfect adventure! You're a Math Explorer!")

        elif stars == 2:
            print("🎉 Great adventure! You did an awesome job!")

        else:
            print("🌱 Nice work! Every challenge makes your math skills stronger!")
