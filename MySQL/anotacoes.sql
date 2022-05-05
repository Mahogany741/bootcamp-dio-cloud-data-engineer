-- CRIANDO A TABELA 
CREATE TABLE pessoas (
    nome VARCHAR(20),
    nascimento DATE
)

-- INSERINDO DADOS NA TABELA
INSERT INTO pessoa (nome, nascimento) VALUES ('Nathally', '1990-05-22');
INSERT INTO pessoa (nome, nascimento) VALUES ('Pedro', '1995-07-17');
INSERT INTO pessoa (nome, nascimento) VALUES ('Marcela', '2000-04-05');
INSERT INTO pessoa (nome, nascimento) VALUES ('Flávio', '2002-12-01');

-- SELECIONANDO OS DADOS 
SELECT * FROM pessoa;

-- OCULTANDO A COLUNA ID 
SELECT 
    nome,
    nascimento
FROM pessoa;

-- ATUALIZANDO DADOS 
UPDATE pessoa 
SET nome = 'Nathally Souza'
WHERE id = 1;

-- DELETANDO DADOS
-- uma boa prática é verificar atráves do SELECT, se o registro a ser excluído, é o correto.
SELECT * FROM pessoa 
WHERE id = 4; 

DELETE FROM pessoa 
WHERE id = 4; 

-- Mostrando que a primary key é realmente única, exclusiva e imutável.
INSERT INTO pessoa (nome, nascimento) VALUES ('Flávio', '2002-12-01'); -- Flavio que antes tinha id 4, agora tem id 5, pois, por mais que o id 4 tenha sido excluido, ele era único e intransferível.

-- ORDENANDO DADOS
SELECT * FROM pessoa
ORDER BY nome;

-- forma decrescente
SELECT * FROM pessoa
ORDER BY nome DESC;


-- AGRUPANDO OS DADOS
SELECT 
    genero,
    count(genero)
FROM pessoa
GROUP BY genero;

-- MÓDULO 2 - Explorando relacionamentos com o workbench

-- verificando os bancos existentes
SHOW DATABASES;

-- conectando ao banco
USE dio_mysql

-- verificando as tabelas existentes
SHOW TABLES;

-- criando tabelas
CREATE TABLE cursos(
    id_curso INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(10)
);

-- inserindo dados na tabela cursos
INSERT INTO cursos (nome) VALUES ('MySQL');
INSERT INTO cursos (nome) VALUES ('HTML');
INSERT INTO cursos (nome) VALUES ('CSS');
INSERT INTO cursos (nome) VALUES ('Economia');

-- verificando os dados na tabela cursos
SELECT * FROM cursos;

-- realizando update
UPDATE cursos 
SET nome = 'HTML 5'
WHERE id_curso = 2;

-- delete 
DELETE FROM cursos 
WHERE id_curso = 4;

-- adicionando campos
ALTER TABLE cursos 
ADD carga_horaria INT(2);

UPDATE cursos
SET carga_horaria = 20;

-- deletando tabela

DROP TABLE pessoas;

-- deletando o banco
DROP DATABASE dio_mysql




