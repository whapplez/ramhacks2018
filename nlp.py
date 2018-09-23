import nltk, re, pprint
from dateutil import parser
import datetime
from nltk import word_tokenize


def main(org, post_date, raw, file=False):
    if file:
        raw = open(raw, 'r').read().lower()
    else:
        raw = raw.lower()
    tokens = word_tokenize(raw)
    text = nltk.Text(tokens)

    post_date = parser.parse(post_date, dayfirst=False)
    print(post_date)

    freeWords = ['free']
    foodWords = ['food', 'snacks', 'bagels']
    daysOfWeek = ['today', 'tomorrow', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if any(free in text for free in freeWords) \
            and any(food in text for food in foodWords):
        pt = nltk.pos_tag(text)
        ne = nltk.ne_chunk(pt)
        foodIndex = text.index('free')

        # time
        tf = None
        if len(re.findall('\d+[:]\d+', raw)) > 0:
            tf = re.findall('\d+[:]\d+', raw)[0]
        else:
            # print(pt)
            is_jj_cd = lambda pos: pos[:2] == 'JJ' or pos[:2] == 'CD'
            jj = [word for (word, pos) in pt if is_jj_cd(pos)]
            plausible = [a for a in jj if any(b in a for b in ['am', 'pm'])]
            tf = plausible[0]
        # https://stackoverflow.com/questions/33587667/extracting-all-nouns-from-a-text-file-using-nltk
        # print(re.findall('\d+:+\d+', str(ss)))
        print(tf)

        # date
        # day of the week, closest in position to the word "free"
        dayf = None
        dayIndex = None
        if any(day in text for day in daysOfWeek):
            r = 1
            while True:
                ss = text[foodIndex-r:foodIndex+r]
                if any(day in ss for day in daysOfWeek):
                    for day in daysOfWeek:
                        if tokens.__contains__(day):
                            dayf = day
                            dayIndex = ss.index(day) + foodIndex-r
                            break
                    break
                r += 1

        print(dayf)

        dt = None
        # ['1/1/70', '01/20/1970', '2-21-79']
        if len(re.findall('\d+[-/]\d+[-/]\d+', raw)) > 0:
            dateraw = re.findall('\d+[-/]\d+[-/]\d+', raw)[0]
            dt = parser.parse(dateraw+' '+tf, dayfirst=False)

        # ['10/31']
        elif len(re.findall('\d+[-/]\d+', raw)) > 0:
            dateraw = re.findall('\d+[-/]\d+', raw)[0]
            dt = parser.parse(dateraw+' '+tf, dayfirst=False)

        # ['Jan 3', 'February 10']
        elif len(re.findall('[A-Z]\w+\s\d+', raw)) > 0:
            dateraw = re.findall('[A-Z]\w+\s\d+', raw)[0]
            dt = parser.parse(dateraw+' '+tf, dayfirst=False)

        # infer - no date specified
        elif dayf is not None:
            def next_weekday(d, weekday, delta=False):
                if delta:
                    return d + datetime.timedelta(weekday)
                days_ahead = weekday - d.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return d + datetime.timedelta(days_ahead)

            daysOfWeekSet = {'today': 0, 'tomorrow': 1, 'monday' : 0, 'tuesday' : 1,
                             'wednesday' : 2, 'thursday' : 3, 'friday' : 4, 'saturday' : 5, 'sunday' : 6}
            d = parser.parse(tf, dayfirst=False).replace(post_date.year, post_date.month, post_date.day)
            if dayf == 'today' or dayf == 'tomorrow':
                dt = next_weekday(d, daysOfWeekSet[dayf], delta=True)
            else:
                # next_monday = next_weekday(d, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
                dt = next_weekday(d, daysOfWeekSet[dayf])

        print('Date/Time: ', dt)

        # location
        location = None
        length = 0

        grammar = "NP: {<IN|DT|NNP>+?<NN>+}"
        cp = nltk.RegexpParser(grammar)
        # print(cp.parse(pt))
        is_np = lambda pos: pos[:2] == 'NP'
        for each in cp.parse(pt):
            if str(type(each)) == "<class 'nltk.tree.Tree'>":
                typ = each.pos()[0][-1]
                if typ == 'NP' and len(each.leaves()) > length:
                    location = " ".join([tp[0] for tp in each.leaves() if tp[1] == 'NN'])
                    length = len(each.leaves())

        print('Location: ', location)

        # return (org, dt, location)

    else:
        print("No free food!")


if __name__ == "__main__":
    main('who?', 'Sat Sep 15 16:12:25 +0000 2018', 'text2.txt', file=True)
