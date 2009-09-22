create table matchrequestqueue (
   matchrequest_id integer not null,
   ai0name varchar(255) not null,
   ai0version varchar(255) not null,
   ai1name varchar(255) not null,
   ai1version varchar(255) not null,
   mapname varchar(255) not null,
   maphash varchar(255) not null,
   modname varchar(255) not null,
   modhash varchar(255) not null,
   cheatingallowed varchar(255) not null default 'yes'
);

