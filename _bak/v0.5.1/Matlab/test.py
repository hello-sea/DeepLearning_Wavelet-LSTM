import matlab
import matlab.engine
import time

def basic_test(eng):
    print("Basic Testing Begin")
    print( "eng.power(100,2) = %d"%eng.power(100,2) )
    print("eng.max(100,200) = %d"%eng.max(100,200) )
    print("eng.rand(5,5) = ")
    print(eng.rand(5,5) )
    print("eng.randi(matlab.double([1,100]),matlab.double([3,4]))"%\
        eng.randi(matlab.double([1,100]),matlab.double([3,4])) )
    print("Basic Testing Begin")

def plot_test(eng):
    print("Plot Testing Begin")
    eng.workspace['data'] =  \
        eng.randi(matlab.double([1,100]),matlab.double([30,2]))
    eng.eval("plot(data(:,1),'ro-')")
    eng.hold('on',nargout=0)
    eng.eval("plot(data(:,2),'bx--')")
    print("Plot testing end")
    

def audio_test(eng,freq,length):
    print ("Audio Testing Begin")
    eval_str = "f = %d;t=%d;"%(freq,length)
    eng.eval(eval_str,nargout = 0)
    eng.eval('fs = 44100;T=1/fs;t=(0:T:t);',nargout = 0)
    eng.eval('y = sin(2 * pi * f * t);',nargout = 0)
    eng.eval('sound(y,fs);',nargout = 0)
    time.sleep(length)
    print("Audio Testing End")


def fourier_test(eng):
    pass



def demo(eng):
    basic_test(eng)
    plot_test(eng)
    audio_test(eng,680,1)



if __name__ == "__main__":
    print("Initializing Matlab Engine")
    eng = matlab.engine.start_matlab()
    print("Initializing Complete!")
    demo(eng)
    print("Exiting Matlab Engine")
    print("Press Any Key to Exit")
    input()
    eng.quit()
    print ("Bye-Bye")