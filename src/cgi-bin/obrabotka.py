# #!/usr/bin/env python3

# import cgi 

# our_form = cgi.FieldStorage()

# in_name = our_form.getfirst("in_name", "не задано")
# in_comment = our_form.getfirst("in_comment", "не задано")


# print("Content-type: text/html")
# print()
# print(in_name)
# print(in_comment)


#!/usr/bin/python3
 
# Импорт модулей для обработки CGI
import cgi, cgitb
 
# Создание экземпляра FieldStorage
form = cgi.FieldStorage()
 
# Получение данных от полей формы
name = form.getvalue('name')
surname = form.getvalue('surname')
info = form.getvalue('info')
 
# Вывод HTTP заголовка
print ('Content-type: text/html\r\n\r\n')
 
# Вывод HTML кода с полученными данными
print ('<html>')
print ('<head>')
print ('<title>ZaLinux.ru: An example of running Python on a web server</title>')
print ('</head>')
print ('<body>')
 
print ('<em>Python script reports: </em>', '<br /><br />')
print ('<b>Name: </b>', name, '<br />')
print ('<b>Surname: </b>', surname, '<br />')
print ('<b>Extra information: </b>', info, '<br />')
 
print ('</body>')
print ('</html>')