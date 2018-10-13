package buffer_program;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.nio.charset.Charset;

import org.json.JSONException;
import org.json.JSONObject;

public class newBufferFtoC2 {

	String URLfromF;
	JSONObject jsonfromF;
	
	public newBufferFtoC2(String URLfromF) {
		this.URLfromF = URLfromF;
	}
	private static String readAll(Reader rd) throws IOException {
	    StringBuilder sb = new StringBuilder();
	    int cp;
	    while ((cp = rd.read()) != -1) {
	      sb.append((char) cp);
	    }
	    return sb.toString();
	  }
	
	public void receiveJSON() throws IOException, JSONException {
		InputStream is = new URL(URLfromF).openStream();
	    try {
	      BufferedReader rd = new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));
	      String jsonText = readAll(rd);
	      jsonfromF = new JSONObject(jsonText);
	    } finally {
	      is.close();
	    }
	}
	
	// TODO: send the image to C program
	public void sendJSON() {
		
	}
	
}
