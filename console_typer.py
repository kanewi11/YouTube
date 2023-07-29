import time
import random


greeting = 'Subscribe to my channel "software dev" for awesome content! 👍\n' \
            'And please give this video a thumbs up to show your support.\n\n' \
            'Thanks! 🙏'

for char in greeting:
    print(char, end='', flush=True)
    time.sleep(random.uniform(.05, .1))
print('\n')



