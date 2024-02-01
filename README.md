# DesafioTunts.Rocks2024
## DESAFIO
Criar uma aplicação em uma linguagem de programação de sua preferência. A aplicação deve ser capaz de ler  uma planilha do google sheets, buscar as informações necessárias, calcular e escrever o  resultado na planilha.
## REGRAS: 
- Calcular a situação de cada aluno baseado na média das 3 provas (P1, P2 e P3), conforme a  tabela: 
  
Média (m) Situação:\
m<5  - Reprovado por Nota\
5<=m<7  - Exame Final\
m>=7  - Aprovado

- Caso o número de faltas ultrapasse 25% do número total de aulas o aluno terá a situação  "Reprovado por Falta", independente da média.  Caso a situação seja "Exame Final" é necessário calcular a "Nota para Aprovação Final"(naf) de  cada aluno de acordo com seguinte fórmula:

5 <= (m + naf)/2

- Caso a situação do aluno seja diferente de "Exame Final", preencha o campo "Nota para  Aprovação Final" com 0. 

- Arredondar o resultado para o próximo número inteiro (aumentar) caso necessário. Utilizar linhas de logs para acompanhamento das atividades da aplicação.

## REFERÊNCIA 
Documentação da Google Sheets: https://developers.google.com/sheets/api/guides/concepts

## How to Run it?
É necessário adicionar o arquivo "credentials.json" do client OAuth criado na Google Clound
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
python main.py
```
##
