import pyaudio
import wave
import sys
import time
import threading
import websocket
 
OPTIONRTASR = 1
OPTIONRECORD = 2
class audioInf():
    def __init__(self,format =  pyaudio.paInt16,channels = 1,rate=16000,chunk = 640,ws=None):
      self.format =   format
      self.channels = channels
      self.rate = rate
      self.chunk = chunk
      self.ws = ws
      
    def recordfile(self,filename="d:\\asr\\file.wav"):      
      self._p = pyaudio.PyAudio()
      self.wf = wave.open(filename, 'wb')
      self.wf.setnchannels(self.channels)
      self.wf.setsampwidth(self._p.get_sample_size(self.format))      
      self.wf.setframerate(self.rate)
      self._stream = self._p.open(format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback = self.getrecordcallback(OPTIONRECORD)
                )
      self._stream.start_stream()
      while self._stream.is_active():
        time.sleep(0.1)
        if self.stop==True :
          print("stop recording is called")
          self.stopRecording()
          self.stop = False
          break
      return self
      
    
    def rtasr(self):        
      self._p = pyaudio.PyAudio()
      self._stream = self._p.open(format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback = self.getrecordcallback(OPTIONRTASR)
                )
      self._stream.start_stream()
      while self._stream.is_active():
        time.sleep(0.1)
        if self.stop==True :
          print("stop recording is called")
          self.stopAsr()
          self.stop = False
          break
      
      return self
      
    def getrecordcallback(self,option=OPTIONRTASR):
      def callback2(in_data, frame_count, time_info, status):
            self.wf.writeframes(in_data)
            #print(len(in_data))
            return in_data, pyaudio.paContinue
      def callback(in_data, frame_count, time_info, status):
        self.ws.send(in_data)
        return in_data, pyaudio.paContinue
      if option == OPTIONRTASR:
        return callback  
      else:
        return callback2
    
    def stopAsr(self):      
      end_tag = "{\"end\": true}"      
      self.ws.send(bytes(end_tag.encode('utf-8')))
      self._stream.stop_stream()
      self._stream.close()
      self._p.terminate()
      
    def stopRecording(self):
      self._stream.stop_stream()
      self._stream.close()
      self._p.terminate()
      self.wf.close() 
      
    
    def pause(self):
      pass    
    
    def resume(self):
      pass
    
    
    def stop(self):
      self.stop = True
      print("helo");
      
  ######################################
      
    def playcallback(self,in_data,frame_count,time_info,status):
      data = self.wf.readframes(frame_count)
      return (data, pyaudio.paContinue)
    
    
    def playfile(self,filename):
      self.playfilename = filename;
          
    def  play(self):
      CHUNK = 1024
      p = pyaudio.PyAudio()
      self.wf = wave.open(self.playfilename, 'rb')
      stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback = self.playcallback
                )
      while stream.is_active():
        time.sleep(0.1)
        if self.stop==True :
          self.stop = False
          break
      
      stream.stop_stream()
      stream.close()
      p.terminate()
      
      
      
if __name__ == '__main__':
    myaudio = audioInf()
    #myaudio.playfile("d:\\asr\\file.wav");
    threading.Thread(target=myaudio.recordfile).start()
    a = input("to stop input any key + enter:")
    print("after sleep, now stop")
    myaudio.stop() 
    
    