create table mods (
   mod_id integer not null,
   modname varchar(255) not null,
   modhash varchar(255) not null,
   modurl varchar(255) not null default ''
);

