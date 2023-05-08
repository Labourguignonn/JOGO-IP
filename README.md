# JOGO-IP

RELATÓRIO FINAL DO PROJETO DE INTRODUÇÃO À PROGRAMAÇÃO (SISTEMA INTERATIVO)
Professor: Filipe Calegário, Ricardo Massa, Sérgio Soares
Alunos: Bruna Ferreira, Fabriely Luana, João Pedro Deo, Lucas Bourguignon, Mateus Rocha, Pedro Campelo


Após a Enchente
Repositório: Labourguignonn/JOGO-IP (github.com)

1. Ferramentas, bibliotecas e frameworks utilizados

  1.1 Visual Studio Code
    Ferramenta de desenvolvimento utilizada pelo grupo para edição de código e para gerenciamento de branches devido à integração ao git/github.

  1.2 Git/Github
    Software utilizado para versionamento do código.

  1.3 Biblioteca Pygame
    Biblioteca Python usada para o desenvolvimento do jogo desde a criação do cenário até as interações entre os objetos, devido às suas funções de colisão, sprites e      grupos.

  1.4 Biblioteca CSV 
    A biblioteca usada para a leitura e escrita dos arquivos em python foi fundamental para o projeto no momento de criar uma planilha com o mapa do jogo, visto que        usamos desse artifício para posicionar os tiles do background no jogo.

  1.5 Discord e Whatsapp
    Ambos usados para manter a comunicação entre os membros do grupo, seja para combinar aspectos relacionados ao projeto ou para reuniões de desenvolvimento.

  1.6 Notion 
    Plataforma usada para organizar os afazeres e tarefas dos membros do grupo através da metodologia Kanban

2. A organização do código

  A organização do código foi uma questão complicada durante o desenvolvimento do jogo, pois foi algo que não tomamos como prioridade logo de início no projeto. Nos esforçamos ao máximo para organizar os códigos em pastas e arquivos separados categoricamente, no entanto encontramos alguns obstáculos ao separar as principais classes devido a problemas constantes de importação circular. Apesar dos desafios, decidimos, no final, manter algumas classes no arquivo “main”, mas desacoplando a maior parte das variáveis e funções, colocando-as em seus respectivos arquivos e depois importando-as para o main. Desta forma a qualidade geral do código melhorou, ele ficou mais limpo e legível.

3. A divisão de trabalho dentro do grupo

  O mapa do jogo foi desenvolvido por Fabriely.
  O desenvolvimento e animação do player foram feitos por Fabriely e Lucas.
  A construção e animação dos inimigos foi feita por Fabriely, Pedro e Bruna.
  O desenvolvimento do item coletável que aumenta a vida foi feito por Fabriely e Lucas.
  A barra de gerenciamento de inimigos mortos foi feita por Bruna.
  A barra de gerenciamento de vida foi feita por Mateus.
  O menu inicial e game over foi desenvolvido por Mateus.
  As colisões do personagem com o mundo, inimigos e água foram feitas por Fabrielly, Lucas e Bruna.
  A responsividade com o teclado foi tarefa de Fabriely e Lucas.
  A organização do código em POO foi feita por Lucas, João Pedro e Pedro.
  O presente relatório e os slides foram feitos por João Pedro, Bruna e Pedro.


4. Conceitos apresentados na disciplina e utilizados no projeto

  No projeto, conseguimos unir todos os conhecimentos adquiridos ao longo da disciplina, desde os mais básicos como condicionais, laços, listas e dicionários, até a 
  técnica principal do projeto: programação orientada a objetos (POO). O que tornou o código mais legível e organizado.
  Além da área de software, utilizamos os conceitos de versionamento de código com o git/github. Nesse, utilizamos as branches, que permitiram uma maior liberdade para 
  cada desenvolvedor e uma maior visibilidade de cada nova feature que o nosso código recebeu.

5. Desafios enfrentados

  5.1 Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
   Não ter separado corretamente os arquivos antes de começar o projeto e a divisão das tarefas do trabalho. Resolvemos esses erros organizando o código e com o passar do tempo cada um foi se dispondo na função que poderia executar melhor.

  5.2 Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
  Os principais problemas encontrados foram aprender a utilizar o git para controlar as versões do projeto, criando mais branchs do que o necessário, o que atrapalhou na organização do projeto. Lidamos com o git na tentativa e erro, utilizando uma branch para cada componente que seria adicionado no projeto. 

5.3 Quais as lições aprendidas durante o projeto?
  É necessário, antes de tudo, organizar tarefas e datas antes de se iniciar o projeto propriamente dito, tendo em vista não acumular funções e pendências. Além disso, ter uma ideia clara do que será necessário em cada etapa do projeto e como será a estrutura do código antes de iniciar o desenvolvimento de fato é essencial.
