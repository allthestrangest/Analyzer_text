import pymorphy2

morph = pymorphy2.MorphAnalyzer()
ignorechars = ''',:'"!?;()'''
ignoreparts = ['PREP', 'CONJ', 'PRCL', 'INTJ']
subject = ['NOUN', 'NUMR', 'NPRO']
predicate = ['VERB', 'INFN', 'ADJS']

def global_type(word):
    return morph.parse(word)[0].tag.POS

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
    return None

def face(word):
    face_ = morph.parse(word)[0].tag.persons
    if face_ == '1per':
        return 1
    elif face_ == '2per':
        return 2
    elif face_ == '3per':
        return 3
    return None

def kind(word): # род
    kind_ = morph.parse(word)[0].tag.gender
    if kind_ == 'femn':
        return -1
    elif kind_ == 'masc':
        return 1
    elif kind == 'neut':
        return 0
    return None

def number(word):
    number_ = morph.parse(word)[0].tag.number
    if number_ == 'sing':
        return -1
    elif number_ == 'plur':
        return 1
    return None

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

    if len(now_subj) == 0:
        return [now_predic, list(subj)]
    if len(now_predic) == 0:
        return now_subj

    basis = []

    for i in now_subj:
        for j in now_predic:
            if number(i) != number(j) and morph.parse(j)[0].tag.POS != 'INFN':
                continue
            elif time(j) == -1 and (kind(i) == kind(j) and global_type(i) != 'NPRO' or global_type(i) == 'NPRO'):
                basis.append([i, j])
            elif time(j) != -1 and number(i) == number(j):
                basis.append([i, j])

    return basis


docs = [
    "Я тихонечко ворчал в углу",
    "Я делало делал делала уделали ворчал",
    "Лисица прыгнула побежал поскакало улетели делает сделают нарисует",
    "Сходив туда, прыгнул на шкаф",
	"Британская полиция знает о местонахождении основателя WikiLeaks",
	"В суде США начинается процесс против россиянина, рассылавшего спам",
	"Церемонию вручения Нобелевской премии мира бойкотируют 19 стран",
	"В Тамбове проходят массовые проверки газового оборудования",
	"Планшет Lenovo Phab 3 получит экран диагональю 7,8 дюйма",
	"Шведский суд отказался рассматривать апелляцию основателя Wikileaks",
	"Вышло четвёртое издание «Книги Памяти»",
	"Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
	"В Стокгольме и Осло сегодня состоится вручение Нобелевских премий",
    "Названы 10 претендентов на титул лучшего в мире автомобиля",
    "Возвращаясь домой, мне стало грустно",
    "Книга была прочитана за считанные часы"
]


for i in docs:
    print(i)
    text = clean(i)
    print(text)
    print()