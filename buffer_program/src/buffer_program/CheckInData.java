package buffer_program;

public class CheckInData {
	String name;
	int checkInStatus;
	int[] meetingID;

	public CheckInData(String name, int checkInStatus, int[] meetingID) {
		this.name = name;
		this.checkInStatus = checkInStatus;
		this.meetingID = meetingID;
	}
}
