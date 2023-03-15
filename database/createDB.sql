
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nhl-data
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nhl-data` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `nhl-data` ;

-- -----------------------------------------------------
-- Table `nhl-data`.`Franchise`
-- id is 3 letter abbreviation (ex. PIT)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Franchise` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Franchise` (
  `id` VARCHAR(3) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `yearFounded` INT NOT NULL,
  `yearDefunct` INT NULL,
  `stanleyCups` INT NULL,
  `isActive` TINYINT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nhl-data`.`Season`
-- id is year (ex. 2017)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Season` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Season` (
  `id` INT NOT NULL,
  `year` INT NOT NULL,
  `championID` VARCHAR(7) NOT NULL,
  `presidentsTrophyID` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Season_Team1_idx` (`championID` ASC) VISIBLE,
  INDEX `fk_Season_Team2_idx` (`presidentsTrophyID` ASC) VISIBLE,
  CONSTRAINT `fk_Season_Team1`
    FOREIGN KEY (`championID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Season_Team2`
    FOREIGN KEY (`presidentsTrophyID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`Team`
-- id is three letter abbreviation and year (PIT2016)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Team` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Team` (
  `id` VARCHAR(7) NOT NULL,
  `franchiseID` VARCHAR(3) NOT NULL,
  `seasonID` INT NOT NULL,
  `teamName` VARCHAR(100) NOT NULL,
  `avgAge` INT NULL,
  `gamesPlayed` INT NOT NULL,
  `wins` INT NOT NULL,
  `losses` INT NOT NULL,
  `otLosses` INT NULL,
  `ties` INT NULL,
  `points` INT NOT NULL,
  `pointsPct` DECIMAL(3,3) NOT NULL,
  `goalsFor` INT NOT NULL,
  `goalsAgainst` INT NOT NULL,
  `simpleRatingSystem` DECIMAL(4,3) NOT NULL,
  `strengthOfSchedule` DECIMAL(4,3) NOT NULL,
  `goalsForPerGame` DECIMAL(4,2) NOT NULL,
  `goalsAgainstPerGame` DECIMAL(4,2) NOT NULL,
  `powerPlayGoals` INT NULL,
  `powerPlayOpportunities` INT NULL,
  `powerPlayPct` DECIMAL(4,2) NULL,
  `powerPlayGoalsAgainst` INT NULL,
  `powerPlayOpportunitiesAgainst` INT NULL,
  `penaltyKillPct` DECIMAL(4,2) NULL,
  `shortHandedGoals` INT NULL,
  `shortHandedGoalsAgainst` INT NULL,
  `shots` INT NULL,
  `shootingPct` DECIMAL(4,2) NULL,
  `shotsAgainst` INT NULL,
  `savePct` DECIMAL(3,3) NULL,
  `shutouts` INT NOT NULL,
  `isCurrent` TINYINT NOT NULL,
  `isPlayoffTeam` TINYINT NOT NULL,
  `result` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Team_Franchise_idx` (`franchiseID` ASC) VISIBLE,
  INDEX `fk_Team_Season1_idx` (`seasonID` ASC) VISIBLE,
  CONSTRAINT `fk_Team_Franchise`
    FOREIGN KEY (`franchiseID`)
    REFERENCES `nhl-data`.`Franchise` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Team_Season1`
    FOREIGN KEY (`seasonID`)
    REFERENCES `nhl-data`.`Season` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `nhl-data`.`PlayerInfo`
-- id is player name and birth year (ex. CrosbySidney1987)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`PlayerInfo` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`PlayerInfo` (
  `id` VARCHAR(100)  NOT NULL,
  `firstName` VARCHAR(100) NOT NULL,
  `lastName` VARCHAR(100) NOT NULL,
  `position` VARCHAR(2) NOT NULL,
  `height` VARCHAR(6) NULL,
  `weight` INT NULL,
  `draftPosition` INT NULL,
  `shoots` VARCHAR(1) NULL,
  `age` INT NULL,
  `isActive` TINYINT NOT NULL,
  `isHallOfFame` TINYINT NOT NULL,
  `jerseyNumber` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`Goalie`
-- id is season, player name, and birth year (ex. 2016FleuryMarcAndre1984)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Goalie` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Goalie` (
  `id` VARCHAR(100) NOT NULL,
  `teamID` VARCHAR(7) NOT NULL,
  `infoID` VARCHAR(100) NOT NULL,
  `isCurrent` TINYINT NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `gamesStarted` INT NULL,
  `wins` INT NOT NULL,
  `losses` INT NOT NULL,
  `tiesPlusOTLosses` INT NOT NULL,
  `goalsAllowed` INT NOT NULL,
  `shotsAgainst` INT NULL,
  `saves` INT NULL,
  `savePct` DECIMAL(3,3) NULL,
  `goalsAllowedAverage` DECIMAL(4,2) NOT NULL,
  `shutouts` VARCHAR(45) NOT NULL,
  `minutes` INT NULL,
  `qualityStarts` INT NULL,
  `qualityStartPct` DECIMAL(3,3) NULL,
  `reallyBadStarts` INT NULL,
  `relativeGoalsAllowedPct` INT NULL,
  `goalsSavedAboveAverage` DECIMAL(3,1) NULL,
  `ajdustedGoalsAllowedAvg` DECIMAL(3,1) NULL,
  `goaliePointShares` DECIMAL(4,2) NULL,
  `goals` INT NULL,
  `assists` INT NULL,
  `points` INT NULL,
  `penaltyMinutes` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Goalie_Team_idx` (`teamID` ASC) VISIBLE,
  INDEX `fk_Goalie_PlayerInfo1_idx` (`infoID` ASC) VISIBLE,
  CONSTRAINT `fk_Goalie_Team`
    FOREIGN KEY (`teamID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Goalie_PlayerInfo1`
    FOREIGN KEY (`infoID`)
    REFERENCES `nhl-data`.`PlayerInfo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`GoalieCareerStats`
-- id is avg plus player name and birth year (ex. AvgFleuryMarcAndre1984)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`GoalieCareerStats` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`GoalieCareerStats` (
  `id` VARCHAR(100) NOT NULL,
  `infoID` VARCHAR(100) NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `gamesStarted` INT NULL,
  `wins` INT NOT NULL,
  `losses` INT NOT NULL,
  `tiesPlusOTLosses` INT NOT NULL,
  `goalsAllowed` INT NOT NULL,
  `shotsAgainst` INT NULL,
  `saves` INT NULL,
  `savePct` DECIMAL(3,3) NULL,
  `goalsAllowedAverage` DECIMAL(4,2) NOT NULL,
  `shutouts` VARCHAR(45) NOT NULL,
  `minutes` INT NULL,
  `qualityStarts` INT NULL,
  `qualityStartPct` DECIMAL(3,3) NULL,
  `reallyBadStarts` INT NULL,
  `relativeGoalsAllowedPct` INT NULL,
  `goalsSavedAboveAverage` DECIMAL(3,1) NULL,
  `ajdustedGoalsAllowedAvg` DECIMAL(3,1) NULL,
  `goaliePointShares` DECIMAL(4,2) NULL,
  `goals` INT NULL,
  `assists` INT NULL,
  `points` INT NULL,
  `penaltyMinutes` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Goalie_PlayerInfo1_idx` (`infoID` ASC) VISIBLE,
  CONSTRAINT `fk_Goalie_PlayerInfo10`
    FOREIGN KEY (`infoID`)
    REFERENCES `nhl-data`.`PlayerInfo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`SeasonAverageGoalies`
-- id is season year plus GoalieAvg (2016GoalieAvg)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`SeasonAverageGoalies` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`SeasonAverageGoalies` (
  `id` VARCHAR(13) NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `gamesStarted` INT NULL,
  `wins` INT NOT NULL,
  `losses` INT NOT NULL,
  `tiesPlusOTLosses` INT NOT NULL,
  `goalsAllowed` INT NOT NULL,
  `shotsAgainst` INT NULL,
  `saves` INT NULL,
  `savePct` DECIMAL(3,3) NULL,
  `goalsAllowedAverage` DECIMAL(4,2) NOT NULL,
  `shutouts` VARCHAR(45) NOT NULL,
  `minutes` INT NULL,
  `qualityStarts` INT NULL,
  `qualityStartPct` DECIMAL(3,3) NULL,
  `reallyBadStarts` INT NOT NULL,
  `relativeGoalsAllowedPct` INT NULL,
  `goalsSavedAboveAverage` DECIMAL(3,1) NULL,
  `ajdustedGoalsAllowedAvg` DECIMAL(3,1) NULL,
  `goaliePointShares` DECIMAL(4,2) NULL,
  `goals` INT NULL,
  `assists` INT NULL,
  `points` INT NULL,
  `penaltyMinutes` INT NULL,
  `seasonID` INT NOT NULL,
  PRIMARY KEY (`id`, `reallyBadStarts`),
  INDEX `fk_SeasonAverageGoalies_Season1_idx` (`seasonID` ASC) VISIBLE,
  CONSTRAINT `fk_SeasonAverageGoalies_Season1`
    FOREIGN KEY (`seasonID`)
    REFERENCES `nhl-data`.`Season` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `nhl-data` ;

-- -----------------------------------------------------
-- Table `nhl-data`.`Game`
-- id is Home abbreviation, Away abbreviation, and date (ex. PITWSH20160302)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Game` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Game` (
  `id` VARCHAR(14) NOT NULL,
  `date` DATETIME NOT NULL,
  `homeTeamID` VARCHAR(7) NOT NULL,
  `awayTeamID` VARCHAR(7) NOT NULL,
  `result` VARCHAR(5) NOT NULL,
  `isOT` TINYINT NULL,
  `homePoints` INT NULL,
  `awayPoints` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Game_Team1_idx` (`homeTeamID` ASC) VISIBLE,
  INDEX `fk_Game_Team2_idx` (`awayTeamID` ASC) VISIBLE,
  CONSTRAINT `fk_Game_Team1`
    FOREIGN KEY (`homeTeamID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Game_Team2`
    FOREIGN KEY (`awayTeamID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`Leader`
-- id is year and category 2016Goals
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Leader` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Leader` (
  `id` VARCHAR(100) NOT NULL,
  `category` VARCHAR(100) NOT NULL,
  `value` DECIMAL(6,3) NOT NULL,
  `seasonID` INT NOT NULL,
  `playerID` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Leader_Season1_idx` (`seasonID` ASC) VISIBLE,
  INDEX `fk_Leader_PlayerInfo1_idx` (`playerID` ASC) VISIBLE,
  CONSTRAINT `fk_Leader_Season1`
    FOREIGN KEY (`seasonID`)
    REFERENCES `nhl-data`.`Season` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Leader_PlayerInfo1`
    FOREIGN KEY (`playerID`)
    REFERENCES `nhl-data`.`PlayerInfo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`SeasonAverageTeams`
-- id is season year plus TeamAvg (2016TeamAvg)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`SeasonAverageTeams` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`SeasonAverageTeams` (
  `id` VARCHAR(11) NOT NULL,
  `avgAge` INT NULL,
  `gamesPlayed` INT NOT NULL,
  `wins` INT NOT NULL,
  `losses` INT NOT NULL,
  `otLosses` INT NULL,
  `ties` INT NULL,
  `points` INT NOT NULL,
  `pointsPct` DECIMAL(3,3) NOT NULL,
  `goalsFor` INT NOT NULL,
  `goalsAgainst` INT NOT NULL,
  `simpleRatingSystem` DECIMAL(3,2) NULL DEFAULT 0.00,
  `powerPlayGoals` INT NULL,
  `powerPlayOpportunities` INT NULL,
  `powerPlayPct` DECIMAL(4,2) NULL,
  `powerPlayGoalsAgainst` INT NULL,
  `powerPlayOpportunitiesAgainst` INT NULL,
  `penaltyKillPct` DECIMAL(4,2) NULL,
  `shortHandedGoals` INT NULL,
  `shortHandedGoalsAgainst` INT NULL,
  `shots` INT NULL,
  `shootingPct` DECIMAL(4,2) NULL,
  `shotsAgainst` INT NULL,
  `savePct` DECIMAL(3,3) NULL,
  `shutouts` INT NOT NULL,
  `seasonID` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_SeasonAverageTeams_Season1_idx` (`seasonID` ASC) VISIBLE,
  CONSTRAINT `fk_SeasonAverageTeams_Season1`
    FOREIGN KEY (`seasonID`)
    REFERENCES `nhl-data`.`Season` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`Skater`
-- id is season, player name, and birth year (ex. 2016MalkinEvgeni1986)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`Skater` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`Skater` (
  `id` VARCHAR(100) NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `goals` INT NOT NULL,
  `assists` INT NOT NULL,
  `points` INT NOT NULL,
  `plusMinus` INT NULL,
  `penaltyMinutes` INT NULL,
  `evenStrengthGoals` INT NULL,
  `powerPlayGoals` INT NULL,
  `shortHandedGoals` INT NULL,
  `gameWinningGoals` INT NULL,
  `evenStrengthAssists` INT NULL,
  `powerPlayAssists` INT NULL,
  `shortHandedAssists` INT NULL,
  `shots` INT NULL,
  `shootingPct` DECIMAL(3,1) NULL,
  `totalShotAttempts` INT NULL,
  `timeOnIce` INT NULL,
  `averageTimeOnIce` VARCHAR(5) NULL,
  `faceoffWins` INT NULL,
  `faceOffLosses` INT NULL,
  `faceoffPct` DECIMAL(3,1) NULL,
  `blockedShots` INT NULL,
  `hits` INT NULL,
  `takeaways` INT NULL,
  `giveaways` INT NULL,
  `isCurrent` TINYINT NOT NULL,
  `infoID` VARCHAR(100) NOT NULL,
  `teamID` VARCHAR(7) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Skater_PlayerInfo1_idx` (`infoID` ASC) VISIBLE,
  INDEX `fk_Skater_Team1_idx` (`teamID` ASC) VISIBLE,
  CONSTRAINT `fk_Skater_PlayerInfo1`
    FOREIGN KEY (`infoID`)
    REFERENCES `nhl-data`.`PlayerInfo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Skater_Team1`
    FOREIGN KEY (`teamID`)
    REFERENCES `nhl-data`.`Team` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`SkaterCareerStats`
-- id is avg plus player name and birth year (ex. AvgCrosbySidney1987)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`SkaterCareerStats` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`SkaterCareerStats` (
  `id` VARCHAR(100) NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `goals` INT NOT NULL,
  `assists` INT NOT NULL,
  `points` INT NOT NULL,
  `plusMinus` INT NULL,
  `penaltyMinutes` INT NULL,
  `evenStrengthGoals` INT NULL,
  `powerPlayGoals` INT NULL,
  `shortHandedGoals` INT NULL,
  `gameWinningGoals` INT NULL,
  `evenStrengthAssists` INT NULL,
  `powerPlayAssists` INT NULL,
  `shortHandedAssists` INT NULL,
  `shots` INT NULL,
  `shootingPct` DECIMAL(3,1) NULL,
  `totalShotAttempts` INT NULL,
  `timeOnIce` INT NULL,
  `averageTimeOnIce` VARCHAR(5) NULL,
  `faceoffWins` INT NULL,
  `faceOffLosses` INT NULL,
  `faceoffPct` DECIMAL(3,1) NULL,
  `blockedShots` INT NULL,
  `hits` INT NULL,
  `takeaways` INT NULL,
  `giveaways` INT NULL,
  `infoID` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_SkaterAverageStats_PlayerInfo1_idx` (`infoID` ASC) VISIBLE,
  CONSTRAINT `fk_SkaterAverageStats_PlayerInfo1`
    FOREIGN KEY (`infoID`)
    REFERENCES `nhl-data`.`PlayerInfo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nhl-data`.`seasonAverageSkaters`
-- id is season year plus SkaterAvg (2016SkaterAvg)
-- -----------------------------------------------------
DROP TABLE IF EXISTS `nhl-data`.`seasonAverageSkaters` ;

CREATE TABLE IF NOT EXISTS `nhl-data`.`seasonAverageSkaters` (
  `id` VARCHAR(13) NOT NULL,
  `gamesPlayed` INT NOT NULL,
  `goals` INT NOT NULL,
  `assists` INT NOT NULL,
  `points` INT NOT NULL,
  `plusMinus` INT NULL,
  `penaltyMinutes` INT NULL,
  `evenStrengthGoals` INT NULL,
  `powerPlayGoals` INT NULL,
  `shortHandedGoals` INT NULL,
  `gameWinningGoals` INT NULL,
  `evenStrengthAssists` INT NULL,
  `powerPlayAssists` INT NULL,
  `shortHandedAssists` INT NULL,
  `shots` INT NULL,
  `shootingPct` DECIMAL(3,1) NULL,
  `totalShotAttempts` INT NULL,
  `timeOnIce` INT NULL,
  `averageTimeOnIce` VARCHAR(5) NULL,
  `faceoffWins` INT NULL,
  `faceOffLosses` INT NULL,
  `faceoffPct` DECIMAL(3,1) NULL,
  `blockedShots` INT NULL,
  `hits` INT NULL,
  `takeaways` INT NULL,
  `giveaways` INT NULL,
  `seasonID` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_seasonAverageSkaters_Season1_idx` (`seasonID` ASC) VISIBLE,
  CONSTRAINT `fk_seasonAverageSkaters_Season1`
    FOREIGN KEY (`seasonID`)
    REFERENCES `nhl-data`.`Season` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


