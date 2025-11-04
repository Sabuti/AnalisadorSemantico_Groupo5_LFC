# AnalisadorSemantico_Groupo5_LFC

## Descrição do Projeto
Este projeto foca no desenvolvimento de um programa em Python para praticar o conceito de analisador semântico, como aprendido em aula. Ele processa e executa expressões em Notação Polonesa Reversa (RPN).
Além disso, o código é usado para gerar validar as expressões em relação a parte léxica e sintática.  
Ao final, o script cria 5 arquivos para verificar o funcionamento atual do programa, além de fornecer a árvore sintática abstrata atribuída para a próxima fase.  
Utiliza-se o PlatformIO, integrado ao VS Code, para definir a precisão dos números de ponto fluante, baseado na arquitetura de 8 bits do Arduino UNO usado no nosso projeto.

## Objetivo
Desenvolver o código em Python para gerar os relatórios e a árvore sintática abstrata atribuída.  
Para mais informações, acessar: [site do professor](https://frankalcantara.com/lf/fase3.html)

## Informações dos Autores e da Matéria
Integrantes do grupo:
- Ana Maria Midori Rocha Hinoshita - [anamariamidori](https://github.com/anamariamidori)
- Lucas Antonio Linhares - [Sabuti](https://github.com/Sabuti)  

Nome do grupo no Canvas: RA3_5  
Professor: Frank Coelho de Alcantara  
Disciplina: Linguagens Formais e Compiladores (LFC)  
Intituição: PUC-PR (Câmpus: Curitiba)  
Ano: 2025

## Divisão de Tarefas
Aluno 1 - Lucas;
Aluno 2 - Ana Maria;
Aluno 3 - Lucas;
Aluno 4 - Ana Maria;

** Combinado entre os alunos que ajuda com suas funções são permitidas **

## Pré-requisitos
1 - Instalar o Visual Studio Code (VS Code)
2 - Adicionar a extensão do PlatformIO dentro do VS Code

## Execução do Código
```bash
1 - Clonar este reposítorio para o ambiente do VS Code
2 - Rodar "python src/trabalho.py arq1.txt" (ou arq2, arq3)
3 - Acessar os arquivos de relatórios gerados
```

## Documentação das Funções Criadas
### - IF
A contrução do IF foi definida como:  

(Comparação Resultado_seVerdade Resultado_seFalso IF)  

Comparação: booleano  
Resultado_seVerdade: int ou float  
Resultado_seFalso: int ou float

### - WHILE
A construção do WHILE foi definida como:  

(Comparação Enquanto_Verdade WHILE)  

Comparação: booleano  
Enquanto_Verdade: int ou float
