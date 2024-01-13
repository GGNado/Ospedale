-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Gen 13, 2024 alle 10:51
-- Versione del server: 10.4.28-MariaDB
-- Versione PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Ospedale`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `Illnesses`
--

CREATE TABLE `Illnesses` (
  `ID` int(11) NOT NULL,
  `nome` varchar(40) NOT NULL,
  `descrizione` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Illnesses`
--

INSERT INTO `Illnesses` (`ID`, `nome`, `descrizione`) VALUES
(1, 'Vita', 'La tua nascita.'),
(2, 'Naso Floreale', 'Il naso sboccia come un fiore ogni primavera.'),
(3, 'Disarmonia Vocale da Camaleonte', 'La voce cambia colore e tonalità in base all\'umore.'),
(4, 'L\'Orecchio Multifunzionale', 'Le orecchie possono funzionare come radar per individuare il cibo preferito.'),
(5, 'Ipersensibilità alla Gravità', 'Chi ne soffre può saltare più in alto degli altri, ma è vulnerabile a sbalzi improvvisi.'),
(6, 'Capelli Bioluminescenti', 'I capelli brillano al buio come una lucciola.'),
(7, 'Eremitismo Istantaneo', 'Le persone possono diventare invisibili a comando, ma solo quando si sentono estremamente timide.'),
(8, 'Dita Multifunzionali', 'Le dita possono allungarsi e contrarsi a piacimento.'),
(9, 'Guance Musicali', 'Le guance producono melodie quando si soffia attraverso di esse.'),
(10, 'Ridolina', 'Ridere troppo può causare dolori addominali momentanei.'),
(11, 'Coda di Drago', 'Una piccola coda cresce nella parte bassa della schiena e può essere usata come strumento per esprimere emozioni.');

-- --------------------------------------------------------

--
-- Struttura della tabella `Patients`
--

CREATE TABLE `Patients` (
  `ID` int(11) NOT NULL,
  `nome` varchar(40) NOT NULL,
  `cognome` varchar(40) NOT NULL,
  `sesso` char(1) NOT NULL,
  `dataNascita` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `Patients`
--

INSERT INTO `Patients` (`ID`, `nome`, `cognome`, `sesso`, `dataNascita`) VALUES
(78, 'Simona', 'Ferrari', 'F', '1982-12-18'),
(79, 'Giovanni', 'Martini', 'M', '1991-06-22'),
(80, 'Chiara', 'Moretti', 'F', '1975-04-07'),
(81, 'Alessandro', 'Vitale', 'M', '1987-08-14'),
(82, 'Valentina', 'De Luca', 'F', '1998-02-28'),
(83, 'Antonio', 'Santoro', 'M', '1980-10-05'),
(84, 'Elisa', 'Costa', 'F', '1993-05-19'),
(85, 'Davide', 'Leone', 'M', '1989-01-26'),
(86, 'Sara', 'Barbieri', 'F', '1977-07-03'),
(87, 'Elena', 'Galli', 'F', '1984-09-11'),
(89, 'Francesca', 'Fabbri', 'F', '1986-06-29'),
(90, 'Riccardo', 'Piras', 'M', '1978-03-22'),
(91, 'Laura', 'Mancini', 'F', '1994-08-07'),
(92, 'Massimo', 'Rizzo', 'M', '1983-11-09'),
(98, 'Gervasio', 'Battimelli', 'M', '2005-10-17'),
(100, 'Biagio Rosario', 'Greco', 'M', '1981-08-17');

-- --------------------------------------------------------

--
-- Struttura della tabella `PatientsIllnesses`
--

CREATE TABLE `PatientsIllnesses` (
  `ID` int(11) NOT NULL,
  `dataCura` date DEFAULT NULL,
  `dataCont` date NOT NULL,
  `FK_Paziente` int(11) DEFAULT NULL,
  `FK_Malattia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `PatientsIllnesses`
--

INSERT INTO `PatientsIllnesses` (`ID`, `dataCura`, `dataCont`, `FK_Paziente`, `FK_Malattia`) VALUES
(81, '2024-01-08', '2024-01-08', 98, 6),
(82, NULL, '2024-01-08', 98, 7),
(83, NULL, '2024-01-08', 98, 8),
(87, NULL, '2024-01-09', 100, 1),
(88, '2024-01-09', '2024-01-09', 100, 5),
(89, '2024-01-09', '2024-01-09', 100, 6),
(90, '2024-01-09', '2024-01-09', 100, 10),
(91, '2024-01-09', '2024-01-09', 100, 11);

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `Illnesses`
--
ALTER TABLE `Illnesses`
  ADD PRIMARY KEY (`ID`);

--
-- Indici per le tabelle `Patients`
--
ALTER TABLE `Patients`
  ADD PRIMARY KEY (`ID`);

--
-- Indici per le tabelle `PatientsIllnesses`
--
ALTER TABLE `PatientsIllnesses`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `FK_Paziente` (`FK_Paziente`),
  ADD KEY `FK_Malattia` (`FK_Malattia`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `Illnesses`
--
ALTER TABLE `Illnesses`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT per la tabella `Patients`
--
ALTER TABLE `Patients`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT per la tabella `PatientsIllnesses`
--
ALTER TABLE `PatientsIllnesses`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=92;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `PatientsIllnesses`
--
ALTER TABLE `PatientsIllnesses`
  ADD CONSTRAINT `patientsillnesses_ibfk_1` FOREIGN KEY (`FK_Paziente`) REFERENCES `Patients` (`ID`),
  ADD CONSTRAINT `patientsillnesses_ibfk_2` FOREIGN KEY (`FK_Malattia`) REFERENCES `Illnesses` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
