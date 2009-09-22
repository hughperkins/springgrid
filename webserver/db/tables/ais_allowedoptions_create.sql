# list of options valid for use by each ai
#
# example:
# (1, 'cheatingon', 'yes')
# (1, 'cheatingoff', 'yes')

create table ais_allowedoptions (
   ai_id integer not null,
   optionname varchar(255),
   optionallowed varchar(255) not null default 'no'
);

