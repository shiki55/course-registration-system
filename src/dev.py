
from regie_pkg.MySQLConnect import MySQLConnect

connect = MySQLConnect()
print(connect.execute_query(query="SELECT * FROM student"))