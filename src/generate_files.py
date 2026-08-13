"""Com base no arquivo recebido, deverá ser criado um arquivo excel chamado INJECAO, com a aba
chamada INJECAO também. a estrutura do arquivo será: ID_ORDEM(irá herdar as ordens da coluna "ORDEM"), terá a a coluna NOTDONE(que não conterá valores, mas como será usado numa 
automação é necessário estar),terá a coluna TP_ORDEM(que vai receber os valores da coluna "ATIVIDADE"
sendo eles "BD" e "PREVENTIVA", os valores com nome "BD" devem ser alterados por "REPARO"), terá
também a coluna "DT_AGENDA"(que deverá conter a data dos próximos três dias sem considerar sabado
e domingo, pense que são ordens que terão injeção de agenda, então as datas precisam ter a quantidade
de ordens equilibradas) e por ultimo a coluna SLOT(pense nessa lógica: hoje é dia 10/08/2026
eu vou usar as três proximas datas para injeção, essas três datas receberão o slot de horário das
08:30-12:30 e depois mais três datas dessas com o slot 12:30-18:00, lembre-se que deve se manter
equilibrado a quantidade)"""

"""O arquivo de cancelamento deverá retornar somente os valores da coluna "ORDEM"."""