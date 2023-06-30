drop table if exists serie_ibge;
drop table if exists localidade_ibge;
drop table if exists nivel_ibge;
drop table if exists resultado_ibge;
drop table if exists mapa_ibge;
drop table if exists variavel_ibge;
drop table if exists agregado_ibge;
drop table if exists consulta;
drop table if exists pesquisa_ibge;
drop table if exists avaliacao_monitor;
drop table if exists avaliacao_professor;
drop table if exists avaliacao_curso;
drop table if exists avaliacao_disciplina;
drop table if exists evento;
drop table if exists turma;
drop table if exists requisito;
drop table if exists curso_disciplina;
drop table if exists inscricao;
drop table if exists disciplina;
drop table if exists curso;
drop table if exists bane_comentario;
drop table if exists comentario;
drop table if exists bane_usuario;
drop table if exists aluno;
drop table if exists monitor;
drop table if exists professor;
drop table if exists moderador;
drop function if exists usuario_tipo;
drop table if exists usuario;

create table usuario (
    cpf char(11) not null,
    nome varchar(120),
    sobrenome varchar(120),
    email varchar(40) not null,
    cod_pais varchar(5),
    ddd integer,
    numero integer,
    senha varchar(255) not null,
    endereco text,
    tipo varchar(9),
    constraint usuario_pk 
        primary key (cpf),
    constraint usuario_email_unique 
        unique (email),
    constraint usuario_tipo 
        check (tipo in ('moderador', 'professor', 'monitor', 'aluno'))
);


create function usuario_tipo(char(11)) returns varchar(9) as $$
    select tipo
    from usuario u
    where u.cpf = cpf;
$$
language sql;

create table moderador (
    usuario char(11) not null,
    constraint moderador_pk 
        primary key (usuario),
    constraint moderador_usuario_fk 
        foreign key (usuario) 
        references usuario(cpf)
        on delete cascade,
    constraint usuario_tipo_moderador 
        check (usuario_tipo(usuario) = 'moderador')
);

create table professor (
    usuario char(11) not null,
    constraint professor_pk 
        primary key (usuario),
    constraint professor_usuario_fk 
        foreign key (usuario) 
        references usuario(cpf)
        on delete cascade,
    constraint usuario_tipo_professor 
        check (usuario_tipo(usuario) = 'professor')
);

create table monitor (
    usuario char(11) not null,
    constraint monitor_pk 
        primary key (usuario),
    constraint monitor_usuario_fk 
        foreign key (usuario) 
        references usuario(cpf)
        on delete cascade,
    constraint usuario_tipo_monitor 
        check (usuario_tipo(usuario) = 'monitor')
);

create table aluno (
    usuario char(11) not null,
    constraint aluno_pk 
        primary key (usuario),
    constraint aluno_usuario_fk 
        foreign key (usuario) 
        references usuario(cpf)
        on delete cascade,
    constraint usuario_tipo_aluno 
        check (usuario_tipo(usuario) = 'aluno')
);

create table bane_usuario (
    usuario char(11) not null,
    moderador char(11) not null,
    banido boolean,
    constraint bane_usuario_pk 
        primary key (usuario),
    constraint bane_usuario_moderador_fk 
        foreign key (moderador) 
        references moderador(usuario)
        on delete restrict,
    constraint bane_usuario_usuario_fk 
        foreign key (usuario) 
        references usuario(cpf)
        on delete restrict
);

create table comentario (
    usuario char(11) not null,
    data_comentario timestamp not null,
    conteudo text,
    resposta_de_usuario char(11),
    resposta_de_data_comentario timestamp,
    constraint comentario_pk 
        primary key (usuario, data_comentario),
    constraint comentario_responde_fk 
        foreign key (usuario, data_comentario) 
        references comentario(usuario, data_comentario)
        on delete set null
);

create table bane_comentario (
    comentario_usuario char(11) not null,
    comentario_data_hora timestamp not null,
    moderador char(11) not null,
    constraint bane_comentario_pk 
        primary key (comentario_usuario, comentario_data_hora),
    constraint bane_comentario_moderador_fk 
        foreign key (moderador) 
        references moderador(usuario)
        on delete restrict
);

create table curso (
    nome varchar(120) not null,
    data_criacao date not null,
    descricao text,
    "online" boolean,
    "local" varchar(120),
    professor char(11),
    constraint curso_pk 
        primary key (nome, data_criacao),
    constraint curso_professor_fk 
        foreign key (professor) 
        references professor(usuario)
        on delete set null,
    constraint curso_professor_unique unique (professor)
);

create table disciplina (
    nome varchar(120) not null,
    descricao text,
    professor char(11),
    constraint disciplina_pk 
        primary key (nome),
    constraint disciplina_professor_fk 
        foreign key (professor) 
        references professor(usuario)
        on delete set null
);

create table inscricao (
    curso_nome varchar(120) not null,
    curso_data_criacao date not null,
    aluno char(11) not null,
    constraint inscricao_pk 
        primary key (curso_nome, curso_data_criacao, aluno),
    constraint inscricao_curso_fk 
        foreign key (curso_nome, curso_data_criacao) 
        references curso(nome, data_criacao)
        on delete restrict,
    constraint inscricao_aluno_fk 
        foreign key (aluno) 
        references aluno(usuario)
        on delete cascade
);

create table curso_disciplina (
    curso_nome varchar(120) not null,
    curso_data_criacao date not null,
    disciplina varchar(120) not null,
    constraint curso_disciplina_pk 
        primary key (curso_nome, curso_data_criacao, disciplina),
    constraint curso_disciplina_curso_fk 
        foreign key (curso_nome, curso_data_criacao) 
        references curso(nome, data_criacao)
        on delete cascade,
    constraint curso_disciplina_disciplina_fk 
        foreign key (disciplina) 
        references disciplina(nome)
        on delete restrict
);

create table requisito (
    disciplina varchar(120) not null,
    requisito varchar(120) not null,
    constraint requisito_pk 
        primary key (disciplina, requisito),
    constraint requisito_disciplina_fk
        foreign key (disciplina)
        references disciplina(nome)
        on delete cascade,
    constraint requisito_requisito_fk
        foreign key (requisito)
        references disciplina(nome)
        on delete restrict
);

create table turma (
    disciplina varchar(120) not null,
    id integer not null,
    constraint turma_pk
        primary key (disciplina, id),
    constraint turma_disciplina_fk
        foreign key (disciplina)
        references disciplina(nome)
        on delete restrict
);

create table evento (
    data_hora_evento timestamp not null,
    titulo varchar(120) not null,
    descricao text,
    turma_disciplina varchar(120),
    turma_id integer,
    constraint evento_pk
        primary key (data_hora_evento, titulo),
    constraint evento_turma_fk
        foreign key (turma_disciplina, turma_id)
        references turma(disciplina, id)
        on delete cascade
);

create table avaliacao_disciplina (
    aluno char(11) not null,
    data_avaliacao timestamp not null,
    nota integer,
    disciplina varchar(120) not null,
    constraint avaliacao_disciplina_pk
        primary key (aluno, data_avaliacao),
    constraint avaliacao_disciplina_disciplina_fk
        foreign key (disciplina)
        references disciplina(nome)
        on delete cascade,
    constraint avaliacao_disciplina_nota_zero_a_cinco
        check (nota between 0 and 5)
);

create table avaliacao_curso (
    aluno char(11) not null,
    data_avaliacao timestamp not null,
    nota integer,
    curso_nome varchar(120) not null,
    curso_data_criacao date not null,
    constraint avaliacao_curso_pk
        primary key (aluno, data_avaliacao),
    constraint avaliacao_curso_curso_fk
        foreign key (curso_nome, curso_data_criacao)
        references curso(nome, data_criacao)
        on delete cascade,
    constraint avaliacao_curso_nota_zero_a_cinco
        check (nota between 0 and 5)
);

create table avaliacao_professor (
    aluno char(11) not null,
    data_avaliacao timestamp not null,
    nota integer,
    professor char(11) not null,
    constraint avaliacao_professor_pk
        primary key (aluno, data_avaliacao),
    constraint avaliacao_professor_professor_fk
        foreign key (professor)
        references professor(usuario)
        on delete cascade,
    constraint avaliacao_professor_nota_zero_a_cinco
        check (nota between 0 and 5)
);

create table avaliacao_monitor (
    aluno char(11) not null,
    data_avaliacao timestamp not null,
    nota integer,
    monitor char(11) not null,
    constraint avaliacao_monitor_pk
        primary key (aluno, data_avaliacao),
    constraint avaliacao_monitor_monitor_fk
        foreign key (monitor)
        references monitor(usuario)
        on delete cascade,
    constraint avaliacao_monitor_nota_zero_a_cinco
        check (nota between 0 and 5)
);

create table pesquisa_ibge (
    id integer not null,
    nome varchar(255) not null,
    constraint pesquisa_ibge_pk
        primary key (id)
);

create table consulta (
    professor char(11) not null,
    pesquisa integer not null,
    constraint consulta_pk
        primary key (professor, pesquisa),
    constraint consulta_professor_fk
        foreign key (professor)
        references professor(usuario)
        on delete cascade,
    constraint consulta_pesquisa_fk
        foreign key (pesquisa)
        references pesquisa_ibge(id)
        on delete restrict
);

create table agregado_ibge (
    id integer not null,
    pesquisa integer not null,
    nome varchar(255),
    assunto text,
    constraint agregado_ibge_pk
        primary key (id),
    constraint acregado_pesquisa_fk
        foreign key (pesquisa)
        references pesquisa_ibge(id)
        on delete restrict
);

create table variavel_ibge (
    id integer not null
    nome varchar(255),
    agregado integer not null,
    unidade varchar(20),
    constraint variavel_ibge_pk
        primary key (id),
    constraint variavel_ibge_agregado_fk
        foreign key (agregado)
        references agregado_ibge(id)
        on delete restrict
);

create table mapa_ibge (
    id integer not null,
    nome varchar(120),
    malha jsonb,
    constraint mapa_ibge_pk
        primary key (id)
);

create table resultado_ibge (
    variavel integer not null,
    classificacao varchar(20) not null,
    mapa integer not null,
    constraint resultado_ibge_pk
        primary key (variavel, classificacao, mapa),
    constraint resultado_ibge_variavel
        foreign key (variavel)
        references variavel_ibge(id)
        on delete restrict,
    constraint resultado_ibge_mapa
        foreign key (mapa)
        references mapa_ibge(id)
        on delete restrict
);

create table nivel_ibge (
    id integer not null,
    nome varchar(50),
    constraint nivel_ibge_pk
        primary key (id)
);

create table localidade_ibge (
    id integer not null,
    nome varchar(50),
    nivel integer not null,
    constraint localidade_ibge_pk
        primary key (id),
    constraint localidade_ibge_nivel_fk
        foreign key (nivel)
        references nivel_ibge(id)
        on delete restrict
);

create table serie_ibge (
    classificacao varchar(20) not null,
    periodo varchar(20) not null,
    valor varchar(20),
    localidade integer not null,
    constraint serie_ibge_pk
        primary key (classificacao, periodo),
    constraint serie_ibge_localidade_fk
        foreign key localidade
        references localidade_ibge(id)
        on delete restrict
);
