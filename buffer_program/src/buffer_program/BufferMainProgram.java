package buffer_program;

import java.io.IOException;

public class BufferMainProgram {
    public static void main(String[] args) throws InterruptedException {
    	BufferC1toF newBufferC1toF = new BufferC1toF("192.168.4.148:5000");
        try {
			newBufferC1toF.receiveImage();
		} catch (IOException e) {
			e.printStackTrace();
		}
//        Thread.sleep(1000);
//        System.out.println("cycle");
    }
}
