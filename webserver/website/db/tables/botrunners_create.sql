# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#  more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in the file licence.txt; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
# 1307 USA
# You can find the licence also on the web at:
# http://www.opensource.org/licenses/gpl-license.php
#

create table botrunners (
   botrunner_id integer not null auto_increment,
   botrunner_name varchar(255) not null,
   botrunner_owneraccountid integer not null,
   botrunner_sharedsecret varchar(255) not null,
   botrunner_lastpingtime varchar(255),
   botrunner_lastpingstatus varchar(255),

   primary key(botrunner_id)
);

alter table botrunners add unique key (botrunner_name );


