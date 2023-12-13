# Inserts dummy data into the database for testing purposes.
import sqlite3
import random
from datetime import datetime, timedelta

db = sqlite3.connect('database.db')
c = db.cursor()

users = [
    {'first_name': "Kendall", 	'last_name': "O'Hara", 		'email': "Jerel_Braun@hotmail.com", 			'password': "Concrete"},
    {'first_name': "Arvid", 	'last_name': "Walker", 		'email': "Jamie85@gmail.com", 					'password': "Mobility"},
    {'first_name': "Makenzie", 	'last_name': "Kassulke", 	'email': "Bria87@gmail.com", 					'password': "Tasty"},
    {'first_name': "Jarret", 	'last_name': "Deckow", 		'email': "Declan.Murphy8@gmail.com", 			'password': "infomediaries"},
    {'first_name': "Carroll", 	'last_name': "Zulauf", 		'email': "Weldon.Jaskolski82@hotmail.com",		'password': "Pants"},
    {'first_name': "Victor", 	'last_name': "Bins", 		'email': "Drake_Hessel51@gmail.com", 			'password': "maroon"},
    {'first_name': "Margaretta",'last_name': "Schmidt", 	'email': "Brice_Ryan@gmail.com", 				'password': "payment"},
    {'first_name': "Javier", 	'last_name': "Buckridge", 	'email': "Lydia_Skiles37@yahoo.com", 			'password': "Account"},
    {'first_name': "Cheyanne", 	'last_name': "Gibson", 		'email': "Fay.Ankunding@yahoo.com", 			'password': "Sausages"},
    {'first_name': "Abdullah", 	'last_name': "Abernathy", 	'email': "Makenna90@gmail.com", 				'password': "extensible"},
    {'first_name': "Mara", 		'last_name': "Lindgren", 	'email': "Alejandra.Smith@gmail.com", 			'password': "Colorado"},
    {'first_name': "Erick", 	'last_name': "Dare", 		'email': "Destany_Schamberger26@hotmail.com",	'password': "Account"}
]
sql_user_tuples = [(x["first_name"], x["last_name"], x["email"], x["password"]) for x in users]
c.executemany('INSERT INTO users (first_name, last_name, email, password) VALUES (?,?,?,?)', sql_user_tuples)
db.commit()


books = [
{'title': "To Kill a Mockingbird" 				,		'description': "A classic novel that explores racial injustice and moral growth through the eyes of a young girl named Scout Finch in the American South during the 1930s." 																	,	'image_location': ""},
{'title': "1984"								,		'description': "A dystopian novel set in a totalitarian society where the government, led by the ominous Big Brother, controls every aspect of people's lives and even their thoughts."															,	'image_location': ""},
{'title': "The Great Gatsby"					,		'description': "A tale of wealth, love, and the American Dream set during the Roaring Twenties, narrated by Nick Carraway, who becomes entangled in the lives of the enigmatic Jay Gatsby and the beautiful Daisy Buchanan."					,	'image_location': ""},
{'title': "One Hundred Years of Solitude"		,		'description': "A magical realist masterpiece that spans generations in the Buendía family, weaving a tale of love, politics, and the supernatural in a fictional town called Macondo."															,	'image_location': ""},
{'title': "The Catcher in the Rye"				,		'description': "Narrated by the teenage Holden Caulfield, this novel explores themes of adolescence, alienation, and the search for authenticity in a world he perceives as phony."																,	'image_location': ""},
{'title': "Pride and Prejudice"					,		'description': "A classic novel by Jane Austen that satirizes the social norms and class structure of early 19th-century England, while telling the love story of Elizabeth Bennet and Mr. Darcy." 												,	'image_location': ""},
{'title': "The Lord of the Rings"				,		'description': "J.R.R. Tolkien's epic fantasy trilogy follows the quest to destroy the One Ring, exploring themes of friendship, heroism, and the battle between good and evil in the land of Middle-earth." 									,	'image_location': "lotr.jpg"},
{'title': "The Chronicles of Narnia"			,		'description': "C.S. Lewis's beloved series of seven fantasy novels that take readers on magical journeys to the enchanted land of Narnia, where they encounter talking animals, mythical creatures, and epic battles between good and evil."	, 	'image_location': ""},
{'title': "Brave New World"						,		'description': "Aldous Huxley's dystopian novel envisions a future society where technological advancements and conditioning control every aspect of human life, exploring the consequences of a highly controlled, pleasure-driven world." 	,	'image_location': ""},
{'title': "The Hitchhiker's Guide to the Galaxy",		'description': "A humorous science fiction series by Douglas Adams that follows the misadventures of Arthur Dent, an unwitting Earthling, as he travels through space with an eclectic group of companions using the titular guidebook."		,	'image_location': ""}
]


sql_book_tuples = [(x["title"], x["description"], x["image_location"]) for x in books]
c.executemany('INSERT INTO books (title, description, image_location) VALUES (?,?,?)', sql_book_tuples)
db.commit()




# Generate 10 insert statements
for i in range(8):
    user_id = random.randint(1, 10)  # Assuming you have users with IDs 1 to 10
    start = datetime.now() - timedelta(days=random.randint(1, 14))  # Current time
    end = start + timedelta(days=random.randint(1, 14))  # End time is 1 to 14 days from now

    # SQL insert statement
    sql = f"INSERT INTO book_loans (book_id, user_id, start, end) VALUES ({i}, {user_id}, '{start}', '{end}');"
    c.execute(sql)
    
    print(sql)
db.commit()