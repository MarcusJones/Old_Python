'''
Created on 2012-03-04

@author: Anonymous
'''
import random
from decimal import Decimal

'''
Created on 2012-03-03

@author: Anonymous
'''
import logging.config

def checkDecimalErr(values):
    for value in values:
        if not isinstance(value, Decimal):
            raise Exception("{} is not a decimal".format(value))  

class MyClass(object):
    
    def __init__(self, aVariable): 
        pass

def decimalDigitsToInt(thisDec):
    """
    Given a Decimal, return the pure digits as an Int
    """
    if not isinstance(thisDec, Decimal):
        raise Exception("Not a decimal")    
    
    # First, get the digits tuple
    xDigits = thisDec.as_tuple().digits
    # Check if it's negative
    neg = 1
    if thisDec.as_tuple().sign:    
        neg = -1
        
    # Convert to list
    xDigits = list(xDigits)
    # Build up a string
    xDigits = [str(dig) for dig in xDigits]
    # Convert back to int
    digitsNoPrecision = int("".join(xDigits))
    
    # Add the sign
    digitsNoPrecision = neg * digitsNoPrecision
    return digitsNoPrecision

def intToList(thisInt):
    if not isinstance(thisInt, int):
        raise
    
    if thisInt < 0:
        thisInt = thisInt * -1
        #raise Exception("Negative integers not supported")
    
    # First, convert to a char array
    numberCharList = list(str(thisInt))
    # Then, convert this list back to Int
    numberIntList = [int(num) for num in numberCharList]
    
    return numberIntList

def exponentMatches(a, b):
    if not isinstance(a, Decimal):
        raise Exception("Not a decimal")
    if not isinstance(b, Decimal):
        raise Exception("Not a decimal")  
      
    #logging.debug("Compare exponents {}, exponent precision is: {}".format(xTuple.exponent,precTuple.exponent))
    
    if a.as_tuple().exponent != b.as_tuple().exponent:
        return False
    else:
        return True
    
def roundTo(value, precision):
    """
    Returns a Decimal, rounded to the nearest base
    """
    if not isinstance(value, Decimal):
        raise Exception("Not a decimal")
    if not isinstance(precision, Decimal):
        raise Exception("Not a decimal")    
    
    if not isExponentMatch(value, precision):
        raise Exception("No precision match")
    
    #xTuple = x.as_tuple()
    #precTuple = precision.as_tuple()
    
    valueDigits = decimalDigitsToInt(value)
    precDigits = decimalDigitsToInt(precision)
    #print xDigits
    #print decimalDigitsToInt(x), decimalDigitsToInt(precisionDec)
    #print ["".join(str(digit)) for digit in xTuple.digits]
    #print "".join(xDigits)
    #return Decimal(str(precisionDec * round(float(x)/precisionDec)))
    #print valueDigits
    #print precDigits
    roundedDigits = int(precDigits * round(float(valueDigits)/precDigits))
    
    #print roundedDigits
    
    roundedDigitsListed = intToList(roundedDigits)
    
    if roundedDigits >= 0:
        roundedDec = Decimal((0, roundedDigitsListed, precision.as_tuple().exponent))
    if roundedDigits <= 0:
        roundedDec = Decimal((1, roundedDigitsListed, precision.as_tuple().exponent))
        
    logging.debug("Rounding {} to nearest {} = {}".format(value,precision,roundedDec))
    
    return roundedDec
    
    #int(base * round(float(x)/base))
    #logging.debug("Compare exponents {}, exponent precision is: {}".format(xTuple.exponent,precTuple.exponent))    
    


def isExponentMatch(x, precisionDec):
    if not isinstance(x, Decimal):
        raise Exception("Not a decimal")
    if not isinstance(precisionDec, Decimal):
        raise Exception("Not a decimal")
    
    xTuple = x.as_tuple()
    precTuple = precisionDec.as_tuple()

    if xTuple.exponent != precTuple.exponent:
        return False
    else:
        return True

def setDecimalPlaces(a,decimalPlaces):
    if not isinstance(a, Decimal):
        raise Exception("Not a decimal")
    if not isinstance(decimalPlaces, int):
        raise Exception("Not an iont")
    if decimalPlaces < 0:
        raise Exception("Negative")
    
    #print "Decimal:",a
    #print "Float:",float(a)
    
    formatString = "{:." + str(decimalPlaces) + "f}"
    decimalString = formatString.format(float(a))
    newValue = Decimal(decimalString)

    logging.debug("Returning {}, from input {} to {} places ".format(newValue, a, decimalPlaces))
    
    return newValue

    a.as_tuple().exponent

    
def matchExponent(x, precisionDec):
    if not isinstance(x, Decimal):
        raise Exception("Not a decimal")
    if not isinstance(precisionDec, Decimal):
        raise Exception("Not a decimal")
    
    xTuple = x.as_tuple()
    precTuple = precisionDec.as_tuple()
    #print precTuple.sign
    if precTuple.exponent >= 0:
        raise Exception("The precision is not in decimal, this is currently unsupported")

    if precTuple.exponent > xTuple.exponent:
        raise Exception("The precision is less than the value")
    
    
    if xTuple.exponent != precTuple.exponent:
        logging.debug("No match, value has: {}, exponent precision is: {}".format(xTuple.exponent,precTuple.exponent))
        #print xTuple
        #print precTuple
        # Need to add 0's to the digits, up to the precision
        theseDigits = list(xTuple.digits)
        #print theseDigits
        #print ((xTuple.exponent - precTuple.exponent))
        for aZero in range(xTuple.exponent - precTuple.exponent):
            theseDigits.append(0) 
        #print theseDigits
        # The new value has padded zeroes, plus the exponent of the required precision
        newValueTuple = (xTuple.sign, theseDigits, precTuple.exponent)
        newValue = Decimal(newValueTuple)
        #print newValue
        #newValueTuple = x.as_tuple()
        #valueTuple.exponent = precisionDec.as_tuple().exponent
        #print Decimal(valueTuple)
        logging.debug("Returning {}, to match {}, from input {} ".format(newValue, precisionDec, x))
        return newValue
    else:
        logging.debug("Precision of {} matches {}".format(x, precisionDec))
        return(x)
        
        

def compareDecimals(a,b):
    if not isinstance(a, Decimal):
        print "Not a decimal"
        return -1
    if not isinstance(b, Decimal):
        print "Not a decimal"
        return -1
    
    a.as_tuple().sign
    a.as_tuple().digits
    a.as_tuple().exponent
    b.as_tuple().sign

#def comparesigFigsDecimal():
def singleStep(value,lower,upper,precision):
    newValue = value + random.choice([precision, -precision])
    
    if newValue > upper:
        #print "Too high"
        newValue = upper
        #print limitedGaussian
    elif newValue < lower:
        #print "newValue low"
        newValue = lower
    else:
        pass
        #print "Just right"
        #newValue = newValue    
    
    logging.debug("Returning {}, {} step from {}".format(newValue, precision, value))
    
    return newValue
    
    return newValue

def gaussianDecimal(value,sigma,lower,upper,precision):
    """
    Permutes the value 
    """
    if not isinstance(lower,Decimal):
        raise Exception("Not a decimal")
    if not isinstance(upper,Decimal):
        raise Exception("Not a decimal")
    if not isinstance(precision,Decimal):
        raise Exception("Not a decimal")    
    if not exponentMatches(lower,precision):
        raise Exception("Precision mismatch")
    if not exponentMatches(upper,precision):
        raise Exception("Precision mismatch")
    
    
    #numberDecimals 
    
    
    
    #desiredDigits = len(value.as_tuple().digits)
    decimalPlaces = -1 * precision.as_tuple().exponent
    

    #print value, "has",desiredDigits
    gaussianVal = Decimal(random.gauss(float(value), sigma))
    #print "Random gauss", gaussianVal
    #newDigits = len(gaussianVal.as_tuple().digits)
    #print gaussianVal, "has", newDigits
    #clippedGaussianList = gaussianVal.as_tuple().digits[0:desiredDigits]
    finalGaussian = setDecimalPlaces(gaussianVal,decimalPlaces)
    #print clippedGaussianList
    
    #finalGaussian = Decimal((gaussianVal.as_tuple().sign, clippedGaussianList, value.as_tuple().exponent))
    
    #print finalGaussian
    
    #print "{0:0.2f}".format(gaussianVal)
    #print roundTo(finalGaussian,precision)
    print lower, finalGaussian, upper 
    #print finalGaussian > upper
    #print finalGaussian < lower
    if finalGaussian > upper:
        #print "Too high"
        limitedGaussian = upper
        #print limitedGaussian
    elif finalGaussian < lower:
        #print "Too low"
        limitedGaussian = lower
    else:
        #print "Just right"
        limitedGaussian = finalGaussian    
    
    logging.debug("Returning {}, a gaussian from {} with sigma = {} ".format(limitedGaussian,value, sigma))
    
    return limitedGaussian
    
def randomDecimal(lower,upper,precision):
    """
    Returns a random decimal in: lower <= Value <= upper
    """
    if not isinstance(lower,Decimal):
        raise Exception("Not a decimal")
    if not isinstance(upper,Decimal):
        raise Exception("Not a decimal")
    if not isinstance(precision,Decimal):
        raise Exception("Not a decimal")    
    if not exponentMatches(lower,precision):
        raise Exception("Precision mismatch")
    if not exponentMatches(upper,precision):
        raise Exception("Precision mismatch")
    
    # First, get the raw digits
    lowerInt = decimalDigitsToInt(lower)
    upperInt = decimalDigitsToInt(upper)    
    precisionInt = decimalDigitsToInt(precision)    
    
    # The desired exponent
    precExp = precision.as_tuple().exponent
    
    # Then generate a random integer
    randomNumber = random.randint(lowerInt,upperInt)
    
    # Now round it to the precision value
    randomNumberRounded = int(precisionInt * round(float(randomNumber)/precisionInt))
    
    randomNumberListed = intToList(randomNumberRounded)
    
    if randomNumberRounded >= 0:
        #print 0,randomNumberListed,precExp
        randomDec = Decimal((0,randomNumberListed,precExp))
    if randomNumberRounded <= 0:
        randomDec = Decimal((1,randomNumberListed,precExp))
    # Finally, reconstruct the random Int as a Decimal
    logging.debug("Returning {} between {} and {}".format(randomDec, lower, upper))
    
    return randomDec

def _testStep():
    value = Decimal('6.00')
    prec = Decimal('0.01')
    
    lower = Decimal('1.00')
    upper = Decimal('8.00')
    
    singleStep(value,lower,upper,prec)
    
    value = Decimal('6.00')
    prec = Decimal('0.01')
    
    lower = Decimal('1.00')
    upper = Decimal('6.00')
    
    singleStep(value,lower,upper,prec)
    
def _testGaussian():
    value = Decimal('6.00')
    prec = Decimal('0.01')
    
    lower = Decimal('1.00')
    upper = Decimal('8.00')
    
    sigma = 0.5
    
    gaussianDecimal(value,sigma,lower,upper,prec)

def _testRandom():
    a = Decimal('1.00')
    b = Decimal('10.00')
    prec = Decimal('.05')
    randomDecimal(a,b,prec)

    a = Decimal('-10.00')
    b = Decimal('10.00')
    prec = Decimal('5.00')
    randomDecimal(a,b,prec)


def _testRoundTo():
    value = Decimal("0.12")
    precision = Decimal('0.05')
    #print 
    roundTo(value, precision)

    value = Decimal("-3.14")
    precision = Decimal('0.05')
    #print 
    roundTo(value, precision)

    value = Decimal("-305")
    precision = Decimal('23')
    #print 
    roundTo(value, precision)
    
    
    
    #print "To 1:", roundTo(value, precision)
    #print "To 2:", roundTo(3.14, 2)
    #print "To 10:", roundTo(3.14, 10)
    ###print "To .1:", roundTo(3.14, .1)
    #print "To .2:", roundTo(3.14, .2)    
    #print "To .0001:", roundTo(3.14, .2)
    
    #print float(3.14)/0.0001
    

def _test3():
    a = Decimal('6')
    prec = Decimal('0.001')
    
    matchExponent(a,prec)
    
    a = Decimal('6.0000')
    prec = Decimal('0.001')    
    matchExponent(a,prec)
        
def _test2():
    print "Play with decimal"
    
    value = Decimal('3.1255666')
    print "Value:", value
    
    print "Tuple:", value.as_tuple()
    
    # Tuple
    t = (0, (1, 1), -5)
    print 'Input  :', t
    print 'Decimal:', Decimal(t)
        
    print "Number decimals:", value.as_tuple().exponent
    
    print Decimal('1') is Decimal
    print isinstance(value, Decimal)


def _testSigFigs():
    value = Decimal('2.7')
    setDecimalPlaces(value,2)

    value = Decimal('-2.7')
    setDecimalPlaces(value,2)
    
    value = Decimal('300')
    setDecimalPlaces(value,2)
    
    value = Decimal('2')
    setDecimalPlaces(value,20)

    value = Decimal('2.5')
    setDecimalPlaces(value,0)
    
def _test1():
    logging.debug("Started _test1".format())
    print "To 1:", roundTo(3.14, 1)
    print "To 2:", roundTo(3.14, 2)
    print "To 10:", roundTo(3.14, 10)
    print "To .1:", roundTo(3.14, .1)
    print "To .2:", roundTo(3.14, .2)    
    print "To .0001:", roundTo(3.14, .2)
    
    print float(3.14)/0.0001
    
    print 
        
    logging.debug("Finished _test1".format())
if __name__ == "__main__":
    logging.config.fileConfig('..\\LoggingConfig\\loggingNofile.conf')
    logging.debug("Started _main".format())

    #_testSigFigs()
    _testStep()
    #_test1()
    #_test2()
    
    #_test3()
    #_testRandom()
    #_testRoundTo()
    #
    #_testGaussian()
    
    
    logging.debug("Started _main".format())
    
