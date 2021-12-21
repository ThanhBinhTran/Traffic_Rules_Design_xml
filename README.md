# Traffic rules design for robotic in ROS
This mini project shows to how to design traffic rules in xacro (xml macro) format. It helps users easy to define traffic rule without concern the programming language

##### To generate paramenter.xml file (run in ROS envirment):
```
xacro parameter.xacro -o parameter.xml
```
##### To generate rules.xml file (run in ROS envirment):
```
xacro rules.xacro -o rules.xml
```
##### play with generating rule
```
python rulesUnderstanding.py 
```

##### to update, modify, alter the rules edit rules.xacro
