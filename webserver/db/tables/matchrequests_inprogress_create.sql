# matchreqeusts that have been given to a calcengine to process
# note: date/time is a string in format yyyymmddhhmmss
# that way, we don't need db specific functions to handle them
create table matchrequests_inprogress (
   matchrequest_id integer,
   calcengine_id integer,
   datetimeassigned varchar(255)
);

