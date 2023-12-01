CREATE DATABASE IF NOT EXISTS pokemonapp;

USE pokemonapp;

DROP TABLE IF EXISTS gamesave;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS pokedex;
DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS allpokemon;


CREATE TABLE gamesave
(
    saveid       int not null AUTO_INCREMENT,
    trainername    varchar(64) not null,
    PRIMARY KEY  (saveid),
    UNIQUE       (trainername)
);

ALTER TABLE gamesave AUTO_INCREMENT = 101;  -- starting value

CREATE TABLE inventory
(
    saveid            int not null,
    pokeballs         int not null,
    coins             int not null,

    FOREIGN KEY (saveid) REFERENCES gamesave(saveid)
);

CREATE TABLE pokemon
(
    pokemonid         int not null AUTO_INCREMENT,

    name              varchar(50) not null,  -- original pokemon name (eg. Pikachu)
    nickname          varchar(50) not null,  -- user-given nickname
    type              varchar(50) not null,  -- pokemon type (water, fire, etc)
    rarity            varchar(50) not null,  -- pokemon rarity (common or legendary)
    level             int not null DEFAULT 1,

    PRIMARY KEY (pokemonid)
);

CREATE TABLE pokedex
(
    saveid            int not null,
    pokemonid         int not null,

    FOREIGN KEY (saveid) REFERENCES gamesave(saveid),
    FOREIGN KEY (pokemonid) REFERENCES pokemon(pokemonid)

);

CREATE TABLE allpokemon
(
    defaultid         int not null AUTO_INCREMENT,
    name              varchar(50) not null,  -- original pokemon name (eg. Pikachu)
    type              varchar(50) not null,  -- pokemon type (water, fire, etc)
    rarity            varchar(50) not null,  -- pokemon rarity (common or legendary)

    PRIMARY KEY (defaultid)
);

--
-- Insert all pokemon from generation 1:
-- 

INSERT INTO allpokemon (name, type, rarity) VALUES
('Bulbasaur', 'Grass', 'Common'),
('Ivysaur', 'Grass', 'Common'),
('Venusaur', 'Grass', 'Common'),
('Charmander', 'Fire', 'Common'),
('Charmeleon', 'Fire', 'Common'),
('Charizard', 'Fire', 'Common'),
('Squirtle', 'Water', 'Common'),
('Wartortle', 'Water', 'Common'),
('Blastoise', 'Water', 'Common'),
('Caterpie', 'Bug', 'Common'),
('Metapod', 'Bug', 'Common'),
('Butterfree', 'Bug', 'Common'),
('Weedle', 'Bug', 'Common'),
('Kakuna', 'Bug', 'Common'),
('Beedrill', 'Bug', 'Common'),
('Pidgey', 'Normal', 'Common'),
('Pidgeotto', 'Normal', 'Common'),
('Pidgeot', 'Normal', 'Common'),
('Rattata', 'Normal', 'Common'),
('Raticate', 'Normal', 'Common'),
('Spearow', 'Normal', 'Common'),
('Fearow', 'Normal', 'Common'),
('Ekans', 'Poison', 'Common'),
('Arbok', 'Poison', 'Common'),
('Pikachu', 'Electric', 'Common'),
('Raichu', 'Electric', 'Common'),
('Sandshrew', 'Ground', 'Common'),
('Sandslash', 'Ground', 'Common'),
('Nidoran♀', 'Poison', 'Common'),
('Nidorina', 'Poison', 'Common'),
('Nidoqueen', 'Poison', 'Common'),
('Nidoran♂', 'Poison', 'Common'),
('Nidorino', 'Poison', 'Common'),
('Nidoking', 'Poison', 'Common'),
('Clefairy', 'Fairy', 'Common'),
('Clefable', 'Fairy', 'Common'),
('Vulpix', 'Fire', 'Common'),
('Ninetales', 'Fire', 'Common'),
('Jigglypuff', 'Normal', 'Common'),
('Wigglytuff', 'Normal', 'Common'),
('Zubat', 'Poison', 'Common'),
('Golbat', 'Poison', 'Common'),
('Oddish', 'Grass', 'Common'),
('Gloom', 'Grass', 'Common'),
('Vileplume', 'Grass', 'Common'),
('Paras', 'Bug', 'Common'),
('Parasect', 'Bug', 'Common'),
('Venonat', 'Bug', 'Common'),
('Venomoth', 'Bug', 'Common'),
('Diglett', 'Ground', 'Common'),
('Dugtrio', 'Ground', 'Common'),
('Meowth', 'Normal', 'Common'),
('Persian', 'Normal', 'Common'),
('Psyduck', 'Water', 'Common'),
('Golduck', 'Water', 'Common'),
('Mankey', 'Fighting', 'Common'),
('Primeape', 'Fighting', 'Common'),
('Growlithe', 'Fire', 'Common'),
('Arcanine', 'Fire', 'Common'),
('Poliwag', 'Water', 'Common'),
('Poliwhirl', 'Water', 'Common'),
('Poliwrath', 'Water', 'Common'),
('Abra', 'Psychic', 'Common'),
('Kadabra', 'Psychic', 'Common'),
('Alakazam', 'Psychic', 'Common'),
('Machop', 'Fighting', 'Common'),
('Machoke', 'Fighting', 'Common'),
('Machamp', 'Fighting', 'Common'),
('Bellsprout', 'Grass', 'Common'),
('Weepinbell', 'Grass', 'Common'),
('Victreebel', 'Grass', 'Common'),
('Tentacool', 'Water', 'Common'),
('Tentacruel', 'Water', 'Common'),
('Geodude', 'Rock', 'Common'),
('Graveler', 'Rock', 'Common'),
('Golem', 'Rock', 'Common'),
('Ponyta', 'Fire', 'Common'),
('Rapidash', 'Fire', 'Common'),
('Slowpoke', 'Water', 'Common'),
('Slowbro', 'Water', 'Common'),
('Magnemite', 'Electric', 'Common'),
('Magneton', 'Electric', 'Common'),
('Farfetchd', 'Normal', 'Common'),
('Doduo', 'Normal', 'Common'),
('Dodrio', 'Normal', 'Common'),
('Seel', 'Water', 'Common'),
('Dewgong', 'Water', 'Common'),
('Grimer', 'Poison', 'Common'),
('Muk', 'Poison', 'Common'),
('Shellder', 'Water', 'Common'),
('Cloyster', 'Water', 'Common'),
('Gastly', 'Ghost', 'Common'),
('Haunter', 'Ghost', 'Common'),
('Gengar', 'Ghost', 'Common'),
('Onix', 'Rock', 'Common'),
('Drowzee', 'Psychic', 'Common'),
('Hypno', 'Psychic', 'Common'),
('Krabby', 'Water', 'Common'),
('Kingler', 'Water', 'Common'),
('Voltorb', 'Electric', 'Common'),
('Electrode', 'Electric', 'Common'),
('Exeggcute', 'Grass', 'Common'),
('Exeggutor', 'Grass', 'Common'),
('Cubone', 'Ground', 'Common'),
('Marowak', 'Ground', 'Common'),
('Hitmonlee', 'Fighting', 'Common'),
('Hitmonchan', 'Fighting', 'Common'),
('Lickitung', 'Normal', 'Common'),
('Koffing', 'Poison', 'Common'),
('Weezing', 'Poison', 'Common'),
('Rhyhorn', 'Ground', 'Common'),
('Rhydon', 'Ground', 'Common'),
('Chansey', 'Normal', 'Common'),
('Tangela', 'Grass', 'Common'),
('Kangaskhan', 'Normal', 'Common'),
('Horsea', 'Water', 'Common'),
('Seadra', 'Water', 'Common'),
('Goldeen', 'Water', 'Common'),
('Seaking', 'Water', 'Common'),
('Staryu', 'Water', 'Common'),
('Starmie', 'Water', 'Common'),
('Mr. Mime', 'Psychic', 'Common'),
('Scyther', 'Bug', 'Common'),
('Jynx', 'Ice', 'Common'),
('Electabuzz', 'Electric', 'Common'),
('Magmar', 'Fire', 'Common'),
('Pinsir', 'Bug', 'Common'),
('Tauros', 'Normal', 'Common'),
('Magikarp', 'Water', 'Common'),
('Gyarados', 'Water', 'Common'),
('Lapras', 'Water', 'Common'),
('Ditto', 'Normal', 'Common'),
('Eevee', 'Normal', 'Common'),
('Vaporeon', 'Water', 'Common'),
('Jolteon', 'Electric', 'Common'),
('Flareon', 'Fire', 'Common'),
('Porygon', 'Normal', 'Common'),
('Omanyte', 'Rock', 'Common'),
('Omastar', 'Rock', 'Common'),
('Kabuto', 'Rock', 'Common'),
('Kabutops', 'Rock', 'Common'),
('Aerodactyl', 'Rock', 'Common'),
('Snorlax', 'Normal', 'Common'),
('Articuno', 'Ice', 'Legendary'),
('Zapdos', 'Electric', 'Legendary'),
('Moltres', 'Fire', 'Legendary'),
('Dratini', 'Dragon', 'Common'),
('Dragonair', 'Dragon', 'Common'),
('Dragonite', 'Dragon', 'Common'),
('Mewtwo', 'Psychic', 'Legendary'),
('Mew', 'Psychic', 'Legendary');

--
-- Insert all pokemon from generation 2:
-- 

INSERT INTO allpokemon (name, type, rarity) VALUES
('Chikorita', 'Grass', 'Common'),
('Bayleef', 'Grass', 'Common'),
('Meganium', 'Grass', 'Common'),
('Cyndaquil', 'Fire', 'Common'),
('Quilava', 'Fire', 'Common'),
('Typhlosion', 'Fire', 'Common'),
('Totodile', 'Water', 'Common'),
('Croconaw', 'Water', 'Common'),
('Feraligatr', 'Water', 'Common'),
('Sentret', 'Normal', 'Common'),
('Furret', 'Normal', 'Common'),
('Hoothoot', 'Normal', 'Common'),
('Noctowl', 'Normal', 'Common'),
('Ledyba', 'Bug', 'Common'),
('Ledian', 'Bug', 'Common'),
('Spinarak', 'Bug', 'Common'),
('Ariados', 'Bug', 'Common'),
('Crobat', 'Poison', 'Common'),
('Chinchou', 'Water', 'Common'),
('Lanturn', 'Water', 'Common'),
('Pichu', 'Electric', 'Common'),
('Cleffa', 'Fairy', 'Common'),
('Igglybuff', 'Normal', 'Common'),
('Togepi', 'Fairy', 'Common'),
('Togetic', 'Fairy', 'Common'),
('Natu', 'Psychic', 'Common'),
('Xatu', 'Psychic', 'Common'),
('Mareep', 'Electric', 'Common'),
('Flaaffy', 'Electric', 'Common'),
('Ampharos', 'Electric', 'Common'),
('Bellossom', 'Grass', 'Common'),
('Marill', 'Water', 'Common'),
('Azumarill', 'Water', 'Common'),
('Sudowoodo', 'Rock', 'Common'),
('Politoed', 'Water', 'Common'),
('Hoppip', 'Grass', 'Common'),
('Skiploom', 'Grass', 'Common'),
('Jumpluff', 'Grass', 'Common'),
('Aipom', 'Normal', 'Common'),
('Sunkern', 'Grass', 'Common'),
('Sunflora', 'Grass', 'Common'),
('Yanma', 'Bug', 'Common'),
('Wooper', 'Water', 'Common'),
('Quagsire', 'Water', 'Common'),
('Espeon', 'Psychic', 'Common'),
('Umbreon', 'Dark', 'Common'),
('Murkrow', 'Dark', 'Common'),
('Slowking', 'Water', 'Common'),
('Misdreavus', 'Ghost', 'Common'),
('Unown', 'Psychic', 'Common'),
('Wobbuffet', 'Psychic', 'Common'),
('Girafarig', 'Normal', 'Common'),
('Pineco', 'Bug', 'Common'),
('Forretress', 'Bug', 'Common'),
('Dunsparce', 'Normal', 'Common'),
('Gligar', 'Ground', 'Common'),
('Steelix', 'Steel', 'Common'),
('Snubbull', 'Fairy', 'Common'),
('Granbull', 'Fairy', 'Common'),
('Qwilfish', 'Water', 'Common'),
('Scizor', 'Bug', 'Common'),
('Shuckle', 'Bug', 'Common'),
('Heracross', 'Bug', 'Common'),
('Sneasel', 'Dark', 'Common'),
('Teddiursa', 'Normal', 'Common'),
('Ursaring', 'Normal', 'Common'),
('Slugma', 'Fire', 'Common'),
('Magcargo', 'Fire', 'Common'),
('Swinub', 'Ice', 'Common'),
('Piloswine', 'Ice', 'Common'),
('Corsola', 'Water', 'Common'),
('Remoraid', 'Water', 'Common'),
('Octillery', 'Water', 'Common'),
('Delibird', 'Ice', 'Common'),
('Mantine', 'Water', 'Common'),
('Skarmory', 'Steel', 'Common'),
('Houndour', 'Dark', 'Common'),
('Houndoom', 'Dark', 'Common'),
('Kingdra', 'Water', 'Common'),
('Phanpy', 'Ground', 'Common'),
('Donphan', 'Ground', 'Common'),
('Porygon2', 'Normal', 'Common'),
('Stantler', 'Normal', 'Common'),
('Smeargle', 'Normal', 'Common'),
('Tyrogue', 'Fighting', 'Common'),
('Hitmontop', 'Fighting', 'Common'),
('Smoochum', 'Ice', 'Common'),
('Elekid', 'Electric', 'Common'),
('Magby', 'Fire', 'Common'),
('Miltank', 'Normal', 'Common'),
('Blissey', 'Normal', 'Common'),
('Raikou', 'Electric', 'Legendary'),
('Entei', 'Fire', 'Legendary'),
('Suicune', 'Water', 'Legendary'),
('Larvitar', 'Rock', 'Common'),
('Pupitar', 'Rock', 'Common'),
('Tyranitar', 'Rock', 'Common'),
('Lugia', 'Psychic', 'Legendary'),
('Ho-Oh', 'Fire', 'Legendary'),
('Celebi', 'Psychic', 'Legendary');

--
-- creating user accounts for database access:
--
-- ref: https://dev.mysql.com/doc/refman/8.0/en/create-user.html
--

DROP USER IF EXISTS 'pokemonapp-read-only';
DROP USER IF EXISTS 'pokemonapp-read-write';

CREATE USER 'pokemonapp-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'pokemonapp-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON pokemonapp.* 
      TO 'pokemonapp-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON pokemonapp.* 
      TO 'pokemonapp-read-write';

FLUSH PRIVILEGES;

--
-- done
--
