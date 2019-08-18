import re
from pprint import pprint

from django.db import IntegrityError
from django.shortcuts import render

from main.api import LingvoAPI
from main.models import Word
from main.private_settings import LINGVO_API_KEY


def index(request):
    api = LingvoAPI(LINGVO_API_KEY)

    # pprint(api.translation('spend'))
    # pprint(api.minicard('ran'))  # ['Translation']['Translation'])

    t = '''


>”Girls, we need to do something,” Fluttershy unexpectedly announces. “It’s about Anon.”
>The other five elements look up from the scrumptious picnic lunch laid out before them to their meek friend, making her shrink under the scrutiny.
>”What’s up with the big guy?” Rainbow asks the groups unspoken question with a raised eyebrow. “He doesn’t seem like the kind of guy to need a lot of help, really.”
>”W-well…” Fluttershy pauses to gather some courage, “haven’t you five noticed something about him? Well, um, it’s not really him, but rather his living conditions.”
>”Dear, Anon is quite the clean and organized individual. I don’t see how there could be something out of sorts with how he lives,” Rarity chimes in.
>”It’s not that, “ the yellow pegasus tries to explain, “you all know that he lives alone, right?”
>The five mares look to one another, slowly starting to piece together what they were being told.
>They all nod together.
>”And how it’s always been like that, for the last few months he’s lived here?”
>A slow, creeping sort of dread begins to form on the faces of Fluttershy’s friends.
>”As in, um…” Fluttershy swallows past the lump in her throat as her voice goes so quiet that the others almost don’t hear what she says.
>”... Throughout the night, too?”
>A suffocating silence overtakes the happy picnic, as horror runs through all the mares.
>”Y-you mean…” Applejack shakily starts, “Tha… tha poor guy has been sleepin’... ALONE... fur months!?!” The farmer almost yells.


'''.lower()
    words = re.findall(r'[a-z’\']+', t, flags=re.IGNORECASE)
    for word in words:
        try:
            Word.objects.get(word=word)
        except Word.DoesNotExist:
            d = api.minicard(word)
            if d:
                print('{} ({})'.format(word, d['Translation']['Translation']))
                Word(word=word, translation=d['Translation']['Translation']).save()
            else:
                print(word)
                Word(word=word).save()
    return ''
