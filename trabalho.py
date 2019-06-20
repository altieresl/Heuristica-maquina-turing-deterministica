import copy
class MTU:
	def __init__(self, entrada):
		aux = entrada.split("000")
		maquina = aux[1]
		palavra = aux[2]
		self.fita1 = maquina.split("00") #Configurãção da fita
		self.fita2 = "1" #Estado atual
		self.fita3 = palavra.split("0") #Palavra

		self.arrSnapshots = []

	def executar(self):
		encontradaTransicao = True
		indiceSimbolo = 0
		simboloAtual = ""
		encontrouLoop = False

		while encontradaTransicao and not encontrouLoop:
			simboloAtual = self.fita3[indiceSimbolo]
			estadoAtual = self.fita2
			encontrouLoop = self.buscarSnapshot(estadoAtual, indiceSimbolo, self.fita3)
			print("loop")
			self.adicionarSnapshot(estadoAtual, indiceSimbolo, self.fita3)
			encontradaTransicao = False
			for i in range(len(self.fita1)):
				transicao = Transicao(self.fita1[i])
				if(transicao.estadoAtual == estadoAtual and transicao.leitura == simboloAtual):
					encontradaTransicao = True
					self.fita3[indiceSimbolo] = transicao.escrita
					self.fita2 = transicao.proximoEstado
					indiceSimbolo = ( indiceSimbolo+1 if transicao.direcao == "1" else indiceSimbolo - 1)
			if(indiceSimbolo > len(self.fita3)-1):
				self.fita3.append("111")
		# print(estadoAtual, "Fim da execução")

	def adicionarSnapshot(self, estadoAtual, indiceSimbolo, fita3):
		self.arrSnapshots.append((estadoAtual, indiceSimbolo, copy.copy(fita3)))

	def buscarSnapshot(self, estadoAtual, indiceSimbolo, fita3):
		for snapshot in self.arrSnapshots:
			if(snapshot == (estadoAtual, indiceSimbolo, fita3)):
				print("Entrou em loop")
				return True
		return False
			
				
class Transicao:
	def __init__(self, stringTransicao):
		aux = stringTransicao.split("0")
		self.estadoAtual = aux[0]
		self.leitura = aux[1]
		self.proximoEstado = aux[2]
		self.escrita = aux[3]
		self.direcao = aux[4]

def main():
	'''
	000 = começo
	000 = fim
	R = 1
	L = 11
	primeira parte da fita = estado atual
	segunda 			=    simbolo atual
	terceira			=    proximo estado
	quarta 				=    escrita
	quinta				=    direção
	'''

	# entrada = "0001011101101110100110101110101001110111011011101000111010111"
	# entrada = "000101110110111010011010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"
	# entrada = "00010111011011101001101011101010011101011010110001110101"
	entrada = "00010111011011101001101011101010011101110111101110100011101"
	#Entrada = 11101011011011000
	objMtu = MTU(entrada)
	objMtu.executar()

if __name__ == '__main__':
	main()