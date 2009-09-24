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

# groups of leagues
# for example, one could group together all cheating leagues
# or all water leagues
# etc ...
#
# leaguegroups can overlap just fine, ie a league can be
# in multiple leaguegroups

create table leaguegroups (
   leaguegroup_id integer not null auto_increment,

   leaguegroup_name varchar(255) not null,
   leaguegroup_creatorid integer not null, # the guy who created it, from accounts

   primary key ( leaguegroup_id )
);

# make sure leagegroup names are unique...
alter table leaguegroups add unique key ( leaguegroup_name );

