#!/usr/bin/python

class Factor(object):
	def __init__(self, variables, valueList, probabilities):
		self.valueTable = dict()
		for i in xrange(0,len(variables)):
			self.valueTable[variables[i]] = valueList[i]
		self.probabilities = probabilities

	def copy(self):
		newFactor = Factor([],[],[])
		newFactor.valueTable = dict(self.valueTable)
		newFactor.probabilities = list(self.probabilities)
		return newFactor

	# function that restricts a variable to some value in a given factor
	@staticmethod
	def restrict(factor, variable, value):
		newFactor = factor.copy()
		indiciesRestricted = list()
		restrictedFactorTable = list()
		restrictedProbabilities = list()
		index = 0
		for val in newFactor.valueTable[variable]:
			if val == value:
				indiciesRestricted.append(index)
			index += 1
		del newFactor.valueTable[variable]
		remainingVariables = newFactor.valueTable.keys()
		for var in remainingVariables:
			restrictedValueList = list()
			for i in xrange(0, len(newFactor.valueTable[var])):
				if i in indiciesRestricted:
					restrictedValueList.append(newFactor.valueTable[var][i])
			restrictedFactorTable.append(restrictedValueList)
		for i in xrange(0, len(remainingVariables)):
			newFactor.valueTable[remainingVariables[i]] = restrictedFactorTable[i]
		for i in xrange(0, len(newFactor.probabilities)):
			if i in indiciesRestricted:
				restrictedProbabilities.append(newFactor.probabilities[i])
		newFactor.probabilities = restrictedProbabilities
		return newFactor

	# function that multiplies two factors
	@staticmethod
	def multiply(factor1, factor2):
		factorVariables1 = factor1.valueTable.keys()
		factorVariables2 = factor2.valueTable.keys()
		commonVariables = list()
		newVariables = list()
		for var in factorVariables1:
			if var in factorVariables2:
				commonVariables.append(var)
				newVariables.append(var)
		for var in factorVariables1:
			if var not in newVariables:
				newVariables.append(var)
		for var in factorVariables2:
			if var not in newVariables:
				newVariables.append(var)
		newValueList = [[] for i in xrange(len(newVariables))]
		newProbabilities = list()
		for i in xrange(len(factor1.probabilities)):
			for j in xrange(len(factor2.probabilities)):
				isMatched = True
				for var in commonVariables:
					if factor1.valueTable[var][i] != factor2.valueTable[var][j]:
						isMatched = False
						break
				if isMatched:
					for k, var in enumerate(newVariables):
						if var in factorVariables1:
							newValueList[k].append(factor1.valueTable[var][i])
						else:
							newValueList[k].append(factor2.valueTable[var][j])
					newProbabilities.append(factor1.probabilities[i] * factor2.probabilities[j])
		return Factor(newVariables, newValueList, newProbabilities)

	# function that sums out a variable in a given factor
	@staticmethod
	def sumout(factor, variable):
		newFactor = factor.copy()
		if len(newFactor.valueTable.keys()) == 1:
			return newFactor
		variableDomain = list()
		for val in newFactor.valueTable[variable]:
			if val not in variableDomain:
				variableDomain.append(val)
		del newFactor.valueTable[variable]
		remainingVariables = newFactor.valueTable.keys()
		newValueList = [[] for i in xrange(len(remainingVariables))]
		newProbabilities = list()
		summedRows = list()
		for i in xrange(len(newFactor.probabilities)):
			if i in summedRows:
				continue
			summedProbability = newFactor.probabilities[i]
			for j in xrange(i+1, len(newFactor.probabilities)):
				needSum = True
				for var in remainingVariables:
					if newFactor.valueTable[var][i] != newFactor.valueTable[var][j]:
						needSum = False
				if needSum and j not in summedRows:
					summedRows.append(j)
					summedProbability += newFactor.probabilities[j]
			for k, var in enumerate(remainingVariables):
				newValueList[k].append(newFactor.valueTable[var][i])
			newProbabilities.append(summedProbability)
		return Factor(remainingVariables, newValueList, newProbabilities)

	# function that normalizes a factor by dividing each entry by the 
	# sum of all the entries. This is useful when the factor is a distribution
	@staticmethod
	def normalize(factor):
		newFactor = factor.copy()
		totalSum = 0
		for prob in newFactor.probabilities:
			totalSum += prob
		for i in xrange(len(newFactor.probabilities)):
			newFactor.probabilities[i] = newFactor.probabilities[i]/totalSum
		return newFactor

	# function that computes P(queryVariables|evidenceList) by variable elimination
	@staticmethod
	def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
		newOrderedListOfHiddenVariables = filter(lambda x: x not in queryVariables and x not in evidenceList.keys(), orderedListOfHiddenVariables)
		for evidence in evidenceList: 
			restrictedFactorList = list()
			for factor in factorList:
				if evidence in factor.valueTable.keys():
					# print
					print 'Restrict:',
					print evidence
					restrictedFactor = Factor.restrict(factor, evidence, evidenceList[evidence])
					for key,val in restrictedFactor.valueTable.items():
						print key, "=>", val
					print restrictedFactor.probabilities
					restrictedFactorList.append(restrictedFactor)
				else:
					restrictedFactorList.append(factor)
			factorList = restrictedFactorList
		for hiddenVariable in newOrderedListOfHiddenVariables:
			factorListToMultiply = list()
			for factor in factorList:
				if hiddenVariable in factor.valueTable.keys():
					factorListToMultiply.append(factor)
			factorList = filter(lambda factor: factor not in factorListToMultiply, factorList)
			if len(factorListToMultiply) > 0:
				# print
				print 'Multiply:',
				print hiddenVariable
				productFactor = reduce(Factor.multiply, factorListToMultiply)
				for key,val in productFactor.valueTable.items():
					print key, "=>", val
				print productFactor.probabilities
			else:
				continue
			# print
			print 'Sumout:',
			print hiddenVariable
			factorSummedOut = Factor.sumout(productFactor, hiddenVariable)
			for key,val in factorSummedOut.valueTable.items():
				print key, "=>", val
			print factorSummedOut.probabilities
			factorList.append(factorSummedOut)
		# print
		print 'Multiply Query Variables:'
		if len(factorList) > 0:
			output = reduce(Factor.multiply, factorList)
			for key,val in output.valueTable.items():
				print key, "=>", val
			print output.probabilities
		# print
		print 'Normalize:'
		normalizedOutput = Factor.normalize(output)
		for key,val in normalizedOutput.valueTable.items():
			print key, "=>", val
		print normalizedOutput.probabilities
		return normalizedOutput

