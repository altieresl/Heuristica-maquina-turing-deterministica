import sys
import copy
class UH:
	def __init__(self, entrada):
		aux = entrada.split("000")
		maquina = aux[1]
		palavra = aux[2]
		self.fita1 = maquina.split("00") #Configuração da fita
		self.fita2 = "1" #Estado atual
		self.fita3 = palavra.split("0") #Palavra

		self.arrSnapshots = []

	def executar(self):
		encontradaTransicao = True
		indiceSimbolo = 0
		simboloAtual = ""
		encontrouLoop = False
		maquinaEhFinita = self.verificarSeEhFinita()

		if(not maquinaEhFinita):
			while encontradaTransicao and not (encontrouLoop):
				simboloAtual = self.fita3[indiceSimbolo]
				estadoAtual = self.fita2

				#Euristica do snapshot
				encontrouLoop = self.buscarSnapshot(estadoAtual, indiceSimbolo, self.fita3)
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
							encontrouLoop = self.verificarLoopBFimFita(transicao)

				if(indiceSimbolo > len(self.fita3)-1): #Se o índice do símbolo (posição de um 'caractere' da palavra de entrada) for maior que a quantidade de símbolos da entrada nós adicionamos um B no final da fita, simulando uma fita com B infinitos
					self.fita3.append("111")
			if(encontrouLoop):
				print("A máquina entrou em loop")
	def verificarSeEhFinita(self):
		fita = self.fita1
		semBAlemEstadoInicial = True
		semTransicaoParaEsquerda = True
		semloopBEstadoInicial = True
		for stringTransicao in fita:
			transicao = Transicao(stringTransicao)
			if(transicao.leitura == "111" and transicao.estadoAtual != "1"): #Busca estado com transição lendo B(111) que não é no estado atual(1)
				semBAlemEstadoInicial = False
			if(transicao.leitura == "111" and transicao.estadoAtual == transicao.proximoEstado):
				semloopBEstadoInicial = False
			if(transicao.direcao == "11"):
				semTransicaoParaEsquerda = False

		if(semBAlemEstadoInicial and semTransicaoParaEsquerda and semloopBEstadoInicial):
			print("A máquina pára")
		return (semBAlemEstadoInicial and semTransicaoParaEsquerda and semloopBEstadoInicial)

	def verificarLoopBFimFita(self, transicao):
		return (transicao.leitura == "111" and transicao.estadoAtual == transicao.proximoEstado and transicao.direcao == "1")


	def adicionarSnapshot(self, estadoAtual, indiceSimbolo, fita3):
		self.arrSnapshots.append((estadoAtual, indiceSimbolo, copy.copy(fita3)))

	def buscarSnapshot(self, estadoAtual, indiceSimbolo, fita3):
		for snapshot in self.arrSnapshots:
			if(snapshot == (estadoAtual, indiceSimbolo, fita3)):
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

	entrada2 = "0001011101101110100110101110101001110111011011101000111010111"
	entrada2 = "000101110110111010011010111010100110110111101101001110110111011010011101110111110111011001111010111101010011110111011111011101100011101011011011000"
	# entrada2 = "000"+"1011101101110100"+"11010111010100"+"111011011011011"+"000"+"11101011"
	# entrada2 = "000"+"1011101101110100"+"11010111010100"+"11101101111011101"+"000"+"11101"
	entrada2 = "000"+"1011101011101"+"000"+"111"

	entrada = ""
	if(len(sys.argv) > 1):
		entrada = sys.argv[1]
	else:
		print("É necessário passar um argumento com a configuração da máquina e a palavra rm(w)")
	#Entrada = 11101011011011000
	objUH = UH(entrada2)
	objUH.executar()

if __name__ == '__main__':
	main()