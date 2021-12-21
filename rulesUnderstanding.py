from xml.dom import minidom
import xml.etree.ElementTree as ET
import numpy as np

rules_file = "rules.xml"

''' get name rule '''
def get_rule_name(rule):
    return rule.attrib.get("name")

''' get elements value '''
def get_elements(rule, element_name):
    element_tag = rule.find(element_name)
    rule_element = element_tag.attrib.get(element_name)
    #print("__________name: {0} data: {1}".format(element_name, rule_element) )
    return rule_element

''' 
apply rules in specific situation, return indexes of matching rules
'''
def apply_specific_situation (obstacle = None, distance = 10, rule_conditions = ""):
    #print ("rule_conditions: ", rule_conditions)
    
    conds = [cmd_str.replace("obstacle", str(obstacle)) for cmd_str in rule_conditions]
    conds = [cond.replace("distance", str(distance) ) for cond in conds]
    #print("rule conditions [applied]", conds)
    
    rule_results = [execute_rule(condition_str) for condition_str in conds]
    print ("rule_maching result [condition]:", rule_results)
    return rule_results
    

''' execute a rule '''
def execute_rule (rule_condition_str):
    # Expression evaluation in String
    # Using eval()
    res = eval(rule_condition_str)
    # printing result
    print("The evaluated result for [{0}] is {1}".format(rule_condition_str, str(res)))
    return res

''' choose a rule which has highest priority and satified the conditions '''
def choose_rule(rule_condition_result, rule_priorities):
    rule_true_condition_priorities = np.multiply(rule_priorities, rule_condition_result)
    rule_choose_idx = np.argmax(rule_true_condition_priorities)
    print ("chosen rule idx", rule_choose_idx)
    return rule_choose_idx

''' print rule out '''
def print_chosen_rule(idx, rule_names, rule_conditions, rule_priorities, 
            rule_confidences, rule_actions):
    print ("rule_names: ", rule_names[idx])
    print ("_rule_actions: ", rule_actions[idx])
    print ("_rule_conditions: ", rule_conditions[idx])
    print ("_rule_priorities: ", rule_priorities[idx])
    print ("_rule_confidences: ", rule_confidences[idx])

def print_rules(rule_names, rule_conditions, rule_priorities, 
            rule_confidences, rule_actions):
    print ("rule_names: ", rule_names)
    print ("_rule_actions: ", rule_actions)
    print ("_rule_conditions: ", rule_conditions)
    print ("_rule_priorities: ", rule_priorities)
    print ("_rule_confidences: ", rule_confidences)

def main(rules_file):
    print(__file__ + " start!!")
    tree = ET.parse(rules_file)
    root = tree.getroot()
    print ("0__________", root.tag,"_" , root.attrib)
    rule_names = []
    rule_conditions = []
    rule_priorities = []
    rule_confidences = []
    rule_actions = []
    rule_names = np.array([get_rule_name(rule) for rule in root])
    rule_conditions = np.array([get_elements(rule, "condition") for rule in root])
    rule_priorities = np.array([get_elements(rule, "priority") for rule in root])
    rule_confidences = np.array([get_elements(rule, "confidence") for rule in root])
    rule_actions = np.array([get_elements(rule, "action") for rule in root])
    rule_priorities = rule_priorities.astype(float)

    print_rules(rule_names, rule_conditions, rule_priorities, 
                rule_confidences, rule_actions)

    # get all rules matching specific situation
    rule_condition_result = apply_specific_situation(obstacle = 1, distance = 30, rule_conditions = rule_conditions)
    rule_idx = choose_rule(rule_condition_result, rule_priorities)
    print_chosen_rule(rule_idx, rule_names, rule_conditions, rule_priorities, 
                rule_confidences, rule_actions)
    
if __name__ == '__main__':
    main(rules_file)