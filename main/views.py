import re

from django.shortcuts import render

from main.api import LingvoAPI
from main.models import Word, NormalizedWord
from main.private_settings import LINGVO_API_KEY


def index(request):
    api = LingvoAPI(LINGVO_API_KEY)

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
        word2 = _normalize(api, word)
        w = _translate(api, word2)
        if w.translation:
            return '{word} <span style="color:#080" data-pk="{pk}">(<b>{tr}</b>)</span>'.format(
                word=word, pk=w.pk, tr=w.translation)
        return word

    result = re.sub(r'([a-z’\']+)', rep, t)
    result = result.replace('\n', '<br>')
    return render(request, 'main/index.html', {
        'text': result,
    })


def _normalize(api, word):
    # noinspection PyUnresolvedReferences
    try:
        # noinspection PyUnresolvedReferences
        return NormalizedWord.objects.get(word=word).normalized
    except NormalizedWord.DoesNotExist:
        pass

    r = api.translation(word)
    if r:
        words = set(i['ArticleId'].split('__')[1] for i in r)
        try:
            words.remove(word)
        except KeyError:
            pass

        if len(words) == 0:
            result = word
        elif len(words) == 1:
            result = words.pop()
        else:
            result = words.pop()  # todo
            # raise ValueError(word, words)
    else:
        result = word

    result = result.lower()
    NormalizedWord(word=word, normalized=result).save()
    return result


def _translate(api, word):
    # noinspection PyUnresolvedReferences
    try:
        # noinspection PyUnresolvedReferences
        return Word.objects.get(word=word)
    except Word.DoesNotExist:
        pass

    r = api.minicard(word)
    translation = r['Translation']['Translation'] if r else None
    w = Word(word=word, translation=translation)
    w.save()
    return w
