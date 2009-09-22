create table aidevs (
   aidev_id integer not null,
   aidev_fullname varchar(255) not null,
   aidev_emailaddress varchar(255) not null default '',
   aidev_password varchar(255) not null
);
