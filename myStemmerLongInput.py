import re
import nltk
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import brown

print('Enter any number to stop the program or a word to stem it!')

def cons(s,i):
    if re.match('[aeiou]',s[i]):
        return 0
    if re.match('y',s[i]):
        if i==0 or i==-(len(s)):
            return 1
        else:
            return (not cons(s,i-1))
    return 1

#This function return the measure of word or word part, (C)(VC)^m(C)
def m(s):
    m = 0
    for i in range(0, len(s) - 1):
        if (not cons(s, i)) and cons(s, i + 1):
            m += 1
    return m

stemmer=PorterStemmer()
count=0
correct=0
correct2=0
stemmer2=SnowballStemmer('english')


for s in brown.words():
    # print(s)
    ts=s;
    if len(s)>3:
        if not re.match('[a-z]*$',s):
            continue
        s=s.lower()
        x=stemmer.stem(s)
        y=stemmer2.stem(s)
        # step 1a
        if re.match('[a-z]*sses$',s):
            s=s[:len(s)-4]+'ss'
        elif re.match('[a-z]*ies$',s):
            s=s[:len(s)-3]+'i'
        elif re.match('[a-z]*s$',s):
            s=s[:len(s)-1]

        #step 1b
        if re.match('[a-z]*eed$',s):
            if m(s[:len(s)-3])>0:
                s=s[:len(s)-3]+'ee'
            else:
                s=s
        if re.match('[a-z]*[aeiou][a-z]*ed$',s):
            s=s[:len(s)-2]
            #cleanup
            if re.match('[a-z]*at$',s):
                s=s+'e'
            elif re.match('[a-z]*bl$',s):
                s+='e'
        if re.match('[a-z]*[aeiou][a-z]*ing$',s):
            s=s[:len(s)-3]
            #cleanup
            if re.match('[a-z]*at$',s):
                s=s+'e'
            elif re.match('[a-z]*bl$', s):
                s += 'e'

        #cleanup
        if cons(s,-1) and cons(s,-2) and s[-1]==s[-2] and (s[-1]!='l' and s[-1]!='s' and s[-1]!='z'):
            s=s[:len(s)-1]
        elif len(s)>=3 and m(s)==1 and cons(s,-1) and not cons(s,-2) and cons(s,-3):
            s+='e'

        #1c Y elimination
        if re.match('[a-z]*[aeiou][a-z]*y$',s):
            s=s[:len(s)-1]+'i'
        #derivational morphology
        elif m(s)>0 and re.match('[a-z]*tional$',s):
            s=s[:len(s)-6]+'te'
        elif m(s)>0 and re.match('[a-z]*ization$',s):
            s=s[:len(s)-7]+'ize'
        elif m(s)>0 and re.match('[a-z]*biliti$',s):
            s=s[:len(s)-6]+'ble'
        elif m(s)>0 and re.match('[a-z]*icate$',s):
            s=s[:len(s)-5]+'ic'
        elif m(s)>0 and re.match('[a-z]*ful$',s):
            s=s[:len(s)-3]
        elif m(s)>0 and re.match('[a-z]*ness$',s):
            s=s[:len(s)-4]
        elif m(s[:len(s)-3])>0 and re.match('[a-z]*tion$',s):
            s=s[:len(s)-3]
        elif m(s[:len(s)-5])>0 and re.match('[a-z]*ation$',s):
            s=s[:len(s)-5]
        elif m(s[:len(s)-4])>0 and re.match('[a-z]*[ae]nce$',s):
            s=s[:len(s)-4]
        elif m(s[:len(s)-4])>0 and re.match('[a-z]*ment$',s):
            s=s[:len(s)-4]
        elif m(s[:len(s)-3])>1 and re.match('[a-z]*ive$',s):
            s=s[:len(s)-3]
        elif m(s[:len(s)-2])>1 and re.match('[a-z]*ly$',s):
            s=s[:len(s)-2]
        elif m(s[:len(s)-4])>1 and re.match('[a-z]*izer*',s):
            s=s[:len(s)-4]

        if m(s[:len(s)-1])>1 and re.match('[a-z]*e$',s):
            s=s[:len(s)-1]
    else:
        s=s
        x=stemmer.stem(s)
        y=stemmer2.stem(s)
    print(s,x,y)
    if s==x:
        correct+=1
    if s==y:
        correct2+=1

    count+=1

print()
print("FINAL ACCURACY according to PorterStemmer: ",correct/count)
print("FINAL ACCURACY according to SnowballStemmer: ",correct2/count)
