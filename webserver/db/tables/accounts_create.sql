# accounts for admin and stuff

# passwords in clear for now, until someone changes that, or shows me
# how to change that, or both...

create table accounts (
   username varchar(255) not null,
   password varchar(255) not null
);

alter table accounts add primary key(username);

