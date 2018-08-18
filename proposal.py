#!/usr/bin/env python
# *- coding: utf8 -*
# Title:  Problema de proposición-aceptación.
# Author: Daniel Martínez Caballero.

import random
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# -- PARÁMETROS PARA MODIFICAR -- #

N = 20 # Número de elementos en cada subconjunto.
NP = 10 # Número de preferencias.
LOOPS = 1000 # Número de repeticiones del proceso.
LOG = False # Habilita el el modo debug.

# ------------------------------ #

LH = [] # Lista usada en el histograma para el subconjunto H.
LM = [] # Lista usada en el histograma para el subconjunto M.

def log(text):
	if LOG:
		print text

# Para cada N del subconjunto M y H se asignan n referencias. 
# Cada referencia corresponderá de forma prioritaria al índice del otro subconjunto.
# Ejemplo -> H(1): {4, 0, 2} -> El proponedor número 1 prefiere el ofertante número 4 como prioridad máxima.
# 	prioridad intermedia a nadie y prioridad más baja el ofertante número 2.
def preferences():
	log('-> PREFERENCIAS H')
	for i in range(N):
		# Preferencias H
		rand = [y for y in range(N)]
		random.shuffle(rand)
		rand = rand[:NP]
		H[i] = rand
		log('	H(' + str(i+1) + '): ' + str(H[i]))
		
		# Preferencias M
		rand = [y for y in range(N)]
		random.shuffle(rand)
		rand = rand[:NP]
		M[i] = rand
	log('-> PRERFERENCIAS M')
	if LOG:
		for i in range(N):
			log('	M(' + str(i+1) + '): ' + str(M[i]))

# Ronda de propuestas.
#  - En orden, los elementos del grupo H informarán a sus prioridades del grupo M su interés. 
#  - Cada M(i) rechazará en caso de no encontrarse el H(j) en su lista de prioridades. En caso contrario, lo preseleccionará.
def rounds():
	log('-> RONDAS')
	
	MP = [[] for y in range(N)] # Propuestas recibidas al grupo M.

	for j in range(NP):
		for i in range(N):
			if ( H[i][j] != 0 ):
				mindex = H[i][j]
				propose = '	Propuesta: H(' + str(i+1) + ') -> M(' + str(mindex) + ')'
				if i+1 in M[mindex-1]:
					log(propose + ' | ;)')
					MP[mindex-1].append(i+1)
				else:
					log(propose + ' |  X Rechazada')
	breaker = False
	for i in range(N):
		for j in range(NP):
			for x in range(len(MP[i])):
				if (MP[i][x] == M[i][j]) and (MP[i][x] not in PAIR):
					PAIR[i] = MP[i][x]
					breaker = True
					break
			if breaker:
				breaker = False
				break
# Elección de pareja.
# Cada M(i) escogerá la mejor propuesta que tenga basándose en su lista de preferencias.
def picks():
	log('-> RESULTADO')
	ptsH = 0
	ptsM = 0
	for i in range(N):
		if PAIR[i] != 0:
			for j in range(NP):
				if M[i][j] == PAIR[i]:
					ptsM = (ptsM + j + 1)
					log('	Elección: H(' + str(PAIR[i]) + ') - M(' + str(i +1) + ') | :D HAPPY END ')
					for x in range(NP):
						if H[PAIR[i]-1][x] == (i+1):
							ptsH = (ptsH + x + 1)

	log('\n	Puntos H: ' + str(ptsH / float(NP)))
	log('	Puntos M: ' + str(ptsM / float(NP)))
	LH.append(np.round(ptsH / float(NP), 3))
	LM.append(np.round(ptsM / float(NP), 3))



# Histograma.
def drawGraph():
	num_bins = 100
	fig, ax = plt.subplots()

	ax.hist(LH, num_bins, facecolor='red', alpha=0.6)
	n, bins, patches = ax.hist(LM, num_bins, facecolor='blue', alpha=0.6)
	plt.xlabel('Puntuacion')
	plt.ylabel('Frecuencia')
	plt.title(r'Cancaneo simulator: N=' + str(N) + '(' + str(NP)  + ') loops=' + str(LOOPS)  )
	plt.subplots_adjust(left=0.15)
	h_patch = mpatches.Patch(color='red', label='H')
	m_patch = mpatches.Patch(color='blue', label='M')
	plt.legend(handles=[h_patch, m_patch])
	plt.grid(True)
	plt.show()

print '\n-- CANCANEO SIMULATOR N=' + str(N) + '(' + str(NP) +  ') loops=' + str(LOOPS) +  '  --- \n'


# main - Simulación

for i in range(LOOPS):
	print 'Simulación-' + str(i)
	# H: Preferencias de los que proponen. M: Preferencias de los que seleccionan.
	H    = [[-1 for x in range(NP)] for y in range(N)]
	M    = [[-1 for x in range(NP)] for y in range(N)]
	# Resultado de parejas finales
	PAIR = [0 for x in range(N)]
	preferences()
	rounds()
	picks()
	


drawGraph()

