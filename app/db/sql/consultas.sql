-- Seleciona todos os alunos em turmas de disciplinas que são requisisto para edição de imagens
SELECT al.cpf, al.nome || ' ' || al.sobrenome AS Nome_Completo 
    FROM usuario AS al 
    JOIN membro_turma AS mt ON al.cpf = mt.aluno 
        WHERE al.tipo = 'aluno' AND 
        mt.turma_disciplina IN (SELECT requisito FROM requisito WHERE disciplina = 'Edição de Imagens') 
    GROUP BY al.cpf, al.nome, al.sobrenome  
        HAVING COUNT(*) = (SELECT COUNT(*) FROM requisito WHERE disciplina = 'Edição de Imagens');

-- Seleciona alunos que estão em uma turma e para as turmas que tem horario marcado os horários e dia da semana, ordenado pelo tempo
SELECT al.cpf, al.nome, mt.turma_disciplina, ht.dia_da_semana, ht.horario 
    FROM usuario AS al 
    JOIN membro_turma AS mt ON al.cpf = mt.aluno 
        LEFT JOIN horario_turma AS ht ON mt.turma_disciplina = ht.turma_disciplina AND mt.turma_id = ht.turma_id 
    WHERE al.tipo = 'aluno' 
    ORDER BY horario;

-- Pega todos os comentários com resposta, pega o nome do dono do comentário original, da resposta, o conteudo dos dois e ordena pela data do post original
-- Aviso: no dataset fornecido a tela vai encher de LOREM IPSUM
SELECT us.nome AS original_poster, co.conteudo AS post, us_resp.nome AS autor_resposta, resp.conteudo AS resposta 
    FROM comentario AS co 
        JOIN usuario AS us ON us.cpf = co.usuario 
            JOIN comentario AS resp ON co.usuario = resp.resposta_de_usuario 
            JOIN usuario AS us_resp ON resp.usuario = us_resp.cpf
    ORDER BY co.data_comentario;

-- Pega todos os usuarios banidos, e para os que são professores e tem avaliações pega também a média de suas avaliações e ordena por ela
SELECT us.nome || ' ' || us.sobrenome AS nome_banido, AVG(ap.nota) AS media_nota 
    FROM bane_usuario AS bu 
        JOIN usuario AS us ON us.cpf = bu.usuario 
            LEFT JOIN avaliacao_professor AS ap ON ap.professor = bu.usuario 
    GROUP BY us.nome, us.sobrenome, us.cpf 
    ORDER BY media_nota;
