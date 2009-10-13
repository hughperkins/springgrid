create table botrunner_supportedmods (
   botrunner_id integer not null,
   mod_id integer not null,
   
   primary key (botrunner_id, mod_id )
);

