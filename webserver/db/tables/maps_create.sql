create table maps (
   map_id integer not null auto_increment,
   map_name varchar(255) not null,
   map_hash varchar(255) not null,
   map_url varchar(255) not null default '',

   primary key (map_id)
);

alter table maps add unique key (map_name);

