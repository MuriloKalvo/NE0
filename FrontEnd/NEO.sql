-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 08/08/2025 às 21:27
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `mydb`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `admin`
--

CREATE TABLE `admin` (
  `IDAdmin` int(11) NOT NULL,
  `Nome` varchar(145) NOT NULL,
  `Email` varchar(145) NOT NULL,
  `Senha` varchar(145) NOT NULL,
  `Telefone` bigint(20) NOT NULL,
  `Endereco` varchar(145) DEFAULT NULL,
  `Genero` varchar(45) DEFAULT NULL,
  `Nascimento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `aluno`
--

CREATE TABLE `aluno` (
  `IDAluno` int(11) NOT NULL,
  `Nome` varchar(145) NOT NULL,
  `Senha` varchar(145) NOT NULL,
  `Email` varchar(145) NOT NULL,
  `Genero` varchar(45) DEFAULT NULL,
  `Nascimento` date NOT NULL,
  `Telefone` bigint(20) NOT NULL,
  `Endereco` varchar(145) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Despejando dados para a tabela `aluno`
--

INSERT INTO `aluno` (`IDAluno`, `Nome`, `Senha`, `Email`, `Genero`, `Nascimento`, `Telefone`, `Endereco`) VALUES
(1, 'a\r\n', 'a', 'a', NULL, '2025-08-06', 1, 'a');

-- --------------------------------------------------------

--
-- Estrutura para tabela `curso`
--

CREATE TABLE `curso` (
  `IDCurso` int(11) NOT NULL,
  `NomeCurso` varchar(45) NOT NULL,
  `NumCurso` int(11) NOT NULL,
  `EstadoCurso` varchar(45) NOT NULL,
  `MateriaCurso` varchar(45) NOT NULL,
  `CHCurso` int(11) NOT NULL,
  `HorarioCurso` datetime NOT NULL,
  `VagasCurso` int(11) NOT NULL,
  `PeriodoCurso` varchar(45) NOT NULL,
  `Modalidade` varchar(45) NOT NULL,
  `PreReqCurso` varchar(45) NOT NULL,
  `Professor_IDProfessor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `ingressados`
--

CREATE TABLE `ingressados` (
  `Aluno_IDAluno` int(11) NOT NULL,
  `Curso_IDCurso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `professor`
--

CREATE TABLE `professor` (
  `IDProfessor` int(11) NOT NULL,
  `Nome` varchar(145) NOT NULL,
  `Senha` varchar(145) NOT NULL,
  `Telefone` bigint(20) NOT NULL,
  `Endereco` varchar(145) DEFAULT NULL,
  `Genero` varchar(45) DEFAULT NULL,
  `Email` varchar(145) NOT NULL,
  `Nascimento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `relatorio`
--

CREATE TABLE `relatorio` (
  `IDRelatorio` int(11) NOT NULL,
  `NotaAluno` float NOT NULL,
  `MediaAluno` float NOT NULL,
  `MediaTurma` float NOT NULL,
  `FaltaAluno` int(11) NOT NULL,
  `FaltaTurma` int(11) NOT NULL,
  `Curso_IDCurso` int(11) NOT NULL,
  `Aluno_IDAluno` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`IDAdmin`);

--
-- Índices de tabela `aluno`
--
ALTER TABLE `aluno`
  ADD PRIMARY KEY (`IDAluno`);

--
-- Índices de tabela `curso`
--
ALTER TABLE `curso`
  ADD PRIMARY KEY (`IDCurso`),
  ADD KEY `fk_Curso_Professor1_idx` (`Professor_IDProfessor`);

--
-- Índices de tabela `ingressados`
--
ALTER TABLE `ingressados`
  ADD PRIMARY KEY (`Aluno_IDAluno`,`Curso_IDCurso`),
  ADD KEY `fk_Aluno_has_Curso_Curso1_idx` (`Curso_IDCurso`),
  ADD KEY `fk_Aluno_has_Curso_Aluno_idx` (`Aluno_IDAluno`);

--
-- Índices de tabela `professor`
--
ALTER TABLE `professor`
  ADD PRIMARY KEY (`IDProfessor`);

--
-- Índices de tabela `relatorio`
--
ALTER TABLE `relatorio`
  ADD PRIMARY KEY (`IDRelatorio`),
  ADD KEY `fk_Relatorio_Curso1_idx` (`Curso_IDCurso`),
  ADD KEY `fk_Relatorio_Aluno1_idx` (`Aluno_IDAluno`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `admin`
--
ALTER TABLE `admin`
  MODIFY `IDAdmin` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `aluno`
--
ALTER TABLE `aluno`
  MODIFY `IDAluno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de tabela `curso`
--
ALTER TABLE `curso`
  MODIFY `IDCurso` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `professor`
--
ALTER TABLE `professor`
  MODIFY `IDProfessor` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `relatorio`
--
ALTER TABLE `relatorio`
  MODIFY `IDRelatorio` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `curso`
--
ALTER TABLE `curso`
  ADD CONSTRAINT `fk_Curso_Professor1` FOREIGN KEY (`Professor_IDProfessor`) REFERENCES `professor` (`IDProfessor`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Restrições para tabelas `ingressados`
--
ALTER TABLE `ingressados`
  ADD CONSTRAINT `fk_Aluno_has_Curso_Aluno` FOREIGN KEY (`Aluno_IDAluno`) REFERENCES `aluno` (`IDAluno`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Aluno_has_Curso_Curso1` FOREIGN KEY (`Curso_IDCurso`) REFERENCES `curso` (`IDCurso`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Restrições para tabelas `relatorio`
--
ALTER TABLE `relatorio`
  ADD CONSTRAINT `fk_Relatorio_Aluno1` FOREIGN KEY (`Aluno_IDAluno`) REFERENCES `aluno` (`IDAluno`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Relatorio_Curso1` FOREIGN KEY (`Curso_IDCurso`) REFERENCES `curso` (`IDCurso`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
