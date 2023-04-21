-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2023 年 04 月 21 日 11:18
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `housingwebsiteproject`
--

-- --------------------------------------------------------

--
-- 資料表結構 `availabletime`
--

CREATE TABLE `availabletime` (
  `pId` int(11) NOT NULL,
  `startTime` datetime NOT NULL,
  `endTime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `browses`
--

CREATE TABLE `browses` (
  `uId` int(10) NOT NULL,
  `pId` int(10) NOT NULL,
  `browseTime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `criticizes`
--

CREATE TABLE `criticizes` (
  `uId` int(10) NOT NULL,
  `pId` int(10) NOT NULL,
  `comment` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `floor`
--

CREATE TABLE `floor` (
  `hId` int(10) NOT NULL,
  `floor` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `house`
--

CREATE TABLE `house` (
  `hId` int(10) NOT NULL,
  `age` int(3) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `type` enum('店面','辦公','住辦','住宅') DEFAULT NULL,
  `twPing` float DEFAULT NULL,
  `lived` tinyint(1) NOT NULL,
  `pId` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `house`
--

INSERT INTO `house` (`hId`, `age`, `name`, `type`, `twPing`, `lived`, `pId`) VALUES
(1, 7, '台北晶麒', '住宅', 10.69, 1, 1),
(2, 7, '台北晶麒', '住宅', 10.41, 1, 2),
(3, 7, '台北晶麒', '住宅', 10.24, 1, 3),
(4, 7, '台北晶麒', '住宅', 13.11, 1, 4),
(5, 7, '台北晶麒', '住宅', 14.28, 1, 5),
(6, 7, '重陽重劃區邊間方正電梯三房平車', '住宅', 29.09, 1, 6),
(7, 15, '合康達觀電梯三房車', '住宅', 21.69, 1, 7),
(8, 26, '新店達觀超正豪美大3房+平面大車位', '住宅', 26.33, 1, 8),
(9, 26, '酷企鵝推薦，超低公設原木系景觀戶', '住宅', 35.17, 1, 9),
(10, 18, '酷企鵝推薦，套房車可改回兩房，速速', '住宅', 15.14, 1, 10),
(11, 5, '寶徠花園天后獨家超美視野1+1房車', '住宅', 15.45, 1, 11),
(12, 6, '獨家縣三禾寅文鼎為美三房雙車／次頂視野戶', '住宅', 23.96, 1, 12);

-- --------------------------------------------------------

--
-- 資料表結構 `houserent`
--

CREATE TABLE `houserent` (
  `hId` int(11) NOT NULL,
  `price` int(10) NOT NULL,
  `electric` int(5) DEFAULT NULL,
  `management` int(5) DEFAULT NULL,
  `web` int(5) DEFAULT NULL,
  `water` int(5) DEFAULT NULL,
  `funiture` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `housesell`
--

CREATE TABLE `housesell` (
  `hId` int(11) NOT NULL,
  `ratioOfPublicArea` float DEFAULT NULL,
  `pricePerTwping` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `image`
--

CREATE TABLE `image` (
  `hId` int(10) NOT NULL,
  `spaceName` enum('房','廳','衛') NOT NULL,
  `image` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `land`
--

CREATE TABLE `land` (
  `lId` int(10) NOT NULL,
  `pId` int(10) NOT NULL,
  `type` enum('廠房','土地') NOT NULL,
  `twPing` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `landrent`
--

CREATE TABLE `landrent` (
  `lId` int(11) NOT NULL,
  `price` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `landsell`
--

CREATE TABLE `landsell` (
  `lId` int(11) NOT NULL,
  `pricePerTwPing` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `message`
--

CREATE TABLE `message` (
  `msgId` int(10) NOT NULL,
  `reciever` int(10) NOT NULL,
  `sender` int(10) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `parkingspace`
--

CREATE TABLE `parkingspace` (
  `psId` int(10) NOT NULL,
  `hId` int(10) NOT NULL,
  `twPing` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `payment`
--

CREATE TABLE `payment` (
  `pId` int(11) NOT NULL,
  `payDate` date NOT NULL,
  `endDate` date NOT NULL,
  `class` enum('黃金','白金','鑽石') NOT NULL,
  `expDate` date NOT NULL,
  `cardNumber` text NOT NULL,
  `cost` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `post`
--

CREATE TABLE `post` (
  `pId` int(10) NOT NULL,
  `uId` int(10) NOT NULL,
  `city` enum('台北市','新北市','桃園市','新竹市','新竹縣','基隆市','宜蘭縣','台中市','彰化縣','苗栗縣','雲林縣','南投縣','高雄市','台南市','嘉義縣','嘉義市','屏東縣','花蓮縣','台東縣','金門縣','澎湖縣','連江縣') NOT NULL,
  `address` varchar(40) NOT NULL,
  `name` varchar(10) NOT NULL,
  `phone` text NOT NULL,
  `description` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `post`
--

INSERT INTO `post` (`pId`, `uId`, `city`, `address`, `name`, `phone`, `description`) VALUES
(1, 1, '台北市', '無', '翁', '1234567890', '妳好'),
(2, 2, '台北市', '無', '翁', '1234567890', '妳好'),
(3, 3, '台北市', '無', '翁', '1234567890', '妳好'),
(4, 4, '台北市', '無', '翁', '1234567890', '妳好'),
(5, 5, '台北市', '無', '翁', '1234567890', '妳好'),
(6, 6, '新北市', '無', '翁', '1234567890', '妳好'),
(7, 7, '新北市', '無', '翁', '1234567890', '妳好'),
(8, 8, '新北市', '無', '翁', '1234567890', '妳好'),
(9, 9, '桃園市', '無', '翁', '1234567890', '妳好'),
(10, 10, '桃園市', '無', '翁', '1234567890', '妳好'),
(11, 11, '桃園市', '無', '翁', '1234567890', '妳好'),
(12, 12, '新竹市', '無', '翁', '1234567890', '妳好');

-- --------------------------------------------------------

--
-- 資料表結構 `space`
--

CREATE TABLE `space` (
  `hId` int(10) NOT NULL,
  `spaceName` enum('房','廳','衛','陽台') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `uId` int(10) NOT NULL,
  `name` varchar(10) NOT NULL,
  `phone` text NOT NULL,
  `email` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `permission` enum('user','manager') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `availabletime`
--
ALTER TABLE `availabletime`
  ADD PRIMARY KEY (`pId`,`startTime`,`endTime`);

--
-- 資料表索引 `browses`
--
ALTER TABLE `browses`
  ADD PRIMARY KEY (`uId`,`pId`);

--
-- 資料表索引 `criticizes`
--
ALTER TABLE `criticizes`
  ADD PRIMARY KEY (`uId`,`pId`);

--
-- 資料表索引 `floor`
--
ALTER TABLE `floor`
  ADD PRIMARY KEY (`hId`,`floor`);

--
-- 資料表索引 `house`
--
ALTER TABLE `house`
  ADD PRIMARY KEY (`hId`);

--
-- 資料表索引 `image`
--
ALTER TABLE `image`
  ADD PRIMARY KEY (`hId`,`spaceName`);

--
-- 資料表索引 `land`
--
ALTER TABLE `land`
  ADD PRIMARY KEY (`lId`);

--
-- 資料表索引 `landrent`
--
ALTER TABLE `landrent`
  ADD PRIMARY KEY (`lId`);

--
-- 資料表索引 `landsell`
--
ALTER TABLE `landsell`
  ADD PRIMARY KEY (`lId`);

--
-- 資料表索引 `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`msgId`);

--
-- 資料表索引 `parkingspace`
--
ALTER TABLE `parkingspace`
  ADD PRIMARY KEY (`psId`);

--
-- 資料表索引 `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`pId`,`payDate`);

--
-- 資料表索引 `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`pId`);

--
-- 資料表索引 `space`
--
ALTER TABLE `space`
  ADD PRIMARY KEY (`hId`,`spaceName`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uId`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `house`
--
ALTER TABLE `house`
  MODIFY `hId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `land`
--
ALTER TABLE `land`
  MODIFY `lId` int(10) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `message`
--
ALTER TABLE `message`
  MODIFY `msgId` int(10) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `parkingspace`
--
ALTER TABLE `parkingspace`
  MODIFY `psId` int(10) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `post`
--
ALTER TABLE `post`
  MODIFY `pId` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `uId` int(10) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
