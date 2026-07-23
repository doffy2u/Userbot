import re
import asyncio

from services.anagram import get_candidates
from services.scramble import lookup, learn


SCRAMBLE_REGEX = r'''🌟 Scrambled Word Challenge! 🌟

🔤 Word:\s*([A-Za-z]+)'''

MY_NAME = "Zia♡⁠˖⁠꒰⁠ᵕ⁠༚⁠ᵕ"

current_scramble = None
current_candidates = []
candidate_index = 0
waiting = False


async def handle_scramble(event):
    global current_scramble
    global current_candidates
    global candidate_index
    global waiting

    text = event.raw_text.strip()

    # -------------------------
    # Detect new scramble
    # -------------------------
    match = re.search(SCRAMBLE_REGEX, text)

    if match:
        scrambled = match.group(1).upper()

        print("Scramble:", scrambled)

        # Check learned database first
        answer = lookup(scrambled)

        if answer:
            print("Cache hit:", answer)
            await event.reply(answer)
            return

        current_scramble = scrambled

        current_candidates = get_candidates(scrambled)

        candidate_index = 0

        if not current_candidates:
            print("No dictionary matches")
            return

        print("Candidates:", current_candidates)

        waiting = True

        await event.reply(
            current_candidates[candidate_index]
        )

        asyncio.create_task(
            try_next_candidate(event)
        )

        return


    # -------------------------
    # Detect winner
    # -------------------------
    if "🏆" in text and "solved it" in text.lower():

        print("Winner detected:", text)

        waiting = False

        if MY_NAME in text.lower():

            if current_scramble and current_candidates:

                solved = current_candidates[candidate_index]

                learn(
                    current_scramble,
                    solved
                )

                print(
                    f"Learned {current_scramble} -> {solved}"
                )

        else:
            print("Someone else won")

        reset_game()


def reset_game():
    global current_scramble
    global current_candidates
    global candidate_index
    global waiting

    current_scramble = None
    current_candidates = []
    candidate_index = 0
    waiting = False


async def try_next_candidate(event):

    global candidate_index
    global waiting

    while waiting:

        await asyncio.sleep(3)

        if not waiting:
            return

        candidate_index += 1

        if candidate_index >= len(current_candidates):

            print("No more guesses")
            waiting = False
            return


        guess = current_candidates[candidate_index]

        print("Trying:", guess)

        await event.reply(guess)
