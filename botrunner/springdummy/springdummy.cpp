// Copyright Hugh Perkins 2009
// hughperkins@gmail.com http://manageddreams.com
//
// This program is free software; you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by the
// Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
// or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
//  more details.
//
// You should have received a copy of the GNU General Public License along
// with this program in the file licence.txt; if not, write to the
// Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
// 1307 USA
// You can find the licence also on the web at:
// http://www.opensource.org/licenses/gpl-license.php
//

#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <fstream>
#include <sstream>

#ifdef WIN32
#define FS "\\"
#else
#define FS "/"
#endif

using namespace std;

string endgamemessageprefix = "[   024131] Team";
string endgamemessagepostfix = " kicked the bucket";

void sleep_seconds( int seconds ) {
#ifdef WIN32
Sleep( seconds * 1000 );
#else
sleep( seconds );
#endif
}

void hang() {
         while(true) {
            sleep_seconds(1000);
         }         
}

ofstream Infolog("infolog.txt");

void openInfolog() {
   // I think it's opened by the constructor
}

void writeToInfolog( string message ) {
   Infolog << message << endl;
}

void createfakereplay() {
   ostringstream replayfilename;
   replayfilename << "demos" << FS << rand();
   ofstream replayfile( replayfilename.str().c_str() );
   // add in path to file in infolog:
   ostringstream messagestream;
   messagestream << "[      0] Recording demo " << replayfilename.str() << endl;
   writeToInfolog( messagestream.str() );
   // let's write about 500k of stuff...
   // though after zipping it it will be much smaller
   // use rand to prevent zipping being too powerful
   for( int i = 0; i < 20000; i++ ) {
      replayfile << "blah " << rand() << " blah " << rand() << " blah " << rand() << "..." << endl;
   }
   replayfile << "if you see this, the whole fake-replay was transmitted ok." << endl;
}

void writeStuffToInfologbis() {
   for( int i = 0; i < 100; i++ ) {
      writeToInfolog("blah");
      writeToInfolog("foo");
   }
}

void writeStuffToInfolog() {
   //for( int i = 0; i < 3; i++ ) {
   writeStuffToInfologbis();
   sleep_seconds(1);
   //}
   //writeStuffToInfologbis();
}

int main( int argc, char** argv ) {
   srand((unsigned)time(0)); // seed the pseudo-random numbers with system time
   int randomnumber = rand() % 5; // use % 6 if you want to simulate hangs too
   int a = 0;
   int b = 0;
   ostringstream messagestream;
   cout << "randomnumber: " << randomnumber << endl;
   switch( randomnumber ) {
      case 3:   // crash
         cout << "crashing" << endl;
         writeStuffToInfolog();
         createfakereplay();
         writeStuffToInfolog();
         writeStuffToInfolog();
         a = 0;
         b = 5 / a;
         break;

      case 4:   // crash
         cout << "crashing, no replay" << endl;
         writeStuffToInfolog();
         writeStuffToInfolog();
         writeStuffToInfolog();
         a = 0;
         b = 5 / a;
         break;

      case 5:   // hang 
         cout << "hanging" << endl;
         writeStuffToInfolog();
         createfakereplay();
         writeStuffToInfolog();
         writeStuffToInfolog();
         hang();
         break;

      case 2:   // ai0 dies
         cout << "ai0 dieing..." << endl;
         writeStuffToInfolog();
         createfakereplay();
         writeStuffToInfolog();
         writeStuffToInfolog();

         messagestream << endgamemessageprefix << 0 << endgamemessagepostfix;
         writeToInfolog( messagestream.str() );
         hang();
         break;

      case 1:   // ai1 dies
         cout << "ai1 dieing..." << endl;
         writeStuffToInfolog();
         createfakereplay();
         writeStuffToInfolog();
         writeStuffToInfolog();

         messagestream << endgamemessageprefix << 1 << endgamemessagepostfix;
         writeToInfolog( messagestream.str() );
         hang();
         break;

      case 0:   // both ais die
         cout << "both dieing..." << endl;
         writeStuffToInfolog();
         createfakereplay();
         writeStuffToInfolog();
         writeStuffToInfolog();

         messagestream << endgamemessageprefix << 0 << endgamemessagepostfix;
         writeToInfolog( messagestream.str() );
         messagestream << endgamemessageprefix << 1 << endgamemessagepostfix;
         writeToInfolog( messagestream.str() );
         hang();
         break;

   }
   return 0;
}

