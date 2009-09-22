# list of mods that each AI can use
create table ais_allowedmods (
   ai_id integer not null,
   modname varchar(255) not null,
   modhash varchar(255) not null
);

