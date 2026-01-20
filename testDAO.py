from database.dao import DAO
num= 5
s= DAO.get_artisti_n_maggiore_album(5)
z= DAO.get_all_edges(num, s)

min = float(3.2)

f= DAO.get_artisti_canzone_min(min, num)

print(f)
print(len(s))