@echo off

del C:\dev\tools\tomcat8\webapps\tethysui.war
mvn clean package 

dir 
copy C:\dev\wmmc\tethys\webapp\docker\tethysui.war C:\dev\tools\tomcat8\webapps\


