# cookie storage

create table cookies (
   cookiereference varchar(255) not null,
   username varchar(255) not null
);

alter table cookies add primary key (cookiereference );

