# test data obviously...

insert into accounts (username, userfullname, passwordsalt, passwordhash) values ('admin', 'admin','r3r3rnbkl35hl5jgl3rlaekgt4t',md5(concat('admin','r3r3rnbkl35hl5jgl3rlaekgt4t') ) );
insert into accounts (username, userfullname, passwordsalt, passwordhash ) values ('guest', 'guest','aerg4g85htgh2fg5ghegrg4g24g', md5(concat('guest','aerg4g85htgh2fg5ghegrg4g24g')));

