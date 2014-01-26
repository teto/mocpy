#/usr/bin/python3

import select
import socket
import asyncore
import logging
import sys
# from struct import *
import struct
import threading

# TODO use python3.4 enums
class State:
    Play, Stop, Pause = range(1,4)


    def __str__(self):
        return "invalid __str__"

    def __repr__(self):
        return "invalid repr"
    # Play = 0x01
    # Stop = 0x02
    # Pause = 0x03

states = {
    State.Play : "play",
    State.Pause : "pause",
    State.Stop : "stop"
}


class Event:
    State = 1  #server has changed the state */
    EV_CTIME = 2 #/* current time of the song has changed */
    EV_SRV_ERROR = 4 # an error occurred */
    EV_BUSY = 5 # another client is connected to the server */
    Data = 6 # data in response to a request will arrive */
    EV_BITRATE = 7 #/* the bitrate has changed */
    EV_RATE = 8 #/* the rate has changed */
    EV_CHANNELS = 9 #/* the number of channels has changed */
    EV_EXIT = 10 # /* the server is about to exit */
    # EV_PONG     0x0b /* response for CMD_PING */
    # EV_OPTIONS  0x0c /* the options has changed */
    # EV_SEND_PLIST   0x0d /* request for sending the playlist */
    # EV_TAGS     0x0e /* tags for the current file have changed */
    # EV_STATUS_MSG   0x0f /* followed by a status message */
    # EV_MIXER_CHANGE 0x10 /* the mixer channel was changed */
    # EV_FILE_TAGS    0x11 /* tags in a response for tags request */
    # EV_AVG_BITRATE  0x12 /* average bitrate has changed (new song) */
    EV_AUDIO_START = 19 # 0x13 /* playing of audio has started */
    EV_AUDIO_STOP = 20 #  0x14 /* playing of audio has stopped */

eventsStr = {
    Event.State : "server changed state"

}

class Command:
    Play   = 0x00 #/* play the first element on the list */
    List_Clear  = 0x01 #/* clear the list */
    List_Add    = 0x02 #/* add an item to the list */
    Stop    = 0x04 #/* stop playing */
    Pause   = 0x05 #/* pause */
    Unpause = 0x06 #/* unpause */
# CMD_LIST_ADD
# CMD_DISCONNECT
    Get_Ctime = 0x0d # get current song time
    Get_State = 0x13

    def pack(self):
        return struct.pack('i',)

# class Player:
#     def __init__(self,controller):
#         self._ctrl ) controller
    


class MocClient:

    def __init__(self, path):
        self._sk = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
        self._sk.connect(path)
        self._cb = {}

    def add(self, file):
        self._send_int( Command.List_Add);
        self._send_str( "/home/teto/Musique/Pharrell - Happy.mp3" );

    @property
    # def state(self):
    #     return self._state

    # @state.setter
    # def state(self, value):
    #     self._state = value

    #     self._send_int( CMD_, )
    
    # TODO je ne touche pas a la playlist
    # def playlist(self):
    def register_cb(eventType, fn):
        # TODO insert
        # TODO check fn is callable and accept a data
        self._cb[eventType] = fn

    # def play(self):
    #     self._send_int( Command.Play )

    # TODO launch threads ?
    # handlevents
    def run(self):
        # TODO it should block ?
        outputs = [ self._sk ]
        inputs = [ ]
        potential_errs = [  ]
        timeout=1
        while True:
            print("Waiting for event")

            readable, writable, in_error = \
                           select.select(
                              outputs,
                              inputs,
                              [],
                              timeout
                              )

            if len(readable) > 0:
            # # 
                print ("A socket is ready")
            
                # for s in ready_to_read:
                # 2nd params are flags
                eventType = self._get_int()
                if eventType:
                    # = data[0]
                    # print ('Received data',repr(data) )
                    print( " event type: %d"%eventType)
                    # result is a tuple 
                    # eventType, *rest  = struct.unpack('i', data[:4] )
                    # type = event[0]
                    # eventType = event[0]
                    # print( "rest", rest)
                    if eventType == Event.Data:
                        print("Additionnal data follows")
                        state = self._get_int()
                        # state, *_ = struct.unpack('i', data[4:8] )
                        print("state %s"% states[state] )

                    elif eventType == Event.State:
                        print("Changed state")
                    elif eventType == Event.EV_AUDIO_START:
                        print("=> Audio started !")
                    elif eventType == Event.EV_AUDIO_STOP:
                        print("=> Audio stopped !")
                    # todo that should be an event ?
                    # handle_server_event()



    #loop
    def prompt(self):
        print("What do yo uwant to do ?\n"
        "-Play (p)\n"
        "-stop (s)\n"
        "-List (l)\n"
        "-pAuse (a)\n"
        "-Unpause (u)\n"
        "-Get state (g)\n"
        "-or nothing (other keys)?")

        cmd = input()

        if cmd == 's':
            # sk.send( CMD_STOP))
            print("Sending command stop")

            
            self._send_int( Command.Stop)

        elif cmd == 'p': 
            print("Start playing")
            self.add( "add item")
            self._send_int( Command.Play)
            # keep empty to resumeplaylist
            # self._send_str( ) 
        elif cmd == 'l':
            print("not impelmented")
        elif cmd == 'g':
            self._send_int( Command.Get_State)
            
        else:
            print("Do nothing")

    def _get_str(self):
        # self._sk
        strLength = self._get_int()
        data = self._sk.recv(strLength,0)
        return struct.unpack("s",data)

    def _get_int(self):
        # size of an int
        data = self._sk.recv( struct.calcsize('i'),0)
        return struct.unpack('i',data)[0]
        # return data

    def _send_str(self,value):
        # self._sk.send()
        self._send_int( len(value))
        #bytes(
        #'utf8'
        self._sk.send( struct.pack("s", value.encode() ) )
        

    def _send_int( self, value ):
        # convert cmd to integer
        self._sk.send( struct.pack("i", value) )


    def close(self):
        self._sk.close();





# CMD_GET_QUEUE
def send_event(type,data):
    sk.send(type)


try:
    c = MocClient('/home/teto/.moc/socket2')
    # c.run()
    t = threading.Thread( name="mocClient",target=c.run, args=[])
    t.start()

    while True:
        c.prompt();
# sk.setblocking(False)
# look at commadns from interface.h
# , msg
except socket.error as e:
    print ( e )
    sys.exit(1)



#define EV_STATE 0x01
#EV_AUDIO_START
#EV_AUDIO_STOP
#define EV_PONG0x0b /* response for CMD_PING */
# send event
# send_event( bytes(EV_AUDIO_STOP), '')



# /* Receive data for the given type of event and return them. Return NULL if
#  * there is no data for the event. */
# static void *get_event_data (const int type)
# {
#     switch (type) {
#         case EV_PLIST_ADD:
#         case EV_QUEUE_ADD:
#             return recv_item_from_srv ();
#         case EV_PLIST_DEL:
#         case EV_QUEUE_DEL:
#         case EV_STATUS_MSG:
#             return get_str_from_srv ();
#         case EV_FILE_TAGS:
#             return recv_tags_data_from_srv ();
#         case EV_PLIST_MOVE:
#         case EV_QUEUE_MOVE:
#             return recv_move_ev_data_from_srv ();
#     }

#     return NULL;
# }

# /* Wait for EV_DATA handling other events. */
# static void wait_for_data ()
# {
#     int event;

#     do {
#         event = get_int_from_srv ();

#         if (event != EV_DATA)
#             event_push (&events, event, get_event_data(event));
#      } while (event != EV_DATA);
# }


# when sending that the answer should be EV_DATA + an integer
# pack/unpack
# print("get state [%d]"%CMD_GET_STATE )
# sk.send( struct.pack('i', 19 ) )
# .encode('utf-8')
# sk.send(bytes(CMD_GET_STATE) )


# # 
# sk.close()



# def changedState(data):
#     print("State changed. Either started or stopped")

# event_callbacks = {
#     EV_AUDIO_START : changedState,
#     EV_AUDIO_STOP : changedState
# }

# static void server_event (const int event, void *data)
# {
#     logit ("EVENT: 0x%02x", event);

#     switch (event) {
#         case EV_BUSY:
#             interface_fatal ("The server is busy; "
#                              "another client is connected!");
#             break;
#         case EV_CTIME:
#             update_ctime ();
#             break;
#         case EV_STATE:
#             update_state ();
#             break;
#         case EV_EXIT:
#             interface_fatal ("The server exited!");
#             break;
#         case EV_BITRATE:
#             update_bitrate ();
#             break;
#         case EV_RATE:
#             update_rate ();
#             break;
#         case EV_CHANNELS:
#             update_channels ();
#             break;
#         case EV_SRV_ERROR:
#             update_error ();
#             break;
#         case EV_OPTIONS:
#             get_server_options ();
#             break;
#         case EV_SEND_PLIST:
#             forward_playlist ();
#             break;
#         case EV_PLIST_ADD:
#             if (options_get_int("SyncPlaylist"))
#                 event_plist_add ((struct plist_item *)data);
#             break;
#         case EV_PLIST_CLEAR:
#             if (options_get_int("SyncPlaylist"))
#                 clear_playlist ();
#             break;
#         case EV_PLIST_DEL:
#             if (options_get_int("SyncPlaylist"))
#                 event_plist_del ((char *)data);
#             break;
#         case EV_PLIST_MOVE:
#             if (options_get_int("SyncPlaylist"))
#                 event_plist_move ((struct move_ev_data *)data);
#             break;
#         case EV_TAGS:
#             update_curr_tags ();
#             break;
#         case EV_STATUS_MSG:
#             iface_set_status ((char *)data);
#             break;
#         case EV_MIXER_CHANGE:
#             update_mixer_name ();
#             break;
#         case EV_FILE_TAGS:
#             ev_file_tags ((struct tag_ev_response *)data);
#             break;
#         case EV_AVG_BITRATE:
#             curr_file.avg_bitrate = get_avg_bitrate ();
#             break;
#         case EV_QUEUE_ADD:
#             event_queue_add ((struct plist_item *)data);
#             break;
#         case EV_QUEUE_DEL:
#             event_queue_del ((char *)data);
#             break;
#         case EV_QUEUE_CLEAR:
#             clear_queue ();
#             break;
#         case EV_QUEUE_MOVE:
#             event_queue_move ((struct move_ev_data *)data);
#             break;
#         case EV_AUDIO_START:
#             break;
#         case EV_AUDIO_STOP:
#             break;
#         default:
#             interface_fatal ("Unknown event: 0x%02x!", event);
#     }

#     free_event_data (event, data);
# }