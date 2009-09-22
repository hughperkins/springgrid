# matchreqeusts that have been given to a calcengine to process
# note: date/time is a string in format yyyymmddhhmmss
# that way, we don't need db specific functions to handle them
create table matchrequests_inprogress (
   matchrequest_id integer not null,
   calcengine_id integer not null,
   datetimeassigned varchar(255) not null,

   primary key (matchrequest_id)
);

