import re

#phrase = "OS:ZoneLoads,\n"
#phrase = "Infiltration Quarter On Schedule;  ! Infiltration Schedule Name"
#print re.split(r"!|->",phrase.rstrip())
#phrase =    " -1.1,"


patValue = r"""
^ \s* \\group \s [\w \s]+ $
"""

patValue = r"""
^ \s* \\group \s [\w \s]+ $
"""

phrase = r"      TIME REL_BAL_ENERGY  |  BAL_ENERG_tot=-DQAIRdt_tot+ QHEAT_tot- QCOOL_tot+  QINF_tot+  QVENT_tot+  QCOUP_tot+  QTRANS_tot+ QGINT_tot+  QWGAIN_tot+ QSOL_tot+ QSOLAIR_tot"
phrase = r" ZoneCoolingSummaryMonthly"

patValue = r"""
[\s]+ | [\s+\|\s+]+ | [=]+
"""

patValue = r".*Monthly$"
regex = re.compile(patValue,re.VERBOSE)


if regex.match(phrase):
    print "yes"
else:
    print "no"
print regex.match(phrase)

#print regex.search(phrase).groups()
raise

phrase = r"  \group Simulation Parameters"

result =re.search(patValue,phrase,re.VERBOSE)


print result.group()

print result
print dir(result)

# We should always use search! 
"""
match()     Determine if the RE matches at the beginning of the string.
search()     Scan through a string, looking for any location where this RE matches.
findall()     Find all substrings where the RE matches, and returns them as a list.
finditer()     Find all substrings where the RE matches, and returns them as an iterator.
"""

pattern = """
    ^      # beginning of string
    \w+    # 1 or more alphanumeric chars
    [\w:]*  # Any number of colons and alphanumerics
    ,        # Comma
    $        # End of the line 
    """
    
pattern = """
    ;
    """
    
patValue = """
    ^      # beginning of string
    \s+    # some spaces
    [0-9 \. \-]+    # 
    ,        # Comma
    """
