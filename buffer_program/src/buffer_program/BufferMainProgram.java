package buffer_program;

public class BufferMainProgram {
    public static void main(String[] args) throws InterruptedException {
    	// BufferC1toF newBufferC1toF = new BufferC1toF("http://127.0.0.1:8000");
    	BufferC1toF newBufferC1toF = new BufferC1toF("https://raw.githubusercontent.com/cornell-cup/cs-wall/develop/image/map.png");
    	while (true) {
        	newBufferC1toF.receiveImage();
        	Thread.sleep(1000);
        	System.out.println("cycle");
    	}
    }
}
