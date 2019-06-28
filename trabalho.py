import sys
import copy
class UH:
	def __init__(self, entrada):
		aux = entrada.split("000")
		maquina = aux[1]
		palavra = aux[2] #W
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

				#Euristica do snapshot - explicação dentro das funções
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
						if(indiceSimbolo > len(self.fita3)-1 and not encontrouLoop):
							'''
							Aproveitando da ideia de se acrescentar um B (111) no final da fita quando o indice do símbolo a ser lido é maior que o tamanho da fita,
							antes de acrescentar um BBB podemos verificar se a transição é do tipo "Lê B, continua no mesmo estado e vai pra direita", caso seja, sabemos que temos um loop (é uma heurística)
							'''
							encontrouLoop = self.verificarLoopBFimFita(transicao)

				if(indiceSimbolo > len(self.fita3)-1): #Se o índice do símbolo (posição de um 'caractere' da palavra de entrada) for maior que a quantidade de símbolos da entrada nós adicionamos um B no final da fita, simulando uma fita com B infinitos
					self.fita3.append("111")
		if(not encontrouLoop or maquinaEhFinita):
			print("A máquina termina a execução corretamente")
		else:
			print("A máquina entrou em loop")

	def verificarSeEhFinita(self): #Heurística - Ao verificar que a máquina não tem loop de leitura de B, não leitura de B após o símbolo inicial e não tem transição para a esquerda, sabemos que ela é finita e não precisamos analisar
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


	def adicionarSnapshot(self, estadoAtual, indiceSimbolo, fita3): #Um snapshot é uma tupla que indica o estado atual, o índice da cabeça de leitura e uma cópia do estado atual da fita
		self.arrSnapshots.append((estadoAtual, indiceSimbolo, copy.copy(fita3)))

	def buscarSnapshot(self, estadoAtual, indiceSimbolo, fita3): 
		'''
		Quando encontramos um snapshot armazenado igual ao snapshot passado por parâmetro (da leitura atual),
	 	isso significa que a máquina de turing já passou por aquela transição, lendo exatamente aquele símbolo (garantido ao se comparar o índice do simbolo e não o símbolo e si) e a fita não se modificou,
	 	logo sabemos que a máquina entrou em loop
	 	'''
		for snapshot in self.arrSnapshots:
			if(snapshot == (estadoAtual, indiceSimbolo, fita3)):
				return True
		return False
			
				
class Transicao: #Classe auxiliar para transformar uma string de transição em um objeto, visando deixar o código mais claro
	def __init__(self, stringTransicao):
		aux = stringTransicao.split("0")
		self.estadoAtual = aux[0]
		self.leitura = aux[1]
		self.proximoEstado = aux[2]
		self.escrita = aux[3]
		self.direcao = aux[4]

def main():
	entrada = ""
	if(len(sys.argv) > 1):
		entrada = sys.argv[1]
	else:
		print("É necessário passar um argumento com a configuração da máquina e a palavra rm(w)")
	objUH = UH(entrada)
	objUH.executar()

if __name__ == '__main__':
	main()