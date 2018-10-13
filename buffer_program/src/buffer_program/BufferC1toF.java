package buffer_program;

import java.awt.Image;
import java.net.URL;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class BufferC1toF {
	
	String URLfromPi;
	
	public BufferC1toF(String URLfromPi) {
		this.URLfromPi = URLfromPi;
	}
	
	public void receiveImage() {
		Image image = null;
		try {
			URL url = new URL(URLfromPi);
			image = ImageIO.read(url);
			JFrame frame = new JFrame();
			frame.setSize(300, 300);
			JLabel label = new JLabel(new ImageIcon(image));
			frame.add(label);
			frame.setVisible(true);
		} catch (Exception e) {
			System.out.println(e.getMessage());
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
