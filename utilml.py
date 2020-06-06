import re
#Vopwalwabbit
import pdfplumber
from glob import glob
from os import path

import textract
from nltk import tokenize
#import nltk
#nltk.download('punkt')
from unicodedata import normalize

uniquek = '247a47f3e28a4e189af5d95f6bda2dec'


def to_vw_format(document, label=None):
    return str(label or '') + ' |text ' + ' '.join(re.findall('\w{3,}', document.lower())) + '\n'


def to_list_format(document, label=None):
    return str(label or '') + ' '.join(re.findall('\w{3,}', document.lower())) 


def find_ext(dr, ext):
    '''
    dr - delimiter
    ext - extention
    return list of filenames for pattern
    '''
    #print(path.join(dr,"*.{}".format(ext)))
    return glob(path.join(dr,"*.{}".format(ext)))


#открыть все docs
def takedocx(unique):
    '''
    unique - dir id
    return arr of texts in string
    '''
    docxarr=[]
    for i in find_ext(r"files\{}\.".format(unique),"docx"):
        docx = textract.process(i)
        text = docx.decode('utf-8')
        docxarr.append(text)

    return docxarr



def takepdf(unique):
    '''
    unique - dir id
    return arr of texts in string
    '''
    pdfarr=[]
    for i in find_ext(r"files\{}\.".format(unique),"pdf"):
        #pdf = pdfplumber.open(i)
        with pdfplumber.open(i) as pdf:
        #здесь пока берем только одну страниу
            for page in pdf.pages[1:6]:
                #page = pdf.pages[0]
                text = page.extract_text()
                pdfarr.append(text)

        pdf.close()

    return pdfarr
    

def generateVWfromdir(unique):
    '''
    writes VW file to same directory   
    '''
    dirarr=[]
    #соберем все необходимые нам файлы в строки
    #pdf
    dirarr = dirarr+takepdf(unique)
    #docx
    dirarr = dirarr+takedocx(unique)
    # запишем в файл в формате VW
    with open('currentvw.txt', 'w') as vw_data:
       for text in dirarr:
            vw_data.write(to_vw_format(text))

    

def generatelistfromdir(unique):
    '''
    returnes list of cleaned texts
    '''
    dirarr=[]
    finalarr=[]
    #соберем все необходимые нам файлы в строки
    #pdf
    dirarr = dirarr+takepdf(unique)
    #docx
    dirarr = dirarr+takedocx(unique)
    for text in dirarr:
        finalarr.append(to_list_format(text))
        
    return finalarr



def stoper(sent):
    '''
    tells if stop words occured
    '''
    #стоп строки
    boolchik = True 
    matches = ["Правительства"]
    if any(x in sent for x in matches):
        boolchik = False

    return boolchik
        

def countsententfilter(sent):
    '''
    filter for length of sentences
    '''
    # эвристика длина
    res = len(re.findall(r'\w+', sent))
    boolchik =False
    if(res> 7 and res< 50):
        boolchik =True
    else:
        boolchik =False

    #эвристика особые стоп слова 
    if(stoper(sent) == True):
        boolchik =True
    else:
        boolchik =False   
    #print(res,boolchik)

    return boolchik


def listofcleanfromdir(unique):
    '''
    returnes list of senteces
    '''
    #сюда тексты
    dirarr=[]

    #сюда сгрузим строки для предобработки
    temparr=[]    

 
    #соберем все необходимые нам файлы
    #pdf
    dirarr = dirarr+takepdf(unique)
    #docx
    dirarr = dirarr+takedocx(unique)
    for text in dirarr:
        for sentence in tokenize.sent_tokenize(text):
            if(countsententfilter(sentence)==True):
                temparr.append(to_list_format(sentence))



    
    return temparr
            

def listofsentences(unique):
    '''
    returnes list of senteces
    '''
    #сюда тексты
    dirarr=[]

    #сюда сгрузим строки для предобработки
    temparr=[]    

 
    #соберем все необходимые нам файлы
    #pdf
    dirarr = dirarr+takepdf(unique)
    #docx
    dirarr = dirarr+takedocx(unique)
    for text in dirarr:
        for sentence in tokenize.sent_tokenize(text):
            if(countsententfilter(sentence)==True):
            #temparr.append(normalize('NFKD', punctpad(sentence).lower()).replace("\n", ""))
                temparr.append(normalize('NFKD', sentence).replace("\n", ""))

    #print(temparr)
    return temparr
    


def punctpad(s):
    '''
    s - string
    add padding after and before punctuation
    '''
    s = re.sub('([.,!?()])', r' \1 ', s)
    s = re.sub('\s{2,}', ' ', s)

    return s
    
def DistJaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return float(len(str1 & str2)) / len(str1 | str2)


def striprtf(text):
   pattern = re.compile(r"\\([a-z]{1,32})(-?\d{1,10})?[ ]?|\\'([0-9a-f]{2})|\\([^a-z])|([{}])|[\r\n]+|(.)", re.I)
   # control words which specify a "destionation".
   destinations = frozenset((
      'aftncn','aftnsep','aftnsepc','annotation','atnauthor','atndate','atnicn','atnid',
      'atnparent','atnref','atntime','atrfend','atrfstart','author','background',
      'bkmkend','bkmkstart','blipuid','buptim','category','colorschememapping',
      'colortbl','comment','company','creatim','datafield','datastore','defchp','defpap',
      'do','doccomm','docvar','dptxbxtext','ebcend','ebcstart','factoidname','falt',
      'fchars','ffdeftext','ffentrymcr','ffexitmcr','ffformat','ffhelptext','ffl',
      'ffname','ffstattext','field','file','filetbl','fldinst','fldrslt','fldtype',
      'fname','fontemb','fontfile','fonttbl','footer','footerf','footerl','footerr',
      'footnote','formfield','ftncn','ftnsep','ftnsepc','g','generator','gridtbl',
      'header','headerf','headerl','headerr','hl','hlfr','hlinkbase','hlloc','hlsrc',
      'hsv','htmltag','info','keycode','keywords','latentstyles','lchars','levelnumbers',
      'leveltext','lfolevel','linkval','list','listlevel','listname','listoverride',
      'listoverridetable','listpicture','liststylename','listtable','listtext',
      'lsdlockedexcept','macc','maccPr','mailmerge','maln','malnScr','manager','margPr',
      'mbar','mbarPr','mbaseJc','mbegChr','mborderBox','mborderBoxPr','mbox','mboxPr',
      'mchr','mcount','mctrlPr','md','mdeg','mdegHide','mden','mdiff','mdPr','me',
      'mendChr','meqArr','meqArrPr','mf','mfName','mfPr','mfunc','mfuncPr','mgroupChr',
      'mgroupChrPr','mgrow','mhideBot','mhideLeft','mhideRight','mhideTop','mhtmltag',
      'mlim','mlimloc','mlimlow','mlimlowPr','mlimupp','mlimuppPr','mm','mmaddfieldname',
      'mmath','mmathPict','mmathPr','mmaxdist','mmc','mmcJc','mmconnectstr',
      'mmconnectstrdata','mmcPr','mmcs','mmdatasource','mmheadersource','mmmailsubject',
      'mmodso','mmodsofilter','mmodsofldmpdata','mmodsomappedname','mmodsoname',
      'mmodsorecipdata','mmodsosort','mmodsosrc','mmodsotable','mmodsoudl',
      'mmodsoudldata','mmodsouniquetag','mmPr','mmquery','mmr','mnary','mnaryPr',
      'mnoBreak','mnum','mobjDist','moMath','moMathPara','moMathParaPr','mopEmu',
      'mphant','mphantPr','mplcHide','mpos','mr','mrad','mradPr','mrPr','msepChr',
      'mshow','mshp','msPre','msPrePr','msSub','msSubPr','msSubSup','msSubSupPr','msSup',
      'msSupPr','mstrikeBLTR','mstrikeH','mstrikeTLBR','mstrikeV','msub','msubHide',
      'msup','msupHide','mtransp','mtype','mvertJc','mvfmf','mvfml','mvtof','mvtol',
      'mzeroAsc','mzeroDesc','mzeroWid','nesttableprops','nextfile','nonesttables',
      'objalias','objclass','objdata','object','objname','objsect','objtime','oldcprops',
      'oldpprops','oldsprops','oldtprops','oleclsid','operator','panose','password',
      'passwordhash','pgp','pgptbl','picprop','pict','pn','pnseclvl','pntext','pntxta',
      'pntxtb','printim','private','propname','protend','protstart','protusertbl','pxe',
      'result','revtbl','revtim','rsidtbl','rxe','shp','shpgrp','shpinst',
      'shppict','shprslt','shptxt','sn','sp','staticval','stylesheet','subject','sv',
      'svb','tc','template','themedata','title','txe','ud','upr','userprops',
      'wgrffmtfilter','windowcaption','writereservation','writereservhash','xe','xform',
      'xmlattrname','xmlattrvalue','xmlclose','xmlname','xmlnstbl',
      'xmlopen',
   ))
   # Translation of some special characters.
   specialchars = {
      'par': '\n',
      'sect': '\n\n',
      'page': '\n\n',
      'line': '\n',
      'tab': '\t',
      'emdash': '\u2014',
      'endash': '\u2013',
      'emspace': '\u2003',
      'enspace': '\u2002',
      'qmspace': '\u2005',
      'bullet': '\u2022',
      'lquote': '\u2018',
      'rquote': '\u2019',
      'ldblquote': '\201C',
      'rdblquote': '\u201D',
   }
   stack = []
   ignorable = False       # Whether this group (and all inside it) are "ignorable".
   ucskip = 1              # Number of ASCII characters to skip after a unicode character.
   curskip = 0             # Number of ASCII characters left to skip
   out = []                # Output buffer.
   for match in pattern.finditer(text):
      word,arg,hex,char,brace,tchar = match.groups()
      if brace:
         curskip = 0
         if brace == '{':
            # Push state
            stack.append((ucskip,ignorable))
         elif brace == '}':
            # Pop state
            ucskip,ignorable = stack.pop()
      elif char: # \x (not a letter)
         curskip = 0
         if char == '~':
            if not ignorable:
                out.append('\xA0')
         elif char in '{}\\':
            if not ignorable:
               out.append(char)
         elif char == '*':
            ignorable = True
      elif word: # \foo
         curskip = 0
         if word in destinations:
            ignorable = True
         elif ignorable:
            pass
         elif word in specialchars:
            out.append(specialchars[word])
         elif word == 'uc':
            ucskip = int(arg)
         elif word == 'u':
            c = int(arg)
            if c < 0: c += 0x10000
            if c > 127: out.append(chr(c)) #NOQA
            else: out.append(chr(c))
            curskip = ucskip
      elif hex: # \'xx
         if curskip > 0:
            curskip -= 1
         elif not ignorable:
            c = int(hex,16)
            if c > 127: out.append(chr(c)) #NOQA
            else: out.append(chr(c))
      elif tchar:
         if curskip > 0:
            curskip -= 1
         elif not ignorable:
            out.append(tchar)
   return ''.join(out)


# не работает
#def takertf(unique):
    #for i in find_ext(r"files\{}\.".format(unique),"rtf"):
        #print(i)
        #print(striprtf(open(i ).read()).encode().decode('iso-8859-1').encode('utf8') )

        


#j = DistJaccard("Меня зовут Ваня", "Ваня")

#print(j)


#s = '«bla. bla? bla.bla! bla...»'
#punctpad(s)
#generateVWfromdir()


#print(generatelistfromdir())


#открыть все документы
#text = textract.process(".\part3.docx")
#print(text.decode('utf-8'))   

#pdf = pdfplumber.open('.\part1.pdf')
#page = pdf.pages[0]
#text = page.extract_text()
#print(text)
#pdf.close()
        
#unique = 'f004c39664dd4031b403c803400b0f59'
#listofsentences(unique)

'''
unique = 'f004c39664dd4031b403c803400b0f59'
for i in listofsentences(unique):
    print("/n")
    print(i)
'''

'''
unique = 'f004c39664dd4031b403c803400b0f59'
takertf(unique)
'''



       
#for i in listofcleanfromdir(uniquek):
#    print("zzzz")
#    print(i)


'''
unique = 'f004c39664dd4031b403c803400b0f59'
textarr = listofsentences(unique)
print(textarr)
'''
