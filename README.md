# Traffic rules design for robotic in ROS
This mini-project shows how to design traffic rules in xacro (XML macro) format. It helps users easy to define/update traffic rules without altering executable program.
* edit rules.xacro file to add, delete, alter the rules 

##### To generate paramenter.xml file (run in ROS envirment):
```
xacro parameter.xacro -o parameter.xml
```
##### To generate rules.xml file (run in ROS envirment):
```
xacro rules.xacro -o rules.xml
```
##### play with generated rule
```
python rulesUnderstanding.py 
```
