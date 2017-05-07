'''
Created on 18.03.2011

@author: mjones
'''

import re

def translate_file(inputFilePath, outputFilePath, translations):
    """Writes a translated text file

    Keyword arguments:
    inputFilePath -- full path of input file
    outputFilePath -- output file full path
    translations -- A tuple containing (regex, replace) pairs - Use raw strings!
    
    Returns nothing
    """
    
    # Open and load and close the input file
    print 'reading:', inputFilePath    
    fIn = open(inputFilePath,'rb')
    s=unicode(fIn.read(),'utf-8')
    fIn.close()
    
    regExTranslations = []
    for translatePair in translations:
        regExTranslations = [ (re.compile(translatePair[0], re.U|re.M), translatePair[1]), 
                   # more regex pairs here
                   ]
    numRep=None
    # Loop each translation pair
    # Each translation contains one search Regex, and a replacement value
    # E.g. (re.compile(ur'''MySearchRegex''', re.U|re.M), ur'''MyNewString''') 
    #translations = [ (re.compile(ur'''MySearchRegex''', re.U|re.M), ur'''MyNewString'''), 
    #               # more regex pairs here
    #               ]
    for translationPair in translations:
        if numRep == None:
            # Search the file for any matches
            numRep = re.search(translationPair[0],s)
        # Do the translation
        outtext = re.sub(translationPair[0],translationPair[1], s)
        s=outtext
    
    if numRep:
        print ' writing:', outputFilePath
        outF = open(outputFilePath,'w')
        outF.write(outtext.encode('utf-8'))
        outF.close()

translations = ((ur'START','MyValue'), ('STOP','MyValue'))
inputFilePath = '..\\Test DCK files\\testForFindReplace.dck'
outputFilePath = '..\\Test DCK files\\testForFindReplaceOut.dck'

translate_file(inputFilePath, outputFilePath, translations)
 
#def replace_words(text, word_dic):
#    """
#    take a text and <strong class="highlight">replace</strong> words that match a key <strong class="highlight">in</strong> a dictionary with
#    the associated value, return the changed text
#    """
#    rc = re.compile('|'.join(map(re.escape, word_dic)))
#    def translate(match):
#        return word_dic[match.group(0)]
#    return rc.sub(translate, text)
# 
# 
#str1 = \
#"""When we see a Space Shuttle sitting on its launch pad, there are two big
#booster rockets attached to the sides of the main fuel tank. These are solid
#rocket boosters, made by Thiokol at their factory <strong class="highlight">in</strong> Utah. The engineers who
#designed the solid rocket boosters might have preferred to make them a bit
#fatter, but they had to be shipped by train from the factory to the launch
#site.  The railroad line from the factory runs through a tunnel <strong class="highlight">in</strong> the
#mountains.  The boosters had to fit through that tunnel.  The tunnel is
#slightly wider than the railroad track.  The width of the railroad track
#came from the width of horse-drawn wagons <strong class="highlight">in</strong> England, which were as wide
#as two horses' behinds.  So, a major design feature of what is the world's
#most advanced transportation system was determined over two thousand years
#ago by the width of a horse's ass!
#"""
# 
#test_file = "Mword1.txt"
## create a test <strong class="highlight">file</strong> for this example
#fout = open(test_file, "w")
#fout.write(str1)
#fout.close()
# 
## read the <strong class="highlight">file</strong>
#fin = open(test_file, "r")
#str2 = fin.read()
#fin.close()
# 
## the dictionary has target_word:replacement_word pairs
#word_dic = {
#'booster': 'rooster',
#'rocket': 'pocket',
#'solid': 'salted',
#'tunnel': 'funnel',
#'ship': 'slip'}
# 
## call the function and get the changed text
#str3 = replace_words(str2, word_dic)
# 
## test
#print str3
# 
## write changed text back out
#fout = open("Mword2.txt", "w")
#fout.write(str3)
#fout.close()