# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import os
import io
import re

# Passo anterior -- Conversão dos PDFs em TXTs:
# => Rodar os comandos dentro da pasta que contém os PDFs, depois mover os .txt gerados para a pasta txt
# $ ls | while read f; do pdftotext "$f" -enc UTF-8; done
# $ mv *.txt ../txt/
# => Deu vários Syntax Warning: Invalid Font Weight -- mas não tratei nada!

# Removendo os espaços dos nomes dos arquivos
# $ ls | while read file; do mv "$file" "$(echo $file | sed 's/ /_/g')"; done

# Recebe um .txt (que era um .pdf e foi convertido automaticamente com um pdftotext) como entrada
# e gera um .json como saída com as edições separadas em objetos




# Processando 1 arquivo com esse script
# $ python3 scripts/limpeza.py txt/Sorria_01_mar_abr_de_2008.txt 

# Fazendo consultas ao arquivo gerado como saída
# $ cat json/Sorria_02_maio_junho_de_2008.json | jq ".[].title"


# TO DO
# - confirmar se o .json está com todas as informações das seções do PDF 



def comeco_secao(linha, secoes):
	return linha in secoes
	
def eh_fim_processamento(linha):
	return re.search("^.?Seja um sócio-mantenedor do GRAACC",linha)


def excluir(linha):
	if (len(linha) == 0):
		return True
	if linha.find("Sorria_") > 0:
		return True
	if linha.find("Anúncio") > 0:
		return True
	if linha.find("Arquivo pessoal") > 0:
		return True
	if re.search("^\d+\/\d+\/\d+ \d+:\d+:\d+ [PA]M$", linha): # data e hora
		return True
	if re.search("^\d+$", linha): # número da página
		return True
	if re.search("\.indd \d+$", linha): 
		return True
	if re.search("^ilustração",linha.lower()) or re.search("^foto",linha.lower()) or re.search("^produção",linha.lower()): # estou ignorando o autor da ilustração ou foto, pois ela não é salva
		return True
	if re.search("^textos? d a r e d a ç ã o",linha.lower()): # estou ignorando o autor quando é a Redação
		return True
	if re.search("^©",linha):
		return True
		
	return False

def eh_inicio_legenda(linha):
	return re.search("^.?À ESQUERDA",linha) or re.search("^.?DA ESQUERDA",linha) or re.search("^.?À DIREITA",linha) or re.search("^.?DA DIREITA",linha)
	
def eh_autoria(linha):
	autor = ""
	if re.search("^texto",linha) and (re.search("R e d a ç ã o",linha) == None):
		autor = linha.replace("texto","")
		autor = re.sub(r' ([^A-Z])', r'\1', autor).lstrip()
#	else:
#		if re.search("^por",linha):
#			autor = linha.replace("por","")
	return autor
	
def eh_coautoria(linha):
	coautor = ""
	if re.search("^e ",linha):
		coautor = linha
	return coautor

def converte_json(texto):
	texto = re.sub(r'([^\s])“',r'\1 “', texto)
	texto = re.sub(r'(\w)-\s+(\w)',r'\1\2',texto)
	texto.replace('"','\"')
	return texto


# Programa principal

# Seções das Edições 1
secoes = ["CARTA DA ROBERTA", "PRAZERES SIMPLES","VALORES ESSENCIAIS","DÁ PRA MUDAR?","MANUAL PRÁTICO","GENTE QUE FAZ"]
ignorar = ["PRA COMEÇAR", "COMUNIDADE SORRIA", "ACONTECEU COMIGO", "MUITO OBRIGADA"] 
# Seções que eu estou ignorando e não estou incluindo no .json
# "índice" => Estava dando trabalho para processar
# "ajudar" => Traz informações pessoais como nomes de pessoas que foram ajudadas pela causa
# "conversar" => Traz informações pessoais como nomes de pessoas que mandaram cartas para a redação


# Seções das Edições 1 a 20
#secoes = ["editorial", "carta do editor", "conversar", "descobrir", "conhecer", "envolver", "cuidar", "conviver", "crescer", "amar", "proteger", "movimentar", "comer", "brincar", "ajudar"]
# seções de 21 a 29:
#secoes = ["editorial", "carta do editor", "descobrir", "conhecer", "envolver", "conviver", "cuidar", "crescer", "amar", "educar", "trabalhar", "movimentar", "comer", "brincar"]
#ignorar = ["índice", "ajudar", "conversar"] 
#secoes 30 a 41:
#secoes = ["CARTA DA ROBERTA", "PRAZERES SIMPLES", "COMO EU FAÇO?", "DÁ PRA MUDAR?", "LUGAR EM COMUM", "VALORES ESSENCIAIS", "NOTA 10", "GENTE QUE FAZ", "DIA ÚTIL", "AÇÃO E DIVERSÃO", "TÁ NA MESA", "COMO VAI VOCÊ?"]
# seções 42 a:
# ignorar = ["indice, comunidade sorria, muito obrigada"]
arq = os.getcwd() + '/' + sys.argv[1]

nome = ""
edicao_data = True
secao = {}
ignora = False
busca_coautor = False
busca_titulo = False
numero = ""
meses =""
ano =""
#stop = False

# LEITURA
# Abre o arquivo .txt de entrada
with io.open(arq,'r',encoding='utf8') as f:
	# Para cada linha
	for linha in f:
#		if len(linha.strip()) == 0: # Não descomentar essa linha!!!!!
#			continue
		if eh_fim_processamento(linha.strip()):
			break
		if edicao_data:
			# Verifica se é o número e data da edição -- Padrão esperado: * 01 mar/abr 2008
			if re.search("^\* *\d+ \w+\/\w+ \d+$", linha.strip()):
				linha = re.sub(r'^\* *',r'',linha.strip())
				(numero,meses,ano) = re.split(" ",linha)
				edicao_data = False
					
			elif re.search("^\* \d+ \w+\/\d+$", linha.strip()):
				linha = re.sub(r'^\* *',r'',linha.strip())
				(numero,data) = re.split(" ",linha.strip())
				(mes1, ano1) = data.split("/")
				meses = mes1 + ano1 + " to "
				ano = ano1
			elif re.search("^\w+\/\d+$", linha.strip()):
				(mes2, ano2) = linha.split("/")
				meses += mes2 + ano2
				edicao_data = False
			elif re.search("^\* *\d+ \w+\. \d+ *\/ *\w+\. *\d+$", linha.strip()): 
				linha = re.sub(r'^\* *',r'',linha.strip())
				(numero,mes1,ano1,barra,mes2,ano2) = re.split(" ",linha.strip())
				meses = mes1 + ano1 + " to " + mes2 + ano2
				ano = ano1
				edicao_data = False
			elif re.search("^\* *\d+ \w+ \d+ *\/ *\w+\ *\d+$", linha.strip()): 
				linha = re.sub(r'^\* *',r'',linha.strip())
				(numero,mes1,data,ano2) = re.split(" ",linha.strip())
				(ano1, mes2) = data.split('/')
				meses = mes1 + ano1 + " to " + mes2 + ano2
				ano = ano1
				edicao_data = False
			elif re.search("^\* *\d+ \w+\.\d+ *\/ *\w+\. *\d+$", linha.strip()): 
				linha = re.sub(r'^\* *',r'',linha.strip())
				(numero,data) = re.split(" ",linha.strip())
				(data1, data2) = re.split("/", data)
				(mes1, ano1) = data1.split(".")
				(mes2, ano2) = data2.split(".")
				meses = mes1 + ano1 + " to " + mes2 + ano2
				ano = ano1
				edicao_data = False
			elif re.search("^\w+\/\w+$", linha.strip()):
				meses = linha.strip()
			elif re.search("^\#\d+$", linha.strip()):
				numero = linha.strip()
				numero = numero.replace("#","")

			elif re.search("^\d{4}", linha.strip()):
				ano = linha.strip()
				edicao_data = False
		# Verifica se é começo de uma das seções que estou ignorando
		if comeco_secao(linha.strip(),ignorar):
			nome = ""
			busca_titulo = False
			continue
		
		# Verifica se é começo de seção com base nos valores em "secoes"
		if comeco_secao(linha.strip(), secoes):
			nova = linha.strip()
			if (nova != nome):
				nome = nova
				secao[nome] = {}
				secao[nome]["autoria"] = ""
				secao[nome]["texto"] = ""
				secao[nome]["titulo"] = ""
				secao[nome]["edicao"] = numero
				secao[nome]["meses"] = meses 
				secao[nome]["ano"] = ano
				busca_titulo = True
		else:
			if busca_titulo:
#				if not(stop):
				if re.search("^\d+$",linha.strip()) or len(linha.strip()) == 0: # Número da página ou linha em branco
#					stop = True
					continue
				else:
					secao[nome]["titulo"] = linha.strip()
					busca_titulo = False
					continue
#				else:
#					busca_titulo = False
			if ignora and (len(linha.strip()) == 0):
				ignora = False			
			else:
				if not(ignora) and not(excluir(linha.strip())) and (len(nome) > 0):
					coautor = ""
					if busca_coautor:
						coautor = eh_coautoria(linha.strip()) 
						if len(coautor) > 0:
							secao[nome]["autoria"] += " " + coautor
						busca_coautor = False
					if len(coautor) == 0:
						autor = eh_autoria(linha.strip()) 
						if len(autor) > 0:
							secao[nome]["autoria"] = autor
							busca_coautor = True
						else:
							ignora = eh_inicio_legenda(linha)	
							if not(ignora) and len(linha.strip()) > 0:
								tira_aspas = linha.strip().replace('"',"'")
								secao[nome]["texto"] += " " + tira_aspas
f.close()

# ESCRITA
# Abre arquivo .json de saída
saida = os.getcwd() + '/json/' + sys.argv[1].split("/")[-1].replace(".txt",".json")
with io.open(saida,'w',encoding='utf8') as f:
	f.write("[\n")
	for i in range(0,len(secoes)):
		if secoes[i] in secao:
			f.write("{\"section\": \"" + secoes[i] + "\", ")
			f.write("\"title\": \"" + secao[secoes[i]]["titulo"] + "\", ")				
			f.write("\"author\": \"" + secao[secoes[i]]["autoria"] + "\", ")	
			f.write("\"edition\": \"" + secao[secoes[i]]["edicao"] + "\", ")
			f.write("\"months\": \"" + secao[secoes[i]]["meses"] + "\", ")
			f.write("\"year\": \"" + secao[secoes[i]]["ano"] + "\", ")				
			f.write("\"text\": \"" + converte_json(secao[secoes[i]]["texto"]).lstrip() + "\"")
			if (i == len(secoes)-1):
				f.write("}\n]")
			else:
				f.write("},\n")
	f.close()


