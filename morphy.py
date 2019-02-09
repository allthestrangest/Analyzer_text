import pymorphy2

morph = pymorphy2.MorphAnalyzer()
ignorechars = ''',:'"!?;()'''
ignoreparts = ['PREP', 'CONJ', 'PRCL', 'INTJ']
subject = ['NOUN', 'NUMR', 'NPRO']
predicate = ['VERB', 'INFN', 'ADJS', 'PRTS']

def search(word, need_type):
    variants = morph.parse(word)
    for i in range(len(variants)):
        if variants[i].tag.POS in need_type:
            return i
    return None

def part_of_speech(word, pos):
    part = morph.parse(word)[pos].tag.POS
    if part in ignoreparts:
        return 0
    elif part in subject:
        return 1
    elif part in predicate:
        return 2
    return 3

def global_type(word, pos):
    return morph.parse(word)[pos].tag.POS

def case(word, pos):
    x = morph.parse(word)[pos].tag.case
    if morph.parse(word)[pos].tag.case == 'nomn':
        return 1
    return 0

def time(word, pos):
    time_ = morph.parse(word)[pos].tag.tense
    if time_ == 'past':
        return -1
    elif time_ == 'pres':
        return 0
    elif time_ == 'futr':
        return 1
    return None

def face(word, pos):
    face_ = morph.parse(word)[pos].tag.persons
    if face_ == '1per':
        return 1
    elif face_ == '2per':
        return 2
    elif face_ == '3per':
        return 3
    return None

def kind(word, pos): # род
    kind_ = morph.parse(word)[pos].tag.gender
    if kind_ == 'femn':
        return -1
    elif kind_ == 'masc':
        return 1
    elif kind_ == 'neut':
        return 0
    return None

def number(word, pos):
    number_ = morph.parse(word)[pos].tag.number
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
    predicate_flag = False
    for word in text:
        try: # if not subject
            subj_position = search(word, subject)
            now_type = part_of_speech(word, subj_position)
            if now_type == 1:
                try:
                    subj[word][0] += 1
                except:
                    subj[word] = [1, 0]

                if case(word):
                    subj[word][1] = 1
                    now_subj.append(word)
        except:
            pass

        try: # if not predicate
            predic_position = search(word, predicate)
            now_type = part_of_speech(word, predic_position)
            if now_type == 2:
                try:
                    predic[word] += 1
                except:
                    predic[word] = 1
                if global_type(word, predic_position) == 'VERB' or global_type(word, predic_position) == 'INFN':
                    predicate_flag = True
        except:
            pass


    now_predic = list(predic)
    basis = []

    if len(now_predic) == 0:
            return now_subj
    if len(now_subj) == 0:
        return [now_predic, list(subj)]

    if predicate_flag:
        for i in now_subj:
            for j in now_predic:
                posi = search(i, subject)
                posj = search(j, predicate)

                if number(i, posi) != number(j, posj) and global_type(j, posj) != 'INFN':
                    continue
                #if global_type(i) == 'NPRO':
                #    basis.append([i, j])
                elif time(j, posj) == -1 and (kind(i, posi) == kind(j, posj) and global_type(i, posi) != 'NPRO' or global_type(i, posi) == 'NPRO'):
                    basis.append([i, j])
                elif time(j, posj) != -1 and number(i, posi) == number(j, posj):
                    basis.append([i, j])

        return basis

    else:
        pass

docs_ = [
    #"Я тихонечко ворчал в углу",
    "Я делало делал делала уделали ворчал",
    "Лисица прыгнула побежал поскакало улетели делает сделают нарисует",
    "Сходив туда, прыгнул на шкаф",
	#"Британская полиция знает о местонахождении основателя WikiLeaks",
	#"В суде США начинается процесс против россиянина, рассылавшего спам",
	"Церемонию вручения Нобелевской премии мира бойкотируют 19 стран",
	"В Тамбове проходят массовые проверки газового оборудования",
	#"Планшет Lenovo Phab 3 получит экран диагональю 7,8 дюйма",
	#"Шведский суд отказался рассматривать апелляцию основателя Wikileaks",
	#"Вышло четвёртое издание «Книги Памяти»",
	#"Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
	#"В Стокгольме и Осло сегодня состоится вручение Нобелевских премий",
    #"Названы 10 претендентов на титул лучшего в мире автомобиля",
    "Возвращаясь домой, мне стало грустно",
    "Книга была прочитана за считанные часы"
]

docs = open("input.txt", "r").read().replace('\n', ' ').split('.')
del docs[len(docs) - 1]


file_ = open("output.txt", "w")

for i in docs_:
    file_.write(i)
    file_.write('\n')
    file_.write(str(clean(i)))
    file_.write('\n')

file_.close()