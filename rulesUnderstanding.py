from xml.dom import minidom
import xml.etree.ElementTree as ET
import numpy as np

rules_file = "rules.xml"
param_file = "parameter.xml"
''' get name rule '''
def get_rule_name(rule):
    return rule.attrib.get("name")

''' get elements value by tag'''
def get_tag_elements(rule, element_name):
    element = rule.find(element_name)
    rule_element = element.attrib.get(element_name)
    #print("__________name: {0} data: {1}".format(element_name, rule_element) )
    return rule_element

''' get parameter value '''
def get_parameter_value(root, element_name):
    for element in root:
        #print ("___________________", element.tag, element.attrib)
        if element.attrib.get("name") == element_name:
            return element.attrib.get("value")
    return None

''' 
apply rules in specific situation, return indexes of matching rules
'''
def apply_specific_situation (obstacle = None, distance = 10, CNN_sign_recognition="0", rule_conditions = ""):
    #print ("rule_conditions: ", rule_conditions)
    
    conds = [cmd_str.replace("OPENCV_obstacle", str(obstacle)) for cmd_str in rule_conditions]
    conds = [cond.replace("LiDAR_distance", str(distance) ) for cond in conds]
    conds = [cond.replace("CNN_sign_recognition", str(CNN_sign_recognition) ) for cond in conds]
    #print("rule conditions [applied]", conds)
    
    rule_results = [execute_rule(condition_str) for condition_str in conds]
    
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
def print_rule(idx, rule_names, rule_conditions, rule_priorities, 
            rule_confidences, rule_actions):
        print ("rule_names: ", rule_names[idx])
        print ("_____actions: ", rule_actions[idx])
        print ("_____condition: ", rule_conditions[idx])
        print ("_____prioritie: ", rule_priorities[idx])
        print ("_____confidence: ", rule_confidences[idx])


def print_rules(rule_names, rule_conditions, rule_priorities, 
            rule_confidences, rule_actions):
    for i in range(len(rule_names)):
        print_rule(i, rule_names, rule_conditions, rule_priorities, 
            rule_confidences, rule_actions)

def main(rules_file, param_file):
    print(__file__ + " start!!")

    ''' parsing rules '''
    tree = ET.parse(rules_file)
    root = tree.getroot()
    rule_names = []
    rule_conditions = []
    rule_priorities = []
    rule_confidences = []
    rule_actions = []
    rule_names = np.array([get_rule_name(rule) for rule in root])
    rule_conditions = np.array([get_tag_elements(rule, "condition") for rule in root])
    rule_priorities = np.array([get_tag_elements(rule, "priority") for rule in root])
    rule_confidences = np.array([get_tag_elements(rule, "confidence") for rule in root])
    rule_actions = np.array([get_tag_elements(rule, "action") for rule in root])
    rule_priorities = rule_priorities.astype(float)
    rule_confidences = rule_confidences.astype(float)

    print_rules(rule_names, rule_conditions, rule_priorities, 
                rule_confidences, rule_actions)
    
    ''' getting parameter '''
    param_tree = ET.parse(param_file)
    param_root = param_tree.getroot()


    ''' applying for specific enviroment '''
    OPENCV_obstacle = get_parameter_value(param_root, "OBSTACLE_FIXED")
    LiDAR_distance = 3.2
    CNN_sign_recognition = get_parameter_value(param_root, "NONE")

    # get all rules matching specific situation
    rule_condition_result = apply_specific_situation(obstacle = OPENCV_obstacle,
                    distance = LiDAR_distance, 
                    CNN_sign_recognition = CNN_sign_recognition, 
                    rule_conditions = rule_conditions)
    print ("rule_maching result [condition]:", rule_condition_result)
    print ("rule_maching result [priorities]:", rule_priorities)
    print ("rule_maching result [confidences]:", rule_confidences)

    rule_idx = choose_rule(rule_condition_result, rule_priorities)
    # print chosen rule
    print_rule(rule_idx, rule_names, rule_conditions, rule_priorities, 
                    rule_confidences, rule_actions)
    
if __name__ == '__main__':
    main(rules_file, param_file)