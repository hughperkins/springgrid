create table botrunner_supportedmaps (
   botrunner_id integer not null,
   map_id integer not null,
   
   primary key (botrunner_id, map_id )
);

