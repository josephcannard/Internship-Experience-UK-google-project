"""A video player class."""

from .video_library import VideoLibrary
import random
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currentlyPlaying =None
        self.paused = False
        self.playlistList = []
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        sortedVideoList = []
        for video in self._video_library._videos.values():
            sortedVideoList.append(video.title +" (" + video.video_id + ") ["+ ' ' .join(video.tags)+"]")
            
        sortedVideoList.sort()    
        for video in sortedVideoList:    
            print(video)

    def find_video_by_id(self,video_id):
        
        for video in self._video_library._videos.values():
            if video.video_id == video_id :
                return video
    
    def check_video_exists(self, video_id):
        return (self._video_library.get_video(video_id))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        self.paused = False
        if self.check_video_exists(video_id) != None:
            self.stop_video_alt()

            self.currentlyPlaying = self.find_video_by_id(video_id)

            print("Playing video: "+ self.currentlyPlaying.title)
        else:
            print("Cannot play video: Video does not exist")

    def stop_video_alt(self):
        if self.currentlyPlaying != None:
            print("Stopping video: "+ self.currentlyPlaying.title)
            self.currentlyPlaying = None

    def stop_video(self):
        
        if self.currentlyPlaying == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: "+ self.currentlyPlaying.title)
            self.currentlyPlaying = None
        

    def play_random_video(self):
        randomNumber = random.randint(0,len(self._video_library.get_all_videos())-1)
        counter = 0
        for video in self._video_library._videos:
            
            if counter == randomNumber:
                
                self.play_video(video)
            counter += 1        
        

    def pause_video(self):
        """Pauses the current video."""
        if self.currentlyPlaying != None:
            if self.paused == False:
                print("Pausing video: "+self.currentlyPlaying.title)
                self.paused = True
            else:
                print("Video already paused: "+ self.currentlyPlaying.title)
        else:
            print("Cannot pause video: No video is currently playing")
    
    def continue_video(self):
        """Resumes playing the current video."""
        if self.currentlyPlaying != None:
            if self.paused == True:
                print("Continuing video: "+self.currentlyPlaying.title)
                self.paused = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.currentlyPlaying == None:
            print("No video is currently playing")
        else:
            if self.paused == False:
                print("Currently playing: "+self.currentlyPlaying.title +" (" + self.currentlyPlaying.video_id + ") ["+ ' ' .join(self.currentlyPlaying.tags)+"]")
            else:
                print("Currently playing: "+self.currentlyPlaying.title +" (" + self.currentlyPlaying.video_id + ") ["+ ' ' .join(self.currentlyPlaying.tags)+"] - PAUSED")

    def find_playlist(self,playlist_name):
        playlist_name = playlist_name.lower()
        for playlist in self.playlistList:
            if playlist.getName().lower() == playlist_name:
                return playlist
        return None

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        newplaylist = self.find_playlist(playlist_name)
        if newplaylist == None:
            self.playlistList.append(Playlist(playlist_name))

            print("Successfully created new playlist: "+ playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

        self.playlistList.sort(key=Playlist.getName)
    
    def find_video(self, playlist, video):

        for playlistvideo in playlist.getVideos():
            if playlistvideo == video:
                return video
        return None

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        playlist = self.find_playlist(playlist_name)
        if playlist != None:

            video = self.find_video_by_id(video_id)
            if video != None:
                if self.find_video(playlist,video) == None:
                    playlist.videos.append(video)
                    print("Added video to "+playlist_name+": "+ video.title)
                else:
                    print("Cannot add video to "+playlist_name+": Video already added")
            else:
                print("Cannot add video to "+playlist_name+": Video does not exist")
        else:
            print("Cannot add video to "+playlist_name+": Playlist does not exist")


    def show_all_playlists(self):
        
        if len(self.playlistList) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist in self.playlistList:
                
                print(playlist.getName())
        

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist != None:
            print("Showing playlist: "+playlist_name)
            if len(playlist.getVideos()) == 0:
                print("No videos here yet")
            else:
                
                for video in playlist.getVideos():
                    print(video.title +" (" + video.video_id + ") ["+ ' ' .join(video.tags)+"]")
        else:
            print("Cannot show playlist another_playlist: Playlist does not exist")
        

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist != None:

            video = self.find_video_by_id(video_id)
            if video != None:
                if self.find_video(playlist,video) != None:
                    playlist.videos.remove(video)
                    print("'Removed video from "+playlist_name+": "+ video.title)
                else:
                    print("Cannot remove video from "+playlist_name+": Video is not in playlist")
            else:
                print("Cannot remove video from "+ playlist_name+": Video does not exist")
        else:
            print("Cannot remove video from "+ playlist_name+": Playlist does not exist")
        

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist != None:

            playlist.videos = []
            print("Successfully removed all videos from "+playlist_name)
        else:
            print("Cannot clear playlist "+ playlist_name+": Playlist does not exist")
       

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.find_playlist(playlist_name)
        if playlist != None:


            self.playlistList.remove(playlist)
            print("Deleted playlist: "+playlist_name)
        else:
            print("Cannot delete playlist "+ playlist_name+": Playlist does not exist")
       
        

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
