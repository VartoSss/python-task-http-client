from HTTPClient import HTTPClient

client = HTTPClient("www.urfu.ru", "/ru/", "GET",
                    "", {}, 3)
a = client.run()

with open('text.txt', 'w') as file:
    file.write(a)
