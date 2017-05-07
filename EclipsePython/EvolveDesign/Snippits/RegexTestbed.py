import re


strings = re.split(",",
                   """
        Proposed variant 3.sql,
        Proposed variant 3.svg,
        Proposed variant 3Table.csv,
        Proposed variant 3Table.html,
        Proposed variant 3Zsz.csv,
        """
        ,)


#re.match(pattern, string, flags=0)
#print thisString
print "Search {}".format(re.search("Table.html$","Proposed variant 3Table.html"))


print "Search {}".format(re.search("Discrete","Discrete variable"))

print "Search {}".format(re.search("Discrete","Discrete variable"))

print "Search {}".format(re.search("dddd","Discrete variable"))

print "Search {}".format(re.search("2dd","Discrete variable"))

#print strings
