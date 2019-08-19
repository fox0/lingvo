import re
from pprint import pprint

from django.shortcuts import render

from main.api import LingvoAPI
from main.models import Word
from main.private_settings import LINGVO_API_KEY


def index(request):
    api = LingvoAPI(LINGVO_API_KEY)

    # pprint(api.translation('spend'))

    t = '''\
>Like a rock to a hornets nest, Applejack’s exclamation sets off her friends, who all erupt into their own laments over the resident human.
>”Poor Anny! It must be so sc-!”
>”T-t-this is an atrocity! An outrage!”
>”What?! There’s no possible way that we didn’t notice for so long!”
>”This is messed up! You can’t just-”
>”Girls!” Fluttershy shouts, this time not shrinking away from the sudden attention.
>She takes a deep breath and looks over all her friends. “I know this is a bad situation,” she says, her voice again soft, “but we shouldn’t sit here and panic. Anon needs us, and we need to figure out how to help him.”
>All eyes immediately turn to Twilight for a plan, who smiles and pulls some paper and a quill from her saddlebags.
>”Ok, I think I know just what we should do. First off…” 
'''.lower()

    def rep(m):
        word = m.group(1)
        # noinspection PyUnresolvedReferences
        try:
            # noinspection PyUnresolvedReferences
            w = Word.objects.get(word=word)
        except Word.DoesNotExist:
            d = api.minicard(word)
            translation = d['Translation']['Translation'] if d else None
            w = Word(word=word, translation=translation).save()

        # print(word, translation)
        if w.translation:
            return '{word} <span style="color:#080" data-pk="{pk}">(<b>{tr}</b>)</span>'.format(
                word=word, pk=w.pk, tr=w.translation)
        return word

    result = re.sub(r'([a-z’\']+)', rep, t)
    result = result.replace('\n', '<br>')
    return render(request, 'main/index.html', {
        'text': result,
    })
