import os


movies = os.listdir(os.getcwd())


wiki = """1. Miki i foczka (ang. Mickey and the Seal, 1948)
2. Przestarszone duchy (ang. Lomesome Ghosts, 1937)
3. Zimowe zapasy (ang.Winter Storage, 1949)
4. Jak podłączyć kino domowe (ang.How to Hook Up Your Home Theater, 2007)
5. Cenne zapasy (ang. Food for Feudin, 1950)
6. Mickey i Pluto w pociągu (ang. Mr. Mouse Takes a Trip, 1940)
7. Konserwatorzy zegara (ang. Clock Cleaners, 1937)
8. Wcześniej do łóżka położę się (ang. Early to Bed, 1941)
9. Sztuka jazdy na nartach (ang. The Art of Skiing, 1941)
10. Pluto i suseł (ang. Pluto and the Gopher, 1950)
11. Pechowa randka (ang. Mickey's Delayed Date, 1947)
12. Wielorybnicy (ang. The Whalers, 1938)
13. Donald kucharzem (ang. Chef Donald, 1941)
14. Jak grać w baseball (ang. How to Play Baseball, 1942)
15. Sweter dla Pluta (ang. Plutoˈs Sweater, 1949)
16. Myszka Miki w Australii (ang. Mickey Down Under, 1948)
17. Wakacje na Hawajach (ang. Hawaiian Holiday, 1937)
18. Klakson z przyczepą (ang. Trailer Horn, 1950)
19. Jak pływać (ang. How to Swim, 1942)
20. Paczuszka niespodzianka dla psa Pluto (ang. Pluto's Surprise Package, 1949)
21. Traperzy z północy (ang. Polar Trappers, 1938)
22. Pies ratowniczy (ang. Rescue Dog, 1947)
23. Podwójne kozłowanie (ang. Double Dribble, 1946)
24. Po drugiej stronie lustra (ang. Thru the Mirror, 1936)
25. Miki magikiem (ang. Magician Mickey, 1937)
26. Budowanie łodzi (ang. Boat Builders, 1938)
27. Kłopoty z oponą (ang. Donald's Tire Trouble, 1943)
28. Rabuś kości (ang. Bone Bandit, 1948)
29. Proste rzeczy (ang. The Simple Things, 1953)
30. Sprawunek Pluta (ang. Pluto's Purchase, 1948)
31. Piknik na plaży (ang. Beach Picnic, 1939)
32. W przyczepie Mikiego (ang. Mickey's Trailer, 1938)
33. Papuga Myszki Miki (ang. Mickey's Parrot, 1938)
34. Pluto bohater (ang. The Society Dog Show, 1939)
35. Jak grać w futbol amerykański (ang. How to Play Football, 1944)
36. Akcja ratunkowa na holowniku Mikiego (ang. Tugboat Mickey, 1940)
37. Trąbka powietrzna (ang. The Little Whirlwind, 1941)
38. Pies pocztowy (ang. Mail Dog, 1947)
39. Na ślizgawce (ang. On Ice, 1935)
40. Koncert podwórkowy (ang. The Band Concert, 1935)
41. Chip i Dale (ang. Chip 'an Dale, 1948)
42. Miki i jego drużyna polo (ang. Mickey's Polo Team, 1936)
43. Mistrz hokeja (ang. The Hokey Champ, 1939)
44. Jak łowić ryby (ang. How to Fish, 1942)
45. Przyjęcie urodzinowe Pluta (ang. Pluto's Party, 1952)
46. Rywal Mikiego (ang. Mickey's Rival, 1936)
47. Łowcy łosi (ang. Moose Hunters, 1937)
48. Pan Kaczor Donald ma randkę (ang. Mr. Duck Steps Out, 1940)
49. Mistrz olimpijski (ang. The Olympic Champ, 1942)
50. Pies do golfa (ang. Canine Caddy, 1941)
51. Dzielny mały krawczyk (ang. Brave Little Tailor, 1938)
52. Gra w golfa (ang. Donald's Golf Game, 1938)
53. Morscy harcerze (ang. Sea Scouts, 1939)
54. Mecz tenisa (ang. Tennis Racquet, 1949)
55. Nie ten wymiar (ang. Out of Scale, 1951)""".split('\n')



for index, movie in enumerate(movies, 1):
	if movie=='movies_names.py':
		continue
	name = (movie.split(' - ')[1].split('.')[0])
	print(index, name)




