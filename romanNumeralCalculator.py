# Author: Willie Stevenson
# Date 06/04/2016
#
# This is a small roman numeral calculator program. It purely deals in roman numerals
# It accepts two roman numeral strings. The second value is subtracted or added to the first passed value.


# We use a tuple because this data structure should be immutable, and we do not need to assign values necessarily. 
# This index ordering also provides a way to evaluate which roman numeral has a higher value. In this way we overcome having to assign
# an actual integer value to them.
romanNumerals = ('M' , 'D', 'C', 'L', 'X', 'V', 'I')

# This dictionary contains equivalent pairs of roman numerals. Notice that value differences only increase by one step.
# We can use these groupings to group and ungroup roman numeral values. This ordering is essential to evaluate roman numerals correctly.
romanNumeralGroupings = {"IIIII":"V", "VV":"X", "XXXXX":"L", "LL":"C", "CCCCC":"D", "DD":"M"}

# This dictionary contains roman numeral subtractives paired with their expanded form. Notice that value differences only increase by one step.
# We can use these groupings to compact and uncompact roman numeral values. This ordering is essential to evaluate roman numerals correctly.
romanNumeralSubtractives = {"IV":"IIII", "IX":"VIIII", "XL":"XXXX", "XC":"LCCCC", "CD":"CCCC", "CM":"DCCCC"}



# romanAdd
#
# Implementation
# 
# 1. Uncompact subtractives
# 2. Concatenate symbols
# 3. Sort symbols from high to low
# 4. Group lower value symbols into higher value symbols
# 5. Compact subtractives
#
#
# # For instance, to add XIX (19) and XLV (45):
# 1. Uncompact subtractives: XIX becomes XVIIII and XLV becomes XXXXV
# 2. Concatenate: XVIIII + XXXXV becomes XVIIIIXXXXV
# 3. Sort: XIIIIXXXXII becomes XXXXXVVIIII
# 4. Group: XXXXXVVIIII becomes LXIIII
# 5. Compact subtractives: LXIIII becomes LXIV, the final answer of 64
#
#
#
# @param string; x; a string containing a roman numeral;
# @param string; y; a string containing a roman numeral;
# @restrictions @param must be of type string;
# @return string; the result of the addition as a roman numeral;
def romanAdd(x, y):
	helper_step_formatter(x + " + " + y ,"ADD *")
	x = helper_uncompact_subtractives(x)
	y = helper_uncompact_subtractives(y)
	helper_step_formatter(x, "Uncompact Subtractives (X)")
	helper_step_formatter(y, "Uncompact Subtractives (Y)")
	ans = helper_concantenate(x, y)
	helper_step_formatter(ans, "Concatenate Symbols")
	ans = helper_sort(ans)
	helper_step_formatter(ans, "Sort symbols from high to low")
	ans = helper_group(ans)
	helper_step_formatter(ans, "Group lower value symbols into higher value symbols")
	ans = helper_compact_subtractives(ans)
	helper_step_formatter(ans, "Compact subtractives")
	helper_step_formatter(ans, "ANSWER")

	return ans


# romanSubtract
#
# Implementation
# 
# 1. Uncompact subtractives
# 2. Eliminate common symbols
# 3. Ungroup symbols
# 4. Eliminate common symbols
# 5. Repeat 3-4 until the number to be subtracted is eliminated
# 6. Compact subtractives 
#
#
# For instance, to subtract XXXVI (36) from XLIV (44):
# 1. Uncompact subtractives: XXXVI doesn't change, but XLIV becomes XXXXIIII
# 2. Eliminate common symbols: XXXXIIII - XXXVI = XIII - V (the red symbols can be eliminated because they appear in both numbers)
# 3. Ungroup symbols: To create more common symbols, ungroup the X into VV: XIII - V = VVIII - V
# 4. Eliminate common symbols: VVIII - V = VIII
# 5. Group lower symbols into higher symbols
# 6. Compact subtractives: VIII doesn't change; we have a final answer of 8
# 
#
# @param string; x; a string containing a roman numeral;
# @param string; y; a string containing a roman numeral;
# @restrictions @param must be of type string;
# @return string; the result of the subtraction as a roman numeral;
def romanSubtract(x, y):
	helper_step_formatter(x + " - " + y ,"SUBTRACT *")
	x = helper_uncompact_subtractives(x)
	y = helper_uncompact_subtractives(y)
	helper_step_formatter(x, "Uncompact Subtractives (X)")
	helper_step_formatter(y, "Uncompact Subtractives (Y)")
	x, y = helper_eliminate_common_symbols(x, y)
	helper_step_formatter(x, "Eliminate common symbols (X)")
	helper_step_formatter(y, "Eliminate common symbols (Y)")

	while (y != ""):
		x = helper_ungroup(x)
		y = helper_ungroup(y)
		helper_step_formatter(x, "Ungroup Symbols (X)")
		helper_step_formatter(y, "Ungroup Symbols (Y)")
		x, y = helper_eliminate_common_symbols(x, y)
		helper_step_formatter(x, "Eliminate common symbols (X)")
		helper_step_formatter(y, "Eliminate common symbols (Y)")

	ans = helper_group(x)
	helper_step_formatter(ans, "Group lower value symbols into higher value symbols")
	ans = helper_compact_subtractives(ans)
	helper_step_formatter(ans, "Compact subtractives")

	helper_step_formatter(ans, "ANSWER")

	return ans


# romanMultiply
#
# Implementation
# 
# 1. Reduce y down to all 'I' and count them
# 2. Add x and x the number of times y was counted 
#
#
# For instance, to multiply VI (6) from VII (7):
# 1. Reduce y: VII -> ungroup V -> IIIII + II -> IIIIIII (count the length of the string)
# 2. Follow steps in romanAdd to add the value of x and x together by the length of y times
# 
#
# @param string; x; a string containing a roman numeral;
# @param string; y; a string containing a roman numeral;
# @restrictions @param must be of type string;
# @return string; the result of the multiplication as a roman numeral;
def romanMultiply(x, y):
	helper_step_formatter(x + " x " + y ,"MULTIPLY *")
	y = helper_reduce(y) # gets the int value of y

	product = x

	for i in range (1, y):
		product = romanAdd(product, x)

	print "\n"
	helper_step_formatter(product, "FINAL ANSWER")


##################################################
##########								 ######### 
##               HELPER FUNCTIONS               ## 
##########           					 #########
##################################################


# takes the compact terms (ex. IV) and translates them to their expanded roman numeral value
def helper_uncompact_subtractives(x):

	for key in romanNumeralSubtractives:
		x = x.replace(key, romanNumeralSubtractives[key])

	return x

def helper_concantenate(x, y):
	return x + y

# sorts the roman numeral - puts high values on left and low on right
def helper_sort(x):
	sortedString = ""

	for i in range (0, len(romanNumerals)):
		sortedString += (romanNumerals[i] * x.count(romanNumerals[i]))

	return sortedString
	
# groups smaller terms into their 1 step up counterpart
def helper_group(x):
	
	for key in romanNumeralGroupings:
		x = x.replace(key, romanNumeralGroupings[key])

	return x

# ungroups bigger terms into their 1 step down counterpart
def helper_ungroup(x):
	
	for key in romanNumeralGroupings:
		x = x.replace(romanNumeralGroupings[key], key)

	return x

# takes expanded terms (ex. IIII) and translates them to their proper roman numeral compact value
def helper_compact_subtractives(x):

	for key in romanNumeralSubtractives:
		x = x.replace(romanNumeralSubtractives[key], key)

	return x

# removes all common roman numerals found in x and y
def helper_eliminate_common_symbols(x, y):

	tempX = x
	tempY = y
	
	for c1 in x:
		if tempY.find(c1) != -1:
			tempX = tempX.replace(c1,"", 1)
			tempY = tempY.replace(c1, "", 1)
	
	return [tempX, tempY]

# reduce roman numeral to all 'I's and the count - effectively finding the integer value of the string
def helper_reduce(x):

	x = helper_uncompact_subtractives(x)

	while (any(c in x for c in romanNumerals[:6])):
		x = helper_ungroup(x)

	return len(x)

# only accounts for invalid chars, not proper roman numerals
def helper_is_string_roman_numeral(x):
	for c in x:
		if c not in romanNumerals:
			return False

	return True

# formats each step 
def helper_step_formatter(x, step_name):
	print("--------------------------------------------------------------------------")
	#print x, "  | \t",  step_name
	print('{0:20} | {1:30}'.format(x, step_name))


##################################################
##########								 ######### 
##             END HELPER FUNCTIONS             ## 
##########           					 #########
##################################################

if __name__ == "__main__":
	print " ------------------------------------------------------------------------------------------------------ "
	print "| This is a roman numeral calculator that supports addition, subtraction, and multiplication (+, -, x) |"
	print " ------------------------------------------------------------------------------------------------------ "

	while (1):
		operation = raw_input("\nWhat would you like to do? Enter [+] [-] [x] [Q - Quit]: ")

		if (operation != "Q" and operation != "+" and operation != "-" and operation != "x"):
			print "Unsupported operation. Please enter a supported operation."

		if operation == "Q":
			break

		operand1 = raw_input("Enter first roman numeral: ")

		operand1 = operand1.upper()

		if not helper_is_string_roman_numeral(operand1):
			print "Unsupported operand(s). Please enter a roman numeral with valid characters." 

		operand2 = raw_input("Enter second roman numeral: ")

		operand2 = operand2.upper()

		if not helper_is_string_roman_numeral(operand2):
			print "Unsupported operand(s). Please enter a roman numeral with valid characters."

		if (helper_reduce(operand2) > helper_reduce(operand1)) and operation == '-':
			print "The second operand you entered is bigger than the first. Negative answers are not supported with roman numerals so this operation cannot be completed."

		if operation == "+":
			romanAdd(operand1, operand2)
		elif operation == "-":
			romanSubtract(operand1, operand2)
		elif operation == "x":
			romanMultiply(operand1, operand2)

	print "Exiting . . ."