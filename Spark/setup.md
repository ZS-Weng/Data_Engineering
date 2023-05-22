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

2. Install Python 3.6 or higher

3. Install Hadoop WinUtils 

4. Spark Binaries

5. Environment Variables 

5. Python IDE 