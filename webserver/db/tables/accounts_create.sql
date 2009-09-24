# accounts for admin and stuff

# passwords in clear for now, until someone changes that, or shows me
# how to change that, or both...

create table accounts (
   account_id integer not null auto_increment,
   username varchar(255) not null,
   userfullname varchar(255) not null default '',
   useremailaddress varchar(255) not null default '',
   password varchar(255) not null,

   primary key (account_id)
);

alter table accounts add unique key(username);

