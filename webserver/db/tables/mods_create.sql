create table mods (
   mod_id integer not null auto_increment,
   mod_name varchar(255) not null,
   mod_hash varchar(255) not null,
   mod_url varchar(255) not null default '',

   primary key(mod_id)
);

