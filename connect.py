import math
import pygame
import numpy
import random
import sys


GRACZ = 0
LOOLEK = 1

BLUE = (20,20,200)
RED = (200,20,20)
YELLOW = (240,240,0)
GREEN =(20,200,20)
wys_planszy = 6
szer_planszy = 7

GRACZ_PIONEK = 1
LOOLEK_PIONEK = 2
PUSTY = 0
CZTERY = 4

def rys_podst_planszy():
	plansza = numpy.zeros((wys_planszy,szer_planszy))
	return plansza
def wyswietl_plansza(plansza):
	print(numpy.flip(plansza, 0))


def wolne_miejsce(plansza, kol):
	return plansza[wys_planszy-1][kol] == 0

def otwieraj_rzad(plansza, kol):
	for r in range(wys_planszy):
		if plansza[r][kol] == 0:
			return r
def ruch(plansza, rzad, kol, pionek):
	plansza[rzad][kol] = pionek


def podliczanie_wyniku(pole, pionek):
	wynik = 0
	opp_pionek = GRACZ_PIONEK
	if pionek == GRACZ_PIONEK:
		opp_pionek = LOOLEK_PIONEK

	if pole.count(pionek) == 4:
		wynik += 1000
	elif pole.count(pionek) == 3 and pole.count(PUSTY) == 1:
		wynik += 5
	elif pole.count(pionek) == 2 and pole.count(PUSTY) == 2:
		wynik += 2

	if pole.count(opp_pionek) == 3 and pole.count(PUSTY) == 1:
		wynik -= 4

	return wynik
def sprawdz_zwyc(plansza, pionek):
	# przekontne
	for c in range(szer_planszy-3):
		for r in range(3, wys_planszy):
			if plansza[r][c] == pionek and plansza[r-1][c+1] == pionek and plansza[r-2][c+2] == pionek and plansza[r-3][c+3] == pionek:
				return True
	for c in range(szer_planszy-3):
		for r in range(wys_planszy-3):
			if plansza[r][c] == pionek and plansza[r+1][c+1] == pionek and plansza[r+2][c+2] == pionek and plansza[r+3][c+3] == pionek:
				return True	
	# poziomo
	for c in range(szer_planszy-3):
		for r in range(wys_planszy):
			if plansza[r][c] == pionek and plansza[r][c+1] == pionek and plansza[r][c+2] == pionek and plansza[r][c+3] == pionek:
				return True

	# pionowo
	for c in range(szer_planszy):
		for r in range(wys_planszy-3):
			if plansza[r][c] == pionek and plansza[r+1][c] == pionek and plansza[r+2][c] == pionek and plansza[r+3][c] == pionek:
				return True


def pozycjonowanie(plansza, pionek):
	wynik = 0

	
	center_array = [int(i) for i in list(plansza[:, szer_planszy//2])]
	center_count = center_array.count(pionek)
	wynik += center_count * 3

	
	for r in range(wys_planszy):
		rzad_array = [int(i) for i in list(plansza[r,:])]
		for c in range(szer_planszy-3):
			pole = rzad_array[c:c+CZTERY]
			wynik += podliczanie_wyniku(pole, pionek)

	for c in range(szer_planszy):
		kol_array = [int(i) for i in list(plansza[:,c])]
		for r in range(wys_planszy-3):
			pole = kol_array[r:r+CZTERY]
			wynik += podliczanie_wyniku(pole, pionek)

	for r in range(wys_planszy-3):
		for c in range(szer_planszy-3):
			pole = [plansza[r+i][c+i] for i in range(CZTERY)]
			wynik += podliczanie_wyniku(pole, pionek)

	for r in range(wys_planszy-3):
		for c in range(szer_planszy-3):
			pole = [plansza[r+3-i][c+i] for i in range(CZTERY)]
			wynik += podliczanie_wyniku(pole, pionek)

	return wynik



def minimax(plansza, glab, alfa, beta, maksymalizacja): #Algorytm MiniMax
	wolne_miejsca = sprawdz_wolne_miejsca(plansza)
	czy_koniec = koniec_gry(plansza)
	if glab == 0 or czy_koniec:
		if czy_koniec:
			if sprawdz_zwyc(plansza, LOOLEK_PIONEK):
				return (None, 99999)
			elif sprawdz_zwyc(plansza, GRACZ_PIONEK):
				return (None, -99999)
			else: 
				return (None, 0)
		else: 
			return (None, pozycjonowanie(plansza, LOOLEK_PIONEK))
	if maksymalizacja:
		wart = -math.inf
		kolumna = random.choice(wolne_miejsca)
		for kol in wolne_miejsca:
			rzad = otwieraj_rzad(plansza, kol)
			b_copy = plansza.copy()
			ruch(b_copy, rzad, kol, LOOLEK_PIONEK)
			nowy_wynik = minimax(b_copy, glab-1, alfa, beta, False)[1]
			if nowy_wynik > wart:
				wart = nowy_wynik
				kolumna = kol
			alfa = max(alfa, wart)
			if alfa >= beta:
				break
		return kolumna, wart

	else: 
		wart = math.inf
		kolumna = random.choice(wolne_miejsca)
		for kol in wolne_miejsca:
			rzad = otwieraj_rzad(plansza, kol)
			b_copy = plansza.copy()
			ruch(b_copy, rzad, kol, GRACZ_PIONEK)
			nowy_wynik = minimax(b_copy, glab-1, alfa, beta, True)[1]
			if nowy_wynik < wart:
				wart = nowy_wynik
				kolumna = kol
			beta = min(beta, wart)
			if alfa >= beta:
				break
		return kolumna, wart

def sprawdz_wolne_miejsca(plansza):
	wolne_miejsca = []
	for kol in range(szer_planszy):
		if wolne_miejsce(plansza, kol):
			wolne_miejsca.append(kol)
	return wolne_miejsca

def koniec_gry(plansza):
	return sprawdz_zwyc(plansza, GRACZ_PIONEK) or sprawdz_zwyc(plansza, LOOLEK_PIONEK) or len(sprawdz_wolne_miejsca(plansza)) == 0

def rys_planszy(plansza): #rysowanie planszy wykorzystując bibliotekę pygame
	for c in range(szer_planszy):
		for r in range(wys_planszy):
			pygame.draw.rect(screen, GREEN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(szer_planszy):
		for r in range(wys_planszy):		
			if plansza[r][c] == GRACZ_PIONEK:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif plansza[r][c] == LOOLEK_PIONEK: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
#Inicjacja gry
plansza = rys_podst_planszy()
wyswietl_plansza(plansza)
koniec = False

pygame.init()

SQUARESIZE = 100

width = szer_planszy * SQUARESIZE
height = (wys_planszy+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
rys_planszy(plansza)
pygame.display.update()

myfont = pygame.font.SysFont("calibri", 80)

tura = random.randint(GRACZ, LOOLEK)
#Pętla gry
while not koniec:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLUE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if tura == GRACZ:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLUE, (0,0, width, SQUARESIZE))

			if tura == GRACZ:
				posx = event.pos[0]
				kol = int(math.floor(posx/SQUARESIZE))

				if wolne_miejsce(plansza, kol):
					rzad = otwieraj_rzad(plansza, kol)
					ruch(plansza, rzad, kol, GRACZ_PIONEK)

					if sprawdz_zwyc(plansza, GRACZ_PIONEK):
						label = myfont.render("Rasa ludzka wygrala", 1, RED)
						screen.blit(label, (40,10))
						koniec = True

					tura += 1
					tura = tura % 2

					wyswietl_plansza(plansza)
					rys_planszy(plansza)


	if tura == LOOLEK and not koniec:				


		kol, minimax_wynik = minimax(plansza, 5, -math.inf, math.inf, True)

		if wolne_miejsce(plansza, kol):
			pygame.time.wait(1000)
			rzad = otwieraj_rzad(plansza, kol)
			ruch(plansza, rzad, kol, LOOLEK_PIONEK)

			if sprawdz_zwyc(plansza, LOOLEK_PIONEK):
				label = myfont.render("Mis Loolek wygral", 1, YELLOW)
				screen.blit(label, (40,10))
				koniec = True

			wyswietl_plansza(plansza)
			rys_planszy(plansza)

			tura += 1
			tura = tura % 2

	if koniec:
		pygame.time.wait(10000)