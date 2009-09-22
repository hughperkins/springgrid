# stores each ai, on a per version basis
create table ais (
   ai_id integer not null,
   ai_name varchar(255) not null,
   ai_version varchar(255) not null,
   ai_downloadurl varchar(255) not null,
   ai_dev_id integer not null
);

