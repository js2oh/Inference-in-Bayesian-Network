#!/usr/bin/python

from factor import Factor

def main():
  f1 = Factor(['Trav'], [['t','f']], [0.05,0.95])
  f2 = Factor(['Fraud','Trav'],[['t','t','f','f'],['t','f','t','f']],[0.01,0.004,0.99,0.996])
  f3 = Factor(['FP','Fraud','Trav'],[['t','t','t','t','f','f','f','f'],['t','t','f','f','t','t','f','f'],['t','f','t','f','t','f','t','f']],[0.9,0.1,0.9,0.01,0.1,0.9,0.1,0.99])
  f4 = Factor(['IP','Fraud','OC'],[['t','t','t','t','f','f','f','f'],['t','t','f','f','t','t','f','f'],['t','f','t','f','t','f','t','f']],[0.02,0.011,0.01,0.001,0.98,0.989,0.99,0.999])
  f5 = Factor(['CRP','OC'],[['t','t','f','f'],['t','f','t','f']],[0.1,0.001,0.9,0.999])
  f6 = Factor(['OC'],[['t','f']],[0.6,0.4])
  factorList = [f1,f2,f3,f4,f5,f6]
  quaryList = ['Fraud']
  hiddenVariables = ['Trav','FP','Fraud','IP','OC','CRP']
  evidenceList1 = dict(IP='t')
  evidenceList2 = dict(IP='t', CRP='t')
  Factor.inference(factorList,quaryList,hiddenVariables,evidenceList1)
  Factor.inference(factorList,quaryList,hiddenVariables,evidenceList2)

main()