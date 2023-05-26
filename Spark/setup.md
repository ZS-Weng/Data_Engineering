# Local Setup for PySpark without VM on Windows 11

## 

1. Install JDK 8 or JDK 11

- Download JDK https://jdk.java.net/
- Unzip files
- copy jdk-11 (entire folder) to C:\Program Files\Java (recommended) or in other location

- Set Home variables (From cmd)
setx JAVA_HOME "C:\Program Files\Java\jdk-11"
- Set Path Variable (From cmd)
setx PATH "%PATH%;%JAVA_HOME%\bin"
- Double check Java is installed correctly with command "java -version"

2. Install Python 3.6 or higher

- Install python from the python website
- Type "python" or "python --version" in command prompt to check on version

3. Install Hadoop WinUtils

- Search for Hadoop Winutils on Google with a GitHub page link (Remember to go to the new winsutil)
- There will be instructions 
- Copy the latest version to the designated location
- setx HADOOP_HOME=<your local hadoop-ver folder>
- setx PATH=%PATH%;%HADOOP_HOME%\bin

4. Spark Binaries

- Download the latest Spark version
- Uncompress the files and copy directory into a permanent location
- setx SPARK_HOME=<your local spark folder>
- Put Path Environment using Windows UI <Spark Home Directory\bin>

5. Checking Installation 

- Run pyspark on cmd

6. Additional Environment Variables

- setx PYTHONPATH <Python Folder within Spark Folder>
- setx PYTHONPATH <"py4j zip file from spark>python>lib>py4j zip file">

7. Python IDE 