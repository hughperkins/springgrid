# maps that an ai can use
create table ais_allowedmaps (
   ai_id integer not null,
   mapname varchar(255) not null,
   maphash varchar(255) not null
);

