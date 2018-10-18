package buffer_program;

import java.awt.Image;
import java.awt.image.BufferedImage; 
import java.net.URL;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class BufferC1toF {
	
	String URLfromPi;
	BufferedImage image;// the image for received from the Raspberry Pi front end
						// processed, and send to the C bank end
	int[][] imageMatrix;
	
	public BufferC1toF(String URLfromPi) {
		this.URLfromPi = URLfromPi;
	}
	
	public void receiveImage() {
		try {
			URL url = new URL(URLfromPi);
			image = ImageIO.read(url);
			
			JFrame frame = new JFrame();
			frame.setSize(300, 300);
			JLabel label = new JLabel(new ImageIcon(image));
			frame.add(label);
			frame.setVisible(true);
			processImage();
			sendImage();
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}
	
	// TODO: process image to image matrix, and create certain json
	public void processImage() {
		
	}
		
	// convert the image in image to grey scale
	public void imageToGreyScale () {
		// get image's width and height 
        int width = image.getWidth(); 
        int height = image.getHeight(); 
  
        // convert to greyscale 
        for (int y = 0; y < height; y++) 
        { 
            for (int x = 0; x < width; x++) 
            { 
                // Here (x,y)denotes the coordinate of image  
                // for modifying the pixel value. 
                int p = image.getRGB(x,y); 
  
                int a = (p>>24)&0xff; 
                int r = (p>>16)&0xff; 
                int g = (p>>8)&0xff; 
                int b = p&0xff; 
  
                // calculate average 
                int avg = (r+g+b)/3; 
  
                // replace RGB value with avg 
                p = (a<<24) | (avg<<16) | (avg<<8) | avg; 
  
                image.setRGB(x, y, p); 
            } 
        } 
	}
	// TODO: send the image to C program
	public void sendImage() {
//		HttpClient httpClient = new DefaultHttpClient(); //Deprecated
//		HttpClient httpClient = HttpClientBuilder.create().build(); //Use this instead 
//
//		try {
//		    HttpPost request = new HttpPost("http://yoururl");
//		    StringEntity params =new StringEntity("details={\"name\":\"myname\",\"age\":\"20\"} ");
//		    request.addHeader("content-type", "application/x-www-form-urlencoded");
//		    request.setEntity(params);
//		    HttpResponse response = httpClient.execute(request);
//
//		    // handle response here...
//		}catch (Exception ex) {
//		    // handle exception here
//		} finally {
//		    httpClient.getConnectionManager().shutdown(); //Deprecated
//		}
	}
}
