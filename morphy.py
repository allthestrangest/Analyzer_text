import pymorphy2

morph = pymorphy2.MorphAnalyzer()
ignorechars = ''',:'"!?;()'''
ignoreparts = ['PREP', 'CONJ', 'PRCL', 'INTJ']
subject = ['NOUN', 'NUMR', 'NPRO']
predicate = ['VERB', 'INFN', 'ADJS']

def part_of_speech(word):
    part = morph.parse(word)[0].tag.POS
    if part in ignoreparts:
        return 0
    elif part in subject:
        return 1
    elif part in predicate:
        return 2
    return 3

def case(word):
    x = morph.parse(word)[0].tag.case
    if morph.parse(word)[0].tag.case == 'nomn':
        return 1
    return 0

def time(word):
    time_ = morph.parse(word)[0].tag.tense
    if time_ == 'past':
        return -1
    elif time_ == 'pres':
        return 0
    elif time_ == 'futr':
        return 1
    return -2

def face(word):
    face_ = morph.parse(word)[0].tag.persons
    if face_ == '1per':
        return 1
    elif face_ == '2per':
        return 2
    elif face_ == '3per':
        return 3
    return 101010101001

def kind(word): # род
    kind_ = morph.parse(word)[0].tag.gender
    if kind_ == 'femn':
        return -1
    elif kind_ == 'masc':
        return 1
    return 0

def number(word):
    number_ = morph.parse(word)[0].tag.NUMBERS
    if number_ == 'sing':
        return -1
    return 1

#def is_normal(first, second):
    # first - род существительного, second - лицо глагола
#    if second == 3 and first ==

def clean(text):
    text = text.lower()

    for chars in ignorechars:
        text = text.replace(chars, '')

    text = text.split()
    words = {}
    subj = {}
    predic = {}

    now_subj = []
    now_predic = []
    for word in text:
        now_type = part_of_speech(word)
        if now_type == 1:
            try:
                subj[word][0] += 1
            except:
                subj[word] = [1, 0]

            if case(word):
                subj[word][1] = 1
                now_subj.append(word)

        elif now_type == 2:
            try:
                predic[word] += 1
            except:
                predic[word] = 1



    now_predic = list(predic)

    basis = []

    for i in now_subj:
        for j in now_predic:
            if number(i) != number(j) and morph.parse(j)[0].tag.POS != 'INFN':
                continue
            if time(j) == -1 and kind(i) == kind(j):
                basis.append([i, j])
            elif time(j) != -1:
                basis.append([i, j])

    return basis


docs = [
	"Британская полиция знает о местонахождении основателя WikiLeaks",
	"В суде США начинается процесс против россиянина, рассылавшего спам",
	"Церемонию вручения Нобелевской премии мира бойкотируют 19 стран",
	"В Тамбове проходят массовые проверки газового оборудования",
	"Украина игнорирует церемонию вручения Нобелевской премии",
	"Шведский суд отказался рассматривать апелляцию основателя Wikileaks",
	"Вышло четвёртое издание «Книги Памяти»",
	"Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
	"В Стокгольме и Осло сегодня состоится вручение Нобелевских премий"
]


for i in docs:
    print(i)
    text = clean(i)
    print(text)
    print()