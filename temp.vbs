
                    Dim speak, wavData
                    Set speak = CreateObject("SAPI.SpVoice")
                    speak.Rate = -3
                    speak.Volume = 100
                    
                    Dim stream
                    Set stream = CreateObject("SAPI.SpFileStream")
                    stream.Open "C:\\Curso_Chines\\static\\audio\\audio_Pz96aC1DTg__.mp3", 3, False
                    Set speak.AudioOutputStream = stream
                    speak.Speak "??"
                    stream.Close
                